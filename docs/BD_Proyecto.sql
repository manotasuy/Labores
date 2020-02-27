-- *** CREACIÓN DE LA BASE LOCAL ***
-- CREATE SCHEMA IF NOT EXISTS bdLabores DEFAULT CHARACTER SET utf8mb4;
-- USE bdLabores;

-- *** Uso de base de datos remota en 'remotemysql.com' ***
USE LvP2Ka0CsK;

-- *** Borrado de tablas para regenerar la base ***

DROP TABLE IF EXISTS empleado_disponibilidad;
DROP TABLE IF EXISTS empleado_tarea;
DROP TABLE IF EXISTS anuncio_disponibilidad;
DROP TABLE IF EXISTS anuncio_tarea;
DROP TABLE IF EXISTS tarea;
DROP TABLE IF EXISTS disponibilidad;
DROP TABLE IF EXISTS referencia;
DROP TABLE IF EXISTS vinculo;
DROP TABLE IF EXISTS postulacion;
DROP TABLE IF EXISTS anuncio;
DROP TABLE IF EXISTS empleado;
DROP TABLE IF EXISTS empleador;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS tipo_usuario;

-- *** CREACIÓN DE LAS TABLAS ***

-- Tabla: Tipo de Usuario
CREATE TABLE IF NOT EXISTS tipo_usuario
(
	id int NOT NULL AUTO_INCREMENT,
	nombre VARCHAR(50) NOT NULL,
    CONSTRAINT PK_tipo_usuario PRIMARY KEY (id),
    CONSTRAINT UK_tipo_usuario UNIQUE (nombre)
);

-- Tabla: Usuario
CREATE TABLE IF NOT EXISTS usuario
(
	id int NOT NULL AUTO_INCREMENT,
	usuario VARCHAR(50) NULL,
	clave VARCHAR(50) NOT NULL,
	id_tipo int NOT NULL,
    CONSTRAINT PK_usuario PRIMARY KEY (id),
    CONSTRAINT UK_usuario UNIQUE (usuario),
    CONSTRAINT FK_usuario_tipo FOREIGN KEY (id_tipo) REFERENCES tipo_usuario(id)
);
CREATE INDEX IDXuser ON usuario (usuario);

-- Tabla: Empleador
CREATE TABLE IF NOT EXISTS empleador
(
	id int NOT NULL AUTO_INCREMENT,
    cedula VARCHAR(20) NOT NULL,
	nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE,
    genero bit, -- 0: Femenino, 1: Masculino
    domicilio VARCHAR(50),
    nacionalidad VARCHAR(50),
    email VARCHAR(50),
    telefono VARCHAR(20),
    registro_bps VARCHAR(20),
    id_usuario int NOT NULL,
    CONSTRAINT PK_empleador PRIMARY KEY (id),
    CONSTRAINT UK_empleador UNIQUE (cedula),
    CONSTRAINT FK_empleador_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);

-- Tabla: Empleado
CREATE TABLE IF NOT EXISTS empleado
(
	id int NOT NULL AUTO_INCREMENT,
    cedula VARCHAR(20) NOT NULL,
	nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE,
    genero bit, -- 0: Femenino, 1: Masculino
    domicilio VARCHAR(50),
    nacionalidad VARCHAR(50),
    email VARCHAR(50),
    telefono VARCHAR(20),
    experiencia_meses int,
    descripcion TEXT,
    id_usuario int NOT NULL,
    CONSTRAINT PK_empleador PRIMARY KEY (id),
    CONSTRAINT UK_empleador UNIQUE (cedula),
    CONSTRAINT FK_empleado_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);

-- Tabla: Anuncio
CREATE TABLE IF NOT EXISTS anuncio
(
	id int NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(50) NOT NULL,
	descripcion TEXT NULL,
    fecha_inicio date NOT NULL,
    fecha_cierre date NULL,
    estado bit NOT NULL, -- 0: Inactivo, 1: Activo
    experiencia boolean NOT NULL,
    salario int,
    id_empleador int NOT NULL,
    calificacion_empleado double NULL,
    calificacion_empleador double NULL,
    CONSTRAINT PK_anuncio PRIMARY KEY (id),
    CONSTRAINT FK_anuncio_empleador FOREIGN KEY (id_empleador) REFERENCES empleador(id)
);

-- Tabla: Postulación
CREATE TABLE IF NOT EXISTS postulacion
(
	id int NOT NULL AUTO_INCREMENT,
    id_empleado int NOT NULL,
    id_anuncio int NOT NULL,    
    fecha date,
    mensaje VARCHAR(50) NULL,
    CONSTRAINT PK_postulacion PRIMARY KEY (id),
    CONSTRAINT FK_postulacion_empleado FOREIGN KEY (id_empleado) REFERENCES empleado(id),
    CONSTRAINT FK_postulacion_anuncio FOREIGN KEY (id_anuncio) REFERENCES anuncio(id)
);

-- Tabla: Vínculo
CREATE TABLE IF NOT EXISTS vinculo
(
	id int NOT NULL AUTO_INCREMENT,
    id_empleado int NOT NULL,
    id_empleador int NOT NULL,
    id_anuncio int NOT NULL,
    fecha_inicio date,
    fecha_fin date,
    motivo_fin TEXT,
    descripcion VARCHAR(200),
    -- estado bit, -- 0: Inactivo, 1: Activo
    calificacion_empleado double,
    calificacion_empleador double,
    CONSTRAINT PK_vinculo PRIMARY KEY (id),
    CONSTRAINT FK_vinculo_empleado FOREIGN KEY (id_empleado) REFERENCES empleado(id),
    CONSTRAINT FK_vinculo_empleador FOREIGN KEY (id_empleador) REFERENCES empleador(id),
    CONSTRAINT FK_vinculo_anuncio FOREIGN KEY (id_anuncio) REFERENCES anuncio(id)
);

-- Tabla: Referencia
CREATE TABLE IF NOT EXISTS referencia
(
	id int NOT NULL AUTO_INCREMENT,
    id_empleado int NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL,    
    fecha_desde date NOT NULL,
    fecha_hasta date NULL,
    CONSTRAINT PK_referencia PRIMARY KEY (id),
    CONSTRAINT FK_referencia_empleado FOREIGN KEY (id_empleado) REFERENCES empleado(id)
);

-- Tabla: Disponibilidad
CREATE TABLE IF NOT EXISTS disponibilidad
(
	id int NOT NULL AUTO_INCREMENT,
    descripcion VARCHAR(50) NOT NULL,
    CONSTRAINT PK_disponibilidad PRIMARY KEY (id)
);

-- Tabla: Tarea
CREATE TABLE IF NOT EXISTS tarea
(
	id int NOT NULL AUTO_INCREMENT,
    descripcion VARCHAR(50) NOT NULL,
    CONSTRAINT PK_tarea PRIMARY KEY (id)
);

-- Tabla: Anuncio_Tarea
CREATE TABLE IF NOT EXISTS anuncio_tarea
(
	id_anuncio int NOT NULL,
    id_tarea int NOT NULL,
    CONSTRAINT PK_anuncio_tarea PRIMARY KEY (id_anuncio, id_tarea),
    CONSTRAINT FK_anuncio_tarea_anuncio FOREIGN KEY (id_anuncio) REFERENCES anuncio(id),
    CONSTRAINT FK_anuncio_tarea_tarea FOREIGN KEY (id_tarea) REFERENCES tarea(id)
);

-- Tabla: Anuncio_Disponibilidad
CREATE TABLE IF NOT EXISTS anuncio_disponibilidad
(
	id_anuncio int NOT NULL,
    id_disponibilidad int NOT NULL,
    CONSTRAINT PK_anuncio_disponibilidad PRIMARY KEY (id_anuncio, id_disponibilidad),
    CONSTRAINT FK_anuncio_disponibilidad_anuncio FOREIGN KEY (id_anuncio) REFERENCES anuncio(id),
    CONSTRAINT FK_anuncio_disponibilidad_disponibilidad FOREIGN KEY (id_disponibilidad) REFERENCES disponibilidad(id)
);

-- Tabla: Empleado_Tarea
CREATE TABLE IF NOT EXISTS empleado_tarea
(
	id_empleado int NOT NULL,
    id_tarea int NOT NULL,
    CONSTRAINT PK_empleado_tarea PRIMARY KEY (id_empleado, id_tarea),
    CONSTRAINT FK_empleado_tarea_empleado FOREIGN KEY (id_empleado) REFERENCES empleado(id),
    CONSTRAINT FK_empleado_tarea_tarea FOREIGN KEY (id_tarea) REFERENCES tarea(id)
);

-- Tabla: Empleado_Disponibilidad
CREATE TABLE IF NOT EXISTS empleado_disponibilidad
(
	id_empleado int NOT NULL,
    id_disponibilidad int NOT NULL,
    CONSTRAINT PK_empleado_disponibilidad PRIMARY KEY (id_empleado, id_disponibilidad),
    CONSTRAINT FK_empleado_disponibilidad_empleado FOREIGN KEY (id_empleado) REFERENCES empleado(id),
    CONSTRAINT FK_empleado_disponibilidad_disponibilidad FOREIGN KEY (id_disponibilidad) REFERENCES disponibilidad(id)
);



-- *** INSERCIONES EN LAS TABLAS ***

-- Tipos de usuarios (Administrador, Empleador y Empleado)
INSERT INTO tipo_usuario (nombre) 
VALUES ('Administrador');
INSERT INTO tipo_usuario (nombre) 
VALUES ('Empleador');
INSERT INTO tipo_usuario (nombre) 
VALUES ('Empleado');

-- Usuarios
INSERT INTO usuario (usuario, clave, id_tipo) 
VALUES ('admin', 'admin', 1);
INSERT INTO usuario (usuario, clave, id_tipo) 
VALUES ('jefe', 'jefe', 2);
INSERT INTO usuario (usuario, clave, id_tipo) 
VALUES ('peon', 'peon', 3);

-- Empleadores
-- INSERT INTO empleador (nombre, ...) 
-- VALUES ('Martin', ...);

-- Empleados
-- INSERT INTO empleado (nombre, ...) 
-- VALUES ('Juan', ...);

-- Anuncios
-- INSERT INTO anuncio (descripcion, fecha, ...) 
-- VALUES ('Limpiar mi casa', '2020-02-22', ...);

-- Postulaciones
-- INSERT INTO postulacion (id_empleado, id_anuncio, fecha, mensaje) 
-- VALUES (1, 1, DATE_FORMAT('2020-02-25', '%Y-%m-%d'), 'Me gustaría obtener el empleo');

-- Vínculos
-- INSERT INTO vinculo (id_empleado, id_empleador, id_anuncio, fecha_inicio, fecha_fin, motivo_fin) 
-- VALUES (1, 1, 1, DATE_FORMAT('2020-02-26', '%Y-%m-%d'), NULL, NULL);

-- Referencias

-- Disponibilidad
INSERT INTO disponibilidad (id, descripcion) 
VALUES (1, 'Por Hora');
INSERT INTO disponibilidad (id, descripcion) 
VALUES (2, 'Por Jornada');
INSERT INTO disponibilidad (id, descripcion) 
VALUES (3, 'Por Tarea Puntual');
INSERT INTO disponibilidad (id, descripcion) 
VALUES (4, 'Por Mes');

-- Tareas
INSERT INTO tarea (id, descripcion) 
VALUES (1, 'Hogar');
INSERT INTO tarea (id, descripcion) 
VALUES (2, 'Oficina');
INSERT INTO tarea (id, descripcion) 
VALUES (3, 'Cocinar');
INSERT INTO tarea (id, descripcion) 
VALUES (4, 'Limpieza de Baños');
INSERT INTO tarea (id, descripcion) 
VALUES (5, 'Limpieza de Cocinas');
INSERT INTO tarea (id, descripcion) 
VALUES (6, 'Limpieza de Dormitorios');
INSERT INTO tarea (id, descripcion) 
VALUES (7, 'Cuidado de Niños');
INSERT INTO tarea (id, descripcion) 
VALUES (8, 'Cuidado de Bebés');
INSERT INTO tarea (id, descripcion) 
VALUES (9, 'Cuidado de Adultos Mayores');
INSERT INTO tarea (id, descripcion) 
VALUES (10, 'Cuidado de Mascotas');

-- Anuncio Tarea

-- Anuncio Disponibilidad

-- Empleado Tarea

-- Empleado Disponibilidad