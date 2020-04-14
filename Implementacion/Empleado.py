import os
from flask import url_for
from datetime import datetime
import Implementacion
from Implementacion.Conexion import getCarpetaCargaImagenes
from Implementacion.Usuario import getUsuarioByID
from Implementacion.Tarea import Tarea
from Implementacion.Tarea import agregarTareaEmpleado
from Implementacion.Tarea import quitarTareaEmpleado
from Implementacion.Tarea import quitarTodasLasTareasDelEmpleado
from Implementacion.Disponibilidad import Disponibilidad
from Implementacion.Disponibilidad import agregarDisponibilidadEmpleado
from Implementacion.Disponibilidad import quitarDisponibilidadEmpleado
from Implementacion.Disponibilidad import quitarTodaLaDisponibilidadDelEmpleado
from Implementacion.DTOAuxEmpleado import TareaSeleccion
from Implementacion.DTOAuxEmpleado import DisponibilidadSeleccion
from Implementacion.Usuario import Usuario
from Implementacion.DTOIndividuoCalificacion import DTOIndividuoCalificacion


class Empleado:

    def __init__(self, pId=0, pCedula='', pNombre='', pApellido='', pNacimiento='', pGenero='', pDom='', pNacional='', pEmail='', pTel='', pExp='', pDesc='None', pFoto='', pCalif='', pUsuario=None, pRefer=None, pTareas=None, pDispon=None):
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
        self.descripcion = pDesc
        self.foto = pFoto
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
            if self.foto is None or self.foto == '':
                self.foto = 'images/Pefiles/NoImage.png'

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
                               self.experiencia_meses,
                               self.descripcion,
                               self.foto,
                               self.promedioCalificacion,
                               self.usuario.id
                           ))
            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            cursor.execute('SELECT MAX(id) FROM empleado')
            retorno = cursor.fetchall()
            idEmpleado = retorno[0][0]
            bd.connection.commit()
            cursor.close()

            # Tengo que recorrer las tareas del empleado y grabarlas en la BD
            if self.tareas is not None:
                for tarea in self.tareas:
                    agregarTareaEmpleado(bd, tarea.id, self.id)

            # Tengo que recorrer la disponibilidad del empleado y grabarlas en la BD
            if self.disponibilidad is not None:
                for dispo in self.disponibilidad:
                    agregarDisponibilidadEmpleado(bd, dispo.id, self.id)

            print('Empleado Creado')
        except Exception as e:
            print("Error en creación del empleado ", e)

    def calificarEmpleado(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE empleado SET
                    promedio_calificacion = %s
                WHERE id = %s''',
                           (
                               self.promedioCalificacion,
                               self.id
                           ))
            bd.connection.commit()
            cursor.close()
            print('Empleado calificado')
        except Exception as e:
            print("Error en calificación de empleado ", e)

    def modificarEmpleado(self, bd):
        try:

            if self.foto is None or self.foto == '':
                self.foto = 'images/Perfiles/NoImage.png'

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
                    foto = %s
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
                               self.id
                           ))
            bd.connection.commit()
            cursor.close()

            # Primero debo borrar las tareas y disponibilidad que tenga asignadas el empleado
            quitarTodasLasTareasDelEmpleado(bd, self.id)
            quitarTodaLaDisponibilidadDelEmpleado(bd, self.id)

            # Luego registro las tareas y disponibilidad del empleado que quiero modificar
            if self.tareas is not None:
                for tarea in self.tareas:
                    agregarTareaEmpleado(bd, tarea.id, self.id)

            if self.disponibilidad is not None:
                for dispo in self.disponibilidad:
                    agregarDisponibilidadEmpleado(bd, dispo.id, self.id)

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

    def postularseParaAnuncio(self, bd, anuncio, fecha):
        try:
            postulacion = Implementacion.Postulacion.Postulacion(0, self, anuncio, fecha)
            postulacion.crearPostulacion(bd)
            print('Postulado para empleo')
        except Exception as e:
            print('Error en postularseParaAnuncio ', e)

    def getTareasSeleccionadas(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                    SELECT 
                    id, 
                    descripcion, 
                    IF((SELECT id_tarea 
                    FROM empleado_tarea 
                    WHERE id_empleado = {} AND id_tarea = id),1,0) AS seleccionada FROM tarea'''.format(self.id))
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
            print("Error en getTareasSeleccionadasEmpleado ", e)

    def getDisponibilidadSeleccionadas(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                    SELECT 
                    id, 
                    descripcion, 
                    IF((SELECT id_disponibilidad 
                    FROM empleado_disponibilidad 
                    WHERE id_empleado = {} AND id_disponibilidad = id),1,0) AS seleccionada FROM disponibilidad'''.format(self.id))
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
            FROM empleado WHERE id = {}'''.format(id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()

        # Si no se puede cargar la foto guardada en la base cargo la imagen default
        foto = retorno[0][12]
        if foto is None or foto == '':
            foto = 'SinImagen'
        rutaFisica = '.' + url_for('static', filename = foto)
        if not os.path.exists(rutaFisica):
            foto = os.path.join(getCarpetaCargaImagenes(), 'NoImage.png')

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
            foto,
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
                e.descripcion,
                e.foto,
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
        # desde el retorno debo generar los objetos Disponibilidad
        disponibilidades = list()
        for tuplaDisponibilidad in retorno:
            disponibilidad = Disponibilidad(
                tuplaDisponibilidad[0], tuplaDisponibilidad[1])
            disponibilidades.append(disponibilidad)
        return disponibilidades
    except Exception as e:
        print("Error en getDisponibilidadEmpleado ", e)


def getRankingPorCalificacionEmpleados(bd, top):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
                SELECT e.id,
                    e.nombre,
                    e.apellido,
                    ROUND(e.promedio_calificacion, 2),
                    e.foto,
                    e.experiencia_meses,
                    COUNT(v.id) cant_vinculos,
                    COUNT(DISTINCT v.id_empleador) cant_calificantes
                FROM empleado e INNER JOIN vinculo v ON e.id = v.id_empleado WHERE e.promedio_calificacion > 0
                GROUP BY e.id
                ORDER BY promedio_calificacion DESC, cant_vinculos DESC, cant_calificantes DESC LIMIT {}'''.format(top))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        # desde el retorno debo generar los objetos DTOIndividuoCalificacion
        ranking = list()
        for tuplaRanking in retorno:
            dtoIndividuoCalificacion = DTOIndividuoCalificacion(tuplaRanking[0], tuplaRanking[1], tuplaRanking[2], tuplaRanking[3], 
            tuplaRanking[4], tuplaRanking[5], tuplaRanking[6], tuplaRanking[7], 'Empleado')
            ranking.append(dtoIndividuoCalificacion)
        return ranking
    except Exception as e:
        print("Error en getRankingPorCalificacionEmpleados ", e)