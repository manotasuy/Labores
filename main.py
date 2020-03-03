import json
from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_mysqldb import MySQL
from datetime import datetime
from enum import Enum

# Paquetes implementación
from Implementacion import Conexion
from Implementacion import Usuario
from Implementacion import Empleado
from Implementacion import Empleador
from Implementacion import Anuncio

app = Flask(__name__)
baseDatos = Conexion.connectionDb(app)

# session
app.secret_key = "session"


class Tipo_Usuario(Enum):
    Administrador = 1
    Empleado = 2
    Empleador = 3

#print(Tipo_Usuario.Administrador)
#print(Tipo_Usuario.Administrador.value)

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
    if session.get('usertype') == None:
        return redirect(url_for('logueo'))
    else:
        return render_template('RecuperarClave.html')


@app.route('/Ingresar', methods=['POST'])
def ingresar():
    if request.method == 'POST':
            parametros = request.form
            user = parametros['user']
            password = parametros['pass']
            usuario = Usuario.Usuario(0, user, password, '')
            retorno = usuario.loginUsuario(baseDatos)
            session['username'] = user
            session['usertype'] = retorno[0][0]

            if session['usertype'] == 'Empleador':
                return redirect(url_for('inicio_empleadores'))
            elif session['usertype'] == 'Empleado':
                return redirect(url_for('inicio_empleados'))
            else:
                return redirect(url_for('administrar'))
        

@app.route('/SignUp/')
def opcion_registrarse():
    return render_template('OpcionRegistro.html')


@app.route('/Registro/<opcion>')
def registrarse(opcion):
    session['useroption'] = opcion
    return render_template('Registro.html')


@app.route('/Registrar/<opcion>', methods=['POST'])
def registrar_usuario(opcion):
    if session.get('usertype') == 'Administrador':
        return redirect(url_for('administrar'))
    else:
        if request.method == 'POST':
            parametros = request.form
            nombre = parametros['txtNombre']
            apellido = parametros['txtApellido']
            txtNacimiento = parametros['txtNacimiento']
            nacimiento = datetime.strptime(txtNacimiento, '%d/%m/%Y')
            genero = 'Masculino'
            cedula = parametros['txtCedula']
            domicilio = parametros['txtDomicilio']
            nacionalidad = parametros['txtNacionalidad']
            mail = parametros['txtMail']
            telefono = parametros['txtTelefono']
            password = 'labores'

            usuario = Usuario.Usuario(0, cedula, password, opcion)
            usuario.crearUsuario(baseDatos)
            usuario.getIdUsuario(baseDatos)

            if opcion == 'Empleado':
                empleado = Empleado.Empleado(0, cedula, nombre, apellido, nacimiento, genero, domicilio, nacionalidad, mail, telefono, None, None, None, None, usuario, None, None, None)
                empleado.crearEmpleado(baseDatos)
                return redirect(url_for('inicio_empleados'))
            elif opcion == 'Empleador':
                empleador = Empleador.Empleador(0, cedula, nombre, apellido, nacimiento, genero, domicilio, nacionalidad, mail, telefono, None, None, None, usuario)
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
            #fechaInicio =  tomarla con datetime
            #fechaCierre =  null
            estado = request.form['estado']
            experiencia = request.form['experiencia']
            salario = request.form['salario']
            #idEmpleador = viene de la sesión
            calEmpleado = request.form['calEmpleado']
            calEmpleador = request.form['calEmpleador']
            tieneVinculo = request.form['tieneVinculo']
            crearAnuncio(
                titulo, 
                descripcion, 
                #fechaInicio, 
                #fechaCierre,
                estado,
                experiencia,
                salario,
                #idEmpleador,
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


if __name__ == '__main__':
    app.run(debug=True)