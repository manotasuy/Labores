
class DTOMensaje():

    def __init__(self, tieneVinculo, existePostulacion, tipoEmisor):
        self.tiene_vinculo = tieneVinculo
        self.existe_postulacion = existePostulacion
        self.tipo_emisor = tipoEmisor

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Tiene vínculo: {}, Existe postulación: {}, Tipo Emisor: {}'.format(self.tiene_vinculo, self.existe_postulacion, self.tipo_emisor)

    def setTieneVinculo(self, tieneVinculo):
        self.tiene_vinculo = tieneVinculo

    def setExistePostulacion(self, existePostulacion):
        self.existe_postulacion = existePostulacion

    def setTipoEmisor(self, tipoEmisor):
        self.tipo_emisor = tipoEmisor

    def getTieneVinculo(self):
        return self.tiene_vinculo

    def getExistePostulacion(self):
        return self.existe_postulacion

    def getTipoEmisor(self):
        return self.tipo_emisor


    def habilitaMensaje(self):
        if self.tipo_emisor == 3:
            return False
        elif not self.existe_postulacion:
            return False
        elif self.tiene_vinculo:
            return True
        elif self.existe_postulacion and not self.tiene_vinculo:
            return True