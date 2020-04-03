
class DTOIndividuoCalificacion:

    def __init__(self, pId=None, pNombre=None, pApellido=None, pPromedio=None, pFoto=None, pExperiencia=None, pCantVinculos=None, pCantCalificantes=None, pTipo=None):
        self.id = pId
        self.nombre = pNombre
        self.apellido = pApellido
        self.promedioCalificacion = pPromedio
        self.foto = pFoto
        self.experiencia = pExperiencia
        self.cantVinculos = pCantVinculos
        self.cantCalificantes = pCantCalificantes
        self.tipo = pTipo

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Nombre: {}, Apellido: {}, Promedio: {}, Cantidad de Vínculos: {}, Cantidad de Calificantes: {}, Foto: {}'.format(self.nombre, self.apellido, self.promedioCalificacion, self.cantVinculos, self.cantCalificantes, self.foto)
