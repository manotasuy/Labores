from flask_mysqldb import MySQL

# *** Conexión a base de datos local ***
#host = 'localhost'
#user = 'root'
#password = 'mysql_root'
#bd = 'bdLabores'

# *** Conexión a base de datos remota ***
host = 'remotemysql.com'
user = 'LvP2Ka0CsK'
password = 'kqGcYKaofd'
bd = 'LvP2Ka0CsK'


def connectionDb(app):
    app.config['MYSQL_HOST'] = host
    app.config['MYSQL_USER'] = user
    app.config['MYSQL_PASSWORD'] = password
    app.config['MYSQL_DB'] = bd
    return MySQL(app)
