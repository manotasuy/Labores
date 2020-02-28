-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 27-02-2020 a las 14:28:29
-- Versión del servidor: 8.0.13-4
-- Versión de PHP: 7.2.24-0ubuntu0.18.04.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `LvP2Ka0CsK`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `anuncio`
--

CREATE TABLE `anuncio` (
  `id` int(11) NOT NULL,
  `titulo` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8_unicode_ci,
  `fecha_inicio` date NOT NULL,
  `fecha_cierre` date DEFAULT NULL,
  `estado` bit(1) NOT NULL,
  `experiencia` tinyint(1) NOT NULL,
  `salario` int(11) DEFAULT NULL,
  `id_empleador` int(11) NOT NULL,
  `calificacion_empleado` double DEFAULT NULL,
  `calificacion_empleador` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `anuncio_disponibilidad`
--

CREATE TABLE `anuncio_disponibilidad` (
  `id_anuncio` int(11) NOT NULL,
  `id_disponibilidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `anuncio_tarea`
--

CREATE TABLE `anuncio_tarea` (
  `id_anuncio` int(11) NOT NULL,
  `id_tarea` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `disponibilidad`
--

CREATE TABLE `disponibilidad` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(50) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `disponibilidad`
--

INSERT INTO `disponibilidad` (`id`, `descripcion`) VALUES
(1, 'Por Hora'),
(2, 'Por Jornada'),
(3, 'Por Tarea Puntual'),
(4, 'Por Mes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `id` int(11) NOT NULL,
  `cedula` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `apellido` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `genero` bit(1) DEFAULT NULL,
  `domicilio` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `nacionalidad` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `telefono` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `experiencia_meses` int(11) DEFAULT NULL,
  `descripcion` text COLLATE utf8_unicode_ci,
  `foto` varchar(150) COLLATE utf8_unicode_ci,
  `id_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleador`
--

CREATE TABLE `empleador` (
  `id` int(11) NOT NULL,
  `cedula` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `apellido` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `genero` bit(1) DEFAULT NULL,
  `domicilio` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `nacionalidad` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `telefono` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `registro_bps` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `foto` varchar(150) COLLATE utf8_unicode_ci,
  `id_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado_disponibilidad`
--

CREATE TABLE `empleado_disponibilidad` (
  `id_empleado` int(11) NOT NULL,
  `id_disponibilidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado_tarea`
--

CREATE TABLE `empleado_tarea` (
  `id_empleado` int(11) NOT NULL,
  `id_tarea` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `postulacion`
--

CREATE TABLE `postulacion` (
  `id` int(11) NOT NULL,
  `id_empleado` int(11) NOT NULL,
  `id_anuncio` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `mensaje` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `referencia`
--

CREATE TABLE `referencia` (
  `id` int(11) NOT NULL,
  `id_empleado` int(11) NOT NULL,
  `nombre` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_desde` date NOT NULL,
  `fecha_hasta` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarea`
--

CREATE TABLE `tarea` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(50) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `tarea`
--

INSERT INTO `tarea` (`id`, `descripcion`) VALUES
(1, 'Hogar'),
(2, 'Oficina'),
(3, 'Cocinar'),
(4, 'Limpieza de Baños'),
(5, 'Limpieza de Cocinas'),
(6, 'Limpieza de Dormitorios'),
(7, 'Cuidado de Niños'),
(8, 'Cuidado de Bebés'),
(9, 'Cuidado de Adultos Mayores'),
(10, 'Cuidado de Mascotas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_usuario`
--

CREATE TABLE `tipo_usuario` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `tipo_usuario`
--

INSERT INTO `tipo_usuario` (`id`, `nombre`) VALUES
(1, 'Administrador'),
(3, 'Empleado'),
(2, 'Empleador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `usuario` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clave` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `id_tipo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `usuario`, `clave`, `id_tipo`) VALUES
(1, 'admin', 'admin', 1),
(2, 'jefe', 'jefe', 2),
(3, 'peon', 'peon', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vinculo`
--

CREATE TABLE `vinculo` (
  `id` int(11) NOT NULL,
  `id_empleado` int(11) NOT NULL,
  `id_empleador` int(11) NOT NULL,
  `id_anuncio` int(11) NOT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `motivo_fin` text COLLATE utf8_unicode_ci,
  `descripcion` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `calificacion_empleado` double DEFAULT NULL,
  `calificacion_empleador` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `anuncio`
--
ALTER TABLE `anuncio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_anuncio_empleador` (`id_empleador`);

--
-- Indices de la tabla `anuncio_disponibilidad`
--
ALTER TABLE `anuncio_disponibilidad`
  ADD PRIMARY KEY (`id_anuncio`,`id_disponibilidad`),
  ADD KEY `FK_anuncio_disponibilidad_disponibilidad` (`id_disponibilidad`);

--
-- Indices de la tabla `anuncio_tarea`
--
ALTER TABLE `anuncio_tarea`
  ADD PRIMARY KEY (`id_anuncio`,`id_tarea`),
  ADD KEY `FK_anuncio_tarea_tarea` (`id_tarea`);

--
-- Indices de la tabla `disponibilidad`
--
ALTER TABLE `disponibilidad`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UK_empleador` (`cedula`),
  ADD KEY `FK_empleado_usuario` (`id_usuario`);

--
-- Indices de la tabla `empleador`
--
ALTER TABLE `empleador`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UK_empleador` (`cedula`),
  ADD KEY `FK_empleador_usuario` (`id_usuario`);

--
-- Indices de la tabla `empleado_disponibilidad`
--
ALTER TABLE `empleado_disponibilidad`
  ADD PRIMARY KEY (`id_empleado`,`id_disponibilidad`),
  ADD KEY `FK_empleado_disponibilidad_disponibilidad` (`id_disponibilidad`);

--
-- Indices de la tabla `empleado_tarea`
--
ALTER TABLE `empleado_tarea`
  ADD PRIMARY KEY (`id_empleado`,`id_tarea`),
  ADD KEY `FK_empleado_tarea_tarea` (`id_tarea`);

--
-- Indices de la tabla `postulacion`
--
ALTER TABLE `postulacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_postulacion_empleado` (`id_empleado`),
  ADD KEY `FK_postulacion_anuncio` (`id_anuncio`);

--
-- Indices de la tabla `referencia`
--
ALTER TABLE `referencia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_referencia_empleado` (`id_empleado`);

--
-- Indices de la tabla `tarea`
--
ALTER TABLE `tarea`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipo_usuario`
--
ALTER TABLE `tipo_usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UK_tipo_usuario` (`nombre`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UK_usuario` (`usuario`),
  ADD KEY `FK_usuario_tipo` (`id_tipo`),
  ADD KEY `IDXuser` (`usuario`);

--
-- Indices de la tabla `vinculo`
--
ALTER TABLE `vinculo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_vinculo_empleado` (`id_empleado`),
  ADD KEY `FK_vinculo_empleador` (`id_empleador`),
  ADD KEY `FK_vinculo_anuncio` (`id_anuncio`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `anuncio`
--
ALTER TABLE `anuncio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `disponibilidad`
--
ALTER TABLE `disponibilidad`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `empleador`
--
ALTER TABLE `empleador`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `postulacion`
--
ALTER TABLE `postulacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `referencia`
--
ALTER TABLE `referencia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tarea`
--
ALTER TABLE `tarea`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `tipo_usuario`
--
ALTER TABLE `tipo_usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `vinculo`
--
ALTER TABLE `vinculo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `anuncio`
--
ALTER TABLE `anuncio`
  ADD CONSTRAINT `FK_anuncio_empleador` FOREIGN KEY (`id_empleador`) REFERENCES `empleador` (`id`);

--
-- Filtros para la tabla `anuncio_disponibilidad`
--
ALTER TABLE `anuncio_disponibilidad`
  ADD CONSTRAINT `FK_anuncio_disponibilidad_anuncio` FOREIGN KEY (`id_anuncio`) REFERENCES `anuncio` (`id`),
  ADD CONSTRAINT `FK_anuncio_disponibilidad_disponibilidad` FOREIGN KEY (`id_disponibilidad`) REFERENCES `disponibilidad` (`id`);

--
-- Filtros para la tabla `anuncio_tarea`
--
ALTER TABLE `anuncio_tarea`
  ADD CONSTRAINT `FK_anuncio_tarea_anuncio` FOREIGN KEY (`id_anuncio`) REFERENCES `anuncio` (`id`),
  ADD CONSTRAINT `FK_anuncio_tarea_tarea` FOREIGN KEY (`id_tarea`) REFERENCES `tarea` (`id`);

--
-- Filtros para la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD CONSTRAINT `FK_empleado_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`);

--
-- Filtros para la tabla `empleador`
--
ALTER TABLE `empleador`
  ADD CONSTRAINT `FK_empleador_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`);

--
-- Filtros para la tabla `empleado_disponibilidad`
--
ALTER TABLE `empleado_disponibilidad`
  ADD CONSTRAINT `FK_empleado_disponibilidad_disponibilidad` FOREIGN KEY (`id_disponibilidad`) REFERENCES `disponibilidad` (`id`),
  ADD CONSTRAINT `FK_empleado_disponibilidad_empleado` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id`);

--
-- Filtros para la tabla `empleado_tarea`
--
ALTER TABLE `empleado_tarea`
  ADD CONSTRAINT `FK_empleado_tarea_empleado` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id`),
  ADD CONSTRAINT `FK_empleado_tarea_tarea` FOREIGN KEY (`id_tarea`) REFERENCES `tarea` (`id`);

--
-- Filtros para la tabla `postulacion`
--
ALTER TABLE `postulacion`
  ADD CONSTRAINT `FK_postulacion_anuncio` FOREIGN KEY (`id_anuncio`) REFERENCES `anuncio` (`id`),
  ADD CONSTRAINT `FK_postulacion_empleado` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id`);

--
-- Filtros para la tabla `referencia`
--
ALTER TABLE `referencia`
  ADD CONSTRAINT `FK_referencia_empleado` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id`);

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `FK_usuario_tipo` FOREIGN KEY (`id_tipo`) REFERENCES `tipo_usuario` (`id`);

--
-- Filtros para la tabla `vinculo`
--
ALTER TABLE `vinculo`
  ADD CONSTRAINT `FK_vinculo_anuncio` FOREIGN KEY (`id_anuncio`) REFERENCES `anuncio` (`id`),
  ADD CONSTRAINT `FK_vinculo_empleado` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id`),
  ADD CONSTRAINT `FK_vinculo_empleador` FOREIGN KEY (`id_empleador`) REFERENCES `empleador` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
