
class DTOMensaje():

    def __init__(self, Vinculo, Postulacion, tipoEmisor):
        self.vinculo = Vinculo
        self.postulacion = Postulacion
        self.tipo_emisor = tipoEmisor

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Vínculo: {}, Postulación: {}, Tipo Emisor: {}'.format(self.vinculo, self.postulacion, self.tipo_emisor)


    def habilitaMensaje(self):
        if self.tipo_emisor == 3 and self.vinculo is None:
            return False
        elif self.tipo_emisor == 3 and self.vinculo is not None:
            return True
        elif self.postulacion is None:
            return False
        elif self.postulacion is not None and self.postulacion.genera_vinculo == True and self.vinculo is None:
            return False
        elif self.postulacion is not None and self.postulacion.genera_vinculo == True and self.vinculo is not None:
            return True
        elif self.postulacion is not None and (self.postulacion.genera_vinculo is None or self.postulacion.genera_vinculo == False):
            return True
        elif self.vinculo is not None:
            return True
        else:
            return False