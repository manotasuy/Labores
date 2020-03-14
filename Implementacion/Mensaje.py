from datetime import datetime
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
            pMensaje):
        self.id = pId
        self.empleado = pEmpleado
        self.empleador = pEmpleador
        self.anuncio = pAnuncio
        self.fecha = pFecha
        self.mensaje = pMensaje

    def __str__(self):
        return 'Id: {}, Empleado: {}, Empleador: {}, Anuncio: {}, Fecha: {}, Mensaje: {}'.format(self.id, self.empleado.id, self.empleador.id, self.anuncio.id, self.fecha, self.mensaje)

    def __getitem__(self, item):
        return self.__dict__[item]

    def crearMensaje(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                INSERT INTO mensaje
                    (
                        id_empleado,
                        id_empleador,
                        id_anuncio,
                        fecha,
                        mensaje
                    )
                VALUES (%s,%s,%s,%s,%s)''',
                           (
                               self.empleado.id,
                               self.empleador.id,
                               self.anuncio.id,
                               self.fecha,
                               self.mensaje
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
                mensaje
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
            retorno[0][5]
        )
        return mensaje
    except Exception as e:
        print("Error en getMensajeByID ", e)


def getMensajesPersonalesPorRemitente(bd, id_persona):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_empleado,
                id_empleador,
                id_anuncio,
                fecha,
                mensaje
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
            retorno[0][5]
        )
        return mensaje
    except Exception as e:
        print("Error en getMensajeByID ", e)