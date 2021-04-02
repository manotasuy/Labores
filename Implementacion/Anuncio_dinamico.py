from datetime import datetime
# si establezco from modulo import clase obtengo referencia ciclíca [Inicio]
from Implementacion import Empleador
# si establezco from modulo import clase obtengo referencia ciclíca [Fin]
from Implementacion.Tarea import Tarea
from Implementacion.Tarea import agregarTareaAnuncio
from Implementacion.Tarea import quitarTareaAnuncio
from Implementacion.Tarea import quitarTodasLasTareasDelAnuncio
from Implementacion.Disponibilidad import Disponibilidad
from Implementacion.Disponibilidad import agregarDisponibilidadAnuncio
from Implementacion.Disponibilidad import quitarDisponibilidadAnuncio
from Implementacion.Disponibilidad import quitarTodaLaDisponibilidadDelAnuncio
from Implementacion.DTOAuxEmpleado import TareaSeleccion
from Implementacion.DTOAuxEmpleado import DisponibilidadSeleccion


class Anuncio:

    def __init__(
        self,
        pId,
        pTitulo,
        pDescripcion,
        pFechaInicio,
        pFechaCierre,
        pEstado,
        pExperiencia,
        pPago_hora,
        pEmpleador,
        pCalDesde,
        pCalHasta,
        pTieneVinculo,
        pDisponibilidad,
        pTareas,
    ):
        self.id = pId
        self.titulo = pTitulo
        self.descripcion = pDescripcion
        self.fecha_inicio = pFechaInicio
        self.fecha_cierre = pFechaCierre
        self.estado = pEstado
        self.experiencia = pExperiencia
        self.pago_hora = pPago_hora
        self.empleador: Empleador = pEmpleador
        self.calificacion_desde = pCalDesde
        self.calificacion_hasta = pCalHasta
        self.tiene_vinculo = pTieneVinculo
        self.disponibilidad = pDisponibilidad
        self.tareas = pTareas

    def __str__(self):
        return 'Id: {}, Título: {}, Empleador: {}, Vinculo: {}'.format(self.id, self.titulo, self.empleador.id, self.tiene_vinculo)

    def __getitem__(self, item):
        return self.__dict__[item]

    def createAnuncio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                INSERT INTO anuncio 
                    (
                        titulo,
                        descripcion,
                        fecha_inicio,
						fecha_cierre,
						estado,
                        experiencia,
                        pago_hora,
                        id_empleador,
                        calificacion_desde,
                        calificacion_hasta,
                        tiene_vinculo
                    )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                           (
                               self.titulo,
                               self.descripcion,
                               self.fecha_inicio,
                               self.fecha_cierre,
                               self.estado,
                               self.experiencia,
                               self.pago_hora,
                               self.empleador.id,
                               self.calificacion_desde,
                               self.calificacion_hasta,
                               self.tiene_vinculo
                           ))
            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            cursor.execute('''SELECT MAX(id) FROM anuncio WHERE id_empleador = {}'''.format(
                self.empleador.id))
            retorno = cursor.fetchall()
            idAnuncio = retorno[0][0]
            bd.connection.commit()
            cursor.close()

            # Tengo que recorrer las tareas del anuncio y grabarlas en la BD
            if self.tareas is not None:
                for tarea in self.tareas:
                    agregarTareaAnuncio(bd, tarea, idAnuncio)

            if self.disponibilidad is not None:
                agregarDisponibilidadAnuncio(
                    bd, self.disponibilidad, idAnuncio)

            print('Anuncio Creado')
        except Exception as e:
            print("Error en createAnuncio ", e)

    def deleteAnuncio(self, bd):
        try:

            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM anuncio_disponibilidad WHERE id_anuncio = {}
                '''.format(self.id))
            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM anuncio_tarea WHERE id_anuncio = {}
                '''.format(self.id))
            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM anuncio WHERE id = {}
                '''.format(self.id))
            bd.connection.commit()
            cursor.close()
            print('Anuncio Borrado')
        except Exception as e:
            print("Error en deleteAnuncio ", e)

    def updateAnuncio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE anuncio SET
                    titulo = %s,
                    descripcion = %s,
                    fecha_cierre = %s,
                    estado = %s,
                    experiencia = %s,
                    pago_hora = %s,
                    calificacion_desde = %s,
                    calificacion_hasta = %s,
                    tiene_vinculo = %s
                WHERE id = %s''',
                           (
                               self.titulo,
                               self.descripcion,
                               self.fecha_cierre,
                               self.estado,
                               self.experiencia,
                               self.pago_hora,
                               self.calificacion_desde,
                               self.calificacion_hasta,
                               self.tiene_vinculo,
                               self.id
                           ))

            bd.connection.commit()
            cursor.close()

            # Primero debo borrar las tareas y disponibilidad que tenga asignadas el anuncio
            quitarTodasLasTareasDelAnuncio(bd, self.id)
            quitarTodaLaDisponibilidadDelAnuncio(bd, self.id)

            # Luego registro las tareas y disponibilidad del anuncio que quiero modificar
            if self.tareas is not None:
                for tarea in self.tareas:
                    agregarTareaAnuncio(bd, tarea.id, self.id)

            if self.disponibilidad is not None:
                agregarDisponibilidadAnuncio(
                    bd, self.disponibilidad.id, self.id)

            print('Anuncio Actualizado')
        except Exception as e:
            print("Error en updateAnuncio ", e)

    def setEstadoAnuncio(self, bd, estado):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE anuncio SET
                    estado = %s
                WHERE id = %s''',
                           (
                               estado,
                               self.id
                           ))
            bd.connection.commit()
            cursor.close()
            print('Estado del Anuncio actualizado')
        except Exception as e:
            print("Error en setEstadoAnuncio ", e)

    def cargarTareas(self, tareas):
        try:
            self.tareas = tareas
        except Exception as e:
            print("Error en cargarTareas ", e)

    def cargarDisponibilidad(self, disponibilidad):
        try:
            self.disponibilidad = disponibilidad
        except Exception as e:
            print("Error en cargarDisponibilidad ", e)

    def getTareasSeleccionadas(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                    SELECT 
                    id, 
                    descripcion, 
                    IF((SELECT id_tarea 
                    FROM anuncio_tarea 
                    WHERE id_anuncio = {} AND id_tarea = id),1,0) AS seleccionada FROM tarea'''.format(self.id))
            retorno = cursor.fetchall()
            bd.connection.commit()
            cursor.close()
            # desde el retorno debo generar los objetos Tarea
            tareas = list()
            for tuplaTarea in retorno:
                tarea = TareaSeleccion(
                    tuplaTarea[0], tuplaTarea[1], tuplaTarea[2])
                tareas.append(tarea)
            return tareas
        except Exception as e:
            print("Error en getTareasSeleccionadas ", e)

    def getDisponibilidadSeleccionadas(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                    SELECT 
                    id, 
                    descripcion, 
                    IF((SELECT id_disponibilidad 
                    FROM anuncio_disponibilidad 
                    WHERE id_anuncio = {} AND id_disponibilidad = id),1,0) AS seleccionada FROM disponibilidad'''.format(self.id))
            retorno = cursor.fetchall()
            bd.connection.commit()
            cursor.close()
            # desde el retono debo generar los objetos Disponibilidad
            disponibilidades = list()
            for tuplaDisponibilidad in retorno:
                disponibilidad = DisponibilidadSeleccion(
                    tuplaDisponibilidad[0], tuplaDisponibilidad[1], tuplaDisponibilidad[2])
                disponibilidades.append(disponibilidad)
            return disponibilidades
        except Exception as e:
            print("Error en getDisponibilidadSeleccionadasEmpleado ", e)


def getTareasAnuncio(bd, idAnuncio):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
                SELECT
                    t.id,
                    t.descripcion
                FROM anuncio_tarea at INNER JOIN tarea t ON at.id_tarea = t.id WHERE at.id_anuncio = {}'''.format(idAnuncio))
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
        print("Error en getTareasAnuncio ", e)


def getDisponibilidadAnuncio(bd, idAnuncio):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
                SELECT
                    d.id,
                    d.descripcion
                FROM anuncio_disponibilidad ad INNER JOIN disponibilidad d ON ad.id_disponibilidad = d.id WHERE ed.id_anuncio = {}'''.format(idAnuncio))
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
        print("Error en getDisponibilidadAnuncio ", e)


def getAnuncioByID(bd, id):
    try:
        if id == None or id == 0:
            return None
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                titulo,
                descripcion,
                fecha_inicio,
                fecha_cierre,
                estado,
                experiencia,
                pago_hora,
                id_empleador,
                calificacion_desde,
                calificacion_hasta,
                tiene_vinculo
            FROM anuncio WHERE id = {}'''.format(id))
        retorno_anuncio = cursor.fetchall()
        bd.connection.commit()
        cursor.close()

        anuncio = Anuncio(
            retorno_anuncio[0][0],
            retorno_anuncio[0][1],
            retorno_anuncio[0][2],
            retorno_anuncio[0][3],
            retorno_anuncio[0][4],
            retorno_anuncio[0][5],
            retorno_anuncio[0][6],
            retorno_anuncio[0][7],
            Empleador.getEmpleadorByID(bd, retorno_anuncio[0][8]),
            retorno_anuncio[0][9],
            retorno_anuncio[0][10],
            retorno_anuncio[0][11],
            getDisponibilidadAnuncio(bd, retorno_anuncio[0][0]),
            getTareasAnuncio(bd, retorno_anuncio[0][0])
        )
        return anuncio
    except Exception as e:
        print("Error en getAnuncioByID ", e)


def getAllAnuncios(bd):
    cur = bd.connection.cursor()
    cur.execute('SELECT * FROM anuncio')
    retornoAnuncios = cur.fetchall()
    cur.close()
    return retornoAnuncios
