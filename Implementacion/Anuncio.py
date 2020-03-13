from datetime import datetime
# si establezco from modulo import clase obtengo referencia ciclíca [Inicio]
from Implementacion import Empleador
# si establezco from modulo import clase obtengo referencia ciclíca [Fin]
from Implementacion.Tarea import Tarea
from Implementacion.Disponibilidad import Disponibilidad


class Anuncio:

    def __init__(
        self,
        pId,
        pTitulo,
        pDescripcion,
        pFechaInicio,
        pFechaCierre,
        pEstado,
        pExperiencia,
        pPago_hora,
        pEmpleador,
        pCalDesde,
        pCalHasta,
        pTieneVinculo,
        pDisponibilidad,
        pTareas,
        # Deberían sacarse estos atributos y cargarlos dinámicamente desde la bd [Inicio]
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
        # Deberían sacarse estos atributos y cargarlos dinámicamente desde la bd [Fin]
    ):
        self.id = pId
        self.titulo = pTitulo
        self.descripcion = pDescripcion
        self.fecha_inicio = pFechaInicio
        self.fecha_cierre = pFechaCierre
        self.estado = pEstado
        self.experiencia = pExperiencia
        self.pago_hora = pPago_hora
        self.empleador: Empleador = pEmpleador
        self.calificacion_desde = pCalDesde
        self.calificacion_hasta = pCalHasta
        self.tiene_vinculo = pTieneVinculo
        self.disponibilidad = pDisponibilidad
        self.tareas = pTareas
        # Deberían sacarse estos atributos y cargarlos dinámicamente desde la bd [Inicio]
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
        # Deberían sacarse estos atributos y cargarlos dinámicamente desde la bd [Fin]

    def __str__(self):
        return 'Id: {}, Título: {}, Empleador: {}, Vinculo: {}'.format(self.id, self.titulo, self.empleador.id, self.tiene_vinculo)

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
						fecha_cierre,
						estado,
                        experiencia,
                        pago_hora,
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
                               self.pago_hora,
                               self.empleador.id,
                               self.calificacion_desde,
                               self.calificacion_hasta,
                               self.tiene_vinculo
                           ))
            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            cursor.execute('''SELECT MAX(id) FROM anuncio WHERE id_empleador = {}'''.format(
                self.empleador.id))
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
                    VALUES ({},{})'''.format(
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
                    VALUES ({},{})'''.format(
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
                    VALUES ({},{})'''.format(
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
                    VALUES ({},{})'''.format(
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
                    VALUES ({},{})'''.format(
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
                    VALUES ({},{})'''.format(
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
                    VALUES ({},{})'''.format(
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
                    VALUES ({},{})'''.format(
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
                    VALUES ({},{})'''.format(
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
                    VALUES ({},{})'''.format(
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
                    VALUES ({},{})'''.format(
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
                    VALUES ({},{})'''.format(
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
                    VALUES ({},{})'''.format(
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
                    VALUES ({},{})'''.format(
                    idAnuncio,
                    10
                ))
                bd.connection.commit()
                cursor.close()
            print('Anuncio Creado')
        except Exception as e:
            print("Error en createAnuncio ", e)

    def deleteAnuncio(self, bd):
        try:

            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM anuncio_disponibilidad WHERE id_anuncio = {}
                '''.format(self.id))
            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM anuncio_tarea WHERE id_anuncio = {}
                '''.format(self.id))
            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM anuncio WHERE id = {}
                '''.format(self.id))
            bd.connection.commit()
            cursor.close()
            print('Anuncio Borrado')
        except Exception as e:
            print("Error en deleteAnuncio ", e)

    def updateAnuncio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE anuncio SET
                    titulo = %s,
                    descripcion = %s,
                    fecha_cierre = %s,
                    estado = %s,
                    experiencia = %s,
                    pago_hora = %s,
                    calificacion_desde = %s,
                    calificacion_hasta = %s,
                    tiene_vinculo = %s
                WHERE id = %s''',
                           (
                               self.titulo,
                               self.descripcion,
                               self.fecha_cierre,
                               self.estado,
                               self.experiencia,
                               self.pago_hora,
                               self.calificacion_desde,
                               self.calificacion_hasta,
                               self.tiene_vinculo,
                               self.id
                           ))

            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM anuncio_disponibilidad WHERE id_anuncio = {}
                '''.format(self.id))
            bd.connection.commit()
            cursor.close()
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM anuncio_tarea WHERE id_anuncio = {}
                '''.format(self.id))
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
                    VALUES ({},{})'''.format(
                    self.id,
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
                    VALUES ({},{})'''.format(
                    self.id,
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
                    VALUES ({},{})'''.format(
                    self.id,
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
                    VALUES ({},{})'''.format(
                    self.id,
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
                    VALUES ({},{})'''.format(
                    self.id,
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
                    VALUES ({},{})'''.format(
                    self.id,
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
                    VALUES ({},{})'''.format(
                    self.id,
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
                    VALUES ({},{})'''.format(
                    self.id,
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
                    VALUES ({},{})'''.format(
                    self.id,
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
                    VALUES ({},{})'''.format(
                    self.id,
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
                    VALUES ({},{})'''.format(
                    self.id,
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
                    VALUES ({},{})'''.format(
                    self.id,
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
                    VALUES ({},{})'''.format(
                    self.id,
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
                    VALUES ({},{})'''.format(
                    self.id,
                    10
                ))
                bd.connection.commit()
                cursor.close()
            print('Anuncio Actualizado')
        except Exception as e:
            print("Error en updateAnuncio ", e)

    def setEstadoAnuncio(self, bd, estado):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE anuncio SET
                    estado = %s
                WHERE id = %s''',
                           (
                               estado,
                               self.id
                           ))
            bd.connection.commit()
            cursor.close()
            print('Estado del Anuncio actualizado')
        except Exception as e:
            print("Error en setEstadoAnuncio ", e)


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
        if (1,) in retorno_tarea:
            bd_hogar = True
        else:
            bd_hogar = False
        if (2,) in retorno_tarea:
            bd_oficina = True
        else:
            bd_oficina = False
        if (3,) in retorno_tarea:
            bd_cocinar = True
        else:
            bd_cocinar = False
        if (4,) in retorno_tarea:
            bd_limp_banios = True
        else:
            bd_limp_banios = False
        if (5,) in retorno_tarea:
            bd_limp_cocinas = True
        else:
            bd_limp_cocinas = False
        if (6,) in retorno_tarea:
            bd_limp_dorm = True
        else:
            bd_limp_dorm = False
        if (7,) in retorno_tarea:
            bd_cuid_ninios = True
        else:
            bd_cuid_ninios = False
        if (8,) in retorno_tarea:
            bd_cuid_bebes = True
        else:
            bd_cuid_bebes = False
        if (9,) in retorno_tarea:
            bd_cuid_adult = True
        else:
            bd_cuid_adult = False
        if (10,) in retorno_tarea:
            bd_cuid_pet = True
        else:
            bd_cuid_pet = False
        anuncio = Anuncio(
            retorno_anuncio[0][0],
            retorno_anuncio[0][1],
            retorno_anuncio[0][2],
            retorno_anuncio[0][3],
            retorno_anuncio[0][4],
            retorno_anuncio[0][5],
            retorno_anuncio[0][6],
            retorno_anuncio[0][7],
            Empleador.getEmpleadorByID(bd, retorno_anuncio[0][8]),
            retorno_anuncio[0][9],
            retorno_anuncio[0][10],
            retorno_anuncio[0][11],
            retorno_disponibilidad[0][0],
            None,
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


def getAllAnuncios(bd):
        cur = bd.connection.cursor()
        cur.execute('SELECT * FROM anuncio')
        retornoAnuncios = cur.fetchall()
        cur.close()
        return retornoAnuncios
