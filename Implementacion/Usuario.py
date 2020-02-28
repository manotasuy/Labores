
class Usuario:

    def __init__(self, pUsuario, pClave, pTipo):
        self.usuario = pUsuario
        self.clave = pClave
        self.tipo = pTipo

    def __str__(self):
        return "Usuario: {}, Clave: {}, Tipo: {}".format(self.usuario, self.clave, self.tipo)

    def loginUsuario(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('SELECT tu.nombre FROM usuario u INNER JOIN tipo_usuario tu ON u.id_tipo = tu.id WHERE u.usuario = %s AND u.clave = %s',
                           (self.usuario, self.clave))
            retorno = cursor.fetchall()
            cursor.close()
            bd.connection.commit()
            return retorno
        except:
            print("Error en login de usuario")

    def crearUsuario(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('INSERT INTO usuario (usuario, clave, tipo) VALUES (%s, %s, %s)',
                           (self.usuario, self.clave, 'Administrador'))
            print('Usuario Creado')
        except:
            print("Error en creación de usuario")

    def cambiarPassword(self, newPassword, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('UPDATE usuario SET clave = %s WHERE usuario = %s AND clave = %s',
                           (newPassword, self.usuario, self.clave))
            print('contraseña cambiada')
        except:
            print("Error en cambio de contraseña")
