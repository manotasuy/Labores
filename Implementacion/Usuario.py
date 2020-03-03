
class Usuario:

    def __init__(self, pId, pUsuario, pClave, pTipo):
        self.id = pId
        self.usuario = pUsuario
        self.clave = pClave
        self.tipo = pTipo

    def __str__(self):
        return "Id: {}, Usuario: {}, Clave: {}, Tipo: {}".format(self.id, self.usuario, self.clave, self.tipo)

    def loginUsuario(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('SELECT tu.nombre FROM usuario u INNER JOIN tipo_usuario tu ON u.id_tipo = tu.id WHERE u.usuario = %s AND u.clave = %s',
                           (self.usuario, self.clave))
            retorno = cursor.fetchall()
            bd.connection.commit()
            cursor.close()
            return retorno
        except:
            print("Error en login de usuario")


    def getIdUsuario(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('SELECT id FROM usuario WHERE usuario = %s AND clave = %s',
                           (self.usuario, self.clave))
            retorno = cursor.fetchall()
            self.id = retorno[0][0]
            bd.connection.commit()
            cursor.close()
            return retorno
        except:
            print("Error en login de usuario")


    def crearUsuario(self, bd):
        try:
            intTipo: int
            if self.tipo == 'Administrador':
                intTipo = 1
            elif self.tipo == 'Empleador':
                intTipo = 2
            elif self.tipo == 'Empleado':
                intTipo = 3

            print(self.usuario)
            print(self.clave)
            print(intTipo)

            cursor = bd.connection.cursor()
            cursor.execute('INSERT INTO usuario (usuario, clave, id_tipo) VALUES (%s, %s, %s)', (self.usuario, self.clave, intTipo))
            bd.connection.commit()
            cursor.close()
            print('Usuario Creado')
        except:
            print("Error en creación de usuario")


    def cambiarPassword(self, newPassword, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('UPDATE usuario SET clave = %s WHERE usuario = %s AND clave = %s',
                           (newPassword, self.usuario, self.clave))
            bd.connection.commit()
            cursor.close()
            print('contraseña cambiada')
        except:
            print("Error en cambio de contraseña")
