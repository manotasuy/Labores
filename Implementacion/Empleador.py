
class Empleador:

    def __init__(self, pCedula, pNombre, pApellido, pNacimiento, pGenero, pDom, pNacional, pEmail, pTel, pFoto, pUsuario):
        self.cedula = pCedula
        self.nombre = pNombre
        self.apellido = pApellido
        self.nacimiento = pNacimiento
        self.genero = pGenero
        self.domicilio = pDom
        self.nacionalidad = pNacional
        self.email = pEmail
        self.telefono = pTel
        self.foto = pFoto
        self.usuario = pUsuario

    def __str__(self):
        return 'Cédula: {}, Nombre: {}, Apellido: {}'.format(self.cedula, self.nombre, self.apellido)

    def crearEmpleador(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('INSERT INTO empleador...')
            print('Empleador Creado')
        except:
            print("Error en creación de empleador")


def prueba():
    print('Hola! soy el empleador')
