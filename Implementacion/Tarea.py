class Tarea:

    def __init__(self, pId=None, pDescripcion=None):
        self.id = pId
        self.descripcion = pDescripcion

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Descripción: {}'.format(self.descripcion)
