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


class Mensaje:

    def __init__(
            self,
            pId,
            pEmpleado,
            pEmpleador,
            pAnuncio,
            pFecha,
            pMensaje,
            pTipoEmisor,
            pTipoReceptor):
        self.id = pId
        self.empleado : Empleado = pEmpleado
        self.empleador : Empleador = pEmpleador
        self.anuncio = pAnuncio
        self.fecha = pFecha
        self.mensaje = pMensaje
        self.tipoEmisor = pTipoEmisor
        self.tipoReceptor = pTipoReceptor

    def __str__(self):
        return 'Id: {}, Empleado: {}, Empleador: {}, Anuncio: {}, Fecha: {}, Mensaje: {}'.format(self.id, self.empleado.id, self.empleador.id, self.anuncio.id, self.fecha, self.mensaje)

    def __getitem__(self, item):
        return self.__dict__[item]

    def crearMensaje(self, bd):
        try:
            if self.anuncio == None:
                idAnuncio = None
            else:
                idAnuncio = self.anuncio.id

            cursor = bd.connection.cursor()
            cursor.execute('''
                INSERT INTO mensaje
                    (
                        id_empleado,
                        id_empleador,
                        id_anuncio,
                        fecha,
                        mensaje,
                        id_tipo_emisor,
                        id_tipo_receptor
                    )
                VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                           (
                               self.empleado.id,
                               self.empleador.id,
                               idAnuncio,
                               self.fecha,
                               self.mensaje,
                               self.tipoEmisor,
                               self.tipoReceptor
                           ))
            bd.connection.commit()
            cursor.close()
            print('Mensaje Creado')
        except Exception as e:
            print("Error en crearMensaje ", e)

    def borrarMensaje(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM mensaje WHERE id = {}
                '''.format(self.id))
            bd.connection.commit()
            cursor.close()
            print('Mensaje Borrado')
        except Exception as e:
            print("Error en borrarMensaje ", e)

    def actualizarMensaje(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE mensaje SET
                    fecha = %s,
                    mensaje = %s
                WHERE id = %s''',
                           (
                               self.fecha,
                               self.mensaje
                           ))

            bd.connection.commit()
            cursor.close()
            print('Mensaje Actualizado')
        except Exception as e:
            print("Error en actualizarMensaje ", e)


def getMensajeByID(bd, id):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_empleado,
                id_empleador,
                id_anuncio,
                fecha,
                mensaje,
                id_tipo_emisor,
                id_tipo_receptor
            FROM mensaje WHERE id = {}'''.format(id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        mensaje = Mensaje(
            retorno[0][0],
            getEmpleadoByID(bd, retorno[0][1]),
            getEmpleadorByID(bd, retorno[0][2]),
            getAnuncioByID(bd, retorno[0][3]),
            retorno[0][4],
            retorno[0][5],
            retorno[0][6],
            retorno[0][7],
        )
        return mensaje
    except Exception as e:
        print("Error en getMensajeByID ", e)


def getMensajesParaEmpleado(bd, id_empleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_empleado,
                id_empleador,
                id_anuncio,
                fecha,
                mensaje,
                id_tipo_emisor,
                id_tipo_receptor
            FROM mensaje WHERE id_empleado = {} AND (id_tipo_emisor = 1 OR id_tipo_receptor = 1)  ORDER BY fecha DESC'''.format(id_empleado))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()

        diccRetorno = OrderedDict()

        # debo devolver un dicc con clave:valor id_empleador:lista de mensajes del empleador
        # entonces al consultar clave obtengo la lista de mensajes con ese empleador
        
        for registro in retorno:
            mensaje = Mensaje(
                registro[0],
                getEmpleadoByID(bd, registro[1]),
                getEmpleadorByID(bd, registro[2]),
                getAnuncioByID(bd, registro[3]),
                registro[4],
                registro[5],
                registro[6],
                registro[7]
            )
            clave = mensaje.empleador.id
            if clave in diccRetorno:
                diccRetorno[clave].append(mensaje)
            else:
                diccRetorno[clave] = [mensaje]

        return diccRetorno
    except Exception as e:
        print("Error en getMensajesParaEmpleado ", e)


def getMensajesParaEmpleador(bd, id_empleador):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_empleado,
                id_empleador,
                id_anuncio,
                fecha,
                mensaje,
                id_tipo_emisor,
                id_tipo_receptor
            FROM mensaje WHERE id_empleador = {} AND (id_tipo_emisor = 2 OR id_tipo_receptor = 2) ORDER BY fecha DESC'''.format(id_empleador))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()

        diccRetorno = OrderedDict()

        # debo devolver un dicc con clave:valor id_empleado:lista de mensajes del empleado
        # entonces al consultar clave obtengo la lista de mensajes con ese empleado
        
        for registro in retorno:
            mensaje = Mensaje(
                registro[0],
                getEmpleadoByID(bd, registro[1]),
                getEmpleadorByID(bd, registro[2]),
                getAnuncioByID(bd, registro[3]),
                registro[4],
                registro[5],
                registro[6],
                registro[7]
            )
            clave = mensaje.empleado.id
            if clave in diccRetorno:
                diccRetorno[clave].append(mensaje)
            else:
                diccRetorno[clave] = [mensaje]

        return diccRetorno
    except Exception as e:
        print("Error en getMensajesParaEmpleador ", e)