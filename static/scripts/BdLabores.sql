USE LvP2Ka0CsK;


DROP TABLE IF EXISTS vinculo;
DROP TABLE IF EXISTS mensaje;
DROP TABLE IF EXISTS postulacion;
DROP TABLE IF EXISTS anuncio_disponibilidad;
DROP TABLE IF EXISTS anuncio_tarea;
DROP TABLE IF EXISTS anuncio;
DROP TABLE IF EXISTS empleado_disponibilidad;
DROP TABLE IF EXISTS empleado_tarea;
DROP TABLE IF EXISTS empleador;
DROP TABLE IF EXISTS tarea;
DROP TABLE IF EXISTS disponibilidad;
DROP TABLE IF EXISTS referencia;
DROP TABLE IF EXISTS empleado;
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


-- Tabla: usuario
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



-- Tabla: tarea
CREATE TABLE IF NOT EXISTS tarea (
	id int NOT NULL AUTO_INCREMENT,
	descripcion varchar(50) NOT NULL,
	CONSTRAINT PK_tarea PRIMARY KEY (id)
);


-- Tabla: disponibilidad
CREATE TABLE IF NOT EXISTS disponibilidad (
	id int NOT NULL AUTO_INCREMENT,
	descripcion varchar(50) NOT NULL,
	CONSTRAINT PK_disponibilidad PRIMARY KEY (id)
);


-- Tabla: empleador
CREATE TABLE IF NOT EXISTS empleador (
	id int NOT NULL AUTO_INCREMENT,
	cedula varchar(20) NOT NULL,
	nombre varchar(50) NOT NULL,
	apellido varchar(50) NOT NULL,
	fecha_nacimiento date DEFAULT NULL,
	genero bit(1) DEFAULT NULL, -- 0:Femenino, 1:Masculino
	domicilio varchar(50) DEFAULT NULL,
	nacionalidad varchar(50) DEFAULT NULL,
	email varchar(50) DEFAULT NULL,
	telefono varchar(20) DEFAULT NULL,
	registro_bps varchar(20) DEFAULT NULL,
	foto varchar(150),
	promedio_calificacion double DEFAULT NULL,
	id_usuario int NOT NULL,
	CONSTRAINT PK_empleador PRIMARY KEY (id),
	CONSTRAINT UK_empleador UNIQUE (cedula),
	CONSTRAINT FK_empleador_usuario FOREIGN KEY (id_usuario) REFERENCES usuario (id)
);


-- Tabla: empleado
CREATE TABLE IF NOT EXISTS empleado (
	id int NOT NULL AUTO_INCREMENT,
	cedula varchar(20) NOT NULL,
	nombre varchar(50) NOT NULL,
	apellido varchar(50) NOT NULL,
	fecha_nacimiento date DEFAULT NULL,
	genero bit(1) DEFAULT NULL, -- 0:Femenino, 1:Masculino
	domicilio varchar(50) DEFAULT NULL,
	nacionalidad varchar(50) DEFAULT NULL,
	email varchar(50) DEFAULT NULL,
	telefono varchar(20) DEFAULT NULL,
	experiencia_meses int DEFAULT NULL,
	descripcion text,
	foto varchar(150),
	promedio_calificacion double DEFAULT NULL,
	id_usuario int NOT NULL,
	CONSTRAINT PK_empleado PRIMARY KEY (id),
	CONSTRAINT UK_empleado UNIQUE (cedula),
	CONSTRAINT FK_empleado_usuario FOREIGN KEY (id_usuario) REFERENCES usuario (id)
);


-- Tabla: empleado_tarea
CREATE TABLE IF NOT EXISTS empleado_tarea (
	id_empleado int NOT NULL,
	id_tarea int NOT NULL,
	CONSTRAINT PK_empleado_tarea PRIMARY KEY (id_empleado, id_tarea),
	CONSTRAINT FK_empleado_tarea_empleado FOREIGN KEY (id_empleado) REFERENCES empleado (id),
	CONSTRAINT FK_empleado_tarea_tarea FOREIGN KEY (id_tarea) REFERENCES tarea (id)
);


-- Tabla: empleado_disponibilidad
CREATE TABLE IF NOT EXISTS empleado_disponibilidad (
	id_empleado int NOT NULL,
	id_disponibilidad int NOT NULL,
	CONSTRAINT PK_empleado_disponibilidad PRIMARY KEY (id_empleado, id_disponibilidad),
	CONSTRAINT FK_empleado_disponibilidad_disponibilidad FOREIGN KEY (id_disponibilidad) REFERENCES disponibilidad (id),
	CONSTRAINT FK_empleado_disponibilidad_empleado FOREIGN KEY (id_empleado) REFERENCES empleado (id)
);


-- Tabla: referencia
CREATE TABLE IF NOT EXISTS referencia (
	id int NOT NULL AUTO_INCREMENT,
	id_empleado int NOT NULL,
	nombre varchar(50) NOT NULL,
	telefono varchar(20) NOT NULL,
	fecha_desde date NOT NULL,
	fecha_hasta date DEFAULT NULL,
	CONSTRAINT PK_referencia PRIMARY KEY (id),
	CONSTRAINT FK_referencia_empleado FOREIGN KEY (id_empleado) REFERENCES empleado (id)
);


-- Tabla: anuncio
CREATE TABLE IF NOT EXISTS anuncio (
	id int NOT NULL AUTO_INCREMENT,
	titulo varchar(50) NOT NULL,
	descripcion text,
	fecha_inicio date NOT NULL,
	fecha_cierre date DEFAULT NULL,
	estado bit(1) NOT NULL, -- 0:Inactivo, 1:Activo
	experiencia tinyint(1) NOT NULL,
	salario int DEFAULT NULL,
	id_empleador int NOT NULL,
	calificacion_desde double DEFAULT NULL,
	calificacion_hasta double DEFAULT NULL,
	tiene_vinculo boolean NULL,
	CONSTRAINT PK_anuncio PRIMARY KEY (id),
	CONSTRAINT FK_anuncio_empleador FOREIGN KEY (id_empleador) REFERENCES empleador (id)
);


-- Tabla: anuncio_disponibilidad
CREATE TABLE IF NOT EXISTS anuncio_disponibilidad (
	id_anuncio int NOT NULL,
	id_disponibilidad int NOT NULL,
	CONSTRAINT PK_anuncio_disponibilidad PRIMARY KEY (id_anuncio, id_disponibilidad),
	CONSTRAINT FK_anuncio_disponibilidad_anuncio FOREIGN KEY (id_anuncio) REFERENCES anuncio (id),
	CONSTRAINT FK_anuncio_disponibilidad_disponibilidad FOREIGN KEY (id_disponibilidad) REFERENCES disponibilidad (id)
);


-- Tabla: anuncio_tarea
CREATE TABLE IF NOT EXISTS anuncio_tarea (
	id_anuncio int NOT NULL,
	id_tarea int NOT NULL,
	CONSTRAINT PK_anuncio_tarea PRIMARY KEY (id_anuncio, id_tarea),
	CONSTRAINT FK_anuncio_tarea_anuncio FOREIGN KEY (id_anuncio) REFERENCES anuncio (id),
	CONSTRAINT FK_anuncio_tarea_tarea FOREIGN KEY (id_tarea) REFERENCES tarea (id)
);


-- Tabla: postulacion
CREATE TABLE IF NOT EXISTS postulacion (
	id int NOT NULL AUTO_INCREMENT,
	id_empleado int NOT NULL,
	id_anuncio int NOT NULL,
	fecha date DEFAULT NULL,
	mensaje varchar(50) DEFAULT NULL,
	genera_vinculo boolean NULL,
	CONSTRAINT PK_postulacion PRIMARY KEY (id),
	CONSTRAINT FK_postulacion_empleado FOREIGN KEY (id_empleado) REFERENCES empleado(id),
	CONSTRAINT FK_postulacion_anuncio FOREIGN KEY (id_anuncio) REFERENCES anuncio(id)
);


-- Tabla: vinculo
CREATE TABLE IF NOT EXISTS vinculo (
	id int NOT NULL AUTO_INCREMENT,
	id_empleado int NOT NULL,
	id_empleador int NOT NULL,
	id_anuncio int NOT NULL,
	fecha_inicio date DEFAULT NULL,
	fecha_fin date DEFAULT NULL,
	motivo_fin text,
	descripcion varchar(200) DEFAULT NULL,
	calificacion_empleado double DEFAULT NULL,
	calificacion_empleador double DEFAULT NULL,
	CONSTRAINT PK_vinculo PRIMARY KEY (id),
	CONSTRAINT FK_vinculo_empleado FOREIGN KEY (id_empleado) REFERENCES empleado(id),
	CONSTRAINT FK_vinculo_empleador FOREIGN KEY (id_empleador) REFERENCES empleador(id),
	CONSTRAINT FK_vinculo_anuncio FOREIGN KEY (id_anuncio) REFERENCES anuncio(id)
);


-- Tabla: mensaje
CREATE TABLE IF NOT EXISTS mensaje (
	id int NOT NULL AUTO_INCREMENT,
	id_empleado int NOT NULL,
	id_empleador int NOT NULL,
	id_anuncio int NOT NULL,
	fecha date NULL,
	mensaje varchar(200) NULL,
	CONSTRAINT PK_mensaje PRIMARY KEY (id),
	CONSTRAINT FK_mensaje_anuncio FOREIGN KEY (id_anuncio) REFERENCES anuncio (id),
	CONSTRAINT FK_mensaje_empleado FOREIGN KEY (id_empleado) REFERENCES empleado (id),
	CONSTRAINT FK_mensaje_empleador FOREIGN KEY (id_empleador) REFERENCES empleador (id)
);


-- *** INSERCIONES EN LAS TABLAS ***

-- En tabla "tipo_usuario"
INSERT INTO tipo_usuario (nombre) 
VALUES ('Administrador');
INSERT INTO tipo_usuario (nombre) 
VALUES ('Empleador');
INSERT INTO tipo_usuario (nombre) 
VALUES ('Empleado');

-- En tabla "usuario"
INSERT INTO usuario (usuario, clave, id_tipo) 
VALUES ('admin', 'admin', 1);
INSERT INTO usuario (usuario, clave, id_tipo) 
VALUES ('jefe', 'jefe', 2);
INSERT INTO usuario (usuario, clave, id_tipo) 
VALUES ('peon', 'peon', 3);

-- En tabla "disponibilidad"
INSERT INTO disponibilidad (descripcion) 
VALUES ('Por Hora');
INSERT INTO disponibilidad (descripcion) 
VALUES ('Por Jornada');
INSERT INTO disponibilidad (descripcion) 
VALUES ('Por Tarea Puntual');
INSERT INTO disponibilidad (descripcion) 
VALUES ('Por Mes');

-- En tabla "tarea"
INSERT INTO tarea (descripcion) 
VALUES ('Hogar');
INSERT INTO tarea (descripcion) 
VALUES ('Oficina');
INSERT INTO tarea (descripcion) 
VALUES ('Cocinar');
INSERT INTO tarea (descripcion) 
VALUES ('Limpieza de Baños');
INSERT INTO tarea (descripcion) 
VALUES ('Limpieza de Cocinas');
INSERT INTO tarea (descripcion) 
VALUES ('Limpieza de Dormitorios');
INSERT INTO tarea (descripcion) 
VALUES ('Cuidado de Niños');
INSERT INTO tarea (descripcion) 
VALUES ('Cuidado de Bebés');
INSERT INTO tarea (descripcion) 
VALUES ('Cuidado de Adultos Mayores');
INSERT INTO tarea (descripcion) 
VALUES ('Cuidado de Mascotas');

-- En tabla "empleado"
INSERT INTO empleado (cedula, nombre, apellido, fecha_nacimiento, genero, domicilio, nacionalidad, email, telefono, experiencia_meses, descripcion, foto, promedio_calificacion, id_usuario)
VALUES (1234567-8, 'el peoncito', 'jodido', '1982-03-12', 1, 'Ejido 1857', 'Uruguayo', 'peoncito@gmail.com', '099987654', 0, '', '', 0, 3);

-- En tabla "empleado_disponibilidad"


-- Eb tabla "empleado_tarea"


-- En tabla "referencia"


-- En tabla "empleador"
INSERT INTO empleador (cedula, nombre, apellido, fecha_nacimiento, genero, domicilio, nacionalidad, email, telefono, registro_bps, foto, promedio_calificacion, id_usuario)
VALUES (1234567-8, 'la jefecita', 'ma mejor', '1975-05-22', 0, 'Yi 1234', 'Uruguayo', 'jefecita@gmail.com', '099123456', 0, '', 0, 2);

-- En tabla "anuncio"


-- En tabla "anuncio_disponibilidad"


-- En tabla "anuncio_tarea"


-- En tabla "postulacion"


-- En tabla "mensaje"


-- En tabla "vinculo"