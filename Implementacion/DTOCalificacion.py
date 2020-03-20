
class DTOCalificacion:

    def __init__(self, pPromedio=None, pCantVinculos=None, pCantCalificantes=None):
        self.promedio = pPromedio
        self.cantVinculos = pCantVinculos
        self.cantCalificantes = pCantCalificantes

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Promedio: {}, Cantidad de Vínculos: {}, Cantidad de Calificantes'.format(self.promedio, self.cantVinculos, self.cantCalificantes)
