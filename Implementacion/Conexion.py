from flask_mysqldb import MySQL

UPLOAD_FOLDER = 'images/Perfiles'

def connectionDb(app, servidor):
    if servidor == 'remotemysql.com':
        app.config['MYSQL_HOST'] = 'remotemysql.com'
        app.config['MYSQL_USER'] = 'LvP2Ka0CsK'
        app.config['MYSQL_PASSWORD'] = 'kqGcYKaofd'
        app.config['MYSQL_DB'] = 'LvP2Ka0CsK'
    elif servidor == 'CloudAccess':
        app.config['MYSQL_HOST'] = 'labores.cloudaccess.host'
        app.config['MYSQL_USER'] = 'amqtvopx'
        app.config['MYSQL_PASSWORD'] = ':*SsJ445aIky8I'
        app.config['MYSQL_DB'] = 'amqtvopx'
    elif servidor == 'aws':
        app.config['MYSQL_HOST'] = 'labores.cdjsb04v3a46.us-east-1.rds.amazonaws.com'
        app.config['MYSQL_USER'] = 'master'
        app.config['MYSQL_PASSWORD'] = 'masterLabores'
        app.config['MYSQL_DB'] = 'bdlabores'
    else:
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = ''
        app.config['MYSQL_DB'] = 'bdlabores'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    return MySQL(app)
