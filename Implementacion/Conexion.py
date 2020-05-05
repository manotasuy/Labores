from flask_mysqldb import MySQL

CARPETA_FISICA_IMAGENES = "./static/images/Perfiles/"
CARPETA_CARGA_IMAGENES = "images/Perfiles/"


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
        app.config['MYSQL_PASSWORD'] = 'masterterLabores'
        app.config['MYSQL_DB'] = 'bdlabores'
    elif servidor == 'a-work':
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'computosMySQLRoot'
        app.config['MYSQL_DB'] = 'bdlabores'
    elif servidor == 'a-home':
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'root'
        app.config['MYSQL_DB'] = 'bdlabores'

    elif servidor == 'PA':
        app.config['MYSQL_HOST'] = 'Labores.mysql.pythonanywhere-services.com'
        app.config['MYSQL_USER'] = 'Labores'
        app.config['MYSQL_PASSWORD'] = 'LaboresApp1234'
        app.config['MYSQL_DB'] = 'Labores$LaboresDB'

    elif servidor == 'gcp':
        app.config['MYSQL_HOST'] = '35.198.46.68'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'rootgcp'
        app.config['MYSQL_DB'] = 'bdlabores'

#URI: postgres://eswmwhvegalapf:22a2aae8cbd55351515ec670984ca1b7bdf744f1147f162244fc2f4f08c9f0bb@ec2-52-202-146-43.compute-1.amazonaws.com:5432/db0f5hpdmfbnh8
    elif servidor == 'postgresql':
        app.config['MYSQL_URI'] = 'postgres://eswmwhvegalapf:22a2aae8cbd55351515ec670984ca1b7bdf744f1147f162244fc2f4f08c9f0bb@ec2-52-202-146-43.compute-1.amazonaws.com:5432/db0f5hpdmfbnh8'


    else:
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = ''
        app.config['MYSQL_DB'] = 'bdlabores'
    app.config['CARPETA_FISICA_IMAGENES'] = CARPETA_FISICA_IMAGENES
    app.config['CARPETA_CARGA_IMAGENES'] = CARPETA_CARGA_IMAGENES

    try:
      import googleclouddebugger
      googleclouddebugger.enable()
    except ImportError:
      pass
    
    return MySQL(app)

def getCarpetaFisicaImagenes():
    return CARPETA_FISICA_IMAGENES;

def getCarpetaCargaImagenes():
    return CARPETA_CARGA_IMAGENES;
