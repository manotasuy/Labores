from datetime import datetime
from collections import defaultdict
from collections import OrderedDict
# si establezco from modulo import clase obtengo referencia ciclíca [Inicio]
from Implementacion import Empleador
from Implementacion import Empleado
from Implementacion import Anuncio
# si establezco from modulo import clase obtengo referencia ciclíca [Fin]
from Implementacion.Empleado import getEmpleadoByID
from Implementacion.Empleador import getEmpleadorByID
from Implementacion.Anuncio import getAnuncioByID
from Implementacion.Postulacion import getPostulacionById
from Implementacion.Vinculo import getVinculoByID

class Recordatorio:

    def __init__(
            self,
            pId,
            pIdTipo,
            pEmpleado,
            pEmpleador,
            pDestinatario,
            pAnuncio,
            pPostulacion,
            pVinculo,
            pFechaRecordatorio,
            pFechaLimite,
            pCantVecesAplazado,
            pLeyenda,
            pBloqueante):
        self.id = pId
        self.tipo = pIdTipo
        self.empleado : Empleado = pEmpleado
        self.empleador : Empleador = pEmpleador
        self.destinatario = pDestinatario
        self.anuncio = pAnuncio
        self.postulacion = pPostulacion
        self.vinculo = pVinculo
        self.fechaRecordatorio = pFechaRecordatorio
        self.fechaLimite = pFechaLimite
        self.cantVecesAplazado = pCantVecesAplazado
        self.leyenda = pLeyenda
        self.bloqueante = pBloqueante

    def __str__(self):
        return 'Id Recordatorio: {}, Id Empleado: {}, Id Empleador: {}, Id Anuncio: {}, Fecha Recordatorio: {}, Fecha Limite: {}, Cant Veces Aplazado: {},Leyenda: {}, Bloqueante? {}'.format(self.id, self.empleado.id, self.empleador.id, self.anuncio.id, self.fechaRecordatorio, self.fechaLimite, self.cantVecesAplazado, self.leyenda, self.bloqueante)

    def __getitem__(self, item):
        return self.__dict__[item]

    def crearRecordatorio(self, bd):
        try:
            if self.anuncio == None:
                idAnuncio = None
            else:
                idAnuncio = self.anuncio.id

            if self.postulacion == None:
                idPostulacion = None
            else:
                idPostulacion = self.postulacion.id

            if self.vinculo == None:
                idVinculo = None
            else:
                idVinculo = self.vinculo.id

            cursor = bd.connection.cursor()
            cursor.execute('''
                INSERT INTO recordatorio
                    (
                        id_tipo, 
                        id_empleado, 
                        id_empleador, 
                        id_destinatario, 
                        id_anuncio, 
                        id_postulacion, 
                        id_vinculo, 
                        fecha_recordatorio, 
                        fecha_limite, 
                        cant_veces_aplazado, 
                        leyenda, 
                        bloqueante
                    )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                           (
                               self.tipo,
                               self.empleado.id,
                               self.empleador.id,
                               self.destinatario.id,
                               idAnuncio,
                               idPostulacion,
                               idVinculo,
                               self.fechaRecordatorio,
                               self.fechaLimite,
                               self.cantVecesAplazado,
                               self.leyenda,
                               self.bloqueante
                           ))
            bd.connection.commit()
            cursor.close()
            print('Recordatorio Creado')
        except Exception as e:
            print("Error en crearRecordatorio ", e)

    def borrarRecordatorio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM recordatorio WHERE id = {}
                '''.format(self.id))
            bd.connection.commit()
            cursor.close()
            print('Recordatorio Borrado')
        except Exception as e:
            print("Error en borrarRecordatorio ", e)

    def actualizarRecordatorio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE recordatorio SET 
                    fecha_recordatorio = %s, 
                    fecha_limite = %s, 
                    cant_veces_aplazado = %s, 
                    leyenda = %s, 
                    bloqueante = %s
                WHERE id = %s''',
                           (
                               self.fechaRecordatorio,
                               self.fechaLimite,
                               self.cantVecesAplazado,
                               self.leyenda,
                               self.bloqueante,
                               self.id
                           ))

            bd.connection.commit()
            cursor.close()
            print('Recordatorio Actualizado')
        except Exception as e:
            print("Error en actualizarRecordatorio ", e)

def getRecordatorioByID(bd, id):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_tipo, 
                id_empleado, 
                id_empleador, 
                id_destinatario, 
                id_anuncio, 
                id_postulacion, 
                id_vinculo, 
                fecha_recordatorio, 
                fecha_limite, 
                cant_veces_aplazado, 
                leyenda, 
                bloqueante
            FROM recordatorio WHERE id = {}'''.format(id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        if retorno[0][4] == retorno[0][2]:
            destinatario = getEmpleadoByID(bd, retorno[0][4])
        elif retorno[0][4] == retorno[0][3]:
            destinatario = getEmpleadorByID(bd, retorno[0][4])

        recordatorio = Recordatorio(
            retorno[0][0],
            retorno[0][1],
            getEmpleadoByID(bd, retorno[0][2]),
            getEmpleadorByID(bd, retorno[0][3]),
            destinatario,
            getAnuncioByID(bd, retorno[0][5]),
            getPostulacionById(bd, retorno[0][6]),
            getVinculoByID(bd, retorno[0][7]),
            retorno[0][8],
            retorno[0][9],
            retorno[0][10],
            retorno[0][11],
            retorno[0][12]
        )
        return recordatorio
    except Exception as e:
        print("Error en getRecordatorioByID ", e)

def comprobarSiHayRecordatoriosParaBloquear(bd):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            UPDATE recordatorio SET  
                bloqueante = 1
            WHERE fecha_limite = CURDATE()''')
        bd.connection.commit()
        cursor.close()
    except Exception as e:
        print("Error en comprobarSiHayRecordatoriosParaBloquear ", e)

def recordatoriosBloqueantes(bd, idDestinatario):
    try:
        if idDestinatario == None or idDestinatario == 0:
            return None
        # primero compruebo si hay recordatorios para bloquear porque se llegó a su fecha límite
        comprobarSiHayRecordatoriosParaBloquear(bd)

        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_tipo, 
                id_empleado, 
                id_empleador, 
                id_destinatario, 
                id_anuncio, 
                id_postulacion, 
                id_vinculo, 
                fecha_recordatorio, 
                fecha_limite, 
                cant_veces_aplazado, 
                leyenda, 
                bloqueante
            FROM recordatorio WHERE id_destinatario = {} AND bloqueante = 1'''.format(idDestinatario))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()

        recordatorios = list()
        for rec in retorno:
            if rec[4] == rec[2]:
                destinatario = getEmpleadoByID(bd, rec[4])
            elif rec[4] == rec[3]:
                destinatario = getEmpleadorByID(bd, rec[4])

            recordatorio = Recordatorio(
                rec[0],
                rec[1],
                getEmpleadoByID(bd, rec[2]),
                getEmpleadorByID(bd, rec[3]),
                destinatario,
                getAnuncioByID(bd, rec[5]),
                getPostulacionById(bd, rec[6]),
                getVinculoByID(bd, rec[7]),
                rec[8],
                rec[9],
                rec[10],
                rec[11],
                rec[12]
            )
            recordatorios.append(recordatorio)
        
        if len(recordatorios) > 0:
            return recordatorios
        else:
            return None
    except Exception as e:
        print("Error en recordatoriosBloqueantes ", e)

def recordatoriosCalificacionesPendientes(bd, idDestinatario):
    try:
        if idDestinatario == None or idDestinatario == 0:
            return None
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_tipo, 
                id_empleado, 
                id_empleador, 
                id_destinatario, 
                id_anuncio, 
                id_postulacion, 
                id_vinculo, 
                fecha_recordatorio, 
                fecha_limite, 
                cant_veces_aplazado, 
                leyenda, 
                bloqueante
            FROM recordatorio WHERE id_destinatario = {} AND fecha_recordatorio <= CURDATE()'''.format(idDestinatario))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()

        recordatorios = list()
        for rec in retorno:
            if rec[4] == rec[2]:
                destinatario = getEmpleadoByID(bd, rec[4])
            elif rec[4] == rec[3]:
                destinatario = getEmpleadorByID(bd, rec[4])

            recordatorio = Recordatorio(
                rec[0],
                rec[1],
                getEmpleadoByID(bd, rec[2]),
                getEmpleadorByID(bd, rec[3]),
                destinatario,
                getAnuncioByID(bd, rec[5]),
                getPostulacionById(bd, rec[6]),
                getVinculoByID(bd, rec[7]),
                rec[8],
                rec[9],
                rec[10],
                rec[11],
                rec[12]
            )
            recordatorios.append(recordatorio)
        
        if len(recordatorios) > 0:
            return recordatorios
        else:
            return None
    except Exception as e:
        print("Error en recordatoriosCalificacionesPendientes ", e)

def getTiposRecordatoriosRegistrados(bd):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('SELECT id, nombre FROM tipo_recordatorio')
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        tipos = list()
        for tipo in retorno:
            t = {
                "id": tipo[0],
                "nombre": tipo[1]
            }
            tipos.append(t)
        return tipos
    except Exception as e:
        print("Error en getTiposRecordatoriosRegistrados ", e)