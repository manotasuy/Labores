import json
from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_mysqldb import MySQL
from enum import Enum

# Paquetes implementación
from Implementacion import Conexion
from Implementacion import Usuario
from Implementacion import Empleado
from Implementacion import Empleador

app = Flask(__name__)
baseDatos = Conexion.connectionDb(app)

# session
app.secret_key = "session"


class Tipo_Usuario(Enum):
    Administrador = 1
    Empleado = 2
    Empleador = 3


print(Tipo_Usuario.Administrador)
print(Tipo_Usuario.Administrador.value)


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
        usuario = Usuario.Usuario(user, password, '')
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


@app.route('/Registro/')
def registrarse():
    return render_template('Registro.html')


@app.route('/Registrar', methods=['POST'])
def registrar_usuario():
    if request.method == 'POST':
        parametros = request.form
        user = parametros['user']
        password = parametros['pass']
        tipo = parametros['type']
        usuario = Usuario.Usuario(user, password, tipo)
        usuario.crearUsuario(baseDatos)


@app.route('/HomeEmpleados/')
def inicio_empleados():
    return render_template('HomeEmpleados.html')


@app.route('/HomeEmpleadores/')
def inicio_empleadores():
    return render_template('HomeEmpleadores.html')


@app.route('/PanelControl/')
def administrar():
    return render_template('ControlPanel.html')


@app.route('/CrearAnuncio/')
def crear_anuncio():
    flash('Anuncio creado!')
    return render_template('CrearAnuncio.html')


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
