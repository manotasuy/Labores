
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
            return retorno
        except:
            print("Error en login de usuario")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")

    def crearUsuario(self, bd):
        try:
            cursor = bd.connection.cursor()
            intTipo: int
            if self.tipo == 'Administrador':
                intTipo = 1
            elif self.tipo == 'Empleador':
                intTipo = 2
            elif self.tipo == 'Empleador':
                intTipo = 3
            cursor.execute('INSERT INTO usuario (usuario, clave, id_tipo) VALUES (%s, %s, %s)', (self.usuario, self.clave, intTipo))
            self.id = cursor.execute('SELECT LAST_INSERT_ID()')
            print(self.id)
            bd.connection.commit()
            print('Usuario Creado')
        except:
            print("Error en creación de usuario")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")


    def cambiarPassword(self, newPassword, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('UPDATE usuario SET clave = %s WHERE usuario = %s AND clave = %s',
                           (newPassword, self.usuario, self.clave))
            bd.connection.commit()
            print('contraseña cambiada')
        except:
            print("Error en cambio de contraseña")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")
