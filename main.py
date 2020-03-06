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
from Implementacion.Usuario import getUsuarioByID
from Implementacion.Empleador import getEmpleadorByID
from Implementacion.Empleador import getEmpleadorByUsuarioID
from Implementacion.Empleado import getEmpleadoByID
from Implementacion.Empleado import getEmpleadoByUsuarioID
from Implementacion.Empleado import getTareasEmpleado
from Implementacion.Empleado import getReferenciasEmpleado
from Implementacion.Empleado import getDisponibilidadEmpleado
from Implementacion.Anuncio import getAnuncioByID
from Implementacion.Anuncio import Anuncio

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
        flash('Anuncio creado!')
        return render_template('CrearAnuncio.html')


# *** En desarrollo por Daniel ***
@app.route('/PublicarAnuncio', methods=['POST'])
def publicar_anuncio():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        if request.method == 'POST':
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            fechaInicio = datetime.now()
            fechaCierre = None
            estado = request.form['estado']
            experiencia = request.form['experiencia']
            salario = request.form['salario']
            idEmpleador = session['id_empleador']
            empleador = getEmpleadorByID(baseDatos, idEmpleador)
            calEmpleado = request.form['calEmpleado']
            calEmpleador = request.form['calEmpleador']
            tieneVinculo = request.form['tieneVinculo']
            empleador.crearAnuncio
            (
                titulo,
                descripcion,
                fechaInicio,
                fechaCierre,
                estado,
                experiencia,
                salario,
                calEmpleado,
                calEmpleador,
                tieneVinculo
            )
            flash('Anuncio creado!')
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
        return render_template('TusAnuncios.html')


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


@app.route('/Candidatos/')
def listar_candidatos():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        return render_template('ListaCandidatos.html')


# @app.route('/registroVale/<opcion>')
# def registroVale(opcion):
    #session['useroption'] = opcion
    # return render_template('registroVale.html')


# @app.route('/perfilEmpleado/')
# def perfilEmpleado():
    # if session.get('usertype') == None:
        # return redirect(url_for('logueo'))
    # elif session.get('usertype') == 'Administrador':
        # return redirect(url_for('administrar'))
    # elif session.get('usertype') == 'Empleador':
        # return redirect(url_for('inicio_empleadores'))
    # else:
        # return render_template('perfilEmpleado.html')


# @app.route('/perfilEmpleador/')
# def perfilEmpleador():
    # if session.get('usertype') == None:
        # return redirect(url_for('logueo'))
    # elif session.get('usertype') == 'Administrador':
        # return redirect(url_for('administrar'))
    # elif session.get('usertype') == 'Empleado':
        # return redirect(url_for('inicio_empleados'))
    # else:
        # return render_template('perfilEmpleador.html')

@app.route('/listarEmpleados/')
def listarEmpleados():
    return render_template('listarEmpleados.html')

@app.route('/listarEmpleadores/')
def listarEmpleadores():
    return render_template('listarEmpleadores.html')


@app.route('/Editar/<opcion>', methods=['POST'])
def editar_usuario(opcion):
    return 'Hola!'


if __name__ == '__main__':
    app.run(debug=True)
