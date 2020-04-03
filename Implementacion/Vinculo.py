from datetime import datetime
# si establezco from modulo import clase obtengo referencia ciclíca [Inicio]
from Implementacion import Empleador
from Implementacion import Empleado
from Implementacion import Anuncio
# si establezco from modulo import clase obtengo referencia ciclíca [Fin]
from Implementacion.Empleado import getEmpleadoByID
from Implementacion.Empleador import getEmpleadorByID
from Implementacion.Anuncio import getAnuncioByID


class Vinculo:

    def __init__(
            self,
            pId,
            pEmpleado,
            pEmpleador,
            pAnuncio,
            pFechaInicio,
            pFechaFin,
            pDescripcion,
            pCalifEmpleado,
            pCalifEmpleador):
        self.id = pId
        self.empleado: Empleado = pEmpleado
        self.empleador: Empleador = pEmpleador
        self.anuncio: Anuncio = pAnuncio
        self.fecha_inicio = pFechaInicio
        self.fecha_fin = pFechaFin
        self.descripcion = pDescripcion
        self.calif_empleado = pCalifEmpleado
        self.calif_empleador = pCalifEmpleador

    def __str__(self):
        return 'Id: {}, Empleado: {}, Empleador: {}, Anuncio: {}, Fecha Inicio: {}, Fecha Fin: {}, Descripcion: {}, Calificacion Empleado: {}, Calificacion Empleado: {}'.format(self.id, self.empleado.id, self.empleador.id, self.anuncio.id, self.fecha_inicio, self.fecha_fin, self.descripcion, self.calif_empleado, self.calif_empleador)

    def __getitem__(self, item):
        return self.__dict__[item]

    def crearVinculo(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                INSERT INTO vinculo 
                    (
                        id_empleado,
                        id_empleador,
                        id_anuncio,
                        fecha_inicio,
                        fecha_fin,
                        descripcion,
                        calificacion_empleado,
                        calificacion_empleador
                    )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',
                           (
                               self.empleado.id,
                               self.empleador.id,
                               self.anuncio.id,
                               self.fecha_inicio,
                               self.fecha_fin,
                               self.descripcion,
                               self.calif_empleado,
                               self.calif_empleador
                           ))
            bd.connection.commit()
            cursor.close()
            print('Vinculo Creado')
        except Exception as e:
            print("Error en crearVinculo ", e)

    def borrarVinculo(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM vinculo WHERE id = {}
                '''.format(self.id))
            bd.connection.commit()
            cursor.close()
            print('Vinculo Borrado')
        except Exception as e:
            print("Error en borrarVinculo ", e)

    def actualizarVinculo(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE vinculo SET
                    fecha_fin = %s,
                    descripcion = %s,
                    calificacion_empleado = %s,
                    calificacion_empleador = %s
                WHERE id = %s''',
                           (
                               self.fecha_fin,
                               self.descripcion,
                               self.calif_empleado,
                               self.calif_empleador,
                               self.id
                           ))

            bd.connection.commit()
            cursor.close()
            print('Vinculo Actualizado')
        except Exception as e:
            print("Error en actualizarVinculo ", e)

    def marcarVinculoComoNotificado(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE vinculo
                SET notificado = true
                WHERE id = {}
                '''.format(self.id))
            bd.connection.commit()
            cursor.close()
            print('Vínculo marcado como notificado')
        except Exception as e:
            print("Error en marcarVinculoComoNotificado ", e)


def getVinculoByID(bd, id):
    try:
        if id == None or id == 0:
            return None
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_empleado,
                id_empleador,
                id_anuncio,
                fecha_inicio,
                fecha_fin,
                descripcion,
                calificacion_empleado,
                calificacion_empleador
            FROM vinculo WHERE id = {}'''.format(id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        vinculo = Vinculo(
            retorno[0][0],
            getEmpleadoByID(bd, retorno[0][1]),
            getEmpleadorByID(bd, retorno[0][2]),
            getAnuncioByID(bd, retorno[0][3]),
            retorno[0][4],
            retorno[0][5],
            retorno[0][6],
            retorno[0][7],
            retorno[0][8]
        )
        return vinculo
    except Exception as e:
        print("Error en getVinculoByID ", e)


def getVinculoByEmpleado(bd, empleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_empleado,
                id_empleador,
                id_anuncio,
                fecha_inicio,
                fecha_fin,
                descripcion,
                calificacion_empleado,
                calificacion_empleador
            FROM vinculo WHERE id_empleado = {}'''.format(empleado.id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        vinculos = []
        for v in retorno:
            vinculo = Vinculo(
                v[0],
                getEmpleadoByID(bd, v[1]),
                getEmpleadorByID(bd, v[2]),
                getAnuncioByID(bd, v[3]),
                v[4],
                v[5],
                v[6],
                v[7],
                v[8]
            )
            #print('Vínculo: ', vinculo)
            vinculos.append(vinculo)
        return vinculos
    except Exception as e:
        print("Error en getVinculoByEmpleado ", e)


def getVinculoByEmpleador(bd, empleador):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_empleado,
                id_empleador,
                id_anuncio,
                fecha_inicio,
                fecha_fin,
                descripcion,
                calificacion_empleado,
                calificacion_empleador
            FROM vinculo WHERE id_empleador = {}'''.format(empleador.id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        vinculos = []
        for v in retorno:
            vinculo = Vinculo(
                v[0],
                getEmpleadoByID(bd, v[1]),
                getEmpleadorByID(bd, v[2]),
                getAnuncioByID(bd, v[3]),
                v[4],
                v[5],
                v[6],
                v[7],
                v[8]
            )
            #print('Vínculo: ', vinculo)
            vinculos.append(vinculo)
        return vinculos
    except Exception as e:
        print("Error en getVinculoByEmpleador ", e)


def getVinculoIDs(bd, id):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_empleado,
                id_empleador,
                id_anuncio,
                fecha_inicio,
                fecha_fin,
                descripcion,
                calificacion_empleado,
                calificacion_empleador
            FROM vinculo WHERE id = {}'''.format(id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        vinculo = Vinculo(
            retorno[0][0],
            retorno[0][1],
            retorno[0][2],
            retorno[0][3],
            retorno[0][4],
            retorno[0][5],
            retorno[0][6],
            retorno[0][7],
            retorno[0][8]
        )
        return vinculo
    except Exception as e:
        print("Error en getVinculoIDs ", e)


def getPromedioByEmpleadoId(bd, idEmpleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id_empleador,
                calificacion_empleado
            FROM vinculo WHERE id_empleado = {}'''.format(idEmpleado))
        retornoV = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        vinculosCal = []
        for vin in retornoV:
            if vin[1] != None:
                vinculosCal.append(vin)

        suma = 0 #contiene la suma de todas las calificaciones del empleado
        for c in vinculosCal:
            suma += c[1]

        cantVinculos = len(vinculosCal) #contiene la cantidad de vinculos calificados

        promedio = 0 #contiene el promedio de las calificaciones
        
        if cantVinculos == 0:
            promedio = None
        else:
            promedio = suma / cantVinculos

        listaEmpleadoresRep = []
        for v in vinculosCal:
            listaEmpleadoresRep.append(v[0])

        listaEmpleadores = list(set(listaEmpleadoresRep)) #contiene una lista con los empleados sin repetir

        cantEmpleadores = len(listaEmpleadores)

        calificaciones = {
            'cantVinculos' : cantVinculos,
            'cantEmpleadores' : cantEmpleadores,
            'promedio': promedio
        }

        
        return calificaciones
    except Exception as e:
        print("Error en getPromedioByEmpleadoId ", e)


def getPromedioByEmpleadorId(bd, idEmpleador):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id_empleado,
                calificacion_empleador
            FROM vinculo WHERE id_empleador = {}'''.format(idEmpleador))
        retornoV = cursor.fetchall() #contiene id_empleado y calificacion_empleador para todos los vinculos del empleadoR
        bd.connection.commit()
        cursor.close()
        vinculosCal = [] #contiene id_empleado y calificacion_empleador para todos los vinculos CALIFICADOS del empleadoR
        for cal in retornoV:
            
            if cal[1] != None:
                vinculosCal.append(cal)
                #print(cal)

        suma = 0 #contiene la suma de todas las calificaciones del empleador
        for c in vinculosCal:
            suma += c[1]

        cantVinculos = len(vinculosCal) #contiene la cantidad de vinculos calificados

        promedio = 0 #contiene el promedio de las calificaciones
        
        if cantVinculos == 0:
            promedio = None
        else:
            promedio = suma / cantVinculos

        listaEmpleadosRep = []
        for v in vinculosCal:
            listaEmpleadosRep.append(v[0])

        listaEmpleados = list(set(listaEmpleadosRep)) #contiene una lista con los empleados sin repetir

        cantEmpleados = len(listaEmpleados)

        calificaciones = {
            'cantVinculos' : cantVinculos,
            'cantEmpleados' : cantEmpleados,
            'promedio': promedio
        }

        
        return calificaciones
    except Exception as e:
        print("Error en getPromedioByEmpleadoId ", e)


def empleadoTieneNotificacionesPendientesVinculos(bd, id_empleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT id FROM vinculo WHERE id_empleado = {} AND notificado = 0
            '''.format(id_empleado))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        if retorno is None or len(retorno) == 0:
            return False
        else:
            return len(retorno[0]) > 0
    except Exception as e:
        print("Error en empleadoTieneNotificacionesPendientesVinculos ", e)


def getVinculosNoNotificadosDelEmpleado(bd, empleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_empleado,
                id_empleador,
                id_anuncio,
                fecha_inicio,
                fecha_fin,
                descripcion,
                calificacion_empleado,
                calificacion_empleador
            FROM vinculo WHERE id_empleado = {} AND notificado = 0'''.format(empleado.id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()

        vinculos = list()
        for v in retorno:
            vinculo = Vinculo(
                v[0],
                getEmpleadoByID(bd, v[1]),
                getEmpleadorByID(bd, v[2]),
                getAnuncioByID(bd, v[3]),
                v[4],
                v[5],
                v[6],
                v[7],
                v[8]
            )
            vinculos.append(vinculo)
        return vinculos
    except Exception as e:
        print("Error en getVinculosNoNotificadosDelEmpleado ", e)


def tieneElEmpleadoVinculoConEmpleador(bd, id_empleado, id_empleador):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id
            FROM vinculo WHERE id_empleado = {} AND id_empleador = {} AND fecha_fin is NULL AND id_anuncio > 0'''
            .format(id_empleado, id_empleador))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        
        if retorno is None or len(retorno) == 0:
            return False
        else:
            return True
    except Exception as e:
        print("Error en tieneElEmpleadoVinculoConEmpleador ", e)


def tieneElEmpleadorVinculoConEmpleado(bd, id_empleador, id_empleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id
            FROM vinculo WHERE id_empleado = {} AND id_empleador = {} AND fecha_fin is NULL AND id_anuncio > 0'''
            .format(id_empleado, id_empleador))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        
        if retorno is None or len(retorno) == 0:
            return False
        else:
            return True
    except Exception as e:
        print("Error en tieneElEmpleadorVinculoConEmpleado ", e)
