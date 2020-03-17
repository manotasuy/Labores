from Implementacion.Empleado import getEmpleadoByID


class Referencia:
    def __init__(self, pId=None, pEmpleado=None, pNombre=None, pTelefono=None, pFechaDesde=None, pFechaHasta=None):
        self.id = pId
        self.empleado = pEmpleado
        self.nombre = pNombre
        self.telefono = pTelefono
        self.fechaDesde = pFechaDesde
        self.fechaHasta = pFechaHasta

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return 'Nombre empleado: {}, Nombre Referencia: {}, Telefono: {}, Fecha desde: {}, Fecha hasta: {}'.format(self.empleado.id, self.nombre, self.telefono, self.fechaDesde, self.fechaHasta)

    def crearReferencia(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                INSERT INTO referencia 
                    (
                        id_empleado,
                        nombre,
                        telefono,
                        fecha_desde,
                        fecha_hasta
                    )
                VALUES (%s,%s,%s,%s,%s)''',
                           (
                               self.empleado.id,
                               self.nombre,
                               self.telefono,
                               self.fechaDesde,
                               self.fechaHasta
                           ))
            bd.connection.commit()
            cursor.close()
            print('Referencia Creada')
        except Exception as e:
            print("Error en crearReferencia ", e)

    def borrarReferencia(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                DELETE FROM referencia WHERE id = {}
                '''.format(self.id))
            bd.connection.commit()
            cursor.close()
            print('Referencia Borrada')
        except Exception as e:
            print("Error en borrarReferencia ", e)

    def actualizarReferencia(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('''
                UPDATE referencia SET
                    nombre = %s,
                    telefono = %s,
                    fecha_desde = %s,
                    fecha_hasta = %s
                WHERE id = %s''',
                           (
                               self.nombre,
                               self.telefono,
                               self.fechaDesde,
                               self.fechaHasta,
                               self.id
                           ))

            bd.connection.commit()
            cursor.close()
            print('Referencia Actualizada')
        except Exception as e:
            print("Error en actualizarReferencia ", e)


def getReferenciaByID(bd, id):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
            SELECT
                id,
                id_empleado,
                nombre,
                telefono,
                fecha_desde,
                fecha_hasta
            FROM referencia WHERE id = {}'''.format(id))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        referencia = Referencia(
            retorno[0][0],
            getEmpleadoByID(bd, retorno[0][1]),
            retorno[0][4],
            retorno[0][5],
            retorno[0][6],
            retorno[0][7]
        )
        return referencia
    except Exception as e:
        print("Error en getReferenciaByID ", e)


def getReferenciasEmpleado(bd, idEmpleado):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('''
                SELECT
                    id,
                    nombre,
                    telefono,
                    fecha_desde,
                    fecha_hasta
                FROM referencia WHERE id_empleado = {}'''.format(idEmpleado))
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        # desde el retono debo generar los objetos Referencia
        referencias = list()
        for tuplaReferencia in retorno:
            referencia = Referencia(tuplaReferencia[0], getEmpleadoByID(bd, idEmpleado), tuplaReferencia[1],
                                    tuplaReferencia[2], tuplaReferencia[3], tuplaReferencia[4])
            referencias.append(referencia)
        return referencias
    except Exception as e:
        print("Error en getReferenciasEmpleado ", e)
