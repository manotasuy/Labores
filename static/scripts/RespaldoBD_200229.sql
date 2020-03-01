-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: remotemysql.com    Database: LvP2Ka0CsK
-- ------------------------------------------------------
-- Server version	8.0.13-4

USE LvP2Ka0CsK;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `anuncio`
--

DROP TABLE IF EXISTS `anuncio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anuncio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8_unicode_ci,
  `fecha_inicio` date NOT NULL,
  `fecha_cierre` date DEFAULT NULL,
  `estado` bit(1) NOT NULL, -- 0:Inactivo, 1:Activo
  `experiencia` tinyint(1) NOT NULL,
  `salario` int(11) DEFAULT NULL,
  `id_empleador` int(11) NOT NULL,
  `calificacion_empleado` double DEFAULT NULL,
  `calificacion_empleador` double DEFAULT NULL,
  `tiene_vinculo` boolean NULL,
  PRIMARY KEY (`id`),
  KEY `FK_anuncio_empleador` (`id_empleador`),
  CONSTRAINT `FK_anuncio_empleador` FOREIGN KEY (`id_empleador`) REFERENCES `empleador` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anuncio`
--

LOCK TABLES `anuncio` WRITE;
/*!40000 ALTER TABLE `anuncio` DISABLE KEYS */;
/*!40000 ALTER TABLE `anuncio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anuncio_disponibilidad`
--

DROP TABLE IF EXISTS `anuncio_disponibilidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anuncio_disponibilidad` (
  `id_anuncio` int(11) NOT NULL,
  `id_disponibilidad` int(11) NOT NULL,
  PRIMARY KEY (`id_anuncio`,`id_disponibilidad`),
  KEY `FK_anuncio_disponibilidad_disponibilidad` (`id_disponibilidad`),
  CONSTRAINT `FK_anuncio_disponibilidad_anuncio` FOREIGN KEY (`id_anuncio`) REFERENCES `anuncio` (`id`),
  CONSTRAINT `FK_anuncio_disponibilidad_disponibilidad` FOREIGN KEY (`id_disponibilidad`) REFERENCES `disponibilidad` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anuncio_disponibilidad`
--

LOCK TABLES `anuncio_disponibilidad` WRITE;
/*!40000 ALTER TABLE `anuncio_disponibilidad` DISABLE KEYS */;
/*!40000 ALTER TABLE `anuncio_disponibilidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anuncio_tarea`
--

DROP TABLE IF EXISTS `anuncio_tarea`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anuncio_tarea` (
  `id_anuncio` int(11) NOT NULL,
  `id_tarea` int(11) NOT NULL,
  PRIMARY KEY (`id_anuncio`,`id_tarea`),
  KEY `FK_anuncio_tarea_tarea` (`id_tarea`),
  CONSTRAINT `FK_anuncio_tarea_anuncio` FOREIGN KEY (`id_anuncio`) REFERENCES `anuncio` (`id`),
  CONSTRAINT `FK_anuncio_tarea_tarea` FOREIGN KEY (`id_tarea`) REFERENCES `tarea` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anuncio_tarea`
--

LOCK TABLES `anuncio_tarea` WRITE;
/*!40000 ALTER TABLE `anuncio_tarea` DISABLE KEYS */;
/*!40000 ALTER TABLE `anuncio_tarea` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `disponibilidad`
--

DROP TABLE IF EXISTS `disponibilidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `disponibilidad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `disponibilidad`
--

LOCK TABLES `disponibilidad` WRITE;
/*!40000 ALTER TABLE `disponibilidad` DISABLE KEYS */;
INSERT INTO `disponibilidad` (`id`, `descripcion`) VALUES (1,'Por Hora'),(2,'Por Jornada'),(3,'Por Tarea Puntual'),(4,'Por Mes');
/*!40000 ALTER TABLE `disponibilidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleado`
--

DROP TABLE IF EXISTS `empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
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
  `promedio_calificacion` double DEFAULT NULL,
  `id_usuario` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_empleador` (`cedula`),
  KEY `FK_empleado_usuario` (`id_usuario`),
  CONSTRAINT `FK_empleado_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleado`
--

LOCK TABLES `empleado` WRITE;
/*!40000 ALTER TABLE `empleado` DISABLE KEYS */;
/*!40000 ALTER TABLE `empleado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleado_disponibilidad`
--

DROP TABLE IF EXISTS `empleado_disponibilidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleado_disponibilidad` (
  `id_empleado` int(11) NOT NULL,
  `id_disponibilidad` int(11) NOT NULL,
  PRIMARY KEY (`id_empleado`,`id_disponibilidad`),
  KEY `FK_empleado_disponibilidad_disponibilidad` (`id_disponibilidad`),
  CONSTRAINT `FK_empleado_disponibilidad_disponibilidad` FOREIGN KEY (`id_disponibilidad`) REFERENCES `disponibilidad` (`id`),
  CONSTRAINT `FK_empleado_disponibilidad_empleado` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleado_disponibilidad`
--

LOCK TABLES `empleado_disponibilidad` WRITE;
/*!40000 ALTER TABLE `empleado_disponibilidad` DISABLE KEYS */;
/*!40000 ALTER TABLE `empleado_disponibilidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleado_tarea`
--

DROP TABLE IF EXISTS `empleado_tarea`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleado_tarea` (
  `id_empleado` int(11) NOT NULL,
  `id_tarea` int(11) NOT NULL,
  PRIMARY KEY (`id_empleado`,`id_tarea`),
  KEY `FK_empleado_tarea_tarea` (`id_tarea`),
  CONSTRAINT `FK_empleado_tarea_empleado` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id`),
  CONSTRAINT `FK_empleado_tarea_tarea` FOREIGN KEY (`id_tarea`) REFERENCES `tarea` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleado_tarea`
--

LOCK TABLES `empleado_tarea` WRITE;
/*!40000 ALTER TABLE `empleado_tarea` DISABLE KEYS */;
/*!40000 ALTER TABLE `empleado_tarea` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleador`
--

DROP TABLE IF EXISTS `empleador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleador` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
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
  `promedio_calificacion` double DEFAULT NULL,
  `id_usuario` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_empleador` (`cedula`),
  KEY `FK_empleador_usuario` (`id_usuario`),
  CONSTRAINT `FK_empleador_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleador`
--

LOCK TABLES `empleador` WRITE;
/*!40000 ALTER TABLE `empleador` DISABLE KEYS */;
/*!40000 ALTER TABLE `empleador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `postulacion`
--

DROP TABLE IF EXISTS `postulacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `postulacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_empleado` int(11) NOT NULL,
  `id_anuncio` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `mensaje` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `genera_vinculo` boolean NULL,
  PRIMARY KEY (`id`),
  KEY `FK_postulacion_empleado` (`id_empleado`),
  KEY `FK_postulacion_anuncio` (`id_anuncio`),
  CONSTRAINT `FK_postulacion_anuncio` FOREIGN KEY (`id_anuncio`) REFERENCES `anuncio` (`id`),
  CONSTRAINT `FK_postulacion_empleado` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `postulacion`
--

LOCK TABLES `postulacion` WRITE;
/*!40000 ALTER TABLE `postulacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `postulacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `referencia`
--

DROP TABLE IF EXISTS `referencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `referencia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_empleado` int(11) NOT NULL,
  `nombre` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_desde` date NOT NULL,
  `fecha_hasta` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_referencia_empleado` (`id_empleado`),
  CONSTRAINT `FK_referencia_empleado` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `referencia`
--

LOCK TABLES `referencia` WRITE;
/*!40000 ALTER TABLE `referencia` DISABLE KEYS */;
/*!40000 ALTER TABLE `referencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tarea`
--

DROP TABLE IF EXISTS `tarea`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tarea` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarea`
--

LOCK TABLES `tarea` WRITE;
/*!40000 ALTER TABLE `tarea` DISABLE KEYS */;
INSERT INTO `tarea` (`id`, `descripcion`) VALUES (1,'Hogar'),(2,'Oficina'),(3,'Cocinar'),(4,'Limpieza de Baños'),(5,'Limpieza de Cocinas'),(6,'Limpieza de Dormitorios'),(7,'Cuidado de Niños'),(8,'Cuidado de Bebés'),(9,'Cuidado de Adultos Mayores'),(10,'Cuidado de Mascotas');
/*!40000 ALTER TABLE `tarea` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_usuario`
--

DROP TABLE IF EXISTS `tipo_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_tipo_usuario` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_usuario`
--

LOCK TABLES `tipo_usuario` WRITE;
/*!40000 ALTER TABLE `tipo_usuario` DISABLE KEYS */;
INSERT INTO `tipo_usuario` (`id`, `nombre`) VALUES (1,'Administrador'),(3,'Empleado'),(2,'Empleador');
/*!40000 ALTER TABLE `tipo_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `clave` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `id_tipo` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_usuario` (`usuario`),
  KEY `FK_usuario_tipo` (`id_tipo`),
  KEY `IDXuser` (`usuario`),
  CONSTRAINT `FK_usuario_tipo` FOREIGN KEY (`id_tipo`) REFERENCES `tipo_usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` (`id`, `usuario`, `clave`, `id_tipo`) VALUES (1,'admin','admin',1),(2,'jefe','jefe',2),(3,'peon','peon',3);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vinculo`
--

DROP TABLE IF EXISTS `vinculo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vinculo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_empleado` int(11) NOT NULL,
  `id_empleador` int(11) NOT NULL,
  `id_anuncio` int(11) NOT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `motivo_fin` text COLLATE utf8_unicode_ci,
  `descripcion` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `calificacion_empleado` double DEFAULT NULL,
  `calificacion_empleador` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_vinculo_empleado` (`id_empleado`),
  KEY `FK_vinculo_empleador` (`id_empleador`),
  KEY `FK_vinculo_anuncio` (`id_anuncio`),
  CONSTRAINT `FK_vinculo_anuncio` FOREIGN KEY (`id_anuncio`) REFERENCES `anuncio` (`id`),
  CONSTRAINT `FK_vinculo_empleado` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id`),
  CONSTRAINT `FK_vinculo_empleador` FOREIGN KEY (`id_empleador`) REFERENCES `empleador` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vinculo`
--

LOCK TABLES `vinculo` WRITE;
/*!40000 ALTER TABLE `vinculo` DISABLE KEYS */;
/*!40000 ALTER TABLE `vinculo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-29 12:27:22
