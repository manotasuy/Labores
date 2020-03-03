from datetime import datetime
from Implementacion import Anuncio

class Empleador:

    def __init__(self, pId, pCedula, pNombre, pApellido, pNacimiento, pGenero, pDom, pNacional, pEmail, pTel, pBps, pFoto, pCalif, pUsuario):
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
        self.registroBps = pBps
        self.foto = pFoto
        self.promedioCalificacion = pCalif
        self.usuario = pUsuario

    def __str__(self):
        return 'Id: {}, Cédula: {}, Nombre: {}, Apellido: {}, Nacimiento: {}, Genero: {}, Domicilio: {}, Nacionalidad: {}, Email: {}, Telefono: {}, Foto: {}, Usuario: {}'.format(self.id, self.cedula, self.nombre, self.apellido, self.nacimiento, self.genero, self.domicilio, self.nacionalidad, self.email, self.telefono, self.foto, self.usuario)

    def crearEmpleador(self, bd):
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
            print(self.registroBps)
            print(self.foto)
            print(self.promedioCalificacion)
            print(self.usuario.id)
            print(self.usuario.usuario)
            print(self.usuario.clave)

            cursor = bd.connection.cursor()
            cursor.execute('''
                INSERT INTO empleador
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
                        registro_bps,
                        foto,
                        promedio_calificacion,
                        id_usuario
                    )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
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
                        self.registroBps,
                        self.foto,
                        self.promedioCalificacion,
                        self.usuario.id
                    ))
            bd.connection.commit()
            cursor.close()
            print('Empleador Creado')        
        except:
            print("Error en creación del empleador")


    def actualizarEmpleador(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            cursor.close()
            print('función para actualizar empleador')
        except:
            print("Error en actualizar el empleador")

    
    def listarEmpleadores(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            cursor.close()
            print('función para listar empleadores')
        except:
            print("Error al listar empleadores")


    def crearAnuncio(self, bd, Titulo, Descripcion, FechaInicio, FechaCierre, Estado, Experiencia, Salario, IdEmpleador, CalEmpleado, CalEmpleador, TieneVinculo):
        try:
            #cursor = bd.connection.cursor()
            #cursor.execute('...')
            #bd.connection.commit()
            #cursor.close()
            newAnuncio = Anuncio.Anuncio(Titulo, Descripcion, FechaInicio, FechaCierre, Estado, Experiencia, Salario, IdEmpleador, CalEmpleado, CalEmpleador, TieneVinculo)
            newAnuncio.createAnuncio(bd)
            print('El empleador generó el anuncio')
        except:
            print("Error al crear anuncio")


    def listarMisAnuncios(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute("SELECT * FROM anuncios WHERE id_empleador = '{}'".format(idEmpleador))
            data = cursor.fetchall()
            return data
        except:
            print("Error al listar mis anuncios")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")


    def realizarBusqueda(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            cursor.close()
            print('función para realizar búsqueda')
        except:
            print("Error al realizar búsqueda")


    def candidatosDeMiAnuncio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            cursor.close()
            print('función para listar candidatos de mi anuncio')
        except:
            print("Error al listar candidatos de mi anuncio")


    def establecerContacto(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            cursor.close()
            print('función para establecer contacto')
        except:
            print("Error al establecer contacto")


def prueba():
    print('Hola! soy el empleador')
