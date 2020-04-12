import os
from flask import url_for
from datetime import datetime
from Implementacion.Conexion import getCarpetaCargaImagenes
from Implementacion.Usuario import getUsuarioByID
from Implementacion.Anuncio import Anuncio
from Implementacion.Usuario import Usuario
from Implementacion.DTOIndividuoCalificacion import DTOIndividuoCalificacion


class Empleador:

    def __init__(self, pId=0, pCedula='', pNombre='', pApellido='', pNacimiento='', pGenero='', pDom='', pNacional='', pEmail='', pTel='', pBps='', pFoto='', pCalif='', pUsuario=None):
        self.id = pId
        self.cedula = pCedula
        self.nombre = pNombre
        self.apellido = pApellido
        self.nacimiento = pNacimiento
        self.genero = pGenero
        self.domicilio = pDom
        self.nacionalidad = pNacional
        self.email = pEmail
        self.telefono = pTel
        self.registroBps = pBps
        self.foto = pFoto
        self.promedioCalificacion = pCalif
        self.usuario: Usuario = pUsuario

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Id: {}, Cédula: {}, Nombre: {}, Apellido: {}, Nacimiento: {}, Genero: {}, Domicilio: {}, Nacionalidad: {}, Email: {}, Telefono: {}, Foto: {}, Usuario: {}'.format(self.id, self.cedula, self.nombre, self.apellido, self.nacimiento, self.genero, self.domicilio, self.nacionalidad, self.email, self.telefono, self.foto, self.usuario.id)

    def crearEmpleador(self, bd):
        try:
            if self.foto is None or self.foto == '':
                self.foto = 'images/Perfiles/NoImage.png'

            cursor = bd.connection.cursor()
            cursor.execute('''
                INSERT INTO empleador
                    (
                        cedula,
                        nombre,
                        apellido,
                        fecha_nacimiento,
                        genero,
                        domicilio,
                        nacionalidad,
                        email,
                        telefono,
                        registro_bps,
                        foto,
                        promedio_calificacion,
                        id_usuario
                    )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                           (
                               self.cedula,
                               self.nombre,
                               self.apellido,
                               self.nacimiento,
                               self.genero,
                               self.domicilio,
                               self.nacionalidad,
                               self.email,
                               self.telefono,
                               self.registroBps,
                               self.foto,
                               self.promedioCalificacion,
                               self.usuario.id
                           ))
            bd.connection.commit()
            cursor.close()
            print('Empleador Creado')
        except Exception as e:
            print("Error en crearEmpleador ", e)

    def calificarEmpleador(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE empleador SET
                    promedio_calificacion = %s
                WHERE id = %s''',
                           (
                               self.promedioCalificacion,
                               self.id
                           ))
            bd.connection.commit()
            cursor.close()
            print('Empleador calificado')
        except Exception as e:
            print("Error en calificación de empleador ", e)

    def modificarEmpleador(self, bd):
        try:
            if self.foto is None or self.foto == '':
                self.foto = 'images/Perfiles/NoImage.png'

            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE empleador SET
                    nombre = %s,
                    apellido = %s,
                    fecha_nacimiento = %s,
                    genero = %s,
                    domicilio = %s,
                    nacionalidad = %s,
                    email = %s,
                    telefono = %s,
                    registro_bps = %s,
                    foto = %s
                WHERE id = %s''',
                           (
                               self.nombre,
                               self.apellido,
                               self.nacimiento,
                               self.genero,
                               self.domicilio,
                               self.nacionalidad,
                               self.email,
                               self.telefono,
                               self.registroBps,
                               self.foto,
                               self.id
                           ))
            bd.connection.commit()
            cursor.close()
            print('Empleador modificado')
        except Exception as e:
            print("Error en actualizarEmpleador ", e)

    def listarEmpleadores(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            cursor.close()
            print('función para listar empleadores')
        except Exception as e:
            print("Error en listarEmpleadores ", e)

    def crearAnuncio(
            self,
            bd,
            Titulo,
            Descripcion,
            FechaInicio,
            FechaCierre,
            Estado,
            Experiencia,
            Pago_hora,
            CalDesde,
            CalHasta,
            TieneVinculo,
            Disponibilidad,
            Hogar,
            Oficina,
            Cocinar,
            LimpBanios,
            LimpCocinas,
            LimpDormitorios,
            CuidadoNinios,
            CuidadoBebes,
            CuidadoAdultos,
            CuidadoMascotas):
        try:
            newAnuncio = Anuncio(
                0,
                Titulo,
                Descripcion,
                FechaInicio,
                FechaCierre,
                Estado,
                Experiencia,
                Pago_hora,
                self,
                CalDesde,
                CalHasta,
                TieneVinculo,
                Disponibilidad,
                None,
                Hogar,
                Oficina,
                Cocinar,
                LimpBanios,
                LimpCocinas,
                LimpDormitorios,
                CuidadoNinios,
                CuidadoBebes,
                CuidadoAdultos,
                CuidadoMascotas)
            newAnuncio.createAnuncio(bd)
            print('El empleador generó el anuncio')
        except Exception as e:
            print("Error en crearAnuncio ", e)

    def actualizarAnuncio(
            self,
            bd,
            elAnuncio,
            Titulo,
            Descripcion,
            FechaInicio,
            FechaCierre,
            Estado,
            Experiencia,
            Pago_hora,
            CalEmpleado,
            CalEmpleador,
            TieneVinculo,
            Disponibilidad,
            Hogar,
            Oficina,
            Cocinar,
            LimpBanios,
            LimpCocinas,
            LimpDormitorios,
            CuidadoNinios,
            CuidadoBebes,
            CuidadoAdultos,
            CuidadoMascotas):
        try:
            newAnuncio = Anuncio(
                elAnuncio.id,
                Titulo,
                Descripcion,
                FechaInicio,
                FechaCierre,
                Estado,
                Experiencia,
                Pago_hora,
                self,
                CalEmpleado,
                CalEmpleador,
                TieneVinculo,
                Disponibilidad,
                None,
                Hogar,
                Oficina,
                Cocinar,
                LimpBanios,
                LimpCocinas,
                LimpDormitorios,
                CuidadoNinios,
                CuidadoBebes,
                CuidadoAdultos,
                CuidadoMascotas
            )
            newAnuncio.updateAnuncio(bd)
            print('El empleador actualizó el anuncio')
        except Exception as e:
            print("Error en actualizarAnuncio ", e)

    def borrarAnuncio(
            self,
            bd,
            elAnuncio,
            Titulo,
            Descripcion,
            FechaInicio,
            FechaCierre,
            Estado,
            Experiencia,
            Pago_hora,
            CalEmpleado,
            CalEmpleador,
            TieneVinculo,
            Disponibilidad,
            Hogar,
            Oficina,
            Cocinar,
            LimpBanios,
            LimpCocinas,
            LimpDormitorios,
            CuidadoNinios,
            CuidadoBebes,
            CuidadoAdultos,
            CuidadoMascotas):
        try:
            delAnuncio = Anuncio(
                elAnuncio.id,
                Titulo,
                Descripcion,
                FechaInicio,
                FechaCierre,
                Estado,
                Experiencia,
                Pago_hora,
                self,
                CalEmpleado,
                CalEmpleador,
                TieneVinculo,
                Disponibilidad,
                None,
                Hogar,
                Oficina,
                Cocinar,
                LimpBanios,
                LimpCocinas,
                LimpDormitorios,
                CuidadoNinios,
                CuidadoBebes,
                CuidadoAdultos,
                CuidadoMascotas
            )
            delAnuncio.deleteAnuncio(bd)
        except Exception as e:
            print("Error en borrarAnuncio ", e)

    def listarMisAnuncios(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute(
                'SELECT * FROM anuncio WHERE id_empleador = {}'.format(self.id))
            data = cursor.fetchall()
            cursor.close()
            return data
        except Exception as e:
            print("Error en listarMisAnuncios ", e)

    def realizarBusqueda(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            cursor.close()
            print('función para realizar búsqueda')
        except Exception as e:
            print("Error en realizarBusqueda ", e)

    def candidatosDeMiAnuncio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            cursor.close()
            print('función para listar candidatos de mi anuncio')
        except Exception as e:
            print("Error en candidatosDeMiAnuncio ", e)

    def establecerContacto(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            cursor.close()
            print('función para establecer contacto')
        except Exception as e:
            print("Error en establecerContacto ", e)


def getEmpleadorByID(bd, id):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                cedula,
                nombre,
                apellido,
                fecha_nacimiento,
                genero,
                domicilio,
                nacionalidad,
                email,
                telefono,
                registro_bps,
                foto,
                promedio_calificacion,
                id_usuario
            FROM empleador WHERE id = {}'''.format(id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()

        # Si no se puede cargar la foto guardada en la base cargo la imagen default
        foto = retorno[0][11]
        if foto is None or foto == '':
            foto = 'SinImagen'
        rutaFisica = '.' + url_for('static', filename = foto)
        if not os.path.exists(rutaFisica):
            foto = os.path.join(getCarpetaCargaImagenes(), 'NoImage.png')

        empleador = Empleador(
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
            retorno[0][11],
            retorno[0][12],
            getUsuarioByID(bd, retorno[0][13]),)
        # print('Empleador: ', empleador)
        return empleador
    except Exception as e:
        print("Error en getEmpleadorByID ", e)


def getEmpleadorByUsuarioID(bd, idUsuario):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
            e.id,
            e.cedula,
            e.nombre,
            e.apellido,
            e.fecha_nacimiento,
            e.genero,
            e.domicilio,
            e.nacionalidad,
            e.email,
            e.telefono,
            e.registro_bps,
            e.foto,
            e.promedio_calificacion,
            e.id_usuario
            FROM empleador e INNER JOIN usuario u ON e.id_usuario = u.id WHERE u.id = {}'''.format(idUsuario))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        empleador = Empleador(
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
            retorno[0][11],
            retorno[0][12],
            getUsuarioByID(bd, retorno[0][13]),)
        return empleador
    except Exception as e:
        print("Error en getEmpleadorByUsuarioID ", e)


def getRankingPorCalificacionEmpleadores(bd, top):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
                SELECT e.id,
                    e.nombre,
                    e.apellido,
                    ROUND(e.promedio_calificacion, 2),
                    e.foto,
                    COUNT(v.id) cant_vinculos,
                    COUNT(DISTINCT v.id_empleado) cant_calificantes
                FROM empleador e INNER JOIN vinculo v ON e.id = v.id_empleador WHERE e.promedio_calificacion > 0
                GROUP BY e.id
                ORDER BY promedio_calificacion DESC, cant_vinculos DESC, cant_calificantes DESC LIMIT {}'''.format(top))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        # desde el retorno debo generar los objetos DTOIndividuoCalificacion
        ranking = list()
        for tuplaRanking in retorno:
            dtoIndividuoCalificacion = DTOIndividuoCalificacion(tuplaRanking[0], tuplaRanking[1], tuplaRanking[2], tuplaRanking[3], 
            tuplaRanking[4], 0, tuplaRanking[5], tuplaRanking[6], 'Empleador')
            ranking.append(dtoIndividuoCalificacion)
        return ranking
    except Exception as e:
        print("Error en getRankingPorCalificacionEmpleadores ", e)