import json
from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_mysqldb import MySQL
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
    session.pop('username')
    session.pop('usertype')
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
        usuario = Usuario.Usuario(0, user, password, '')
        retorno = usuario.loginUsuario(baseDatos)
        print(retorno)
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
    session['user_option'] = opcion
    return render_template('Registro.html')


@app.route('/Registrar/<opcion>', methods=['POST'])
def registrar_usuario(opcion):
    if request.method == 'POST':
        parametros = request.form
        nombre = parametros['txtNombre']
        apellido = parametros['txtApellido']
        nacimiento = parametros['txtNacimiento']
        genero = 'Masculino'
        cedula = parametros['txtCedula']
        domicilio = parametros['txtDomicilio']
        nacionalidad = parametros['txtNacionalidad']
        mail = parametros['txtMail']
        telefono = parametros['txtTelefono']
        password = 'labores'

        usuario = Usuario.Usuario(0, cedula, password, opcion)
        usuario.crearUsuario(baseDatos)

        if opcion == 'Empleado':
            empleado = Empleado.Empleado(0, cedula, nombre, apellido, nacimiento, genero, domicilio, nacionalidad, mail, telefono, None, None, None, usuario, None, None, None)
            empleado.crearEmpleado(baseDatos)
            return redirect(url_for('inicio_empleados'))
        elif opcion == 'Empleador':
            empleador = Empleador.Empleador(0, cedula, nombre, apellido, nacimiento, genero, domicilio, nacionalidad, mail, telefono, None, usuario)
            print(empleador)
            empleador.crearEmpleador(baseDatos)
            return redirect(url_for('inicio_empleadores'))


@app.route('/HomeEmpleados/')
def inicio_empleados():
    return render_template('HomeEmpleados.html')


@app.route('/HomeEmpleadores/')
def inicio_empleadores():
    return render_template('HomeEmpleadores.html')


@app.route('/PanelControl/')
def administrar():
    return render_template('ControlPanel.html')


#en desarrollo!!
@app.route('/CrearAnuncio/', methods=["POST"])
def crear_anuncio():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        #fechaInicio =  tomarla con datetime
        #fechaCierre =  null
        estado = request.form['estado']
        experiencia = request.form['experiencia']
        salario = request.form['salario']
        #idEmpleador = viene de la seción
        calEmpleado = request.form['calEmpleado']
        calEmpleador = request.form['calEmpleador']
        tieneVinculo = request.form['tieneVinculo']
        Empleador.crearAnuncio(
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
    return render_template('TusAnuncios.html')


@app.route('/Anuncios/')
def listar_anuncios():
    return render_template('ListaAnuncios.html')


@app.route('/Candidatos/')
def listar_candidatos():
    return render_template('ListaCandidatos.html')


if __name__ == '__main__':
    app.run(debug=True)