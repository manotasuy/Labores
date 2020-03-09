import json
from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_mysqldb import MySQL
from datetime import datetime
from enum import Enum

# Paquetes implementación
from Implementacion.Conexion import connectionDb
from Implementacion.Usuario import Usuario
from Implementacion.Empleado import Empleado
from Implementacion.Empleador import Empleador
from Implementacion.Anuncio import Anuncio
from Implementacion.Postulación import Postulacion
from Implementacion.Tarea import Tarea
from Implementacion.Disponibilidad import Disponibilidad

from Implementacion.Usuario import getUsuarioByID
from Implementacion.Empleador import getEmpleadorByID
from Implementacion.Empleador import getEmpleadorByUsuarioID
from Implementacion.Empleado import getEmpleadoByID
from Implementacion.Empleado import getEmpleadoByUsuarioID
from Implementacion.Empleado import getTareasEmpleado
from Implementacion.Empleado import getReferenciasEmpleado
from Implementacion.Empleado import getDisponibilidadEmpleado
from Implementacion.Anuncio import getAnuncioByID
from Implementacion.Postulación import getPostulacionesAnuncio
from Implementacion.Postulación import getPostulacionesEmpleado

app = Flask(__name__)

#baseDatos = connectionDb(app, 'local')
#baseDatos = connectionDb(app, 'remotemysql.com')
baseDatos = connectionDb(app, 'aws')


# session
app.secret_key = "session"


@app.route('/')
@app.route('/Inicio/')
def inicio():
    return render_template('Inicio.html')


@app.route('/Contacto/')
def contacto():
    return render_template('Contacto.html')


@app.route('/Ayuda/')
def ayuda():
    return render_template('Ayuda.html')


@app.route('/LogIn/')
def logueo():
    return render_template('Login.html')


@app.route('/LogOut/')
def deslogueo():
    session.clear()
    return redirect(url_for('inicio'))


@app.route('/RecuperarPass/')
def recuperar_pass():
    return render_template('RecuperarClave.html')


@app.route('/Ingresar', methods=['POST'])
def ingresar():
    if request.method == 'POST':
        parametros = request.form
        user = parametros['user']
        password = parametros['pass']
        usuario = Usuario(0, user, password, '')
        retorno = usuario.loginUsuario(baseDatos)
        # Si no existe el usuario debo alertar
        if retorno == ():
            print('No existe el usuario!')
            flash('No existe el usuario!')
            return redirect(url_for('logueo'))
        else:
            print("Retorno: ", retorno)
            session['username'] = user
            session['usertype'] = retorno[0][0]
            session['id_usuario'] = retorno[0][1]

            if session['usertype'] == 'Empleador':
                # debo obtener el empleador y guardar su id en la sesion
                empleador = getEmpleadorByUsuarioID(baseDatos, retorno[0][1])
                session['id_empleador'] = empleador.id
                return redirect(url_for('inicio_empleadores'))
            elif session['usertype'] == 'Empleado':
                # debo obtener el empleado y guardar su id en la sesion
                empleado = getEmpleadoByUsuarioID(baseDatos, retorno[0][1])
                session['id_empleado'] = empleado.id
                return redirect(url_for('inicio_empleados'))
            else:
                return redirect(url_for('administrar'))


@app.route('/SignUp/')
def opcion_registrarse():
    return render_template('OpcionRegistro.html')


# @app.route('/Registro/<opcion>')
# def registrarse(opcion):
    #session['useroption'] = opcion
    # return render_template('Registro.html')


@app.route('/Perfil/<opcion>', methods=['POST', 'GET'])
def perfil(opcion):
    if session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        logueado = session.get('usertype') is not None

        # Debo traer las tareas y disponibilidades para cargarlas dinámicamente
        #tareasTodas = getTareas(baseDatos)
        #disponibilidadTodas = getDisponibilidades(baseDatos)

        if opcion == 'Empleado':
            objeto = Empleado()
            if logueado:
                # debo cargar sus datos en el form
                # debo obtener los datos del empleado
                idEmpleado = session['id_empleado']
                objeto = getEmpleadoByID(baseDatos, idEmpleado)
                # luego cargar sus tareas, referencias y disponibilidad
                tareas = getTareasEmpleado(baseDatos, objeto.id)
                objeto.cargarTareas(tareas)
                referencias = getReferenciasEmpleado(baseDatos, objeto.id)
                objeto.cargarReferencias(referencias)
                disponibilidad = getDisponibilidadEmpleado(
                    baseDatos, objeto.id)
                objeto.cargarDisponibilidad(disponibilidad)
                return render_template('Perfil.html', tipo=opcion, data=objeto)
            # else:
                # cargo el formulario vacío porque es registro
                #data = Empleado(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            return render_template('Perfil.html', tipo=opcion, data=objeto)

        elif opcion == 'Empleador':
            objeto = Empleador()
            if logueado:
                # debo cargar sus datos en el form
                # debo obtener los datos del empleado
                idEmpleador = session['id_empleador']
                objeto = getEmpleadorByID(baseDatos, idEmpleador)
                return render_template('Perfil.html', tipo=opcion, data=objeto)
            # else:
                # cargo el formulario vacío porque es registro
                #objeto = Empleador(None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            return render_template('Perfil.html', tipo=opcion, data=objeto)


@app.route('/GuardarPerfil/<tipo>', methods=['POST'])
def guardar_perfil(tipo):
    if session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        if request.method == 'POST':
            parametros = request.form
            nombre = parametros['nombre']
            apellido = parametros['apellido']
            nacimiento = parametros['cumple']
            genero = 'Masculino'
            cedula = parametros['cedula']
            domicilio = parametros['domicilio']
            nacionalidad = parametros['nacionalidad']
            mail = parametros['email']
            telefono = parametros['tel']
            password = parametros['password']

            logueado = session.get('usertype') is not None
            usuario = None

            if not logueado:
                # debo crear primero el usuario ya que se trata de un registro (alta) ya que no está logueado
                usuario = Usuario(0, cedula, password, tipo)
                usuario.crearUsuario(baseDatos)
                usuario.getIdUsuario(baseDatos)

            # chequear el tipo para realizar las operaciones en empleado o empleador
            if tipo == 'Empleado':
                # debo crear un empleado
                empleado = Empleado(session['id_empleado'], cedula, nombre, apellido, nacimiento, genero, domicilio,
                                    nacionalidad, mail, telefono, None, None, None, None, usuario, None, None, None)

                # como es edición de perfil debo modificar la contraseña y el empleado
                if logueado:
                    empleado.modificarEmpleado(baseDatos)
                # como es registro (alta) debo crear el empleado
                else:
                    empleado.crearEmpleado(baseDatos)
                return redirect(url_for('inicio_empleados'))

            elif tipo == 'Empleador':
                # debo crear un empleador
                empleador = Empleador(session['id_empleador'], cedula, nombre, apellido, nacimiento,
                                      genero, domicilio, nacionalidad, mail, telefono, None, None, None, usuario)

                # como es edición de perfil debo modificar la contraseña y el empleador
                if logueado:
                    empleador.modificarEmpleador(baseDatos)
                # como es registro (alta) debo crear el empleado
                else:
                    empleador.crearEmpleador(baseDatos)
                return redirect(url_for('inicio_empleadores'))


# Se deja standby porque requiere desactivar un montón de cosas y no era parte de las funcionalidades planteadas
@app.route('/EliminarCuenta/', methods=['POST'])
def cancelar_cuenta():
    usuarioLogueado = session.get('usertype')
    if usuarioLogueado == 'Empleado':
        idEmpleado = session['id_empleado']
        objeto = getEmpleadoByID(baseDatos, idEmpleado)
    else:
        idEmpleador = session['id_empleador']
        objeto = getEmpleadorByID(baseDatos, idEmpleador)
    return 'Hola!'


@app.route('/HomeEmpleados/')
def inicio_empleados():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleador':
        return redirect(url_for('inicio_empleadores'))
    else:
        return render_template('HomeEmpleados.html')


@app.route('/HomeEmpleadores/')
def inicio_empleadores():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        return render_template('HomeEmpleadores.html')


@app.route('/PanelControl/')
def administrar():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Empleador':
        return redirect(url_for('inicio_empleadores'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        return render_template('ControlPanel.html')


@app.route('/CrearAnuncio/')
def crear_anuncio():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        return render_template('CrearAnuncio.html')


# *** En desarrollo por Daniel ***
@app.route('/PublicarAnuncio/', methods=['POST'])
def publicar_anuncio():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        if request.method == 'POST':
            empleador = getEmpleadorByID(baseDatos, session['id_empleador'])
            nDisponibilidad = request.form.get('radioDisponibilidad') 
            nHogar = request.form.getlist('chkHogar') 
            nOficina = request.form.getlist('chkOficina') 
            nCocinar = request.form.getlist('chkCocinar')
            nLimpBanios = request.form.getlist('chkLimpBanios') 
            nLimpCocinas = request.form.getlist('chkLimpCocinas') 
            nLimpDormitorios = request.form.getlist('chkLimpDormitorios') 
            nCuidadoNinios = request.form.getlist('chkCuidadoNinios') 
            nCuidadoBebes = request.form.getlist('chkCuidadoBebes') 
            nCuidadoAdultos = request.form.getlist('chkCuidadoAdultos') 
            nCuidadoMascotas = request.form.getlist('chkCuidadoMascotas') 
            ntitulo = request.form['txtTitulo']
            ndescripcion = request.form['txtDescripcion']
            nfecha_incio = datetime.now()
            nfecha_cierre = None
            if request.form.get('radioEstado') == '1':
                nestado = 1
            elif request.form.get('radioEstado') == '0':
                nestado = 0
            nexperiencia = request.form.get('radioExperiencia')
            npago_hora = request.form['pagoPorHora']
            ncal_desde = None #esto no va?
            ncal_hasta = None #esto no va?
            nvinculo = None #esto hay que ver como lo hacemos
            empleador.crearAnuncio(
                baseDatos, 
                ntitulo, 
                ndescripcion, 
                nfecha_incio, 
                nfecha_cierre, 
                nestado, 
                nexperiencia, 
                npago_hora, 
                ncal_desde, 
                ncal_hasta, 
                nvinculo,
                nDisponibilidad,
                nHogar,
                nOficina,
                nCocinar,
                nLimpBanios,
                nLimpCocinas,
                nLimpDormitorios,
                nCuidadoNinios,
                nCuidadoBebes,
                nCuidadoAdultos,
                nCuidadoMascotas)
            flash('Anuncio creado!')
            return redirect(url_for('tus_anuncios'))




@app.route('/eliminandoAnuncio/<idAnuncio>/', methods = ['POST','GET'])
def borrandoAnuncio(idAnuncio):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        empleador = getEmpleadorByID(baseDatos, session['id_empleador'])
        print(empleador)
        del_titulo = None
        del_descripcion = None
        del_fecha_incio = None
        del_fecha_cierre = None
        del_estado = None
        del_experiencia = None
        del_pago_hora = None
        del_cal_desde = None
        del_cal_hasta = None
        del_vinculo = None
        del_Disponibilidad = None
        del_Hogar = None
        del_Oficina = None
        del_Cocinar = None
        del_LimpBanios = None
        del_LimpCocinas = None
        del_LimpDormitorios = None
        del_CuidadoNinios = None
        del_CuidadoBebes = None
        del_CuidadoAdultos = None
        del_CuidadoMascotas = None 
        empleador.borrarAnuncio(
            baseDatos, 
            idAnuncio, 
            del_titulo, 
            del_descripcion, 
            del_fecha_incio, 
            del_fecha_cierre, 
            del_estado, 
            del_experiencia, 
            del_pago_hora, 
            del_cal_desde, 
            del_cal_hasta, 
            del_vinculo,
            del_Disponibilidad,
            del_Hogar,
            del_Oficina,
            del_Cocinar,
            del_LimpBanios,
            del_LimpCocinas,
            del_LimpDormitorios,
            del_CuidadoNinios,
            del_CuidadoBebes,
            del_CuidadoAdultos,
            del_CuidadoMascotas)
        flash('Anuncio eliminado!')
        return redirect(url_for('listandoMisAnuncios'))

#acá va la funcion que envía los datos viejos para llenar el form del anuncio q se va a cambiar
@app.route('/actualizandoAnuncio/<idAnuncio>/', methods=['POST', 'GET'])
def ectualizandoAnuncio(idAnuncio):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        anuncio = getAnuncioByID(baseDatos, idAnuncio)
        print(anuncio)
        if anuncio.estado == b'\x01':
            estado = 1
        else:
            estado = 0
        lista = [
            idAnuncio,
            anuncio.titulo,
            anuncio.descripcion,
            anuncio.disponibilidad,
            anuncio.hogar,
            anuncio.oficina,
            anuncio.cocinar,
            anuncio.limp_banios,
            anuncio.limp_cocinas,
            anuncio.limp_dormitorios,
            anuncio.cuidado_ninios,
            anuncio.cuidado_bebes,
            anuncio.cuidado_adultos,
            anuncio.cuidado_mascotas,
            anuncio.experiencia,
            anuncio.pago_hora,
            estado
            ]
        return render_template('editarAnuncio.html', anuncio = lista)



#esta funcion recibe los nuevos datos y actualiza la bd:
@app.route('/editandoAnuncio/<idAnuncio>/', methods=['POST'])
def editandoAnuncio(idAnuncio):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        if request.method == 'POST':
            empleador = getEmpleadorByID(baseDatos, session['id_empleador'])
            new_Disponibilidad = request.form.get('radioDisponibilidad') 
            new_Hogar = request.form.getlist('chkHogar') 
            new_Oficina = request.form.getlist('chkOficina') 
            new_Cocinar = request.form.getlist('chkCocinar')
            new_LimpBanios = request.form.getlist('chkLimpBanios') 
            new_LimpCocinas = request.form.getlist('chkLimpCocinas') 
            new_LimpDormitorios = request.form.getlist('chkLimpDormitorios') 
            new_CuidadoNinios = request.form.getlist('chkCuidadoNinios') 
            new_CuidadoBebes = request.form.getlist('chkCuidadoBebes') 
            new_CuidadoAdultos = request.form.getlist('chkCuidadoAdultos') 
            new_CuidadoMascotas = request.form.getlist('chkCuidadoMascotas') 
            new_titulo = request.form['txtTitulo']
            new_descripcion = request.form['txtDescripcion']
            old_fecha_incio = None
            new_fecha_cierre = None
            if request.form.get('radioEstado') == '1':
                new_estado = 1
            elif request.form.get('radioEstado') == '0':
                new_estado = 0
            new_experiencia = request.form.get('radioExperiencia')
            new_pago_hora = request.form['pagoPorHora']
            new_cal_desde = None #esto no va?
            new_cal_hasta = None #esto no va?
            new_vinculo = None #esto hay que ver como lo hacemos
            empleador.actualizarAnuncio(
                baseDatos, 
                idAnuncio, 
                new_titulo, 
                new_descripcion, 
                old_fecha_incio, 
                new_fecha_cierre, 
                new_estado, 
                new_experiencia, 
                new_pago_hora, 
                new_cal_desde, 
                new_cal_hasta, 
                new_vinculo,
                new_Disponibilidad,
                new_Hogar,
                new_Oficina,
                new_Cocinar,
                new_LimpBanios,
                new_LimpCocinas,
                new_LimpDormitorios,
                new_CuidadoNinios,
                new_CuidadoBebes,
                new_CuidadoAdultos,
                new_CuidadoMascotas
                )
            return redirect(url_for('tus_anuncios'))


@app.route('/TusAnuncios/')
def tus_anuncios():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        empleador = getEmpleadorByID(baseDatos, session['id_empleador'])
        retorno = empleador.listarMisAnuncios(baseDatos)
        listado = []
        for anuncio in retorno:
            lista = []
            lista += [anuncio[0]]
            lista += [anuncio[1]]
            lista += [anuncio[2]]
            lista += [anuncio[3]]
            lista += [anuncio[4]]
            if anuncio[5] == b'\x01':
                lista += [1]
            else: 
                lista += [0]
            if anuncio[6] == b'\x01':
                lista += [1]
            else: 
                lista += [0]
            lista += [anuncio[7]]
            lista += [anuncio[8]]
            lista += [anuncio[9]]
            lista += [anuncio[10]]
            lista += [anuncio[11]]
            listado += [lista]
        return render_template('TusAnuncios.html', listaMisAnuncios = listado)


@app.route('/Anuncios/')
def listar_anuncios():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleador':
        return redirect(url_for('inicio_empleadores'))
    else:
        return render_template('ListaAnuncios.html')


@app.route('/Candidatos/<anuncio>', methods=['POST', 'GET'])
def listar_candidatos(anuncio):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        # Debo obtener la lista de postulaciones para el anuncio dado
        postulaciones = getPostulacionesAnuncio(baseDatos, anuncio)
        print('Anuncio: ', anuncio)
        print('Postulaciones:', postulaciones)
        return render_template('ListaCandidatos.html', data=postulaciones)


@app.route('/Editar/<opcion>', methods=['POST'])
def editar_usuario(opcion):
    return 'Hola!'


@app.route('/chat/')
def chat():
    return render_template('chat.html')

@app.route('/verOferta/')
def verOferta():
    return render_template('verOferta.html')


if __name__ == '__main__':
    app.run(debug=True)
