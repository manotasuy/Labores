from flask_mysqldb import MySQL


def connectionDb(app, servidor):
    if servidor == 'remotemysql.com':
        app.config['MYSQL_HOST'] = 'remotemysql.com'
        app.config['MYSQL_USER'] = 'LvP2Ka0CsK'
        app.config['MYSQL_PASSWORD'] = 'kqGcYKaofd'
        app.config['MYSQL_DB'] = 'LvP2Ka0CsK'
        return MySQL(app)
    elif servidor == 'CloudAccess':
        app.config['MYSQL_HOST'] = 'labores.cloudaccess.host'
        app.config['MYSQL_USER'] = 'amqtvopx'
        app.config['MYSQL_PASSWORD'] = ':*SsJ445aIky8I'
        app.config['MYSQL_DB'] = 'amqtvopx'
        return MySQL(app)
    elif servidor == 'aws':
        app.config['MYSQL_HOST'] = 'labores.cdjsb04v3a46.us-east-1.rds.amazonaws.com'
        app.config['MYSQL_USER'] = 'master'
        app.config['MYSQL_PASSWORD'] = 'masterLabores'
        app.config['MYSQL_DB'] = 'bdlabores'
        return MySQL(app)
    else:
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'mysql_root'
        app.config['MYSQL_DB'] = 'bdlabores'
        return MySQL(app)
