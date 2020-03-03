from datetime import datetime

class Empleado:

    def __init__(self, pId, pCedula, pNombre, pApellido, pNacimiento, pGenero, pDom, pNacional, pEmail, pTel, pExp, pFoto, pDesc, pCalif, pUsuario, pRefer, pTareas, pDispon):
        self.id = pId
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
        self.promedioCalificacion = pCalif
        self.usuario = pUsuario
        self.referencias = pRefer
        self.tareas = pTareas
        self.disponibilidad = pDispon

    def __str__(self):
        return 'Cédula: {}, Nombre: {}, Apellido: {}'.format(self.cedula, self.nombre, self.apellido)

    def crearEmpleado(self, bd):
        try:
            intGenero: int
            print(self.genero)
            if self.genero == 'Femenino':
                intGenero = 0
            else:
                intGenero = 1
            print(self.nacimiento)
            fechaFormateada = self.nacimiento.strftime('%Y-%m-%d')

            print(self.cedula)
            print(self.nombre)
            print(self.apellido)
            print(fechaFormateada)
            print(intGenero)
            print(self.domicilio)
            print(self.nacionalidad)
            print(self.email)
            print(self.telefono)
            print(self.experiencia_meses)
            print(self.descripcion)
            print(self.foto)
            print(self.promedioCalificacion)
            print(self.usuario.id)
            print(self.usuario.usuario)
            print(self.usuario.clave)

            cursor = bd.connection.cursor()
            cursor.execute('''
                INSERT INTO empleado 
                    (
                        cedula,
                        nombre,
                        apellido,
                        fecha_nacimiento,
                        genero,
                        domicilio,
                        nacionalidad,
                        email,
                        telefono,
                        experiencia_meses,
                        descripcion,
                        foto,
                        promedio_calificacion,
                        id_usuario
                    )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                    (
                        self.cedula,
                        self.nombre,
                        self.apellido,
                        fechaFormateada,
                        intGenero,
                        self.domicilio,
                        self.nacionalidad,
                        self.email,
                        self.telefono,
                        self.experiencia_meses,
                        self.descripcion,
                        self.foto,
                        self.promedioCalificacion,
                        self.usuario.id
                    ))
            bd.connection.commit()
            cursor.close()
            print('Empleado Creado')        
        except:
            print("Error en creación del empleado")


    def modificarEmpleado(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('UPDATE empleado...')
            bd.connection.commit()
            cursor.close()
            print('Empleado modificado')
        except:
            print("Error en edición de empleado")


    def eliminarEmpleado(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('DELETE FROM empleado...')
            bd.connection.commit()
            cursor.close()
            print('Empleado Eliminado')
        except:
            print("Error en eliminación de empleado")


    def listarEmpleados(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('SELECT * FROM empleado...')
            bd.connection.commit()
            cursor.close()
            print('Listado de empleados')
        except:
            print("Error al listar los empleados")


    def postularseParaAnuncio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('SELECT * FROM empleado...')
            bd.connection.commit()
            cursor.close()
            print('Postulado para empleo')
        except:
            print('Error en postulación')


def prueba():
    print('Hola! soy el empleado')
