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
from Implementacion.Anuncio import Anuncio, getAllAnuncios
from Implementacion.Postulacion import Postulacion
from Implementacion.Tarea import Tarea
from Implementacion.Disponibilidad import Disponibilidad
from Implementacion.Vinculo import Vinculo
from Implementacion.Mensaje import Mensaje
from Implementacion.DTOAuxEmpleado import DTOAuxEmpleado
from Implementacion.DTOAuxEmpleado import TareaSeleccion
from Implementacion.DTOAuxEmpleado import DisponibilidadSeleccion
from Implementacion.Referencia import Referencia

from Implementacion.Usuario import getUsuarioByID
from Implementacion.Empleador import getEmpleadorByID
from Implementacion.Empleador import getEmpleadorByUsuarioID
from Implementacion.Empleado import getEmpleadoByID
from Implementacion.Empleado import getEmpleadoByUsuarioID
from Implementacion.Empleado import getTareasEmpleado
from Implementacion.Empleado import getDisponibilidadEmpleado
from Implementacion.Anuncio import getAnuncioByID
from Implementacion.Vinculo import getVinculoByID
from Implementacion.Postulacion import getPostulacionesAnuncio
from Implementacion.Postulacion import getPostulacionesEmpleado
from Implementacion.Postulacion import getPostulacionEmpleadoAnuncio
from Implementacion.Postulacion import getPostulacionesEmpleadoIDs
from Implementacion.Tarea import getTareasRegistradas
from Implementacion.Disponibilidad import getDisponibilidadesRegistradas
from Implementacion.Referencia import getReferenciaByID
from Implementacion.Referencia import getReferenciasEmpleado


app = Flask(__name__)

#baseDatos = connectionDb(app, 'local')
#baseDatos = connectionDb(app, 'remotemysql.com')
baseDatos = connectionDb(app, 'CloudAccess')
#baseDatos = connectionDb(app, 'aws')


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


def login(user, password):
    usuario = Usuario(0, user, password, '')
    retorno = usuario.loginUsuario(baseDatos)
    # Si no existe el usuario debo alertar
    if retorno == ():
        print('No existe el usuario!')
        flash('No existe el usuario!')
        return redirect(url_for('logueo'))
    else:
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
        return login(user, password)


@app.route('/SignUp/')
def opcion_registrarse():
    return render_template('OpcionRegistro.html')


@app.route('/VistaPerfil/<opcion>/<id>', methods=['POST', 'GET'])
def vista_perfil(opcion, id):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        objeto = None
        if opcion == 'Empleado':
            objeto = getEmpleadoByID(baseDatos, id)
            tareas = getTareasEmpleado(baseDatos, objeto.id)
            objeto.cargarTareas(tareas)
            referencias = getReferenciasEmpleado(baseDatos, objeto.id)
            objeto.cargarReferencias(referencias)
            disponibilidad = getDisponibilidadEmpleado(baseDatos, objeto.id)
            objeto.cargarDisponibilidad(disponibilidad)

        elif opcion == 'Empleador':
            objeto = getEmpleadorByID(baseDatos, id)

        return render_template('VistaPerfil.html', tipo=opcion, data=objeto)


@app.route('/Perfil/<opcion>', methods=['POST', 'GET'])
def perfil(opcion):
    if session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        logueado = session.get('usertype') is not None
        empleado: Empleado = Empleado()
        dtoAuxEmpleado: DTOAuxEmpleado = DTOAuxEmpleado()
        empleador: Empleador = Empleador()

        if opcion == 'Empleado':
            if logueado:
                # obtengo los datos del empleado
                idEmpleado = session['id_empleado']
                empleado = getEmpleadoByID(baseDatos, idEmpleado)
                # Debo traer las tareas y disponibilidades (estableciendo las seleccionadas por el empleado) para cargarlas dinámicamente
                tareasSeleccion = empleado.getTareasSeleccionadas(baseDatos)
                disponibilidadSeleccion = empleado.getDisponibilidadSeleccionadas(
                    baseDatos)
                # cargo sus tareas, referencias y disponibilidad
                tareas = getTareasEmpleado(baseDatos, empleado.id)
                empleado.cargarTareas(tareas)
                referencias = getReferenciasEmpleado(baseDatos, empleado.id)
                empleado.cargarReferencias(referencias)
                disponibilidad = getDisponibilidadEmpleado(
                    baseDatos, empleado.id)
                empleado.cargarDisponibilidad(disponibilidad)
                # convierto byte a entero, el atributo "género" en mysql es de tipo bit
                generoInt = int.from_bytes(empleado.genero, "big")
                empleado.genero = generoInt

                dtoAuxEmpleado = DTOAuxEmpleado(
                    tareasSeleccion, disponibilidadSeleccion)
            return render_template('Perfil.html', tipo=opcion, data=empleado, aux=dtoAuxEmpleado)

        elif opcion == 'Empleador':
            if logueado:
                # obtengo los datos del empleador
                idEmpleador = session['id_empleador']
                empleador = getEmpleadorByID(baseDatos, idEmpleador)
                # convierto byte a entero, el atributo "género" en mysql es de tipo bit
                generoInt = int.from_bytes(empleador.genero, "big")
                empleador.genero = generoInt
            return render_template('Perfil.html', tipo=opcion, data=empleador)


@app.route('/GuardarPerfil/<tipo>', methods=['POST'])
def guardar_perfil(tipo):
    if session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        if request.method == 'POST':
            parametros = request.form

            #for param in parametros:
                #print('Parámetro: ', param)
                
            nombre = parametros['nombre']
            apellido = parametros['apellido']
            nacimiento = parametros['cumple']
            genero = int(parametros['genero'])
            domicilio = parametros['domicilio']
            nacionalidad = parametros['nacionalidad']
            mail = parametros['email']
            telefono = parametros['tel']
            password = parametros['password']

            logueado = session.get('usertype') is not None
            usuario = None

            if not logueado:
                # debo crear primero el usuario ya que se trata de un registro (alta) ya que no está logueado
                cedula = parametros['cedula']
                usuario = Usuario(0, cedula, password, tipo)
                usuario.crearUsuario(baseDatos)
                usuario.getIdUsuario(baseDatos)

            # chequear el tipo para realizar las operaciones en empleado o empleador
            if tipo == 'Empleado':
                # debo crear un empleado
                empleado = Empleado(0, None, nombre, apellido, nacimiento, genero, domicilio,
                                    nacionalidad, mail, telefono, 0, '', 'images/NoImage.png', 0, usuario, None, None, None)

                # como es edición de perfil debo modificar la contraseña y el empleado
                if logueado:
                    # modificar contraseña?

                    # recorrer la disponibilidad seleccionada y cargarsela al empleado
                    disponibilidad = list()
                    disponibilidadesRegistradas = getDisponibilidadesRegistradas(baseDatos)
                    for disp in disponibilidadesRegistradas:
                        indice = str(disponibilidadesRegistradas.index(disp)+1)
                        if 'disp'+indice in parametros:
                            #print('**** Debería cargar esta disponibilidad: ID=', disp.id, ', DESC=', disp.descripcion)
                            d = Disponibilidad(disp.id, disp.descripcion)
                            disponibilidad.append(d)
                    empleado.cargarDisponibilidad(disponibilidad)

                    # recorrer las tareas seleccionadas y cargarselas al empleado
                    tareas = list()
                    tareasRegistradas = getTareasRegistradas(baseDatos)
                    for tarea in tareasRegistradas:
                        indice = str(tareasRegistradas.index(tarea)+1)
                        if 'tarea'+indice in parametros:
                            #print('**** Debería cargar esta tarea: ID=', tarea.id, ', DESC=', tarea.descripcion)
                            t = Tarea(tarea.id, tarea.descripcion)
                            tareas.append(t)
                    empleado.cargarTareas(tareas)

                    tiene_experiencia = parametros['experiencia']
                    if tiene_experiencia == '1':
                        experiencia = parametros['mesesExperiencia']
                    else:
                        experiencia = 0

                    descripcion = parametros['presentacion']
                    foto = parametros['fotoPerfil']
                    empleado.id = session['id_empleado']
                    empleado.experiencia_meses = experiencia
                    empleado.descripcion = descripcion
                    if foto != '':
                        empleado.foto = foto
                    empleado.modificarEmpleado(baseDatos)

                    if request.form.get('btnAgregarReferencia'):
                        print('Estoy agregando una referencia')
                        # Agregar referencia que se visualizará en la grilla al recargar el template
                        empleado = getEmpleadoByID(baseDatos, empleado.id)
                        nombre = request.form['refNombreEmp']
                        telefono = request.form['refTelefonoEmp']
                        trabaja_desde = request.form['refTrabDesde']
                        trabaja_hasta = request.form['refTrabDesde']
                        referencia = Referencia(0, empleado, nombre, telefono,
                                                trabaja_desde, trabaja_hasta)
                        referencia.crearReferencia(baseDatos)
                        # El retorno debe ser el propio form pero da error
                    else:
                        return redirect(url_for('inicio_empleados'))

                # como es registro (alta) debo crear el empleado
                else:
                    empleado.crearEmpleado(baseDatos)
                    login(cedula, password)
                    return redirect(url_for('inicio_empleados'))

            elif tipo == 'Empleador':
                # debo crear un empleador
                empleador = Empleador(0, None, nombre, apellido, nacimiento,
                                      genero, domicilio, nacionalidad, mail, telefono, 0, 'images/NoImage.png', 0, usuario)

                # como es edición de perfil debo modificar la contraseña y el empleador
                if logueado:
                    # modificar contraseña?
                    tiene_bps = parametros['bps']
                    if tiene_bps == '1':
                        regBPS = parametros['empleadorNumRegBPS']
                    else:
                        regBPS = '0'

                    foto = parametros['fotoPerfil']
                    empleador.registroBps = regBPS
                    if foto != '':
                        empleador.foto = foto
                    empleador.id = session['id_empleador']
                    empleador.modificarEmpleador(baseDatos)
                # como es registro (alta) debo crear el empleado
                else:
                    empleador.crearEmpleador(baseDatos)
                    login(cedula, password)
                return redirect(url_for('inicio_empleadores'))


# Se deja standby porque requiere desactivar un montón de cosas y no era parte de las funcionalidades planteadas
@app.route('/EliminarCuenta/', methods=['POST'])
def cancelar_cuenta():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        usuarioLogueado = session.get('usertype')
        if usuarioLogueado == 'Empleado':
            idEmpleado = session['id_empleado']
            objeto = getEmpleadoByID(baseDatos, idEmpleado)
        else:
            idEmpleador = session['id_empleador']
            objeto = getEmpleadorByID(baseDatos, idEmpleador)
        return 'No implementada'


@app.route('/HomeEmpleados/')
def inicio_empleados():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleador':
        return redirect(url_for('inicio_empleadores'))
    else:
        empleado = getEmpleadoByID(baseDatos, session['id_empleado'])
        return render_template('HomeEmpleados.html', sujeto=empleado)


@app.route('/HomeEmpleadores/')
def inicio_empleadores():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        empleador = getEmpleadorByID(baseDatos, session['id_empleador'])
        return render_template('HomeEmpleadores.html', sujeto=empleador)


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


@app.route('/Anuncio/<accion>')
def anuncio(accion):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        return render_template('Anuncio.html', opcion=accion)


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
            nfecha_inicio = datetime.now()
            nfecha_cierre = None
            # En el alta el anuncio queda activo, si quiere desactivar debe modificarlo [Inicio]
            # if request.form['radioEstado'] == 'estadoActiva':
            # nestado = 1
            # else:
            # nestado = 0
            # En el alta el anuncio queda activo, si quiere desactivar debe modificarlo [Fin]
            nexperiencia = request.form.get('radioExperiencia')
            npago_hora = request.form['pagoPorHora']
            ncal_desde = None  # por ahora no se maneja a nivel de anuncio
            ncal_hasta = None  # por ahora no se maneja a nivel de anuncio
            nvinculo = False  # cuando se crea no hay vínculo
            empleador.crearAnuncio(
                baseDatos,
                ntitulo,
                ndescripcion,
                nfecha_inicio,
                nfecha_cierre,
                True,  # al crear el anuncio este queda activo
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


@app.route('/verOferta/')
def verOferta():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        # 2020-03-08 (A) - Se unifica todo el manejo de anuncios en un único form: Anuncio.html [Inicio]
        # return render_template('verOferta.html')
        return render_template('Anuncio.html')
        # 2020-03-08 (A) - Se unifica todo el manejo de anuncios en un único form: Anuncio.html [Fin]


@app.route('/listandoMisAnuncios/')
def listandoMisAnuncios():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        empleador = getEmpleadorByID(baseDatos, session['id_empleador'])
        retorno = empleador.listarMisAnuncios(baseDatos)
        return render_template('TusAnuncios.html', listaMisAnuncios=retorno)


@app.route('/eliminandoAnuncio/<idAnuncio>/', methods=['POST', 'GET'])
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
        anuncio = getAnuncioByID(baseDatos, idAnuncio)
        empleador.borrarAnuncio(
            baseDatos,
            anuncio,
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

# acá va la funcion que envía los datos viejos para llenar el form del anuncio q se va a cambiar
@app.route('/actualizandoAnuncio/<idAnuncio>/', methods=['POST', 'GET'])
def actualizandoAnuncio(idAnuncio):
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
        return render_template('editarAnuncio.html', anuncio=lista)


# esta funcion recibe los nuevos datos y actualiza la bd:
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
            new_cal_desde = None  # por ahora no se maneja a nivel de anuncio
            new_cal_hasta = None  # por ahora no se maneja a nivel de anuncio
            new_vinculo = None  # cuando se crea no hay vínculo
            anuncio = getAnuncioByID(baseDatos, idAnuncio)
            empleador.actualizarAnuncio(
                baseDatos,
                anuncio,
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
        return render_template('TusAnuncios.html', listaMisAnuncios=listado)


@app.route('/Anuncios/')
def listar_anuncios():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleador':
        return redirect(url_for('inicio_empleadores'))
    else:
        idEmpleado = session['id_empleado']
        empleado = getEmpleadoByID(baseDatos, idEmpleado)
        tareas = []
        disponibilidades = []
        if empleado.experiencia_meses == None:
            experiencia = 0
        elif empleado.experiencia_meses == 0:
            experiencia = 0
        else:
            experiencia = 1
        for tarea in getTareasEmpleado(baseDatos, idEmpleado):
            tareas.append(tarea.id)
        for disponibilidad in getDisponibilidadEmpleado(baseDatos, idEmpleado):
            disponibilidades.append(disponibilidad.id)
        empl = [
            experiencia,
            set(tareas),
            disponibilidades
        ]
        retornoAnuncios = getAllAnuncios(baseDatos)
        listaAnuncios = []
        for anuncio in retornoAnuncios:
            anuncioConID = [anuncio[0]]
            anuncioConID.append(getAnuncioByID(baseDatos, anuncio[0]))
            listaAnuncios.append(anuncioConID)
        listaDeAnuncios = []
        for elAnuncio in listaAnuncios:
            anun = []

            idAnuncio = elAnuncio[0]
            disponibilidadAnuncio = elAnuncio[1].disponibilidad
            experienciaAnuncio = None
            if elAnuncio[1].experiencia == b'\x00':
                experienciaAnuncio = 0
            else:
                experienciaAnuncio = 1
            tareasAnuncio = []

            if elAnuncio[1].estado == b'\x01':

                if elAnuncio[1].hogar == True:
                    tareasAnuncio.append(1)
                if elAnuncio[1].oficina == True:
                    tareasAnuncio.append(2)
                if elAnuncio[1].cocinar == True:
                    tareasAnuncio.append(3)
                if elAnuncio[1].limp_banios == True:
                    tareasAnuncio.append(4)
                if elAnuncio[1].limp_cocinas == True:
                    tareasAnuncio.append(5)
                if elAnuncio[1].limp_dormitorios == True:
                    tareasAnuncio.append(6)
                if elAnuncio[1].cuidado_ninios == True:
                    tareasAnuncio.append(7)
                if elAnuncio[1].cuidado_bebes == True:
                    tareasAnuncio.append(8)
                if elAnuncio[1].cuidado_adultos == True:
                    tareasAnuncio.append(9)
                if elAnuncio[1].cuidado_mascotas == True:
                    tareasAnuncio.append(10)

                anun.append(idAnuncio)
                anun.append(disponibilidadAnuncio)
                anun.append(experienciaAnuncio)
                anun.append(set(tareasAnuncio))
                listaDeAnuncios.append(anun)

        listaMatcheo = []
        for a in listaDeAnuncios:
            if a[1] in empl[2] and empl[0] >= a[2] and a[3] & empl[1] == a[3]:
                unAnuncio = [
                    a[0],
                    getAnuncioByID(baseDatos, a[0])
                ]
                listaMatcheo.append(unAnuncio)
                
        misPostulaciones = getPostulacionesEmpleadoIDs(baseDatos, idEmpleado)
        listaIdsMisAnunciosPostulados = []
        for miPostulacion in misPostulaciones:
            listaIdsMisAnunciosPostulados.append(miPostulacion.anuncio)
        for k in listaMatcheo:
            if k[0] in listaIdsMisAnunciosPostulados:
                k.append(1)
            else:
                k.append(0)


        return render_template('ListaAnuncios.html', anuncios=listaMatcheo)


@app.route('/verAnuncio/<idAnuncio>/<postulacion>')
def ver_anuncio(idAnuncio, postulacion):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleador':
        return redirect(url_for('inicio_empleadores'))
    else:
        elAnuncio = getAnuncioByID(baseDatos, idAnuncio),
        empleador = elAnuncio[0].empleador
        listaEmpleador = [
            empleador.nombre,
            empleador.apellido,
            empleador.foto,
            empleador.registroBps
        ]
        tareasAnuncio = []
        if elAnuncio[0].hogar == True:
            tareasAnuncio.append(1)
        if elAnuncio[0].oficina == True:
            tareasAnuncio.append(2)
        if elAnuncio[0].cocinar == True:
            tareasAnuncio.append(3)
        if elAnuncio[0].limp_banios == True:
            tareasAnuncio.append(4)
        if elAnuncio[0].limp_cocinas == True:
            tareasAnuncio.append(5)
        if elAnuncio[0].limp_dormitorios == True:
            tareasAnuncio.append(6)
        if elAnuncio[0].cuidado_ninios == True:
            tareasAnuncio.append(7)
        if elAnuncio[0].cuidado_bebes == True:
            tareasAnuncio.append(8)
        if elAnuncio[0].cuidado_adultos == True:
            tareasAnuncio.append(9)
        if elAnuncio[0].cuidado_mascotas == True:
            tareasAnuncio.append(10)
        if elAnuncio[0].experiencia == b'\x00':
            experienciaAnuncio = 0
        else:
            experienciaAnuncio = 1

        listaAnuncio = [
            elAnuncio[0].titulo,
            elAnuncio[0].descripcion,
            elAnuncio[0].disponibilidad,
            tareasAnuncio,
            elAnuncio[0].pago_hora,
            experienciaAnuncio,
            idAnuncio
        ]
        context = {
            'empleador': listaEmpleador,
            'anuncio': listaAnuncio,
            'postulacion': postulacion
        }
        # el desempaquetado tendrá 3 claves, 'empleador', 'anuncio' y psotulacion
        # 'empleador' : [nombre, apellido, foto, registroBps]
        # 'anuncio' : [titulo, descripcion, disponibilidad, [tareas], pago_hora, experiencia, idAnuncio]
		# 'postulación': contiene 1 si el usuario está postulado al anuncio, y 0 si no lo está
        return render_template('verOferta.html', **context)


@app.route('/postularse/<idAnuncio>')
def postularse(idAnuncio):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleador':
        return redirect(url_for('inicio_empleadores'))
    else:
        empleado = getEmpleadoByID(baseDatos, session['id_empleado'])
        anuncio = getAnuncioByID(baseDatos, idAnuncio)
        new_postulacion = Postulacion(
            None, empleado, anuncio, datetime.now(), None)
        new_postulacion.crearPostulacion(baseDatos)
        flash('Postulación enviada!')
        return redirect(url_for('listar_anuncios'))

@app.route('/MisPostulaciones/')
def mis_postulaciones():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleador':
        return redirect(url_for('inicio_empleadores'))
    else:
        idEmpleado = session['id_empleado']
        postulaciones = getPostulacionesEmpleadoIDs(baseDatos, idEmpleado)
        misPostulaciones = []
        for postulacion in postulaciones:
            lista = []
            lista.append(postulacion.anuncio)
            lista.append(getAnuncioByID(baseDatos, postulacion.anuncio))
            lista.append(getPostulacionEmpleadoAnuncio(baseDatos, idEmpleado, postulacion.anuncio))
            misPostulaciones.append(lista)

        for post in misPostulaciones:
            if post[1].estado == b'\x01':
                post.append(1)
            else:
                post.append(0)

        return render_template('TusPostulaciones.html', postulaciones = misPostulaciones)


@app.route('/Candidatos/<id_anuncio>', methods=['POST', 'GET'])
def listar_candidatos(id_anuncio):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        # guardo el id del anuncio en la sesion ya que lo preciso más adelante a la hora de contactar y eventualmente contratar
        session['id_anuncio'] = id_anuncio
        # Obtengo la lista de postulaciones para el anuncio dado
        anuncio = getAnuncioByID(baseDatos, id_anuncio)
        postulaciones = getPostulacionesAnuncio(baseDatos, id_anuncio)
        pares = postulaciones[0:][::2]
        impares = postulaciones[1:][::2]
        return render_template('ListaCandidatos.html', elemPares=pares, elemImpares=impares, elanuncio=anuncio)


@app.route('/Mensajes/')
def chat():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        return render_template('chat.html')


@app.route('/Contratar/<idEmpleado>')
def contactar(idEmpleado):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        empleado = getEmpleadoByID(baseDatos, idEmpleado)
        tareas = getTareasEmpleado(baseDatos, empleado.id)
        empleado.cargarTareas(tareas)
        referencias = getReferenciasEmpleado(baseDatos, empleado.id)
        empleado.cargarReferencias(referencias)
        disponibilidad = getDisponibilidadEmpleado(baseDatos, empleado.id)
        empleado.cargarDisponibilidad(disponibilidad)

        empleador = getEmpleadorByID(baseDatos, session['id_empleador'])
        anuncio = getAnuncioByID(baseDatos, session['id_anuncio'])

        # Se debe generar el vínculo
        vinculo = Vinculo(0, empleado, empleador, anuncio,
                          datetime.now(), None, None, '', None, None)
        vinculo.crearVinculo(baseDatos)

        # El anuncio debe quedar inactivo
        anuncio.setEstadoAnuncio(baseDatos, False)

        # Se debe actualizar la postulación a genera_vinculo = true
        postulacion: Postulacion = getPostulacionEmpleadoAnuncio(
            baseDatos, empleado.id, anuncio.id)
        postulacion.generarVinculoEnPostulacion(baseDatos)

        # Se debe notificar al empleado mediante mensaje de que el empleador "X" lo contrató
        mensajeEmpleado = Mensaje(
            0, empleado, empleador, anuncio, datetime.now(), 'Felicidades!!! Has sido contratado por: {} {}, les deseamos un buen vínculo laboral.'.format(empleador.nombre, empleador.apellido))
        mensajeEmpleado.crearMensaje(baseDatos)

        # Se debe notificar al empleador mediante mensaje de que contrató al empleador "X"
        mensajeEmpleador = Mensaje(
            0, empleado, empleador, anuncio, datetime.now(), 'Felicidades!!! Has contratado a: {} {}, les deseamos un buen vínculo laboral.'.format(empleado.nombre, empleado.apellido))
        mensajeEmpleador.crearMensaje(baseDatos)

        flash('Empleado Contratado!')
        return render_template('contactoEmpleado.html', data=empleado)


@app.route('/AgregarReferencia/<id_empleado>', methods=['POST', 'GET'])
def agregar_referencia(id_empleado):
    if request.method == 'POST':
        # Agregar referencia que se visualizará en la grilla al recargar el template
        opcion = 'Empleado'
        empleado = getEmpleadoByID(baseDatos, id_empleado)
        nombre = request.form['refNombreEmp']
        telefono = request.form['refTelefonoEmp']
        trabaja_desde = request.form['refTrabDesde']
        trabaja_hasta = request.form['refTrabDesde']
        referencia = Referencia(0, empleado, nombre, telefono,
                                trabaja_desde, trabaja_hasta)
        referencia.crearReferencia(baseDatos)
        flash('Referencia agregada')
        # return redirect(url_for('/Perfil/Empleado'))
        return render_template('Perfil.html', tipo=opcion, data=empleado)


@app.route('/EditarReferencia/<id_referencia>', methods=['POST'])
def editar_referencia(id_referencia):
    if request.method == 'POST':
        # Debería cargar en el form de referencia los datos de la referencia a editar
        # El botón debería cambiar de "Agregar Referencia" a "Actualizar Referencia"
        return 'No implementada'


@app.route('/ActualizarReferencia/<id_referencia>', methods=['POST'])
def actualizar_referencia(id_referencia):
    if request.method == 'POST':
        # Actualizar la referencia que se visualizará en la grilla al recargar el template
        nombre = request.form['refNombreEmp']
        telefono = request.form['refTelefonoEmp']
        trabaja_desde = request.form['refTrabDesde']
        trabaja_hasta = request.form['refTrabDesde']
        referencia = Referencia(id_referencia, None, nombre, telefono,
                                trabaja_desde, trabaja_hasta)
        referencia.actualizarReferencia(baseDatos)
        flash('Referencia actualizada')
        return redirect(url_for('/Perfil/Empleado'))


@app.route('/BorrarReferencia/<id_referencia>', methods=['POST', 'GET'])
def borrar_referencia(id_referencia):
    referencia = getReferenciaByID(baseDatos, id_referencia)
    referencia.borrarReferencia(baseDatos)
    flash('Referencia Borrada')
    return 'No implementada'


# ***** Pendientes ***********

@app.route('/MisVinculos')
def mis_vinculos():
    return 'Está pendiente'

# ****************************


if __name__ == '__main__':
    app.run(debug=True)
