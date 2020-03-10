from Implementacion.Empleado import Empleado
from Implementacion.Anuncio import Anuncio
from Implementacion.Empleado import getEmpleadoByID
from Implementacion.Anuncio import getAnuncioByID


class Postulacion:

    def __init__(self, pId=None, pEmpleado=None, pAnuncio=None, pfecha='', pGeneraVinculo=''):
        self.id = pId
        self.empleado : Empleado = pEmpleado
        self.anuncio : Anuncio = pAnuncio
        self.fecha = pfecha
        self.genera_vinculo = pGeneraVinculo

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Id: {}, Empleado: {}, Anuncio: {}, Fecha: {}, Tiene vinculo: {}'.format(self.id, self.empleado.id, self.anuncio.id, self.fecha, self.genera_vinculo)


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
        #print('Postulaciones desde Postulacion: ', postulaciones)
        return postulaciones
    except Exception as e:
        print('Error en getPostulacionesEmpleado ', e)
