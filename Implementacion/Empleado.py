from datetime import datetime
from Implementacion.Usuario import getUsuarioByID
from Implementacion.Tarea import Tarea
from Implementacion.Usuario import Usuario
from Implementacion.Disponibilidad import Disponibilidad


class Empleado:

    def __init__(self, pId=0, pCedula='', pNombre='', pApellido='', pNacimiento='', pGenero='', pDom='', pNacional='', pEmail='', pTel='', pExp='', pFoto='', pDesc='None', pCalif='', pUsuario=None, pRefer=None, pTareas=None, pDispon=None):
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
        self.usuario: Usuario = pUsuario
        self.referencias = pRefer
        self.tareas = pTareas
        self.disponibilidad = pDispon

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Cédula: {}, Nombre: {}, Apellido: {}, Foto: {}'.format(self.cedula, self.nombre, self.apellido, self.foto)

    def crearEmpleado(self, bd):
        try:
            intGenero: int
            # print(self.genero)
            if self.genero == 'Femenino':
                intGenero = 0
            else:
                intGenero = 1
            # print(self.nacimiento)
            #fechaFormateada = self.nacimiento.strftime('%Y-%m-%d')

            # print(self.cedula)
            # print(self.nombre)
            # print(self.apellido)
            # print(fechaFormateada)
            # print(intGenero)
            # print(self.domicilio)
            # print(self.nacionalidad)
            # print(self.email)
            # print(self.telefono)
            # print(self.experiencia_meses)
            # print(self.descripcion)
            # print(self.foto)
            # print(self.promedioCalificacion)
            # print(self.usuario.id)
            # print(self.usuario.usuario)
            # print(self.usuario.clave)

            if self.foto is None or self.foto == '':
                self.foto = 'images/NoImage.png'

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
                               #fechaFormateada,
                               self.nacimiento,
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
        except Exception as e:
            print("Error en creación del empleado ", e)

    def modificarEmpleado(self, bd):
        try:
            if self.foto is None or self.foto == '':
                self.foto = 'images/NoImage.png'

            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE empleado SET
                    nombre = %s,
                    apellido = %s,
                    fecha_nacimiento = %s,
                    genero = %s,
                    domicilio = %s,
                    nacionalidad = %s,
                    email = %s,
                    telefono = %s,
                    experiencia_meses = %s,
                    descripcion = %s,
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
                               self.experiencia_meses,
                               self.descripcion,
                               self.foto,
                               self.promedioCalificacion,
                               self.id
                           ))
            bd.connection.commit()
            cursor.close()
            print('Empleado modificado')
        except Exception as e:
            print("Error en edición de empleado ", e)

    def cargarTareas(self, tareas):
        try:
            self.tareas = tareas
        except Exception as e:
            print("Error en cargarTareas ", e)

    def cargarReferencias(self, referencias):
        try:
            self.referencias = referencias
        except Exception as e:
            print("Error en cargarReferencias ", e)

    def cargarDisponibilidad(self, disponibilidad):
        try:
            self.disponibilidad = disponibilidad
        except Exception as e:
            print("Error en cargarDisponibilidad ", e)

    def eliminarEmpleado(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('DELETE FROM empleado...')
            bd.connection.commit()
            cursor.close()
            print('Empleado Eliminado')
        except Exception as e:
            print("Error en eliminación de empleado ", e)

    def listarEmpleados(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('SELECT * FROM empleado...')
            bd.connection.commit()
            cursor.close()
            print('Listado de empleados')
        except Exception as e:
            print("Error al listar los empleados ", e)

    def postularseParaAnuncio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('SELECT * FROM empleado...')
            bd.connection.commit()
            cursor.close()
            print('Postulado para empleo')
        except Exception as e:
            print('Error en postulación ', e)


class Referencia:
    def __init__(self, pId=None, pEmpleado=None, pNombre=None, pTelefono=None, pFechaDesde=None, pFechaHasta=None):
        self.id = pId
        self.empleado = pEmpleado
        self.nombre = pNombre
        self.telefono = pTelefono
        self.fechaDesde = pFechaDesde
        self.fechaHasta = pFechaHasta

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Nombre empleado: {}, Nombre Referencia: {}, Telefono: {}, Fecha desde: {}, Fecha hasta: {}'.format(self.empleado.id, self.nombre, self.telefono, self.fechaDesde, self.fechaHasta)


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
                foto,
                descripcion,
                promedio_calificacion,
                id_usuario
            FROM empleado WHERE id = {}'''.format(id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        empleado = Empleado(
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
            retorno[0][13],
            getUsuarioByID(bd, retorno[0][14]),
            None,
            None,
            None)
        #print('Empleado: ', empleado)
        return empleado
    except Exception as e:
        print("Error en getEmpleadoByID ", e)


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
                e.foto,
                e.descripcion,
                e.promedio_calificacion,
                e.id_usuario
            FROM empleado e INNER JOIN usuario u ON e.id_usuario = u.id WHERE u.id = {}'''.format(idUsuario))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        empleado = Empleado(
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
            retorno[0][13],
            getUsuarioByID(bd, retorno[0][14]),
            None,
            None,
            None)
        return empleado
    except Exception as e:
        print("Error en getEmpleadoByUsuarioID ", e)


def getTareasEmpleado(bd, idEmpleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
                SELECT
                    t.id,
                    t.descripcion
                FROM empleado_tarea et INNER JOIN tarea t ON et.id_tarea = t.id WHERE et.id_empleado = {}'''.format(idEmpleado))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        # desde el retorno debo generar los objetos Tarea
        tareas = list()
        for tuplaTarea in retorno:
            tarea = Tarea(tuplaTarea[0], tuplaTarea[1])
            tareas.append(tarea)
        return tareas
    except Exception as e:
        print("Error en getTareasEmpleado ", e)


def getDisponibilidadEmpleado(bd, idEmpleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
                SELECT
                    d.id,
                    d.descripcion
                FROM empleado_disponibilidad ed INNER JOIN disponibilidad d ON ed.id_disponibilidad = d.id WHERE ed.id_empleado = {}'''.format(idEmpleado))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        # desde el retono debo generar los objetos Disponibilidad
        disponibilidades = list()
        for tuplaDisponibilidad in retorno:
            disponibilidad = Disponibilidad(
                tuplaDisponibilidad[0], tuplaDisponibilidad[1])
            disponibilidades.append(disponibilidad)
        return disponibilidades
    except Exception as e:
        print("Error en getDisponibilidadEmpleado ", e)


def getReferenciasEmpleado(bd, idEmpleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
                SELECT
                    id,
                    nombre,
                    telefono,
                    fecha_desde,
                    fecha_hasta
                FROM referencia WHERE id_empleado = {}'''.format(idEmpleado))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        # desde el retono debo generar los objetos Referencia
        referencias = list()
        for tuplaReferencia in retorno:
            referencia = Referencia(tuplaReferencia[0], getEmpleadoByID(bd, idEmpleado), tuplaReferencia[1],
                                    tuplaReferencia[2], tuplaReferencia[3], tuplaReferencia[4])
            referencias.append(referencia)
        return referencias
    except Exception as e:
        print("Error en getReferenciasEmpleado ", e)
