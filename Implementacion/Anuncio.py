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
        except Exception as e:
            print("Error en createAnuncio ", e)

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
        except Exception as e:
            print("Error en updateAnuncio ", e)


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
            FROM anuncio WHERE id = {}'''.format(id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        anuncio = Anuncio(
            retorno[0][0],
            retorno[0][1],
            retorno[0][2],
            retorno[0][3],
            retorno[0][4],
            retorno[0][5],
            retorno[0][6],
            retorno[0][7],
            retorno[0][8],
            retorno[0][9],
            retorno[0][10],
            retorno[0][11])
        return anuncio
    except Exception as e:
        print("Error en getAnuncioByID ", e)
