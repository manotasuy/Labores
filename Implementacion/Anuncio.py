
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
            print('Anuncio Creado')        
        except:
            print("Error en creación del anuncio")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")

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
                )''',(
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
            print('Anuncio Actualizado')        
        except:
            print("Error al actualizar el anuncio")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")