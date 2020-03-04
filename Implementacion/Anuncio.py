from datetime import datetime


class Anuncio:

    def __init__(self, pTitulo, pDescripcion, pFechaInicio, pFechaCierre, pEstado, pExperiencia, pSalario, pIdEmpleador, pCalDesde, pCalHasta, pTieneVinculo):
        self.titulo = pTitulo
        self.descripcion = pDescripcion
        self.fecha_inicio = pFechaInicio
        self.fecha_cierre = pFechaCierre
        self.estado = pEstado
        self.experiencia = pExperiencia
        self.salario = pSalario
        self.id_empleador = pIdEmpleador
        self.calificacion_desde = pCalDesde
        self.calificacion_hasta = pCalHasta
        self.tiene_vinculo = pTieneVinculo

    def __str__(self):
        return 'Título: {}, Empleador {}, Vinculo {}'.format(self.titulo, self.id_empleador, self.tiene_vinculo)

    def createAnuncio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                INSERT INTO anuncio 
                    (
                        titulo,
                        descripcion,
                        fecha_inicio,
                        fecha_cierre,
                        estado,
                        experiencia,
                        salario,
                        id_empleador,
                        calificacion_desde,
                        calificacion_hasta,
                        tiene_vinculo
                    )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                           (
                               self.titulo,
                               self.descripcion,
                               self.fecha_inicio,
                               self.fecha_cierre,
                               self.estado,
                               self.experiencia,
                               self.salario,
                               self.id_empleador,
                               self.calificacion_desde,
                               self.calificacion_hasta,
                               self.tiene_vinculo
                           ))
            bd.connection.commit()
            cursor.close()
            print('Anuncio Creado')
        except:
            print("Error en creación del anuncio")

    def updateAnuncio(self, bd, id):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE anuncio SET
                    titulo = %s,
                    descripcion = %s,
                    fecha_inicio = %s,
                    fecha_cierre = %s,
                    estado = %s,
                    experiencia = %s,
                    salario = %s,
                    id_empleador = %s,
                    calificacion_desde = %s,
                    calificacion_hasta = %s,
                    tiene_vinculo = %s
                WHERE id = %s
                )''', (
                self.titulo,
                self.descripcion,
                self.fecha_inicio,
                self.fecha_cierre,
                self.estado,
                self.experiencia,
                self.salario,
                self.id_empleador,
                self.calificacion_desde,
                self.calificacion_hasta,
                self.tiene_vinculo,
                id
            ))
            bd.connection.commit()
            cursor.close()
            print('Anuncio Actualizado')
        except:
            print("Error al actualizar el anuncio")


def getAnuncioByID(bd, id):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                titulo,
                descripcion,
                fecha_inicio,
                fecha_cierre,
                estado,
                experiencia,
                pago_hora,
                id_empleador,
                calificacion_desde,
                calificacion_hasta,
                tiene_vinculo
            FROM anuncio WHERE id = %s''', (id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        anuncio = Anuncio(
            retorno['id'],
            retorno['titulo'],
            retorno['descripcion'],
            retorno['fecha_inicio'],
            retorno['fecha_cierre'],
            retorno['estado'],
            retorno['experiencia'],
            retorno['pago_hora'],
            retorno['id_empleador'],
            retorno['calificacion_desde'],
            retorno['calificacion_hasta'],
            retorno['tiene_vinculo'])
        return anuncio
    except:
        print("Error en getAnuncioByID")
