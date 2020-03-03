class Empleador:

    def __init__(self, pId, pCedula, pNombre, pApellido, pNacimiento, pGenero, pDom, pNacional, pEmail, pTel, pFoto, pUsuario):
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
        self.foto = pFoto
        self.usuario = pUsuario

    def __str__(self):
        return 'Id: {}, Cédula: {}, Nombre: {}, Apellido: {}, Nacimiento: {}, Genero: {}, Domicilio: {}, Nacionalidad: {}, Email: {}, Telefono: {}, Foto: {}, Usuario: {}'.format(self.id, self.cedula, self.nombre, self.apellido, self.nacimiento, self.genero, self.domicilio, self.nacionalidad, self.email, self.telefono, self.foto, self.usuario)

    def crearEmpleador(self, bd):
        try:
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
                        '',
                        '',
                        0,
                        self.usuario.id
                    ))
            bd.connection.commit()
            print('Empleador Creado')        
        except:
            print("Error en creación del empleador")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")

    def actualizarEmpleador(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            print('función para actualizar empleador')
        except:
            print("Error en actualizar el empleador")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")
    
    def listarEmpleadores(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            print('función para listar empleadores')
        except:
            print("Error al listar empleadores")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")


    def crearAnuncio(self, bd, Titulo, Descripcion, FechaInicio, FechaCierre, Estado, Experiencia, Salario, IdEmpleador, CalEmpleado, CalEmpleador, TieneVicnulo):
        try:
            newAnuncio = anuncio.Anuncio(Titulo, Descripcion, FechaInicio, FechaCierre, Estado, Experiencia, Salario, IdEmpleador, CalEmpleado, CalEmpleador, TieneVinculo)
            newAnuncio.createAnuncio
            print('El empleador mandó el anuncio')
        except:
            print("Error al crear anuncio")


    def listarMisAnuncios(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            print('función para listar mis anuncios')
        except:
            print("Error al listar mis anuncios")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")

    def realizarBusqueda(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            print('función para realizar búsqueda')
        except:
            print("Error al realizar búsqueda")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")

    def candidatosDeMiAnuncio(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            print('función para listar candidatos de mi anuncio')
        except:
            print("Error al listar candidatos de mi anuncio")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")

    def establecerContacto(self, bd):
        try:
            cursor = bd.connection.cursor()
            cursor.execute('...')
            bd.connection.commit()
            print('función para establecer contacto')
        except:
            print("Error al establecer contacto")
        finally:
            if (bd.connection.open):
                cursor.close()
                bd.connection.close()  
                print("MySQL connection is closed")


def prueba():
    print('Hola! soy el empleador')
