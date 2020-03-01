
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

    def modificarEmpleado(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('UPDATE empleado...')
            print('Empleado modificado')
        except:
            print("Error en edición de empleado")

    def eliminarEmpleado(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('DELETE FROM empleado...')
            print('Empleado Eliminado')
        except:
            print("Error en eliminación de empleado")

    def listarEmpleados(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('SELECT * FROM empleado...')
            print('Listado de empleados')
        except:
            print("Error al listar los empleados")

    def postularseParaAnuncio(self, bd):
        try:
            print('Postulado para empleo')
        except:
            print('Error en postulación')
