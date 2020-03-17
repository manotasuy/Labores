
def getCantCuentasRegistradasEmpleadores(bd):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM empleador')
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        cant = int(retorno[0][0])
        return cant
    except Exception as e:
        print("Error en getCantCuentasRegistradasEmpleadores ", e)


def getCantCuentasRegistradasEmpleados(bd):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM empleado')
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        cant = int(retorno[0][0])
        return cant
    except Exception as e:
        print("Error en getCantCuentasRegistradasEmpleados ", e)


def ofertasPublicadas(bd):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM anuncio')
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        cant = int(retorno[0][0])
        return cant
    except Exception as e:
        print("Error en ofertasPublicadas ", e)


def postulacionesRegistradas(bd):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM postulacion')
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        cant = int(retorno[0][0])
        return cant
    except Exception as e:
        print("Error en postulacionesRegistradas ", e)


def promedioCalificacionesEmpleadores(bd):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('SELECT AVG(promedio_calificacion) FROM empleador')
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        cant = int(retorno[0][0])
        return cant
    except Exception as e:
        print("Error en promedioCalificacionesEmpleadores ", e)


def promedioCalificacionesEmpleados(bd):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('SELECT AVG(promedio_calificacion) FROM empleado')
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        cant = int(retorno[0][0])
        return cant
    except Exception as e:
        print("Error en getCantCuentasRegistradasEmpleados ", e)


def cuentasCerradasEmpleadores(bd):
    try:
        #cursor = bd.connection.cursor()
        # hay que agregar una columna de estado 0:Inactivo, 1:Activo
        #cursor.execute('SELECT COUNT(*) FROM empleador WHERE estado = 0')
        #retorno = cursor.fetchall()
        # bd.connection.commit()
        # cursor.close()
        #cant = int(retorno[0][0])
        cant = 0
        return cant
    except Exception as e:
        print("Error en cuentasCerradasEmpleadores ", e)


def cuentasCerradasEmpleados(bd):
    try:
        #cursor = bd.connection.cursor()
        # hay que agregar una columna de estado 0:Inactivo, 1:Activo
        #cursor.execute('SELECT COUNT(*) FROM empleado WHERE estado = 0')
        #retorno = cursor.fetchall()
        # bd.connection.commit()
        # cursor.close()
        #cant = int(retorno[0][0])
        cant = 0
        return cant
    except Exception as e:
        print("Error en cuentasCerradasEmpleados ", e)


def vinculosEstablecidos(bd):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM vinculo')
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        cant = int(retorno[0][0])
        return cant
    except Exception as e:
        print("Error en vinculosEstablecidos ", e)
