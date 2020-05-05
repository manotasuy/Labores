import json
import os
import logging
from flask import Flask, request, Response, render_template, url_for, redirect, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from enum import Enum

# Paquetes implementación
from Implementacion.Conexion import connectionDb
from Implementacion.Usuario import Usuario, getUsuarioByID
from Implementacion.Empleado import Empleado, getEmpleadoByID, getEmpleadoByUsuarioID, getTareasEmpleado, getDisponibilidadEmpleado, getRankingPorCalificacionEmpleados
from Implementacion.Empleador import Empleador, getEmpleadorByID, getEmpleadorByUsuarioID, getRankingPorCalificacionEmpleadores
from Implementacion.Anuncio import Anuncio, getAllAnuncios, getAnuncioByID
from Implementacion.Postulacion import Postulacion, getPostulacionesAnuncio, getPostulacionesEmpleado, getPostulacionEmpleadoAnuncio, getPostulacionesEmpleadoIDs, empleadorTieneNotificacionesPendientesPostulaciones, getPostulacionById, existePostulacionDeEmpleadoEnAnuncioDeEmpleador
from Implementacion.Tarea import Tarea, getTareasRegistradas
from Implementacion.Disponibilidad import Disponibilidad, getDisponibilidadesRegistradas
from Implementacion.Vinculo import Vinculo, getVinculoByID, getVinculoByEmpleado, getVinculoByEmpleador, getVinculoIDs, getPromedioByEmpleadorId, getPromedioByEmpleadoId, getVinculosNoNotificadosDelEmpleado, empleadoTieneNotificacionesPendientesVinculos, tieneElEmpleadorVinculoConEmpleado, tieneElEmpleadoVinculoConEmpleador
from Implementacion.Mensaje import Mensaje, getMensajesParaEmpleado, empleadoTieneMensajesSinLeer, getMensajesParaEmpleador, empleadorTieneMensajesSinLeer, tieneElEmpleadoMensajeDeEmpleador, tieneElEmpleadorMensajeDeEmpleado
from Implementacion.DTOAuxEmpleado import DTOAuxEmpleado, TareaSeleccion, DisponibilidadSeleccion
from Implementacion.Referencia import Referencia, getReferenciaByID, getReferenciasEmpleado
from Implementacion.Admin import getDatosAdmin
from Implementacion.Recordatorio import Recordatorio, getRecordatorioByID, recordatoriosBloqueantes, recordatoriosCalificacionesPendientes
from Implementacion.DTOMensaje import DTOMensaje

EXTENSIONES_ADMITIDAS = set(['jpg', 'png', 'jpeg', 'bmp', 'gif'])

app = Flask(__name__)

#baseDatos = connectionDb(app, 'remotemysql.com')
#baseDatos = connectionDb(app, 'aws')
#baseDatos = connectionDb(app, 'CloudAccess')
#baseDatos = connectionDb(app, 'a-work')
#baseDatos = connectionDb(app, 'a-home')
#baseDatos = connectionDb(app, 'local')
baseDatos = connectionDb(app, 'PA')
#baseDatos = connectionDb(app, 'gcp')



# session
app.secret_key = "session"


def archivoAdmitido(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in EXTENSIONES_ADMITIDAS


def login(user, password):
    usuario = Usuario(0, user, password, '')
    retorno = usuario.loginUsuario(baseDatos)

    # Si no existe el usuario debo alertar
    if retorno == ():
        mensaje = 'La cédula o la contraseña ingresada no es correcta'
        flash(mensaje)
        return redirect(url_for('logueo', mensaje=mensaje))
    else:
        tipo_usuario = retorno[0][0]
        id_usuario = retorno[0][1]
        session['username'] = user
        session['usertype'] = tipo_usuario
        session['id_usuario'] = id_usuario

        if session['usertype'] == 'Empleador':
            # debo obtener el empleador y guardar su id en la sesion
            empleador = getEmpleadorByUsuarioID(baseDatos, id_usuario)
            session['id_empleador'] = empleador.id
            session['nombre'] = '{} {}'.format(
                empleador.nombre, empleador.apellido)
            return redirect(url_for('inicio_empleadores'))
        elif session['usertype'] == 'Empleado':
            # debo obtener el empleado y guardar su id en la sesion
            empleado = getEmpleadoByUsuarioID(baseDatos, id_usuario)
            session['id_empleado'] = empleado.id
            session['nombre'] = '{} {}'.format(
                empleado.nombre, empleado.apellido)
            return redirect(url_for('inicio_empleados'))
        else:
            session['nombre'] = 'Administrador'
            return redirect(url_for('administrar'))


def getRecordatoriosDelDia():
    if session.get('usertype') == None:
        return None
    elif session.get('usertype') == 'Administrador':
        return None
    else:
        recordatorios = list()
        recordatoriosDelDia = list()
        if session.get('usertype') == 'Empleado':
            idEmpleado = session['id_empleado']
            recordatorios = recordatoriosCalificacionesPendientes(baseDatos, idEmpleado)
        elif session.get('usertype') == 'Empleador':
            idEmpleador = session['id_empleador']
            recordatorios = recordatoriosCalificacionesPendientes(baseDatos, idEmpleador)

        if recordatorios is None:
            return None
        else:
            for rec in recordatorios:
                if str(rec.fechaRecordatorio) == datetime.now().strftime('%Y-%m-%d'):
                    recordatoriosDelDia.append(rec)
            
            if len(recordatoriosDelDia) == 0:
                return None
            else:
                return recordatoriosDelDia


def getRecordatoriosCalificacionesPendientes():
    if session.get('usertype') == None:
        return None
    elif session.get('usertype') == 'Administrador':
        return None
    elif session.get('usertype') == 'Empleado':
        idEmpleado = session['id_empleado']
        return recordatoriosCalificacionesPendientes(baseDatos, idEmpleado)
    elif session.get('usertype') == 'Empleador':
        idEmpleador = session['id_empleador']
        return recordatoriosCalificacionesPendientes(baseDatos, idEmpleador)
    else:
        return None


def getRecordatoriosBloqueantes():
    if session.get('usertype') == None:
        return None
    elif session.get('usertype') == 'Administrador':
        return None
    elif session.get('usertype') == 'Empleado':
        idEmpleado = session['id_empleado']
        return recordatoriosBloqueantes(baseDatos, idEmpleado)
    elif session.get('usertype') == 'Empleador':
        idEmpleador = session['id_empleador']
        return recordatoriosBloqueantes(baseDatos, idEmpleador)
    else:
        return None


def getTop3EmpleadosParaBaseTemplate():
    return getRankingPorCalificacionEmpleados(baseDatos, 3)


def getTop3EmpleadoresParaBaseTemplate():
    return getRankingPorCalificacionEmpleadores(baseDatos, 3)

@app.context_processor
def contexto():
    contextProcessor = dict()
    contextProcessor['rankEmpleados'] = getTop3EmpleadosParaBaseTemplate
    contextProcessor['rankEmpleadores'] = getTop3EmpleadoresParaBaseTemplate
    contextProcessor['recordatoriosBloqueantes'] = getRecordatoriosBloqueantes
    contextProcessor['recordatoriosCalificacionesPendientes'] = getRecordatoriosCalificacionesPendientes
    contextProcessor['recordatoriosDelDia'] = getRecordatoriosDelDia
    return contextProcessor


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


@app.route("/LogIn/")
def logueo():
    # return render_template('Login.html', mensaje=mensaje)
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
    if session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    elif session.get('usertype') == 'Empleador':
        return redirect(url_for('inicio_empleadores'))
    else:
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
        # objeto = None
        if opcion == 'Empleado':
            objeto = getEmpleadoByID(baseDatos, id)
            # Si no se puede cargar la foto guardada en la base cargo la imagen default
            rutaFisica = '.' + url_for('static', filename=objeto.foto)
            if not os.path.exists(rutaFisica):
                objeto.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
            dtoAuxEmpleado: DTOAuxEmpleado = DTOAuxEmpleado()
            # Debo traer las tareas y disponibilidades (estableciendo las seleccionadas por el empleado) para cargarlas dinámicamente
            tareasSeleccion = objeto.getTareasSeleccionadas(baseDatos)
            disponibilidadSeleccion = objeto.getDisponibilidadSeleccionadas(
                baseDatos)
            tareas = getTareasEmpleado(baseDatos, objeto.id)
            objeto.cargarTareas(tareas)
            referencias = getReferenciasEmpleado(baseDatos, objeto.id)
            objeto.cargarReferencias(referencias)
            disponibilidad = getDisponibilidadEmpleado(baseDatos, objeto.id)
            objeto.cargarDisponibilidad(disponibilidad)
            # convierto byte a entero, el atributo "género" en mysql es de tipo bit
            generoInt = int.from_bytes(objeto.genero, "big")
            objeto.genero = generoInt

            dtoAuxEmpleado = DTOAuxEmpleado(
                tareasSeleccion, disponibilidadSeleccion)

            cal = getPromedioByEmpleadoId(baseDatos, objeto.id)            
            return render_template('VistaPerfil.html', tipo=opcion, data=objeto, aux=dtoAuxEmpleado, cal=cal)

        elif opcion == 'Empleador':
            objeto = getEmpleadorByID(baseDatos, id)
            # Si no se puede cargar la foto guardada en la base cargo la imagen default
            rutaFisica = '.' + url_for('static', filename=objeto.foto)
            if not os.path.exists(rutaFisica):
                objeto.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
            return render_template('VistaPerfil.html', tipo=opcion, data=objeto)


@app.route('/VistaPerfilContratado/<opcion>/<id>', methods=['POST', 'GET'])
def vista_perfil_contratado(opcion, id):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        # objeto = None
        if opcion == 'Empleado':
            objeto = getEmpleadoByID(baseDatos, id)
            # Si no se puede cargar la foto guardada en la base cargo la imagen default
            rutaFisica = '.' + url_for('static', filename=objeto.foto)
            if not os.path.exists(rutaFisica):
                objeto.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')

            dtoAuxEmpleado: DTOAuxEmpleado = DTOAuxEmpleado()
            # Debo traer las tareas y disponibilidades (estableciendo las seleccionadas por el empleado) para cargarlas dinámicamente
            tareasSeleccion = objeto.getTareasSeleccionadas(baseDatos)
            disponibilidadSeleccion = objeto.getDisponibilidadSeleccionadas(
                baseDatos)
            tareas = getTareasEmpleado(baseDatos, objeto.id)
            objeto.cargarTareas(tareas)
            referencias = getReferenciasEmpleado(baseDatos, objeto.id)
            objeto.cargarReferencias(referencias)
            disponibilidad = getDisponibilidadEmpleado(baseDatos, objeto.id)
            objeto.cargarDisponibilidad(disponibilidad)
            # convierto byte a entero, el atributo "género" en mysql es de tipo bit
            generoInt = int.from_bytes(objeto.genero, "big")
            objeto.genero = generoInt

            dtoAuxEmpleado = DTOAuxEmpleado(
                tareasSeleccion, disponibilidadSeleccion)
            cal = getPromedioByEmpleadoId(baseDatos, objeto.id)
            return render_template('VistaPerfilContratado.html', tipo=opcion, data=objeto, aux=dtoAuxEmpleado, cal=cal)

        elif opcion == 'Empleador':
            objeto = getEmpleadorByID(baseDatos, id)
            # Si no se puede cargar la foto guardada en la base cargo la imagen default
            rutaFisica = '.' + url_for('static', filename=objeto.foto)
            if not os.path.exists(rutaFisica):
                objeto.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
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
        referenciaParaEditar = None

        if opcion == 'Empleado':
            if logueado:
                # obtengo los datos del empleado
                idEmpleado = session['id_empleado']
                empleado = getEmpleadoByID(baseDatos, idEmpleado)
                # Si no se puede cargar la foto guardada en la base cargo la imagen default
                rutaFisica = '.' + url_for('static', filename=empleado.foto)
                if not os.path.exists(rutaFisica):
                    empleado.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')

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
                if 'id_refer' in session:
                    id_referencia = int(session['id_refer'])
                    print('id_referencia en Perfil: ', id_referencia)
                    referenciaParaEditar = getReferenciaByID(
                        baseDatos, id_referencia)
            return render_template('Perfil.html', tipo=opcion, data=empleado, aux=dtoAuxEmpleado, refer=referenciaParaEditar)
        elif opcion == 'Empleador':
            if logueado:
                # obtengo los datos del empleador
                idEmpleador = session['id_empleador']
                empleador = getEmpleadorByID(baseDatos, idEmpleador)
                # Si no se puede cargar la foto guardada en la base cargo la imagen default
                rutaFisica = '.' + url_for('static', filename=empleador.foto)
                if not os.path.exists(rutaFisica):
                    empleador.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
                # convierto byte a entero, el atributo "género" en mysql es de tipo bit
                generoInt = int.from_bytes(empleador.genero, "big")
                empleador.genero = generoInt
            return render_template('Perfil.html', tipo=opcion, data=empleador)


@app.route('/GuardarPerfil/<tipo>', methods=['GET', 'POST'])
def guardar_perfil(tipo):
    if session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        if request.method == 'POST':
            parametros = request.form

            if request.form.get('btnGuardarReferencia'):
                if not 'id_refer' in session:
                    new_empleado = getEmpleadoByID(
                        baseDatos, session['id_empleado'])
                    nombre = request.form['refNombreEmp']
                    apellido = request.form['refApellidoEmp']
                    telefono = request.form['refTelefonoEmp']
                    trabaja_desde = request.form['refTrabDesde']
                    trabaja_hasta = request.form['refTrabHasta']
                    referencia = Referencia(
                        0, new_empleado, nombre, apellido, telefono, trabaja_desde, trabaja_hasta)
                    referencia.crearReferencia(baseDatos)
                    print('Referencia creada')
                else:
                    id_referencia = int(session['id_refer'])
                    print('id_referencia en GuardarReferencia: ', id_referencia)
                    referencia = getReferenciaByID(baseDatos, id_referencia)
                    referencia.nombre = request.form['refNombreEmp']
                    referencia.apellido = request.form['refApellidoEmp']
                    referencia.telefono = request.form['refTelefonoEmp']
                    referencia.trabaja_desde = request.form['refTrabDesde']
                    referencia.trabaja_hasta = request.form['refTrabHasta']
                    referencia.actualizarReferencia(baseDatos)
                    print('Referencia actualizada')
                    session.pop('id_refer')
                return redirect(url_for('refresh_referencia'))

            elif request.form.get('btnEditarReferencia'):
                id_referencia = int(parametros['btnEditarReferencia'])
                print('id_referencia en EditarReferencia: ', id_referencia)
                session['id_refer'] = id_referencia
                return redirect(url_for('refresh_referencia'))

            elif request.form.get('btnBorrarReferencia'):
                id_referencia = int(parametros['btnBorrarReferencia'])
                print('id_referencia en BorrarReferencia: ', id_referencia)
                referencia = getReferenciaByID(baseDatos, id_referencia)
                referencia.borrarReferencia(baseDatos)
                return redirect(url_for('refresh_referencia'))

            else:
                nombre = parametros['nombre']
                apellido = parametros['apellido']
                nacimiento = parametros['cumple']
                genero = int(parametros['genero'])
                domicilio = parametros['domicilio']
                nacionalidad = parametros['nacionalidad']
                mail = parametros['email']
                telefono = parametros['tel']
                password = parametros['password']

                # Debo controlar si la cédula está en los parámetros, porque cuando se deshabilita
                # en la edición del perfil la cédula no viene en la lista de parámetros y explota, OJO!
                if 'cedula' in parametros:
                    cedula = parametros['cedula']
                else:
                    cedula = None

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
                    new_empleado = Empleado(0, cedula, nombre, apellido, nacimiento, genero, domicilio,
                                            nacionalidad, mail, telefono, 0, '', 'images/Perfiles/NoImage.png', 0, usuario, None, None, None)

                    # como es edición de perfil debo modificar la contraseña y el empleado
                    if logueado:
                        # modificar contraseña?

                        # recorrer la disponibilidad seleccionada y cargarsela al empleado
                        disponibilidad = list()
                        disponibilidadesRegistradas = getDisponibilidadesRegistradas(
                            baseDatos)
                        for disp in disponibilidadesRegistradas:
                            indice = str(
                                disponibilidadesRegistradas.index(disp)+1)
                            if 'disp'+indice in parametros:
                                # print('**** Debería cargar esta disponibilidad: ID=', disp.id, ', DESC=', disp.descripcion)
                                d = Disponibilidad(disp.id, disp.descripcion)
                                disponibilidad.append(d)
                        new_empleado.cargarDisponibilidad(disponibilidad)

                        # recorrer las tareas seleccionadas y cargarselas al empleado
                        tareas = list()
                        tareasRegistradas = getTareasRegistradas(baseDatos)
                        for tarea in tareasRegistradas:
                            indice = str(tareasRegistradas.index(tarea)+1)
                            if 'tarea'+indice in parametros:
                                # print('**** Debería cargar esta tarea: ID=', tarea.id, ', DESC=', tarea.descripcion)
                                t = Tarea(tarea.id, tarea.descripcion)
                                tareas.append(t)
                        new_empleado.cargarTareas(tareas)

                        tiene_experiencia = parametros['experiencia']
                        if tiene_experiencia == '1':
                            experiencia = parametros['mesesExperiencia']
                        else:
                            experiencia = 0

                        descripcion = parametros['presentacion']
                        new_empleado.id = session['id_empleado']
                        new_empleado.experiencia_meses = experiencia
                        new_empleado.descripcion = descripcion

                        if request.files:
                            foto = request.files["fotoPerfil"]
                            if foto.filename == '':
                                #print('No hay foto cargada, mantengo la que tenía')
                                filename = secure_filename(getEmpleadoByID(baseDatos, session['id_empleado']).foto)
                                rutaFisica = os.path.join(app.config['CARPETA_FISICA_IMAGENES'], filename)
                                # Si no se pudo cargar la foto cargo la imagen default
                                if not os.path.exists(rutaFisica):
                                    filename = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
                                new_empleado.foto = filename
                            else:
                                if archivoAdmitido(foto.filename):
                                    filename = secure_filename(foto.filename)
                                    rutaFisica = os.path.join(app.config['CARPETA_FISICA_IMAGENES'], filename)
                                    #print('rutaFisica: ', rutaFisica)
                                    foto.save(rutaFisica)
                                    # Si no se pudo guardar la foto cargo la imagen default
                                    if not os.path.exists(rutaFisica):
                                        filename ='NoImage.png'
                                        foto.save(os.path.join(app.config['CARPETA_FISICA_IMAGENES'], filename))
                                    new_empleado.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], filename)

                        new_empleado.modificarEmpleado(baseDatos)
                        return redirect(url_for('inicio_empleados'))

                    # como es registro (alta) debo crear el empleado
                    else:
                        new_empleado.crearEmpleado(baseDatos)
                        login(cedula, password)
                        return redirect(url_for('inicio_empleados'))

                elif tipo == 'Empleador':
                    # debo crear un empleador
                    new_empleador = Empleador(0, cedula, nombre, apellido, nacimiento, genero,
                                              domicilio, nacionalidad, mail, telefono, 0, 'images/Perfiles/NoImage.png', 0, usuario)

                    # como es edición de perfil debo modificar la contraseña y el empleador
                    if logueado:
                        # modificar contraseña?
                        tiene_bps = parametros['bps']
                        if tiene_bps == '1':
                            regBPS = parametros['empleadorNumRegBPS']
                        else:
                            regBPS = '0'

                        if request.files:
                            foto = request.files["fotoPerfil"]
                            if foto.filename == '':
                                #print('No hay foto cargada, mantengo la que tenía')
                                filename = secure_filename(getEmpleadorByID(baseDatos, session['id_empleador']).foto)
                                rutaFisica = os.path.join(app.config['CARPETA_FISICA_IMAGENES'], filename)
                                # Si no se pudo cargar la foto cargo la imagen default
                                if not os.path.exists(rutaFisica):
                                    filename = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
                                new_empleador.foto = filename
                            else:
                                if archivoAdmitido(foto.filename):
                                    filename = secure_filename(foto.filename)
                                    rutaFisica = os.path.join(app.config['CARPETA_FISICA_IMAGENES'], filename)
                                    #print('rutaFisica: ', rutaFisica)
                                    foto.save(rutaFisica)
                                    # Si no se pudo guardar la foto cargo la imagen default
                                    if not os.path.exists(rutaFisica):
                                        filename ='NoImage.png'
                                        foto.save(os.path.join(app.config['CARPETA_FISICA_IMAGENES'], filename))
                                    new_empleador.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], filename)

                        new_empleador.registroBps = regBPS
                        new_empleador.id = session['id_empleador']
                        new_empleador.modificarEmpleador(baseDatos)

                    # como es registro (alta) debo crear el empleado
                    else:
                        new_empleador.crearEmpleador(baseDatos)
                        login(cedula, password)
                    return redirect(url_for('inicio_empleadores'))


@app.route('/RefreshReferencia/', methods=['POST', 'GET'])
def refresh_referencia():
    return redirect(url_for('perfil', opcion='Empleado') + '#anclaReferencias')


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


@app.route('/HomeEmpleados/', methods=['POST', 'GET'])
def inicio_empleados():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleador':
        return redirect(url_for('inicio_empleadores'))
    else:
        empleado = getEmpleadoByID(baseDatos, session['id_empleado'])
        # Si no se puede cargar la foto guardada en la base cargo la imagen default
        rutaFisica = '.' + url_for('static', filename=empleado.foto)
        if not os.path.exists(rutaFisica):
            empleado.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')

        # se debe verificar que el empleado no tenga mensajes sin leer, en caso afirmativo se debe notificar
        tieneNotifMensajes = empleadoTieneMensajesSinLeer(baseDatos, empleado.id)
        # se debe verificar que el empleado este notificado sobre todos sus vínculos, en caso negativo se debe notificar
        tieneNotifVinculos = empleadoTieneNotificacionesPendientesVinculos(baseDatos, session['id_empleado'])
        # Se debe verificar que el empleado no tenga recordatorios pendientes para resolver
        tieneRecordatoriosPendientes = getRecordatoriosCalificacionesPendientes()
        #print('tieneRecordatoriosPendientes: ', tieneRecordatoriosPendientes)
        cal = getPromedioByEmpleadoId(baseDatos, empleado.id)
        return render_template('HomeEmpleados.html', sujeto=empleado, tieneMensajesSinLeer=tieneNotifMensajes, 
        tieneNotifPendientesVinculos=tieneNotifVinculos, tieneRecordatorios=tieneRecordatoriosPendientes, cal=cal)


@app.route('/HomeEmpleadores/', methods=['POST', 'GET'])
def inicio_empleadores():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        #print('getRecordatoriosDelDia(): ', getRecordatoriosDelDia())
        empleador = getEmpleadorByID(baseDatos, session['id_empleador'])
        # Si no se puede cargar la foto guardada en la base cargo la imagen default
        rutaFisica = '.' + url_for('static', filename=empleador.foto)
        if not os.path.exists(rutaFisica):
            empleador.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
        # se debe verificar que el empleador no tenga mensajes sin leer, en caso afirmativo se debe notificar
        tieneNotifMensajes = empleadorTieneMensajesSinLeer(baseDatos, empleador.id)
        # se debe verificar que el empleador este notificado sobre todas las postulaciones a sus anuncios, 
        # en caso negativo se debe notificar
        tieneNotifPostulaciones = empleadorTieneNotificacionesPendientesPostulaciones(baseDatos, session['id_empleador'])
        # Se debe verificar que el empleador no tenga recordatorios pendientes para resolver
        tieneRecordatoriosPendientes = getRecordatoriosCalificacionesPendientes()
        #print('tieneRecordatoriosPendientes: ', tieneRecordatoriosPendientes)
        cal = getPromedioByEmpleadorId(baseDatos, empleador.id)
        return render_template('HomeEmpleadores.html', sujeto=empleador, tieneMensajesSinLeer=tieneNotifMensajes, 
        tieneNotifPendientesPostulaciones=tieneNotifPostulaciones, tieneRecordatorios=tieneRecordatoriosPendientes, cal=cal)


@app.route('/PanelControl/')
def administrar():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Empleador':
        return redirect(url_for('inicio_empleadores'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        datosAdmin = getDatosAdmin(baseDatos)
        return render_template('ControlPanel.html', data=datosAdmin)


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
            if request.form['radioExperiencia'] == 'experienciaSi':
                nexperiencia = 1
            else:
                nexperiencia = 0
            print("request.form.get('radioExperiencia'):",
                  request.form.get('radioExperiencia'))
            npago_hora = request.form['pagoPorHora']
            print('nexperiencia: ', nexperiencia)
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
            #flash('Anuncio creado!')
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
        #flash('Anuncio eliminado!')
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
        estadoInt = int.from_bytes(anuncio.estado, "big")
        anuncio.estado = estadoInt

        if anuncio.estado == 1:
            estado = 1
        else:
            estado = 0
        if anuncio.experiencia == 1:
            experiencia = 1
        else:
            experiencia = 0
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
            experiencia,
            anuncio.pago_hora,
            estado
        ]
        print(lista[14])
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
            if request.form.get('radioExperiencia') == '1':
                new_experiencia = 1
            elif request.form.get('radioExperiencia') == '0':
                new_experiencia = 0
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
        domicilio = empleado.domicilio
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
            disponibilidades,
            domicilio
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
            domicilioAnuncio = elAnuncio[1].empleador.domicilio
            idAnuncio = elAnuncio[0]
            disponibilidadAnuncio = elAnuncio[1].disponibilidad
            experienciaAnuncio = elAnuncio[1].experiencia
            # if elAnuncio[1].experiencia == 0:
            #    experienciaAnuncio = 0
            # else:
            #    experienciaAnuncio = 1
            tareasAnuncio = []

            if elAnuncio[1].estado == b'\x01':
                # empleador = getEmpleadorByID(baseDatos, elAnuncio.)
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
                anun.append(domicilioAnuncio)
                listaDeAnuncios.append(anun)
        listaMatcheo = []

        for a in listaDeAnuncios:
            if a[3] & empl[1] == a[3] and a[1] in empl[2] and a[4] == empl[3] and empl[0] >= a[2]:
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
        # Si no se puede cargar la foto guardada en la base cargo la imagen default
        rutaFisica = '.' + url_for('static', filename=empleador.foto)
        if not os.path.exists(rutaFisica):
            empleador.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')

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
        if elAnuncio[0].experiencia == 0:
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
        cal = getPromedioByEmpleadorId(baseDatos, empleador.id)

        post = getPostulacionEmpleadoAnuncio(baseDatos, session['id_empleado'], idAnuncio)
        context = {
            'empleador': empleador,
            'anuncio': listaAnuncio,
            'postulacion': postulacion,
            'cal': cal,
            'post' : post
        }

        # el desempaquetado tendrá 3 claves, 'empleador', 'anuncio' y psotulacion
        # 'empleador' : objeto empleador
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

        # Se debe notificar al empleado mediante mensaje de que se ha postulado
        mensajeEmpleado = Mensaje(0, empleado, anuncio.empleador, anuncio, datetime.now(
        ), 'Buena suerte {} {}!!! te has postulado al anuncio "{}"'.format(empleado.nombre, empleado.apellido, anuncio.titulo), 3, 1, False)
        mensajeEmpleado.crearMensaje(baseDatos)

        # Se debe notificar al empleador mediante mensaje de que se ha postulado
        mensajeEmpleador = Mensaje(0, empleado, anuncio.empleador, anuncio, datetime.now(
        ), 'Buenas noticias!!! {} {} se ha postulado a tu anuncio "{}"'.format(empleado.nombre, empleado.apellido, anuncio.titulo), 3, 2, False)
        mensajeEmpleador.crearMensaje(baseDatos)

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
            lista.append(getPostulacionEmpleadoAnuncio(
                baseDatos, idEmpleado, postulacion.anuncio))
            lista.append(postulacion)
            misPostulaciones.append(lista)

        for post in misPostulaciones:
            if post[1].estado == b'\x01':
                post.append(1)
            else:
                post.append(0)

        return render_template('TusPostulaciones.html', postulaciones=misPostulaciones)


@app.route('/despostularse/<idPostulacion>') 
def despostularse(idPostulacion):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleador':
        return redirect(url_for('inicio_empleadores'))
    else:
        empleado = getEmpleadoByID(baseDatos, session['id_empleado'])
        postulacion = getPostulacionById(baseDatos, idPostulacion)
        postulacion.borrarPostulacion(baseDatos)
        anuncio = postulacion.anuncio

        # Se debe notificar al empleado mediante mensaje de que se ha despostulado del anuncio
        mensajeEmpleado = Mensaje(0, empleado, anuncio.empleador, anuncio, datetime.now(
        ), '{} {}, te has despostulado del anuncio "{}"'.format(empleado.nombre, empleado.apellido, anuncio.titulo), 3, 1, False)
        mensajeEmpleado.crearMensaje(baseDatos)

        # Se debe notificar al empleador mediante mensaje de que se han despostulado de su anuncio
        mensajeEmpleador = Mensaje(0, empleado, anuncio.empleador, anuncio, datetime.now(
        ), '{} {} se ha despostulado de tu anuncio "{}"'.format(empleado.nombre, empleado.apellido, anuncio.titulo), 3, 2, False)
        mensajeEmpleador.crearMensaje(baseDatos)

        return redirect(url_for('mis_postulaciones'))


@app.route('/MisVinculos')
def mis_vinculos():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        if session.get('usertype') == 'Empleado':
            empleado = getEmpleadoByID(baseDatos, session['id_empleado'])
            context = {
                'vinculos': getVinculoByEmpleado(baseDatos, empleado),
                'sesion': session.get('usertype')
            }
            # Obtener la lista de vínculos que no hayan sido notificados al Empleado
            listaVinculosNoNotif = getVinculosNoNotificadosDelEmpleado(baseDatos, empleado)
            # se deben marcar los vinculos como notificados
            for vinculo in listaVinculosNoNotif:
                #print('ID de vinculo a marcar como notificado: ', vinculo.id)
                vinculo.marcarVinculoComoNotificado(baseDatos)

            return render_template('MisVinculos.html', **context)
        elif session.get('usertype') == 'Empleador':
            empleador = getEmpleadorByID(baseDatos, session['id_empleador'])

            context = {
                'vinculos': getVinculoByEmpleador(baseDatos, empleador),
                'sesion': session.get('usertype')
            }
            return render_template('MisVinculos.html', **context)
        else:
            return redirect(url_for('logueo'))


@app.route('/verVinculo/<idVinculo>')
def ver_vinculo(idVinculo):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        vinculo = getVinculoIDs(baseDatos, idVinculo)
        empleador = getEmpleadorByID(baseDatos, vinculo.empleador)
        # Si no se puede cargar la foto guardada en la base cargo la imagen default
        rutaFisica = '.' + url_for('static', filename=empleador.foto)
        if not os.path.exists(rutaFisica):
            empleador.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
        empleado = getEmpleadoByID(baseDatos, vinculo.empleado)
        # Si no se puede cargar la foto guardada en la base cargo la imagen default
        rutaFisica = '.' + url_for('static', filename=empleado.foto)
        if not os.path.exists(rutaFisica):
            empleado.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
        anuncio = getAnuncioByID(baseDatos, vinculo.anuncio)
        extension = datetime.now().date() - vinculo.fecha_inicio
        calempleado = getPromedioByEmpleadoId(baseDatos, empleado.id)
        calempleador = getPromedioByEmpleadorId(baseDatos, empleador.id)
        context = {
            'vinculo': vinculo,
            'anuncio': anuncio,
            'empleado': empleado,
            'empleador': empleador,
            'user': session.get('usertype'),
            'extension': int(str(extension.days)),
            'calEmpleado': calempleado,
            'calEmpleador': calempleador

        }
        return render_template('verVinculo.html', **context)


@app.route('/notVinculo/<idVinculo>')
def not_vinculo(idVinculo):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        vinculo = getVinculoByID(baseDatos, idVinculo)
        postulacion = getPostulacionEmpleadoAnuncio(baseDatos, session['id_empleado'], vinculo.anuncio.id)
        vinculo.borrarVinculo(baseDatos)
        postulacion.eliminarVinculoEnPostulacion(baseDatos)
        return redirect(url_for('mis_vinculos'))

    else:
        vinculo = getVinculoByID(baseDatos, idVinculo)
        postulacion = getPostulacionEmpleadoAnuncio(baseDatos, vinculo.empleado.id, vinculo.anuncio.id)
        vinculo.borrarVinculo(baseDatos)
        postulacion.eliminarVinculoEnPostulacion(baseDatos)
        return redirect(url_for('mis_vinculos'))


@app.route('/calVinculo/<idVinculo>/', methods=['POST'])
def cal_vinculo(idVinculo):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':    
        if request.method == 'POST':
            cal = request.form.get('rating')
            vinculo = getVinculoByID(baseDatos, idVinculo)
            vinculo.calif_empleador = cal
            vinculo.actualizarVinculo(baseDatos)
            empleador = vinculo.empleador# Si no se puede cargar la foto guardada en la base cargo la imagen default
            rutaFisica = '.' + url_for('static', filename=empleador.foto)
            if not os.path.exists(rutaFisica):
                empleador.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
            empleador.promedioCalificacion = getPromedioByEmpleadorId(baseDatos, empleador.id)['promedio']
            empleador.calificarEmpleador(baseDatos)
        return redirect(url_for('ver_vinculo', idVinculo = idVinculo))
    else:
        if request.method == 'POST':
            cal = request.form.get('rating')
            vinculo = getVinculoByID(baseDatos, idVinculo)
            vinculo.calif_empleado = cal
            vinculo.actualizarVinculo(baseDatos)
            empleado = vinculo.empleado
            # Si no se puede cargar la foto guardada en la base cargo la imagen default
            rutaFisica = '.' + url_for('static', filename=empleado.foto)
            if not os.path.exists(rutaFisica):
                empleado.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
            empleado.promedioCalificacion = getPromedioByEmpleadoId(baseDatos, empleado.id)['promedio']
            empleado.calificarEmpleado(baseDatos)
        return redirect(url_for('ver_vinculo', idVinculo = idVinculo))


@app.route('/calificarVinculosPendientes/<bloqueado>', methods=['POST'])
def calificar_vinculos_pendientes(bloqueado):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        if request.method == 'POST':
            parametros = request.form
            #for param in parametros:
                #print('parametro: ', param)
            idRecordatorio = parametros.get('idRecordatorio')
            idVinculo = parametros.get('idVinculo')
            cant_recordatorios = int(parametros.get('cant_recordatorios'))
            cal = parametros.get('rating' + str(idVinculo))
            vinculo = getVinculoByID(baseDatos, idVinculo)
            recordatorio : Recordatorio = getRecordatorioByID(baseDatos, idRecordatorio)

            if 'btnCalificarAhora' in parametros:
                # como está calificando debo eliminar el recordatorio
                recordatorio.borrarRecordatorio(baseDatos)
                # genero el mensaje que se mostrará en el ambito que corresponda
                flash('Has calificado satisfactoriamente con ' + str(cal) + ' estrellas tu vínculo sobre el anuncio: ' + str(vinculo.anuncio.titulo))
            elif 'btnCalificarLuego' in parametros:
                # como está posponiendo el recordatorio debo actualizar su fecha, 
                # la cantidad de veces aplazado y si debe ser o no bloqueante
                recordatorio.fechaRecordatorio += timedelta(days=90)
                recordatorio.cantVecesAplazado += 1
                recordatorio.actualizarRecordatorio(baseDatos)

            if session.get('usertype') == 'Empleado':
                if 'btnCalificarAhora' in parametros:             
                    vinculo.calif_empleador = cal
                    vinculo.actualizarVinculo(baseDatos)
                    empleador = vinculo.empleador
                    # Si no se puede cargar la foto guardada en la base cargo la imagen default
                    rutaFisica = '.' + url_for('static', filename=empleador.foto)
                    if not os.path.exists(rutaFisica):
                        empleador.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
                    empleador.promedioCalificacion = getPromedioByEmpleadorId(baseDatos, empleador.id)['promedio']
                    empleador.calificarEmpleador(baseDatos)

                # Si había un solo recordatorio como ya lo procesó lo debo enviar al Home
                if cant_recordatorios == 1:
                    return redirect(url_for('inicio_empleados'))


            elif session.get('usertype') == 'Empleador':
                if 'btnCalificarAhora' in parametros:
                    vinculo.calif_empleado = cal
                    vinculo.actualizarVinculo(baseDatos)
                    empleado = vinculo.empleado
                    # Si no se puede cargar la foto guardada en la base cargo la imagen default
                    rutaFisica = '.' + url_for('static', filename=empleado.foto)
                    if not os.path.exists(rutaFisica):
                        empleado.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
                    empleado.promedioCalificacion = getPromedioByEmpleadoId(baseDatos, empleado.id)['promedio']
                    empleado.calificarEmpleado(baseDatos)

                # Si había un solo recordatorio como ya lo procesó lo debo enviar al Home
                if cant_recordatorios == 1:
                    return redirect(url_for('inicio_empleadores'))
            
            # Como son varios los recordatorios tengo que regresar al form de origen para que siga calificando
            if bloqueado == 'True':
                return redirect(url_for('desbloqueo_cuenta'))
            else:
                if 'ventanaModal' in parametros and session.get('usertype') == 'Empleado':
                    return redirect(url_for('inicio_empleados'))
                elif 'ventanaModal' in parametros and session.get('usertype') == 'Empleador':
                    return redirect(url_for('inicio_empleadores'))
                else:
                    return redirect(url_for('calificaciones_pendientes'))
                

@app.route('/endVinculo/<idVinculo>/', methods=['POST'])
def end_vinculo(idVinculo):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        if request.method == 'POST':
            cal = request.form.get('rating')
            vinculo = getVinculoByID(baseDatos, idVinculo)
            empleador = vinculo.empleador
            # Si no se puede cargar la foto guardada en la base cargo la imagen default
            rutaFisica = '.' + url_for('static', filename=empleador.foto)
            if not os.path.exists(rutaFisica):
                empleador.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
            empleado = vinculo.empleado
            # Si no se puede cargar la foto guardada en la base cargo la imagen default
            rutaFisica = '.' + url_for('static', filename=empleado.foto)
            if not os.path.exists(rutaFisica):
                empleado.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')
            anuncio = vinculo.anuncio

            if session.get('usertype') == 'Empleado':
                vinculo.calif_empleador = cal
                vinculo.fecha_fin = datetime.now()
                vinculo.actualizarVinculo(baseDatos)
                empleador.promedioCalificacion = getPromedioByEmpleadorId(baseDatos, empleador.id)['promedio']
                empleador.calificarEmpleador(baseDatos)
        
            if session.get('usertype') == 'Empleador':
                vinculo.calif_empleado = cal
                vinculo.fecha_fin = datetime.now()
                vinculo.actualizarVinculo(baseDatos)
                empleado.promedioCalificacion = getPromedioByEmpleadoId(baseDatos, empleado.id)['promedio']
                empleado.calificarEmpleado(baseDatos)
    
            # Se debe notificar al empleado mediante mensaje de que el vínculo con el empleador "X" finalizó
            mensajeEmpleado = Mensaje(0, empleado, empleador, anuncio, datetime.now(), 
            'Su vínculo con {} {} por el anuncio "{}" ha finalizado. Recuerde que puede calificar el vínculo cuantas veces lo considere desde "Mis Vínculos"'
            .format(empleador.nombre, empleador.apellido, anuncio.titulo), 3, 1, False)
            mensajeEmpleado.crearMensaje(baseDatos)

            # Se debe notificar al empleador mediante mensaje de que el vínculo con el empleado "X" finalizó
            mensajeEmpleador = Mensaje(0, empleado, empleador, anuncio, datetime.now(), 
            'Su vínculo con {} {} por el anuncio "{}" ha finalizado. Recuerde que puede calificar el vínculo cuantas veces lo considere desde "Mis Vínculos"'
            .format(empleado.nombre, empleado.apellido, anuncio.titulo), 3, 2, False)
            mensajeEmpleador.crearMensaje(baseDatos)

            return redirect(url_for('ver_vinculo', idVinculo = idVinculo))


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
        listaPostulaciones = getPostulacionesAnuncio(baseDatos, id_anuncio)
        postulaciones = []
        for postulacion in listaPostulaciones:
            
            # se deben marcar como notificadas las postulaciones que no lo estén
            if not postulacion.fueNotificada(baseDatos):
                #print('ID de postulación a marcar como notificada: ', postulacion.id)
                postulacion.marcarPostulacionComoNotificada(baseDatos)
            
            post = []
            cal = getPromedioByEmpleadoId(baseDatos, postulacion.empleado.id)
            l = [postulacion]
            post.append(l)
            post.append(cal)
            postulaciones.append(post)

        pares = postulaciones[0:][::2]
        impares = postulaciones[1:][::2]


        return render_template('ListaCandidatos.html', elemPares=pares, elemImpares=impares, elanuncio=anuncio)


@app.route('/MensajesEmpleado/<idEmpleado>/<idEmpleador>', methods=['POST', 'GET'])
def mensajes_empleado(idEmpleado, idEmpleador):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleador':
        return redirect(url_for('inicio_empleadores'))
    else:
        diccMensajes = getMensajesParaEmpleado(baseDatos, idEmpleado)
        objeto = getEmpleadoByID(baseDatos, idEmpleado)

        vinculo = tieneElEmpleadoVinculoConEmpleador(baseDatos, idEmpleado, idEmpleador)
        postulacion = existePostulacionDeEmpleadoEnAnuncioDeEmpleador(baseDatos, idEmpleado, idEmpleador)
        if tieneElEmpleadoMensajeDeEmpleador(baseDatos, idEmpleado, idEmpleador):
            tipoEmisor = 2
        else:
            tipoEmisor = 3
        dtoMensaje = DTOMensaje(vinculo, postulacion, tipoEmisor)

        if int(idEmpleador) == 0:
            # carga inicial del form, no hay remitente seleccionado,
            # solo se va a cargar la lista de remitentes con panel de mensajes vacío
            elEmpleador = None
        else:
            elEmpleador = getEmpleadorByID(baseDatos, int(idEmpleador))
            # se deben marcar los mensajes como leídos
            for mensaje in diccMensajes.get(int(idEmpleador)):
                if mensaje.tipoReceptor == 1 and mensaje.leido == False:
                    mensaje.marcarMensajeComoLeido(baseDatos)

        return render_template('Mensajes.html', diccmensajes=diccMensajes, actor=objeto, interactuanteseleccionado=elEmpleador, dto=dtoMensaje)


@app.route('/MensajesEmpleador/<idEmpleador>/<idEmpleado>', methods=['POST', 'GET'])
def mensajes_empleador(idEmpleador, idEmpleado):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    elif session.get('usertype') == 'Empleado':
        return redirect(url_for('inicio_empleados'))
    else:
        diccMensajes = getMensajesParaEmpleador(baseDatos, idEmpleador)
        objeto = getEmpleadorByID(baseDatos, idEmpleador)

        vinculo = tieneElEmpleadorVinculoConEmpleado(baseDatos, idEmpleador, idEmpleado)
        postulacion = existePostulacionDeEmpleadoEnAnuncioDeEmpleador(baseDatos, idEmpleado, idEmpleador)
        dtoMensaje = DTOMensaje(vinculo, postulacion, 1)

        if int(idEmpleado) == 0:
            # carga inicial del form, no hay remitente seleccionado,
            # solo se va a cargar la lista de remitentes con panel de mensajes vacío
            elEmpleado = None
        else:
            elEmpleado = getEmpleadoByID(baseDatos, int(idEmpleado))
            # se deben marcar los mensajes como leídos
            for mensaje in diccMensajes.get(int(idEmpleado)):
                if mensaje.tipoReceptor == 2 and mensaje.leido == False:
                    mensaje.marcarMensajeComoLeido(baseDatos)

        return render_template('Mensajes.html', diccmensajes=diccMensajes, actor=objeto, interactuanteseleccionado=elEmpleado, dto=dtoMensaje)


@app.route('/AgregarMensaje/<idDestinatario>/<idAnuncio>', methods=['POST', 'GET'])
def agregar_mensaje(idDestinatario, idAnuncio):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        if request.method == 'POST':
            mensaje = request.form['cajaMensaje']
            if int(idAnuncio) == 0:
                anuncio = None
            else:
                anuncio = getAnuncioByID(baseDatos, idAnuncio)

            if session['usertype'] == 'Empleado':
                empleado = getEmpleadoByID(baseDatos, session['id_empleado'])
                empleador = getEmpleadorByID(baseDatos, idDestinatario)
                mensajeEmpleado = Mensaje(
                    0, empleado, empleador, anuncio, datetime.now(), mensaje, 1, 2, False)
                mensajeEmpleado.crearMensaje(baseDatos)
                return redirect(url_for('mensajes_empleado', idEmpleado=empleado.id, idEmpleador=empleador.id))

            elif session['usertype'] == 'Empleador':
                empleador = getEmpleadorByID(
                    baseDatos, session['id_empleador'])
                empleado = getEmpleadoByID(baseDatos, idDestinatario)
                mensajeEmpleador = Mensaje(
                    0, empleado, empleador, anuncio, datetime.now(), mensaje, 2, 1, False)
                mensajeEmpleador.crearMensaje(baseDatos)
                return redirect(url_for('mensajes_empleador', idEmpleador=empleador.id, idEmpleado=empleado.id))


@app.route('/Contratar/<idEmpleado>')
def contratar(idEmpleado):
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
                          datetime.now(), None, '', None, None)
        vinculo.crearVinculo(baseDatos)

        # El anuncio debe quedar inactivo
        anuncio.setEstadoAnuncio(baseDatos, False)

        # Se debe actualizar la postulación a genera_vinculo = true
        postulacion: Postulacion = getPostulacionEmpleadoAnuncio(
            baseDatos, empleado.id, anuncio.id)
        postulacion.generarVinculoEnPostulacion(baseDatos)

        # Se debe notificar al empleado mediante mensaje de que el empleador "X" lo contrató
        mensajeEmpleado = Mensaje(
            0, empleado, empleador, anuncio, datetime.now(), 'Felicidades!!! Has sido contratado por {} {}, por el anuncio "{}", les deseamos un buen vínculo laboral.'.format(empleador.nombre, empleador.apellido, anuncio.titulo), 3, 1, False)
        mensajeEmpleado.crearMensaje(baseDatos)

        # Se debe notificar al empleador mediante mensaje de que contrató al empleador "X"
        mensajeEmpleador = Mensaje(
            0, empleado, empleador, anuncio, datetime.now(), 'Felicidades!!! Has contratado a {} {}, por el anuncio "{}", les deseamos un buen vínculo laboral.'.format(empleado.nombre, empleado.apellido, anuncio.titulo), 3, 2, False)
        mensajeEmpleador.crearMensaje(baseDatos)

        # Se debe generar recordatorio de calificación para el empleado
        recordatorioEmpleado = Recordatorio(0, 1, empleado, empleador, empleado, anuncio, postulacion, vinculo, datetime.now() + timedelta(days=90), datetime.now() + timedelta(days=270), 0, 'Debe calificar el vínculo', 0)
        recordatorioEmpleado.crearRecordatorio(baseDatos)
        
        # Se debe generar recordatorio de calificación para el empleador
        recordatorioEmpleador = Recordatorio(0, 1, empleado, empleador, empleador, anuncio, postulacion, vinculo, datetime.now() + timedelta(days=90), datetime.now() + timedelta(days=270), 0, 'Debe calificar el vínculo', 0)
        recordatorioEmpleador.crearRecordatorio(baseDatos)

        return render_template('contactoEmpleado.html', data=empleado)


@app.route('/RankingPorCalificacion/<tipo>')
def ranking_calificaciones(tipo):
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    #elif session.get('usertype') == 'Administrador':
        #return redirect(url_for('administrar'))
    else:
        listado = list()
        if tipo == 'Empleador':
            listado = getRankingPorCalificacionEmpleadores(baseDatos, 20)
        elif tipo == 'Empleado':
            listado = getRankingPorCalificacionEmpleados(baseDatos, 20)

        for item in listado:
            rutaFisica = '.' + url_for('static', filename=item.foto)
            # Si no se puede cargar la foto guardada en la base cargo la imagen default
            if not os.path.exists(rutaFisica):
                item.foto = os.path.join(app.config['CARPETA_CARGA_IMAGENES'], 'NoImage.png')

        pares = listado[0:][::2]
        impares = listado[1:][::2]
        return render_template('RankingPorCalificacion.html', elemPares=pares, elemImpares=impares, tipo=tipo)


@app.route('/PlanesPremium')
def planes_premium():
    return render_template('PlanesPremium.html')


@app.route('/CalificacionesPendientes/')
def calificaciones_pendientes():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        if getRecordatoriosCalificacionesPendientes() is None:
            return render_template('Inicio.html')
        else:
            return render_template('CalificacionesPendientes.html')


@app.route('/DesbloqueoCuenta/')
def desbloqueo_cuenta():
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    elif session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        if getRecordatoriosBloqueantes() is None:
            return render_template('Inicio.html')
        else:
            return render_template('DesbloqueoCuenta.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)
