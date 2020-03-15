
class DTOAuxEmpleado:

    def __init__(self, pTareas=None, pDispon=None, pContratado=None):
        self.tareas: list() = pTareas
        self.disponibilidad: list() = pDispon
        self.contratado =pContratado

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Tareas: {}, Disponibilidad: {}'.format(self.tareas.__dict__, self.disponibilidad.__dict__)

    def cargarTareas(self, tareas):
        try:
            self.tareas = tareas
        except Exception as e:
            print("Error en cargarTareas ", e)

    def cargarDisponibilidad(self, disponibilidad):
        try:
            self.disponibilidad = disponibilidad
        except Exception as e:
            print("Error en cargarDisponibilidad ", e)

    def getTareas(self):
        try:
            return self.tareas
        except Exception as e:
            print("Error en getTareas ", e)

    def getDisponibilidad(self):
        try:
            return self.disponibilidad
        except Exception as e:
            print("Error en getDisponibilidad ", e)


class TareaSeleccion:

    def __init__(self, pId=None, pDescripcion=None, pSeleccionada=None):
        self.id = pId
        self.descripcion = pDescripcion
        self.seleccionada = pSeleccionada

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Descripción: {}, Seleccionada: {}'.format(self.descripcion, self.seleccionada)


class DisponibilidadSeleccion:

    def __init__(self, pId=None, pDescripcion=None, pSeleccionada=None):
        self.id = pId
        self.descripcion = pDescripcion
        self.seleccionada = pSeleccionada

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Descripción: {}, Seleccionada: {}'.format(self.descripcion, self.seleccionada)
