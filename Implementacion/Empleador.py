from datetime import datetime
from Implementacion import Anuncio


class Empleador:

    def __init__(self, pId=None, pCedula=None, pNombre=None, pApellido=None, pNacimiento=None, pGenero=None, pDom=None, pNacional=None, pEmail=None, pTel=None, pBps=None, pFoto=None, pCalif=None, pUsuario=None):
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

    def __getitem__(self, item):
        return self.__dict__[item]

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
        except Exception as e:
            print("Error en crearEmpleador ", e)

    def modificarEmpleador(self, bd):
        try:
            print('Self: ', self)
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE empleador SET
                    nombre = %s,
                    apellido = %s,
                    fecha_nacimiento = %s,
                    genero = %s,
                    domicilio = %s,
                    nacionalidad = %s,
                    email = %s,
                    telefono = %s,
                    registro_bps = %s,
                    foto = %s,
                    promedio_calificacion = %s
                WHERE id = %s''',
                           (
                               self.nombre,
                               self.apellido,
                               self.nacimiento,
                               self.genero,
                               self.domicilio,
                               self.nacionalidad,
                               self.email,
                               self.telefono,
                               self.registroBps,
                               self.foto,
                               self.promedioCalificacion,
                               self.id
                           ))
            bd.connection.commit()
            cursor.close()
            print('Empleador modificado')
        except Exception as e:
            print("Error en actualizarEmpleador ", e)

    def listarEmpleadores(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            cursor.close()
            print('función para listar empleadores')
        except Exception as e:
            print("Error en listarEmpleadores ", e)

    def crearAnuncio(self, bd, Titulo, Descripcion, FechaInicio, FechaCierre, Estado, Experiencia, Salario, CalEmpleado, CalEmpleador, TieneVinculo):
        try:
            # cursor = bd.connection.cursor()
            # cursor.execute('...')
            # bd.connection.commit()
            # cursor.close()
            newAnuncio = Anuncio.Anuncio(Titulo, Descripcion, FechaInicio, FechaCierre, Estado,
                                         Experiencia, Salario, self.id, CalEmpleado, CalEmpleador, TieneVinculo)
            newAnuncio.createAnuncio(bd)
            print('El empleador generó el anuncio')
        except Exception as e:
            print("Error en crearAnuncio ", e)

    def listarMisAnuncios(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute(
                'SELECT * FROM anuncios WHERE id_empleador = {}'.format(self.id))
            data = cursor.fetchall()
            cursor.close()
            bd.connection.close()
            return data
        except Exception as e:
            print("Error en listarMisAnuncios ", e)

    def realizarBusqueda(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            cursor.close()
            print('función para realizar búsqueda')
        except Exception as e:
            print("Error en realizarBusqueda ", e)

    def candidatosDeMiAnuncio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            cursor.close()
            print('función para listar candidatos de mi anuncio')
        except Exception as e:
            print("Error en candidatosDeMiAnuncio ", e)

    def establecerContacto(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            cursor.close()
            print('función para establecer contacto')
        except Exception as e:
            print("Error en establecerContacto ", e)


def getEmpleadorByID(bd, id):
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
                registro_bps,
                foto,
                promedio_calificacion,
                id_usuario
            FROM empleador WHERE id = {}'''.format(id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        empleador = Empleador(
            retorno[0][0],
            retorno[0][1],
            retorno[0][2],
            retorno[0][3],
            retorno[0][4],
            retorno[0][5],
            retorno[0][6],
            retorno[0][7],
            retorno[0][8],
            retorno[0][9],
            retorno[0][10],
            retorno[0][11],
            retorno[0][12],
            retorno[0][13])
        return empleador
    except Exception as e:
        print("Error en getEmpleadorByID ", e)


def getEmpleadorByUsuarioID(bd, idUsuario):
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
            e.registro_bps,
            e.foto,
            e.promedio_calificacion,
            e.id_usuario
            FROM empleador e INNER JOIN usuario u ON e.id_usuario = u.id WHERE u.id = {}'''.format(idUsuario))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        empleador = Empleador(
            retorno[0][0],
            retorno[0][1],
            retorno[0][2],
            retorno[0][3],
            retorno[0][4],
            retorno[0][5],
            retorno[0][6],
            retorno[0][7],
            retorno[0][8],
            retorno[0][9],
            retorno[0][10],
            retorno[0][11],
            retorno[0][12],
            retorno[0][13])
        return empleador
    except Exception as e:
        print("Error en getEmpleadorByUsuarioID ", e)
