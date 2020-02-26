import json
from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_mysqldb import MySQL

# Paquetes implementación
from Logica import HandlerAdministrador

app = Flask(__name__)

# *** Conexión a base de datos local ***
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'computosMySQLRoot'
# app.config['MYSQL_DB'] = 'bdLabores'

# *** Conexión a base de datos remota ***
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'LvP2Ka0CsK'
app.config['MYSQL_PASSWORD'] = 'kqGcYKaofd'
app.config['MYSQL_DB'] = 'LvP2Ka0CsK'
# app.config['MYSQL_DB_PORT'] = '3306'
bd = MySQL(app)

# session
app.secret_key = "session"

print(HandlerAdministrador.prueba())


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
        session['username'] = request.form['user']
        password = request.form['pass']
        cursor = bd.connection.cursor()
        cursor.execute('SELECT tu.nombre FROM usuario u INNER JOIN tipo_usuario tu ON u.id_tipo = tu.id WHERE u.usuario = %s AND u.clave = %s',
                       (session['username'], password))
        retorno = cursor.fetchall()
        cursor.close()
        bd.connection.commit()
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


@app.route('/Registro/', methods=['POST'])
def registrarse():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['pass']
        cursor = bd.connection.cursor()
        cursor.execute('INSERT INTO usuario (usuario, clave, tipo) VALUES (%s, %s, %s)',
                       (user, password, 'Empleador'))
        return render_template('Registro.html')


@app.route('/HomeEmpleados/')
def inicio_empleados():
    return render_template('HomeEmpleados.html')


@app.route('/HomeEmpleadores/')
def inicio_empleadores():
    return render_template('HomeEmpleadores.html')


@app.route('/PanelControl/')
def administrar():
    return render_template('ControlPanel.html')


if __name__ == '__main__':
    app.run(debug=True)
