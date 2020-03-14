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


def agregarDisponibilidadEmpleado(bd, id_disponibilidad, id_empleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('INSERT INTO empleado_disponibilidad (id_empleado, id_disponibilidad) VALUES ({}, {})'.format(id_empleado, id_disponibilidad))
        bd.connection.commit()
        cursor.close()
        #print('Disponibilidad "', id_disponibilidad, '" agregada en el empleado')
    except Exception as e:
        print("Error en agregarDisponibilidadEmpleado ", e)


def quitarDisponibilidadEmpleado(bd, id_disponibilidad, id_empleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('DELETE FROM empleado_disponibilidad WHERE id_empleado = {} AND id_disponibilidad = {}'.format(id_empleado, id_disponibilidad))
        bd.connection.commit()
        cursor.close()
        #print('Disponibilidad quitada del empleado')
    except Exception as e:
        print("Error en quitarDisponibilidadEmpleado ", e)


def quitarTodaLaDisponibilidadDelEmpleado(bd, id_empleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('DELETE FROM empleado_disponibilidad WHERE id_empleado = {}'.format(id_empleado))
        bd.connection.commit()
        cursor.close()
        #print('Toda disponibilidad quitada del empleado')
    except Exception as e:
        print("Error en quitarTodaLaDisponibilidadDelEmpleado ", e)