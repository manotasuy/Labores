
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
        cursor = bd.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM empleador WHERE activo = 0')
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        cant = int(retorno[0][0])
        return cant
    except Exception as e:
        print("Error en cuentasCerradasEmpleadores ", e)


def cuentasCerradasEmpleados(bd):
    try:
        cursor = bd.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM empleado WHERE activo = 0')
        retorno = cursor.fetchall()
        bd.connection.commit()
        cursor.close()
        cant = int(retorno[0][0])
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


def getDatosAdmin(bd):
    datos = dict()
    datos ['ctasEmpleadores'] = getCantCuentasRegistradasEmpleadores(bd)
    datos ['ctasEmpleados'] = getCantCuentasRegistradasEmpleados(bd)
    datos['cantAnuncios'] = ofertasPublicadas(bd)
    datos['cantPostulaciones'] = postulacionesRegistradas(bd)
    datos['promCalificEmpleadores'] = promedioCalificacionesEmpleadores(bd)
    datos['promCalificEmpleados'] = promedioCalificacionesEmpleados(bd)
    datos['ctasCerradasEmpleadores'] = cuentasCerradasEmpleadores(bd)
    datos['ctasCerradasEmpleados'] = cuentasCerradasEmpleados(bd)
    datos['cantVinculos'] = vinculosEstablecidos(bd)
    return datos