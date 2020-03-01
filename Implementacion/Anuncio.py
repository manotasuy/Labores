
class Anuncio:

    def __init__(self, pTitulo, pDescripcion, pFechaInicio, pFechaCierre, pEstado, pExperiencia, pSalario, pIdEmpleador, pCalEmpleado, pCalEmpleador, pTieneVicnulo):
        self.titulo = pTitulo
        self.descripcion = pDescripcion
        self.fecha_inicio = pFechaInicio
        self.fecha_cierre = pFechaCierre
        self.estado = pEstado
        self.experiencia = pExperiencia
        self.salario = pSalario
        self.id_empleador = pIdEmpleador
        self.calificacion_empleado = pCalEmpleado
        self.calificacion_empleador = pCalEmpleador
        self.tiene_vinculo = pTieneVicnulo

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
                        calificacion_empleado,
                        calificacion_empleador,
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
                        self.calificacion_empleado,
                        self.calificacion_empleador,
                        self.tiene_vinculo
                    ))
            mysql.connection.commit()
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
                    calificacion_empleado = %s,
                    calificacion_empleador = %s,
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
                        self.calificacion_empleado,
                        self.calificacion_empleador,
                        self.tiene_vinculo,
                        id                        
                        ))
            mysql.connection.commit()
            print('Anuncio Actualizado')        
        except:
            print("Error al actualizar el anuncio")