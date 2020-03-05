from flask_mysqldb import MySQL


def connectionDb(app, baseRemota):
    if baseRemota:
        app.config['MYSQL_HOST'] = 'remotemysql.com'
        app.config['MYSQL_USER'] = 'LvP2Ka0CsK'
        app.config['MYSQL_PASSWORD'] = 'kqGcYKaofd'
        app.config['MYSQL_DB'] = 'LvP2Ka0CsK'
        return MySQL(app)
    else:
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'mysql_root'
        app.config['MYSQL_DB'] = 'bdLabores'
        return MySQL(app)