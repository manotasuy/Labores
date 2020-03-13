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
