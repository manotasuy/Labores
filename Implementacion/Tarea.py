class Tarea:

    def __init__(self, pId=None, pDescripcion=None):
        self.id = pId
        self.descripcion = pDescripcion

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Descripción: {}'.format(self.descripcion)


def getTareasRegistradas(bd):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('SELECT id, descripcion FROM tarea')
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        tareas = list()
        for tuplaTarea in retorno:
            tarea = Tarea(tuplaTarea[0], tuplaTarea[1])
            tareas.append(tarea)
        return tareas
    except Exception as e:
        print("Error en getTareasRegistradas ", e)


def agregarTareaEmpleado(bd, id_tarea, id_empleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('INSERT INTO empleado_tarea (id_empleado, id_tarea) VALUES ({}, {})'.format(id_empleado, id_tarea))
        bd.connection.commit()
        cursor.close()
        #print('Tarea "', id_tarea, '" agregada en el empleado')
    except Exception as e:
        print("Error en agregarTareaEmpleado ", e)


def quitarTareaEmpleado(bd, id_tarea, id_empleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('DELETE FROM empleado_tarea WHERE id_empleado = {} AND id_tarea = {}'.format(id_empleado, id_tarea))
        bd.connection.commit()
        cursor.close()
        #print('Tarea quitada del empleado')
    except Exception as e:
        print("Error en quitarTareaEmpleado ", e)


def quitarTodasLasTareasDelEmpleado(bd, id_empleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('DELETE FROM empleado_tarea WHERE id_empleado = {}'.format(id_empleado))
        bd.connection.commit()
        cursor.close()
        #print('Todas las tareas quitadas del empleado')
    except Exception as e:
        print("Error en quitarTodasLasTareasDelEmpleado ", e)