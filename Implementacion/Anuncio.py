from datetime import datetime
from Implementacion.Tarea import Tarea
from Implementacion.Disponibilidad import Disponibilidad


class Anuncio:

    def __init__(
        self, 
        pTitulo, 
        pDescripcion, 
        pFechaInicio, 
        pFechaCierre, 
        pEstado, 
        pExperiencia, 
        pPago_hora, 
        pIdEmpleador, 
        pCalDesde, 
        pCalHasta, 
        pTieneVinculo,
        pDisponibilidad,
        pHogar,
        pOficina,
        pCocinar,
        pLimpBanios,
        pLimpCocinas,
        pLimpDormitorios,
        pCuidadoNinios,
        pCuidadoBebes,
        pCuidadoAdultos,
        pCuidadoMascotas
        ):

        self.titulo = pTitulo
        self.descripcion = pDescripcion
        self.fecha_inicio = pFechaInicio
        self.fecha_cierre = pFechaCierre
        self.estado = pEstado
        self.experiencia = pExperiencia
        self.pago_hora = pPago_hora
        self.id_empleador = pIdEmpleador
        self.calificacion_desde = pCalDesde
        self.calificacion_hasta = pCalHasta
        self.tiene_vinculo = pTieneVinculo
        self.disponibilidad = pDisponibilidad
        self.hogar = pHogar
        self.oficina = pOficina
        self.cocinar = pCocinar
        self.limp_banios = pLimpBanios
        self.limp_cocinas = pLimpCocinas
        self.limp_dormitorios = pLimpDormitorios
        self.cuidado_ninios = pCuidadoNinios
        self.cuidado_bebes = pCuidadoBebes
        self.cuidado_adultos = pCuidadoAdultos
        self.cuidado_mascotas = pCuidadoMascotas

    def __str__(self):
        return 'Título: {}, Empleador {}, Vinculo {}'.format(self.titulo, self.id_empleador, self.tiene_vinculo)

    def __getitem__(self, item):
        return self.__dict__[item]

    def createAnuncio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                INSERT INTO anuncio 
                    (
                        titulo,
                        descripcion,
                        fecha_inicio,
                        estado,
                        experiencia,
                        pago_hora,
                        id_empleador,
                        calificacion_desde,
                        calificacion_hasta,
                        tiene_vinculo
                    )
                VALUES ("{}","{}", "{}","{}","{}","{}","{}","{}","{}","{}")'''.format(
                               self.titulo,
                               self.descripcion,
                               datetime.now().date(),
                               self.estado,
                               self.experiencia,
                               self.pago_hora,
                               self.id_empleador,
                               self.calificacion_desde,
                               self.calificacion_hasta,
                               self.tiene_vinculo
                           ))
            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            cursor.execute('''SELECT MAX(id) FROM anuncio WHERE id_empleador = {}'''.format(self.id_empleador))
            retorno = cursor.fetchall()
            idAnuncio = retorno[0][0]
            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            if self.disponibilidad == 'hora':
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_disponibilidad
                        (
                            id_anuncio,
                            id_disponibilidad
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                1
                            ))
                bd.connection.commit()
                cursor.close()
            elif self.disponibilidad == 'jornada':
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_disponibilidad
                        (
                            id_anuncio,
                            id_disponibilidad
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                2
                            ))
                bd.connection.commit()
                cursor.close()                            
            elif self.disponibilidad == 'tarea':
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_disponibilidad
                        (
                            id_anuncio,
                            id_disponibilidad
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                3
                            ))
                bd.connection.commit()
                cursor.close()                            
            elif self.disponibilidad == 'mes':
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_disponibilidad
                        (
                            id_anuncio,
                            id_disponibilidad
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                4
                            ))
                bd.connection.commit()
                cursor.close()                            
            if self.hogar:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                1
                            ))
                bd.connection.commit()
                cursor.close()
            if self.oficina:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                2
                            ))
                bd.connection.commit()
                cursor.close()
            if self.cocinar:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                3
                            ))
                bd.connection.commit()
                cursor.close()
            if self.limp_banios:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                4
                            ))
                bd.connection.commit()
                cursor.close()        
            if self.limp_cocinas:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                5
                            ))
                bd.connection.commit()
                cursor.close()         
            if self.limp_dormitorios:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                6
                            ))
                bd.connection.commit()
                cursor.close()           
            if self.cuidado_ninios:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                7
                            ))
                bd.connection.commit()
                cursor.close()    
            if self.cuidado_bebes:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                8
                            ))
                bd.connection.commit()
                cursor.close()
            if self.cuidado_adultos:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                9
                            ))
                bd.connection.commit()
                cursor.close()
            if self.cuidado_mascotas:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                10
                            ))
                bd.connection.commit()
                cursor.close()                
            print('Anuncio Creado')
        except Exception as e:
            print("Error en createAnuncio ", e)

    def deleteAnuncio(self, bd, idAnuncio):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM anuncio WHERE id = "{}"
                '''.format(idAnuncio))
            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM anuncio_disponibilidad WHERE id_anuncio = "{}"
                '''.format(idAnuncio))
            bd.connection.commit()
            cursor.close()       
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM anuncio_tareas WHERE id_anuncio = "{}"
                '''.format(idAnuncio))
            bd.connection.commit()
            cursor.close()                 
            print('Anuncio Borrado')
        except Exception as e:
            print("Error en deleteAnuncio ", e)

    def updateAnuncio(self, bd, idAnuncio):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE anuncio SET
                    titulo = "{}",
                    descripcion = "{}",
                    fecha_cierre = "{}",
                    estado = "{}",
                    experiencia = "{}",
                    pago_hora = "{}",
                    calificacion_desde = "{}",
                    calificacion_hasta = "{}",
                    tiene_vinculo = "{}"
                WHERE id = "{}"
                '''.format(
                self.titulo,
                self.descripcion,
                self.fecha_cierre,
                self.estado,
                self.experiencia,
                self.pago_hora,
                self.calificacion_desde,
                self.calificacion_hasta,
                self.tiene_vinculo,
                idAnuncio
            ))
            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM anuncio_disponibilidad WHERE id_anuncio = "{}"
                '''.format(idAnuncio))
            bd.connection.commit()
            cursor.close()       
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM anuncio_tareas WHERE id_anuncio = "{}"
                '''.format(idAnuncio))
            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            if self.disponibilidad == 'hora':
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_disponibilidad
                        (
                            id_anuncio,
                            id_disponibilidad
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                1
                            ))
                bd.connection.commit()
                cursor.close()
            elif self.disponibilidad == 'jornada':
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_disponibilidad
                        (
                            id_anuncio,
                            id_disponibilidad
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                2
                            ))
                bd.connection.commit()
                cursor.close()                            
            elif self.disponibilidad == 'tarea':
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_disponibilidad
                        (
                            id_anuncio,
                            id_disponibilidad
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                3
                            ))
                bd.connection.commit()
                cursor.close()                            
            elif self.disponibilidad == 'mes':
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_disponibilidad
                        (
                            id_anuncio,
                            id_disponibilidad
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                4
                            ))
                bd.connection.commit()
                cursor.close()                            
            if self.hogar:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                1
                            ))
                bd.connection.commit()
                cursor.close()
            if self.oficina:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                2
                            ))
                bd.connection.commit()
                cursor.close()
            if self.cocinar:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                3
                            ))
                bd.connection.commit()
                cursor.close()
            if self.limp_banios:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                4
                            ))
                bd.connection.commit()
                cursor.close()        
            if self.limp_cocinas:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                5
                            ))
                bd.connection.commit()
                cursor.close()         
            if self.limp_dormitorios:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                6
                            ))
                bd.connection.commit()
                cursor.close()           
            if self.cuidado_ninios:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                7
                            ))
                bd.connection.commit()
                cursor.close()    
            if self.cuidado_bebes:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                8
                            ))
                bd.connection.commit()
                cursor.close()
            if self.cuidado_adultos:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                9
                            ))
                bd.connection.commit()
                cursor.close()
            if self.cuidado_mascotas:
                cursor = bd.connection.cursor()
                cursor.execute('''
                    INSERT INTO anuncio_tarea
                        (
                            id_anuncio,
                            id_tarea
                        )
                    VALUES ("{}","{}")'''.format(
                                idAnuncio,
                                10
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
        retorno_anuncio = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT id_tarea FROM anuncio_tarea WHERE id_anuncio = {}'''.format(id))
        retorno_tarea = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT id_disponibilidad FROM anuncio_disponibilidad WHERE id_anuncio = {}'''.format(id))
        retorno_disponibilidad = cursor.fetchall()
        bd.connection.commit()
        cursor.close()    
        if 1 in retorno_tarea:
            bd_hogar = True
        else:
            bd_hogar = False
        if 2 in retorno_tarea:
            bd_oficina = True
        else:
            bd_oficina = False
        if 3 in retorno_tarea:
            bd_cocinar = True
        else:
            bd_cocinar = False
        if 4 in retorno_tarea:
            bd_limp_banios = True
        else:
            bd_limp_banios = False
        if 5 in retorno_tarea:
            bd_limp_cocinas = True
        else:
            bd_limp_cocinas = False 
        if 6 in retorno_tarea:
            bd_limp_dorm = True
        else:
            bd_limp_dorm = False     
        if 7 in retorno_tarea:
            bd_cuid_ninios = True
        else:
            bd_cuid_ninios = False 
        if 8 in retorno_tarea:
            bd_cuid_bebes = True
        else:
            bd_cuid_bebes = False
        if 9 in retorno_tarea:
            bd_cuid_adult = True
        else:
            bd_cuid_adult = False  
        if 10 in retorno_tarea:
            bd_cuid_pet = True
        else:
            bd_cuid_pet = False                                                                             
        anuncio = Anuncio(
            retorno_anuncio[0][1],
            retorno_anuncio[0][2],
            retorno_anuncio[0][3],
            retorno_anuncio[0][4],
            retorno_anuncio[0][5],
            retorno_anuncio[0][6],
            retorno_anuncio[0][7],
            retorno_anuncio[0][8],
            retorno_anuncio[0][9],
            retorno_anuncio[0][10],
            retorno_anuncio[0][11],
            retorno_disponibilidad[0][0],
            bd_hogar,
            bd_oficina,
            bd_cocinar,
            bd_limp_banios,
            bd_limp_cocinas,
            bd_limp_dorm,
            bd_cuid_ninios,
            bd_cuid_bebes,
            bd_cuid_adult,
            bd_cuid_pet
            )
        return anuncio
    except Exception as e:
        print("Error en getAnuncioByID ", e)
