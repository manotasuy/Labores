
class Empleado:

    def __init__(self, pCedula, pNombre, pApellido, pNacimiento, pGenero, pDom, pNacional, pEmail, pTel, pExp, pFoto, pDesc, pUsuario, pRefer, pTareas, pDispon):
        self.cedula = pCedula
        self.nombre = pNombre
        self.apellido = pApellido
        self.nacimiento = pNacimiento
        self.genero = pGenero
        self.domicilio = pDom
        self.nacionalidad = pNacional
        self.email = pEmail
        self.telefono = pTel
        self.experiencia_meses = pExp
        self.foto = pFoto
        self.descripcion = pDesc
        self.usuario = pUsuario
        self.referencias = pRefer
        self.tareas = pTareas
        self.disponibilidad = pDispon

    def __str__(self):
        return 'Cédula: {}, Nombre: {}, Apellido: {}'.format(self.cedula, self.nombre, self.apellido)

    def crearEmpleado(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('INSERT INTO empleado...')
            print('Empleado Creado')
        except:
            print("Error en creación de empleado")
