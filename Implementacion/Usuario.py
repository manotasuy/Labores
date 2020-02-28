from Implementacion import Conexion


class Usuario:
    usuario = ''
    clave = ''
    tipo = ''

    def __init__(self, **kwargs):
        self.usuario = kwargs.get("usuario")
        self.clave = kwargs.get("clave")
        self.tipo = kwargs.get("tipo")

    def __str__(self):
        return "Usuario: {}, Clave: {}, Tipo: {}".format(self.usuario, self.clave, self.tipo)


def loginUsuario(bd, usuario, clave):
    cursor = bd.connection.cursor()
    cursor.execute('SELECT tu.nombre FROM usuario u INNER JOIN tipo_usuario tu ON u.id_tipo = tu.id WHERE u.usuario = %s AND u.clave = %s',
                   (usuario, clave))
    retorno = cursor.fetchall()
    cursor.close()
    bd.connection.commit()
    return retorno


def crearUsuario(bd, user, password, type):
    cursor = bd.connection.cursor()
    cursor.execute('INSERT INTO usuario (usuario, clave, tipo) VALUES (%s, %s, %s)',
                   (user, password, 'Administrador'))
    print('crear usuario')


def cambiarPassword(user, oldPassword, newPassword):
    bd = Conexion.getConnection()
    cursor = bd.connection.cursor()
    cursor.execute('UPDATE usuario SET clave = %s WHERE usuario = %s AND clave = %s',
                   (newPassword, user, oldPassword))
    print('contraseña cambiada')
