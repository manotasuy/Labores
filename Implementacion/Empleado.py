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


def getEmpleadoByID(bd, id):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
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
            FROM empleado WHERE id = %s''', (id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        empleado = Empleado(
            retorno['id'],
            retorno['cedula'],
            retorno['nombre'],
            retorno['apellido'],
            retorno['fecha_nacimiento'],
            retorno['genero'],
            retorno['domicilio'],
            retorno['nacionalidad'],
            retorno['email'],
            retorno['telefono'],
            retorno['experiencia_meses'],
            retorno['descripcion'],
            retorno['foto'],
            retorno['promedio_calificacion'],
            retorno['id_usuario'])
        return empleado
    except:
        print("Error en getEmpleadoByID")


def getEmpleadoByUsuarioID(bd, idUsuario):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                e.id,
                e.cedula,
                e.nombre,
                e.apellido,
                e.fecha_nacimiento,
                e.genero,
                e.domicilio,
                e.nacionalidad,
                e.email,
                e.telefono,
                e.experiencia_meses,
                e.descripcion,
                e.foto,
                e.promedio_calificacion,
                e.id_usuario
            FROM empleado e INNER JOIN usuario u ON e.id_usuario = u.id WHERE u.id = %s''', (idUsuario))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        empleado = Empleado(
            retorno['id'],
            retorno['cedula'],
            retorno['nombre'],
            retorno['apellido'],
            retorno['fecha_nacimiento'],
            retorno['genero'],
            retorno['domicilio'],
            retorno['nacionalidad'],
            retorno['email'],
            retorno['telefono'],
            retorno['experiencia_meses'],
            retorno['descripcion'],
            retorno['foto'],
            retorno['promedio_calificacion'],
            retorno['id_usuario'])
        return empleado
    except:
        print("Error en getEmpleadoByUsuarioID")
