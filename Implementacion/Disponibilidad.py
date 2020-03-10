class Disponibilidad:

    def __init__(self, pId=None, pDescripcion=None):
        self.id = pId
        self.descripcion = pDescripcion

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Descripción: {}'.format(self.descripcion)


def getDisponibilidadesRegistradas(bd):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('SELECT id, descripcion FROM disponibilidad')
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        disponibilidades = list()
        for tuplaDisponibilidad in retorno:
            disponibilidad = Disponibilidad(
                tuplaDisponibilidad[0], tuplaDisponibilidad[1])
            disponibilidades.append(disponibilidad)
        return disponibilidades
    except Exception as e:
        print("Error en getDisponibilidadesRegistradas ", e)