import json
from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_mysqldb import MySQL

# Paquetes implementación
from Logica import HandlerAdministrador

app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'computosMySQLRoot'
app.config['MYSQL_DB'] = 'bdLabores'
bd = MySQL(app)

# session
app.secret_key = "session"

print(HandlerAdministrador.prueba())


@app.route('/')
@app.route('/Inicio')
def inicio():
    return render_template('Inicio.html')


@app.route('/Contacto')
def contacto():
    return render_template('Contacto.html')


@app.route('/Ayuda')
def ayuda():
    return render_template('Ayuda.html')


@app.route('/LogIn')
def logueo():
    return render_template('Login.html')


@app.route('/LogOut')
def deslogueo():
    session.pop('username')
    session.pop('usertype')
    return redirect(url_for('inicio'))


@app.route('/Ingresar', methods=['POST'])
def ingresar():
    if request.method == 'POST':
        session['username'] = request.form['user']
        password = request.form['pass']
        cursor = bd.connection.cursor()
        #cursor.execute('INSERT INTO usuario (usuario, clave, tipo) VALUES (%s, %s, %s)', (user, password, 'Empleador'))
        cursor.execute(
            'SELECT tipo FROM usuario WHERE usuario = %s AND clave = %s', (session['username'], password))
        retorno = cursor.fetchall()
        cursor.close()
        bd.connection.commit()
        #tipo = retorno[0]
        session['usertype'] = retorno[0][0]

        if session['usertype'] == 'Empleador':
            return redirect(url_for('inicio_empleadores'))
        elif session['usertype'] == 'Empleado':
            return redirect(url_for('inicio_empleados'))
        else:
            return redirect(url_for('administrar'))


@app.route('/SignUp')
def registrarse():
    # return render_template('SignUp.html')
    return render_template('Registro.html')


@app.route('/HomeEmpleados')
def inicio_empleados():
    return render_template('HomeEmpleados.html')


@app.route('/HomeEmpleadores')
def inicio_empleadores():
    return render_template('HomeEmpleadores.html')


@app.route('/PanelControl')
def administrar():
    return render_template('ControlPanel.html')


if __name__ == '__main__':
    app.run(debug=True)
