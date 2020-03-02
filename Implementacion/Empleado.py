
class Empleado:

    def __init__(self, pId, pCedula, pNombre, pApellido, pNacimiento, pGenero, pDom, pNacional, pEmail, pTel, pExp, pFoto, pDesc, pUsuario, pRefer, pTareas, pDispon):
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
        self.usuario = pUsuario
        self.referencias = pRefer
        self.tareas = pTareas
        self.disponibilidad = pDispon

    def __str__(self):
        return 'Cédula: {}, Nombre: {}, Apellido: {}'.format(self.cedula, self.nombre, self.apellido)

    def crearEmpleado(self, bd):
        try:
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
                        self.nacimiento,
                        self.genero,
                        self.domicilio,
                        self.nacionalidad,
                        self.email,
                        self.telefono,
                        None,
                        None,
                        None,
                        None,
                        self.usuario.id
                    ))
            bd.connection.commit()
            print('Empleado Creado')        
        except:
            print("Error en creación del empleado")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")

    def modificarEmpleado(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('UPDATE empleado...')
            bd.connection.commit()
            print('Empleado modificado')
        except:
            print("Error en edición de empleado")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")

    def eliminarEmpleado(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('DELETE FROM empleado...')
            bd.connection.commit()
            print('Empleado Eliminado')
        except:
            print("Error en eliminación de empleado")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")

    def listarEmpleados(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('SELECT * FROM empleado...')
            bd.connection.commit()
            print('Listado de empleados')
        except:
            print("Error al listar los empleados")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")

    def postularseParaAnuncio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('SELECT * FROM empleado...')
            bd.connection.commit()
            print('Postulado para empleo')
        except:
            print('Error en postulación')
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")


def prueba():
    print('Hola! soy el empleado')
