from flask_mysqldb import MySQL

host = 'remotemysql.com'
user = 'LvP2Ka0CsK'
password = 'kqGcYKaofd'
bd = 'LvP2Ka0CsK'


def connection_Db(app):
    # *** Conexión a base de datos local ***
    # app.config['MYSQL_HOST'] = 'localhost'
    # app.config['MYSQL_USER'] = 'root'
    # app.config['MYSQL_PASSWORD'] = 'computosMySQLRoot'
    # app.config['MYSQL_DB'] = 'bdLabores'

    # *** Conexión a base de datos remota ***
    app.config['MYSQL_HOST'] = host
    app.config['MYSQL_USER'] = user
    app.config['MYSQL_PASSWORD'] = password
    app.config['MYSQL_DB'] = bd
    return MySQL(app)
