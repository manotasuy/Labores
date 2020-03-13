# si establezco from modulo import clase obtengo referencia ciclíca [Inicio]
from Implementacion import Empleado
from Implementacion import Anuncio
# si establezco from modulo import clase obtengo referencia ciclíca [Fin]
from Implementacion.Empleado import getEmpleadoByID
from Implementacion.Anuncio import getAnuncioByID


class Postulacion:

    def __init__(self, pId=None, pEmpleado=None, pAnuncio=None, pfecha='', pGeneraVinculo=''):
        self.id = pId
        self.empleado: Empleado = pEmpleado
        self.anuncio: Anuncio = pAnuncio
        self.fecha = pfecha
        self.genera_vinculo = pGeneraVinculo

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Id: {}, Empleado: {}, Anuncio: {}, Fecha: {}, Tiene vinculo: {}'.format(self.id, self.empleado.id, self.anuncio.id, self.fecha, self.genera_vinculo)

    def crearPostulacion(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                INSERT INTO postulacion
                    (
                        id_empleado,
                        id_anuncio,
                        fecha,
                        genera_vinculo
                    )
                VALUES (%s,%s,%s,%s)''',
                           (
                               self.empleado.id,
                               self.anuncio.id,
                               self.fecha,
                               self.genera_vinculo
                           ))
            bd.connection.commit()
            cursor.close()
            print('Postulación creada')
        except Exception as e:
            print('Error en crearPostulacion ', e)

    def generarVinculoEnPostulacion(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute(
                'UPDATE postulacion SET genera_vinculo=true WHERE id= {}'.format(self.id))
            bd.connection.commit()
            cursor.close()
            print('Se grabó el vínculo en la postulación')
        except Exception as e:
            print('Error en generarVinculoEnPostulacion ', e)


def getPostulacionesAnuncio(bd, idAnuncio):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_empleado,
                id_anuncio,
                fecha, 
                genera_vinculo
            FROM postulacion 
            WHERE id_anuncio = {}''' .format(idAnuncio))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()

        # desde el retorno debo generar los objetos Postulacion
        postulaciones = list()
        for tuplaPostulacion in retorno:
            postulacion = Postulacion(
                tuplaPostulacion[0],
                getEmpleadoByID(bd, tuplaPostulacion[1]),
                getAnuncioByID(bd, tuplaPostulacion[2]),
                tuplaPostulacion[3],
                tuplaPostulacion[4])
            postulaciones.append(postulacion)
        #print('Postulaciones desde Postulacion: ', postulaciones)
        return postulaciones
    except Exception as e:
        print('Error en getPostulacionesAnuncio ', e)


def getPostulacionesEmpleado(bd, idEmpleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_empleado,
                id_anuncio,
                fecha, 
                genera_vinculo
            FROM postulacion 
            WHERE id_empleado = {}''' .format(idEmpleado))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()

        # desde el retorno debo generar los objetos Postulacion
        postulaciones = list()
        for tuplaPostulacion in retorno:
            postulacion = Postulacion(
                tuplaPostulacion[0],
                getEmpleadoByID(bd, tuplaPostulacion[1]),
                getAnuncioByID(bd, tuplaPostulacion[2]),
                tuplaPostulacion[3],
                tuplaPostulacion[4])
            postulaciones.append(postulacion)
        return postulaciones
    except Exception as e:
        print('Error en getPostulacionesEmpleado ', e)


def getPostulacionEmpleadoAnuncio(bd, idEmpleado, idAnuncio):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_empleado,
                id_anuncio,
                fecha, 
                genera_vinculo
            FROM postulacion 
            WHERE id_empleado = {} AND id_anuncio = {}''' .format(idEmpleado, idAnuncio))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()

        postulacion = Postulacion(
            retorno[0][0],
            getEmpleadoByID(bd, retorno[0][1]),
            getAnuncioByID(bd, retorno[0][2]),
            retorno[0][3],
            retorno[0][4])
        return postulacion
    except Exception as e:
        print('Error en getPostulacionEmpleadoAnuncio ', e)
