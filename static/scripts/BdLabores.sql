-- DROP SCHEMA bdLabores;
-- CREATE SCHEMA IF NOT EXISTS bdlabores DEFAULT CHARACTER SET utf8mb4;

-- Si se usa CloudAccess
-- USE amqtvopx;

-- Si se usa RemoteMySQL
-- USE LvP2Ka0CsK;

-- Si se usa AWS o localhost
-- USE bdlabores;

DROP TABLE IF EXISTS vinculo;
DROP TABLE IF EXISTS mensaje;
DROP TABLE IF EXISTS tipo_emisor_receptor_mensaje;
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
	usuario VARCHAR(50) NOT NULL,
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
	fecha_nacimiento date NULL,
	genero bit(1) NULL, -- 0:Femenino, 1:Masculino
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
	fecha_nacimiento date NULL,
	genero bit(1) NOT NULL, -- 0:Femenino, 1:Masculino
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
    apellido varchar(50) NOT NULL,
	telefono varchar(20) NOT NULL,
	fecha_desde date NOT NULL,
	fecha_hasta date NULL,
	CONSTRAINT PK_referencia PRIMARY KEY (id),
	CONSTRAINT FK_referencia_empleado FOREIGN KEY (id_empleado) REFERENCES empleado (id)
);


-- Tabla: anuncio
CREATE TABLE IF NOT EXISTS anuncio (
	id int NOT NULL AUTO_INCREMENT,
	titulo varchar(100) NOT NULL,
	descripcion text,
	fecha_inicio date NOT NULL,
	fecha_cierre date NULL,
	estado bit(1) NOT NULL, -- 0:Inactivo, 1:Activo
	experiencia boolean NOT NULL, -- 0:Sin Experiencia, 1:Con Experiencia
	pago_hora int NULL,
	id_empleador int NOT NULL,
	calificacion_desde double NULL,
	calificacion_hasta double NULL,
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
	fecha date NULL,
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
	fecha_inicio date NULL,
	fecha_fin date NULL,
	descripcion text DEFAULT NULL,
	calificacion_empleado double DEFAULT NULL,
	calificacion_empleador double DEFAULT NULL,
	CONSTRAINT PK_vinculo PRIMARY KEY (id),
	CONSTRAINT FK_vinculo_empleado FOREIGN KEY (id_empleado) REFERENCES empleado(id),
	CONSTRAINT FK_vinculo_empleador FOREIGN KEY (id_empleador) REFERENCES empleador(id),
	CONSTRAINT FK_vinculo_anuncio FOREIGN KEY (id_anuncio) REFERENCES anuncio(id)
);


-- Tabla: Tipo de Emisor/Receptor de Mensaje
CREATE TABLE IF NOT EXISTS tipo_emisor_receptor_mensaje
(
	id int NOT NULL AUTO_INCREMENT,
	nombre VARCHAR(50) NOT NULL,
    CONSTRAINT PK_tipo_emisor_mensaje PRIMARY KEY (id),
    CONSTRAINT UK_tipo_emisor_mensaje UNIQUE (nombre)
);

-- Tabla: mensaje
CREATE TABLE IF NOT EXISTS mensaje (
	id int NOT NULL AUTO_INCREMENT,
	id_empleado int NOT NULL,
	id_empleador int NOT NULL,
	id_anuncio int NULL, -- Puede ser vacío
	fecha timestamp NULL,
	mensaje text NULL,
    id_tipo_emisor int NOT NULL,
    id_tipo_receptor int NOT NULL,
	CONSTRAINT PK_mensaje PRIMARY KEY (id),
	CONSTRAINT FK_mensaje_empleado FOREIGN KEY (id_empleado) REFERENCES empleado (id),
	CONSTRAINT FK_mensaje_empleador FOREIGN KEY (id_empleador) REFERENCES empleador (id),
    CONSTRAINT FK_mensaje_tipo_emisor FOREIGN KEY (id_tipo_emisor) REFERENCES tipo_emisor_receptor_mensaje (id),
    CONSTRAINT FK_mensaje_tipo_receptor FOREIGN KEY (id_tipo_receptor) REFERENCES tipo_emisor_receptor_mensaje (id)
);


-- *** INSERCIONES EN LAS TABLAS ***

-- En tabla "tipo_usuario"
INSERT INTO tipo_usuario (nombre) 
VALUES ('Administrador');
INSERT INTO tipo_usuario (nombre) 
VALUES ('Empleador');
INSERT INTO tipo_usuario (nombre) 
VALUES ('Empleado');

-- En tabla "tipo_emisor_receptor_mensaje"
INSERT INTO tipo_emisor_receptor_mensaje (nombre) 
VALUES ('Empleado');
INSERT INTO tipo_emisor_receptor_mensaje (nombre) 
VALUES ('Empleador');
INSERT INTO tipo_emisor_receptor_mensaje (nombre) 
VALUES ('Sistema');

-- En tabla "usuario"
INSERT INTO usuario (usuario, clave, id_tipo) 
VALUES ('admin', 'admin', 1);
INSERT INTO usuario (usuario, clave, id_tipo) 
VALUES ('11111111', '1', 2);
INSERT INTO usuario (usuario, clave, id_tipo) 
VALUES ('22222222', '2', 3);
INSERT INTO usuario (usuario, clave, id_tipo) 
VALUES ('38628415', 'prueba', 3);
INSERT INTO usuario (usuario, clave, id_tipo) 
VALUES ('23562363', 'prueba', 3);

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
INSERT INTO tarea (descripcion) 
VALUES ('Otra');

-- En tabla "empleado"
INSERT INTO empleado (cedula, nombre, apellido, fecha_nacimiento, genero, domicilio, nacionalidad, email, telefono, experiencia_meses, descripcion, foto, promedio_calificacion, id_usuario)
VALUES (22222222, 'Ramón', 'Santos', '1982-03-12', 1, 'Ejido 1857', 'Uruguayo', 'rsantos@gmail.com', '099987654', 0, 'Muy ordenado', 'images/Perfiles/RSantos.png', 0, 3);
INSERT INTO empleado_disponibilidad (id_empleado, id_disponibilidad)
VALUES (1, 4);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (1, 3);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (1, 4);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (1, 5);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (1, 6);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (1, 7);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (1, 9);
INSERT INTO empleado (cedula, nombre, apellido, fecha_nacimiento, genero, domicilio, nacionalidad, email, telefono, experiencia_meses, descripcion, foto, promedio_calificacion, id_usuario)
VALUES (38628415, 'Juana', 'Perez', '1975-01-23', 0, 'Rodeau 1411', 'Uruguayo', 'jperez@gmail.com', '091030215', 25, 'Proactiva', 'images/Perfiles/JPerez.png', 0, 4);
INSERT INTO empleado_disponibilidad (id_empleado, id_disponibilidad)
VALUES (2, 1);
INSERT INTO empleado_disponibilidad (id_empleado, id_disponibilidad)
VALUES (2, 4);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (2, 3);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (2, 4);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (2, 5);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (2, 6);
INSERT INTO empleado (cedula, nombre, apellido, fecha_nacimiento, genero, domicilio, nacionalidad, email, telefono, experiencia_meses, descripcion, foto, promedio_calificacion, id_usuario)
VALUES (23562363, 'Maria', 'Gutierrez', '1977-04-02', 0, 'Yi 2110', 'Uruguayo', 'mguti@gmail.com', '095251600', 38, '', 'images/Perfiles/MGutierrez.png', 0, 5);
INSERT INTO empleado_disponibilidad (id_empleado, id_disponibilidad)
VALUES (3, 1);
INSERT INTO empleado_disponibilidad (id_empleado, id_disponibilidad)
VALUES (3, 2);
INSERT INTO empleado_disponibilidad (id_empleado, id_disponibilidad)
VALUES (3, 3);
INSERT INTO empleado_disponibilidad (id_empleado, id_disponibilidad)
VALUES (3, 4);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (3, 3);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (3, 4);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (3, 5);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (3, 6);
INSERT INTO empleado_tarea (id_empleado, id_tarea)
VALUES (3, 7);

-- En tabla "referencia"
INSERT INTO referencia (id_empleado, nombre, apellido, telefono, fecha_desde, fecha_hasta)
VALUES (1, 'Susana', 'Riux', '091115028', '2015-02-23', '2017-04-22');
INSERT INTO referencia (id_empleado, nombre, apellido, telefono, fecha_desde, fecha_hasta)
VALUES (1, 'Leopoldo', 'Garcia', '096524741', '2017-06-21', '2019-11-05');

-- En tabla "empleador"
INSERT INTO empleador (cedula, nombre, apellido, fecha_nacimiento, genero, domicilio, nacionalidad, email, telefono, registro_bps, foto, promedio_calificacion, id_usuario)
VALUES (11111111, 'Luisa', 'Ramos', '1975-05-22', 0, 'Yi 1234', 'Uruguayo', 'lramos@gmail.com', '099123456', '', 'images/Perfiles/LRamos.png', 0, 2);

-- En tabla "anuncio"
INSERT INTO anuncio (titulo, descripcion, fecha_inicio, fecha_cierre, estado, experiencia, pago_hora, id_empleador, calificacion_desde, calificacion_hasta, tiene_vinculo)
VALUES ('Necesito limpiar mi casa', 'Casa grande, 3 dormitorios, cocina, living y 2 baños', '2020-02-20', NULL, true, 1, 120, 1, NULL, NULL, false);
INSERT INTO anuncio_disponibilidad (id_anuncio, id_disponibilidad)
VALUES (1, 4);
INSERT INTO anuncio_tarea (id_anuncio, id_tarea)
VALUES (1, 4);
INSERT INTO anuncio_tarea (id_anuncio, id_tarea)
VALUES (1, 5);
INSERT INTO anuncio_tarea (id_anuncio, id_tarea)
VALUES (1, 6);
INSERT INTO anuncio (titulo, descripcion, fecha_inicio, fecha_cierre, estado, experiencia, pago_hora, id_empleador, calificacion_desde, calificacion_hasta, tiene_vinculo)
VALUES ('Cuidado de niños', 'Uno tiene 6, fatal!!!, el otro tiene 16, buenísimo pero es metalero', '2020-02-25', NULL, true, 1, 200, 1, NULL, NULL, false);
INSERT INTO anuncio_disponibilidad (id_anuncio, id_disponibilidad)
VALUES (2, 2);
INSERT INTO anuncio_tarea (id_anuncio, id_tarea)
VALUES (2, 7);
INSERT INTO anuncio (titulo, descripcion, fecha_inicio, fecha_cierre, estado, experiencia, pago_hora, id_empleador, calificacion_desde, calificacion_hasta, tiene_vinculo)
VALUES ('Limpieza de oficina', 'Es una oficina chica, en 2 horitas debería quedar pronta', '2020-02-26', NULL, true, 1, 180, 1, NULL, NULL, false);
INSERT INTO anuncio_disponibilidad (id_anuncio, id_disponibilidad)
VALUES (3, 3);
INSERT INTO anuncio_tarea (id_anuncio, id_tarea)
VALUES (3, 2);

-- En tabla "postulacion"
INSERT INTO postulacion (id_empleado, id_anuncio, fecha, genera_vinculo)
VALUES (1, 1, '2020-02-20', false);
INSERT INTO postulacion (id_empleado, id_anuncio, fecha, genera_vinculo)
VALUES (1, 3, '2020-02-28', false);
INSERT INTO postulacion (id_empleado, id_anuncio, fecha, genera_vinculo)
VALUES (2, 1, '2020-02-21', false);
INSERT INTO postulacion (id_empleado, id_anuncio, fecha, genera_vinculo)
VALUES (2, 2, '2020-02-29', false);
INSERT INTO postulacion (id_empleado, id_anuncio, fecha, genera_vinculo)
VALUES (2, 3, '2020-03-05', false);
INSERT INTO postulacion (id_empleado, id_anuncio, fecha, genera_vinculo)
VALUES (3, 1, '2020-03-06', false);

-- En tabla "mensaje"
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (1, 1, 1, '2019-11-28 11:20:05', 'Estoy interesado en el anuncio, tengo buenas referencias', 1, 2);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (1, 1, 1, '2019-11-29 14:32:18', 'Vi tus referencias, me generan dudas', 2, 1);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (1, 1, 3, '2020-02-20 08:25:16', 'Quisiera postularme para el empleo, aguardo respuesta', 1, 2);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (1, 1, 3, '2020-02-21 10:12:35', 'Estoy evaluando candidatos', 2, 1);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (1, 1, 3, '2020-02-22 13:25:14', 'Bueno, muchas gracias!', 1, 2);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (2, 1, 1, '2019-10-14 10:02:58', 'Lo quiero... al empleo, no a ud.', 1, 2);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (2, 1, 1, '2019-10-14 11:15:09', 'Que lastima, me había ilusionado', 2, 1);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (2, 1, 1, '2019-10-14 11:30:06', 'Bueno, quizás un poco a los 2', 1, 2);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (2, 1, 1, '2019-10-16 18:23:47', 'Ni que fuera Tinder esto', 2, 1);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (2, 1, 1, '2019-10-16 20:23:19', 'Perdón', 1, 2);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (2, 1, 1, '2019-10-16 20:23:50', 'Mala mía!', 1, 2);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (2, 1, 2, '2019-12-22 13:52:03',  'Me encanta el empleo', 1, 2);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (2, 1, 2, '2019-12-26 09:02:36',  'La tendré en cuenta', 2, 1);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (2, 1, 3, '2020-01-18 11:11:28', 'Tengo gran experiencia en limpieza de oficinas', 1, 2);
INSERT INTO mensaje (id_empleado, id_empleador, id_anuncio, fecha, mensaje, id_tipo_emisor, id_tipo_receptor)
VALUES (2, 1, 3, '2020-01-22 15:36:01', 'Interesante', 2, 1);

-- En tabla "vinculo"
