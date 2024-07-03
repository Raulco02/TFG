-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: smartesi
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `acciones`
--

DROP TABLE IF EXISTS `acciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `acciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acciones`
--

LOCK TABLES `acciones` WRITE;
/*!40000 ALTER TABLE `acciones` DISABLE KEYS */;
INSERT INTO `acciones` VALUES (1,'SET'),(2,'ALERT');
/*!40000 ALTER TABLE `acciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acciones-reglas`
--

DROP TABLE IF EXISTS `acciones-reglas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `acciones-reglas` (
  `regla_id` int NOT NULL,
  `atributo_id` int DEFAULT NULL,
  `dispositivo_id` varchar(255) DEFAULT NULL,
  `accion_id` int NOT NULL,
  `valor_accion` varchar(255) NOT NULL,
  KEY `fk_regla_id_disparador_idx` (`regla_id`),
  KEY `fk_atributo_id_accion_idx` (`atributo_id`),
  KEY `fk_dispositivo_id_accion_idx` (`dispositivo_id`),
  KEY `fk_id_accion_reglas_idx` (`accion_id`),
  CONSTRAINT `fk_atributo_id_accion` FOREIGN KEY (`atributo_id`) REFERENCES `atributos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_dispositivo_id_accion` FOREIGN KEY (`dispositivo_id`) REFERENCES `dispositivos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_id_accion_reglas` FOREIGN KEY (`accion_id`) REFERENCES `acciones` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_regla_id_accion` FOREIGN KEY (`regla_id`) REFERENCES `reglas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acciones-reglas`
--

LOCK TABLES `acciones-reglas` WRITE;
/*!40000 ALTER TABLE `acciones-reglas` DISABLE KEYS */;
INSERT INTO `acciones-reglas` VALUES (8,87,'Shelly TRV ',1,'12'),(9,87,'Shelly TRV ',1,'1'),(11,87,'Shelly TRV ',2,'12');
/*!40000 ALTER TABLE `acciones-reglas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `atributos`
--

DROP TABLE IF EXISTS `atributos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `atributos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `unidades` varchar(5) NOT NULL,
  `actuable` varchar(5) NOT NULL DEFAULT 'false',
  `tipo` int NOT NULL,
  `icono` varchar(255) DEFAULT NULL,
  `limite_superior` float DEFAULT NULL,
  `limite_inferior` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `nombre_UNIQUE` (`nombre`),
  KEY `fk_tipo_atributo_idx` (`tipo`),
  CONSTRAINT `fk_tipo_atributo` FOREIGN KEY (`tipo`) REFERENCES `tipos_atributos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=337 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `atributos`
--

LOCK TABLES `atributos` WRITE;
/*!40000 ALTER TABLE `atributos` DISABLE KEYS */;
INSERT INTO `atributos` VALUES (1,'Temperatura','ºC','false',1,'Temperatura',25,17),(2,'CO2','ppm','false',1,'CO2',NULL,NULL),(3,'Humedad','%','false',1,'Humedad',40,15),(4,'Lux','Lux','false',1,'Luz',NULL,NULL),(8,'Batería','%','false',1,'Bateria',50,30),(40,'a','a','false',1,NULL,NULL,NULL),(49,'Temperaturaa','ºC','true',1,NULL,NULL,NULL),(53,'Atributo actuable','%','true',1,NULL,NULL,NULL),(55,'Atributo no actuable','%','false',1,NULL,NULL,NULL),(56,'Atributo no actuable 2','%','false',1,NULL,NULL,NULL),(57,'Atributo actuable 2','%','true',1,NULL,NULL,NULL),(58,'Atributo no actuable 3','%','false',1,NULL,NULL,NULL),(59,'Atributo actuable 3','%','true',1,NULL,NULL,NULL),(66,'Atributo web 1','ºC','false',1,NULL,NULL,NULL),(68,'Atributo web x','ºC','false',1,NULL,NULL,NULL),(70,'edqwd','wed','false',1,NULL,NULL,NULL),(72,'qxzqwxq','q','false',1,NULL,NULL,NULL),(74,'qxdwdx','XD','false',1,NULL,NULL,NULL),(75,'fwerfcws','wed','false',1,NULL,NULL,NULL),(76,'xwexcdewed','cw','true',1,NULL,NULL,NULL),(77,'wcxwecwewe','wcec','false',1,NULL,NULL,NULL),(78,'dwecascx','cxwd','true',1,NULL,NULL,NULL),(87,'Temperatura objetivo','ºC','true',2,'Temperatura_Obj',NULL,NULL),(197,'Atributo actuable o no','%','false',1,NULL,NULL,NULL),(198,'Atributo no actuable o sí','%','true',1,NULL,NULL,NULL),(200,'Otro disitnito tambien','%','true',1,'Temperatura',NULL,NULL),(202,'Otro disitnvwrfwito tambien','%','true',1,NULL,NULL,NULL),(203,'Otro  tambien','%','true',1,NULL,19.5,NULL),(205,'Otro  tambxdtnhxien','%','true',1,NULL,19.5,18.5),(206,'Otro  sdfcs','%','true',1,NULL,19.5,18.5),(207,'Holiwi','a','false',1,'info',2,1),(208,'elnrvlk','wex','false',1,'account_circle',4,3),(209,'atributo1','units','false',1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `atributos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `criterios`
--

DROP TABLE IF EXISTS `criterios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `criterios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `regla_id` int NOT NULL,
  `atributo_id` int NOT NULL,
  `dispositivo_id` varchar(255) NOT NULL,
  `valor` decimal(10,2) NOT NULL,
  `comparador` enum('<','>','=') NOT NULL,
  `tipo` enum('d','c') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_regla_id_disparador_idx` (`regla_id`),
  KEY `fk_atributo_id_disparador_idx` (`atributo_id`),
  KEY `fk_dispositivo_id_disparador_idx` (`dispositivo_id`),
  CONSTRAINT `fk_atributo_id_disparador` FOREIGN KEY (`atributo_id`) REFERENCES `atributos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_dispositivo_id_disparador` FOREIGN KEY (`dispositivo_id`) REFERENCES `dispositivos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_regla_id_disparador` FOREIGN KEY (`regla_id`) REFERENCES `reglas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `criterios`
--

LOCK TABLES `criterios` WRITE;
/*!40000 ALTER TABLE `criterios` DISABLE KEYS */;
INSERT INTO `criterios` VALUES (12,8,1,'Shelly TRV ',30.00,'<','d'),(13,8,3,'Shelly1',45.00,'>','c'),(14,9,1,'Shelly 6',12.00,'>','d'),(15,9,3,'Shelly1',14.00,'<','c'),(20,11,1,'Shelly TRV ',30.00,'>','d'),(21,11,3,'Shelly1',45.00,'>','c');
/*!40000 ALTER TABLE `criterios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard-seccion`
--

DROP TABLE IF EXISTS `dashboard-seccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard-seccion` (
  `id-dashboard` int NOT NULL,
  `id-seccion` int NOT NULL,
  PRIMARY KEY (`id-dashboard`,`id-seccion`),
  KEY `fk_id_seccion_dashboard_idx` (`id-seccion`),
  CONSTRAINT `fk_id_dashboard_seccion` FOREIGN KEY (`id-dashboard`) REFERENCES `dashboards` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_id_seccion_dashboard` FOREIGN KEY (`id-seccion`) REFERENCES `secciones` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard-seccion`
--

LOCK TABLES `dashboard-seccion` WRITE;
/*!40000 ALTER TABLE `dashboard-seccion` DISABLE KEYS */;
INSERT INTO `dashboard-seccion` VALUES (6,1),(5,2),(6,3),(4,4),(5,5),(4,6),(5,7),(4,8),(6,9),(5,10),(6,11),(8,12),(11,13),(6,14),(2,15),(4,16),(4,17),(5,18),(5,19),(5,20),(5,21),(7,22),(5,23),(4,24),(4,25),(5,26),(1,27),(4,28),(6,29),(14,30),(15,31),(15,32),(15,33),(15,34),(15,35),(15,36),(8,37),(8,38),(8,39),(15,40),(15,41),(15,42),(15,43),(8,44),(8,45),(21,51),(25,53),(26,54),(28,55),(31,56),(33,57),(35,58),(38,59),(40,60),(42,61),(43,62),(44,63),(45,64),(46,65),(47,66),(48,67),(49,68),(50,69),(51,70),(52,71),(53,72),(54,73),(55,74),(56,75),(57,76),(58,77),(59,78),(60,79),(61,80),(62,81),(63,82),(64,83),(65,84),(66,85),(67,86),(68,87),(69,88),(70,89),(71,90),(72,91),(73,92),(74,93),(75,94),(76,95),(77,96),(78,97),(79,98),(80,99),(81,100),(82,101),(83,102),(84,103),(85,104),(86,105),(87,106),(88,107),(89,108),(91,110),(92,111),(93,112),(94,113),(95,114),(96,115),(97,116),(98,117),(99,118),(101,120),(102,121),(103,122),(104,123),(105,124),(106,125),(107,126),(108,127),(110,129),(111,130),(112,131),(113,132),(114,133),(115,134),(116,135),(117,136),(118,137),(120,139),(121,140),(122,141),(123,142),(124,143),(125,144),(126,145),(127,146),(129,148),(130,149),(131,150),(132,151),(133,152),(134,153),(135,154),(136,155),(138,157),(139,158),(140,159),(141,160),(142,161),(143,162),(144,163),(145,164),(147,166),(148,167),(149,168),(150,169),(151,170),(152,171),(153,172),(154,173),(156,175),(157,176),(158,177),(159,178),(160,179),(161,180),(162,181),(163,182),(165,184),(166,185),(167,186),(168,187),(169,188),(170,189),(171,190),(172,191),(173,192),(174,193),(175,194),(176,195),(178,197),(179,198),(180,199),(181,200),(182,201),(183,202),(184,203),(185,204),(186,205),(187,206),(188,207),(189,208),(191,210),(192,211),(193,212),(194,213),(195,214),(196,215),(197,216),(198,217),(199,218),(200,219),(201,220),(202,221),(203,222),(205,224),(206,225),(207,226),(208,227),(208,228),(209,229),(210,230),(211,231),(212,232),(213,233),(214,234),(215,235),(216,236),(217,237),(218,238),(220,240),(221,241),(222,242),(223,243),(223,244),(224,245),(225,246),(226,247),(227,248),(228,249),(229,250),(230,251),(231,252),(232,253),(233,254),(234,255),(235,256),(237,258),(238,259),(239,260),(240,261),(240,262),(241,263),(242,264),(243,265),(244,266),(245,267),(246,268),(247,269),(248,270),(249,271),(250,272),(251,273),(252,274),(254,276),(255,277),(256,278),(257,279),(257,280),(258,281),(259,282),(260,283),(261,284),(262,285),(263,286),(264,287),(265,288),(266,289),(267,290),(268,291),(269,292),(271,294),(272,295),(273,296),(274,297),(274,298),(275,299),(276,300),(277,301),(278,302),(279,303),(280,304),(281,305),(282,306),(283,307),(284,308),(285,309),(287,311),(288,312),(289,313),(290,314),(290,315),(291,316),(292,317),(293,318),(294,319),(295,320),(296,321),(297,322),(298,323),(299,324),(300,325),(301,326),(303,328),(304,329),(305,330),(306,331),(306,332),(307,333),(308,334),(309,335),(310,336),(311,337),(312,338),(313,339),(314,340),(315,341),(316,342),(317,343),(319,345),(320,346),(321,347),(322,348),(322,349),(323,350),(324,351),(325,352),(326,353),(327,354),(328,355),(329,356),(330,357),(331,358),(332,359),(333,360),(335,362),(336,363),(337,364),(338,365),(338,366),(339,367),(340,368),(341,369),(342,370),(343,371),(344,372),(345,373),(346,374),(347,375),(348,376),(349,377),(351,379),(352,380),(353,381),(354,382),(354,383),(355,384),(356,385),(357,386),(358,387),(359,388),(360,389),(361,390),(362,391),(363,392),(364,393),(365,394),(366,395),(367,396),(369,398),(370,399),(371,400),(372,401),(372,402),(373,403),(374,404),(375,405),(376,406),(377,407),(378,408),(379,409),(380,410),(381,411),(382,412),(383,413),(384,414),(386,416),(387,417),(388,418),(389,419),(389,420),(390,421),(391,422),(392,423),(393,424),(394,425),(395,426),(396,427),(397,428),(398,429),(399,430),(400,431),(401,432),(403,434),(404,435),(405,436),(406,437),(406,438),(407,439),(408,440),(409,441),(410,442),(411,443),(412,444),(413,445),(414,446),(415,447),(416,448),(417,449),(418,450),(420,452),(421,453),(422,454),(423,455),(423,456),(424,457),(425,458),(426,459),(427,460),(428,461),(429,462),(430,463),(431,464),(432,465),(433,466),(434,467),(435,468),(436,469),(437,470),(439,472),(440,473),(441,474),(442,475),(442,476),(443,477),(444,478),(445,479),(446,480),(447,481),(448,482);
/*!40000 ALTER TABLE `dashboard-seccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboards`
--

DROP TABLE IF EXISTS `dashboards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(25) NOT NULL,
  `icono` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=449 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboards`
--

LOCK TABLES `dashboards` WRITE;
/*!40000 ALTER TABLE `dashboards` DISABLE KEYS */;
INSERT INTO `dashboards` VALUES (1,'Dashboard 1','home'),(2,'Dashboard 1','home'),(4,'Nuevo dashboard','home'),(5,'Dashboard1','info'),(6,'Dashboard2','account_circle'),(7,'Otro','home'),(8,'Dashboard3','home'),(9,'Dashboard4','info'),(10,'Dashboard5','home'),(11,'Dashboard 1','home'),(14,'Nuevo dashboard','dashboard'),(15,'Dashboard4','home'),(21,'Dashboard5','add'),(25,'New Dashboard','icon.png'),(26,'New Dashboard','icon.png'),(28,'Nuevo dashboard','dashboard'),(31,'Nuevo dashboard','dashboard'),(33,'Nuevo dashboard','dashboard'),(35,'Nuevo dashboard','dashboard'),(38,'Nuevo dashboard','dashboard'),(40,'Nuevo dashboard','dashboard'),(42,'Nuevo dashboard','dashboard'),(43,'Nuevo dashboard','dashboard'),(44,'New Dashboard','icon.png'),(45,'New Dashboard','icon.png'),(46,'Nuevo dashboard','dashboard'),(47,'New Dashboard','icon.png'),(48,'Nuevo dashboard','dashboard'),(49,'Nuevo dashboard','dashboard'),(50,'Nuevo dashboard','dashboard'),(51,'Nuevo dashboard','dashboard'),(52,'New Dashboard','icon.png'),(53,'Nuevo dashboard','dashboard'),(54,'Nuevo dashboard','dashboard'),(55,'Nuevo dashboard','dashboard'),(56,'Nuevo dashboard','dashboard'),(57,'Nuevo dashboard','dashboard'),(58,'New Dashboard','icon.png'),(59,'Nuevo dashboard','dashboard'),(60,'Nuevo dashboard','dashboard'),(61,'Nuevo dashboard','dashboard'),(62,'Nuevo dashboard','dashboard'),(63,'Nuevo dashboard','dashboard'),(64,'New Dashboard','icon.png'),(65,'Nuevo dashboard','dashboard'),(66,'Nuevo dashboard','dashboard'),(67,'New Dashboard','icon.png'),(68,'Nuevo dashboard','dashboard'),(69,'Nuevo dashboard','dashboard'),(70,'New Dashboard','icon.png'),(71,'Nuevo dashboard','dashboard'),(72,'Nuevo dashboard','dashboard'),(73,'New Dashboard','icon.png'),(74,'Nuevo dashboard','dashboard'),(75,'Nuevo dashboard','dashboard'),(76,'New Dashboard','icon.png'),(77,'Nuevo dashboard','dashboard'),(78,'Nuevo dashboard','dashboard'),(79,'Edited Dashboard','new_icon.png'),(80,'Nuevo dashboard','dashboard'),(81,'Nuevo dashboard','dashboard'),(82,'Nuevo dashboard','dashboard'),(83,'Nuevo dashboard','dashboard'),(84,'New Dashboard','icon.png'),(85,'Nuevo dashboard','dashboard'),(86,'Nuevo dashboard','dashboard'),(87,'Edited Dashboard','new_icon.png'),(88,'Nuevo dashboard','dashboard'),(89,'Nuevo dashboard','dashboard'),(91,'Nuevo dashboard','dashboard'),(92,'Nuevo dashboard','dashboard'),(93,'Nuevo dashboard','dashboard'),(94,'New Dashboard','icon.png'),(95,'Nuevo dashboard','dashboard'),(96,'Nuevo dashboard','dashboard'),(97,'Edited Dashboard','new_icon.png'),(98,'Nuevo dashboard','dashboard'),(99,'Nuevo dashboard','dashboard'),(101,'Nuevo dashboard','dashboard'),(102,'Nuevo dashboard','dashboard'),(103,'New Dashboard','icon.png'),(104,'Nuevo dashboard','dashboard'),(105,'Nuevo dashboard','dashboard'),(106,'Edited Dashboard','new_icon.png'),(107,'Nuevo dashboard','dashboard'),(108,'Nuevo dashboard','dashboard'),(110,'Nuevo dashboard','dashboard'),(111,'Nuevo dashboard','dashboard'),(112,'Nuevo dashboard','dashboard'),(113,'New Dashboard','icon.png'),(114,'Nuevo dashboard','dashboard'),(115,'Nuevo dashboard','dashboard'),(116,'Edited Dashboard','new_icon.png'),(117,'Nuevo dashboard','dashboard'),(118,'Nuevo dashboard','dashboard'),(120,'Nuevo dashboard','dashboard'),(121,'Nuevo dashboard','dashboard'),(122,'New Dashboard','icon.png'),(123,'Nuevo dashboard','dashboard'),(124,'Nuevo dashboard','dashboard'),(125,'Edited Dashboard','new_icon.png'),(126,'Nuevo dashboard','dashboard'),(127,'Nuevo dashboard','dashboard'),(129,'Nuevo dashboard','dashboard'),(130,'Nuevo dashboard','dashboard'),(131,'New Dashboard','icon.png'),(132,'Nuevo dashboard','dashboard'),(133,'Nuevo dashboard','dashboard'),(134,'Edited Dashboard','new_icon.png'),(135,'Nuevo dashboard','dashboard'),(136,'Nuevo dashboard','dashboard'),(138,'Nuevo dashboard','dashboard'),(139,'Nuevo dashboard','dashboard'),(140,'New Dashboard','icon.png'),(141,'Nuevo dashboard','dashboard'),(142,'Nuevo dashboard','dashboard'),(143,'Edited Dashboard','new_icon.png'),(144,'Nuevo dashboard','dashboard'),(145,'Nuevo dashboard','dashboard'),(147,'Nuevo dashboard','dashboard'),(148,'Nuevo dashboard','dashboard'),(149,'New Dashboard','icon.png'),(150,'Nuevo dashboard','dashboard'),(151,'Nuevo dashboard','dashboard'),(152,'Edited Dashboard','new_icon.png'),(153,'Nuevo dashboard','dashboard'),(154,'Nuevo dashboard','dashboard'),(156,'Nuevo dashboard','dashboard'),(157,'Nuevo dashboard','dashboard'),(158,'New Dashboard','icon.png'),(159,'Nuevo dashboard','dashboard'),(160,'Nuevo dashboard','dashboard'),(161,'Edited Dashboard','new_icon.png'),(162,'Nuevo dashboard','dashboard'),(163,'Nuevo dashboard','dashboard'),(165,'Nuevo dashboard','dashboard'),(166,'Nuevo dashboard','dashboard'),(167,'Nuevo dashboard','dashboard'),(168,'Nuevo dashboard','dashboard'),(169,'Nuevo dashboard','dashboard'),(170,'Nuevo dashboard','dashboard'),(171,'New Dashboard','icon.png'),(172,'Nuevo dashboard','dashboard'),(173,'Nuevo dashboard','dashboard'),(174,'Edited Dashboard','new_icon.png'),(175,'Nuevo dashboard','dashboard'),(176,'Nuevo dashboard','dashboard'),(178,'Nuevo dashboard','dashboard'),(179,'Nuevo dashboard','dashboard'),(180,'Nuevo dashboard','dashboard'),(181,'Nuevo dashboard','dashboard'),(182,'Nuevo dashboard','dashboard'),(183,'Nuevo dashboard','dashboard'),(184,'New Dashboard','icon.png'),(185,'Nuevo dashboard','dashboard'),(186,'Nuevo dashboard','dashboard'),(187,'Edited Dashboard','new_icon.png'),(188,'Nuevo dashboard','dashboard'),(189,'Nuevo dashboard','dashboard'),(191,'Nuevo dashboard','dashboard'),(192,'Nuevo dashboard','dashboard'),(193,'Nuevo dashboard','dashboard'),(194,'Nuevo dashboard','dashboard'),(195,'Nuevo dashboard','dashboard'),(196,'Nuevo dashboard','dashboard'),(197,'Nuevo dashboard','dashboard'),(198,'New Dashboard','icon.png'),(199,'Nuevo dashboard','dashboard'),(200,'Nuevo dashboard','dashboard'),(201,'Edited Dashboard','new_icon.png'),(202,'Nuevo dashboard','dashboard'),(203,'Nuevo dashboard','dashboard'),(205,'Nuevo dashboard','dashboard'),(206,'Nuevo dashboard','dashboard'),(207,'Nuevo dashboard','dashboard'),(208,'Nuevo dashboard','dashboard'),(209,'Nuevo dashboard','dashboard'),(210,'Nuevo dashboard','dashboard'),(211,'Nuevo dashboard','dashboard'),(212,'Nuevo dashboard','dashboard'),(213,'New Dashboard','icon.png'),(214,'Nuevo dashboard','dashboard'),(215,'Nuevo dashboard','dashboard'),(216,'Edited Dashboard','new_icon.png'),(217,'Nuevo dashboard','dashboard'),(218,'Nuevo dashboard','dashboard'),(220,'Nuevo dashboard','dashboard'),(221,'Nuevo dashboard','dashboard'),(222,'Nuevo dashboard','dashboard'),(223,'Nuevo dashboard','dashboard'),(224,'Nuevo dashboard','dashboard'),(225,'Nuevo dashboard','dashboard'),(226,'Nuevo dashboard','dashboard'),(227,'Nuevo dashboard','dashboard'),(228,'Nuevo dashboard','dashboard'),(229,'Nuevo dashboard','dashboard'),(230,'New Dashboard','icon.png'),(231,'Nuevo dashboard','dashboard'),(232,'Nuevo dashboard','dashboard'),(233,'Edited Dashboard','new_icon.png'),(234,'Nuevo dashboard','dashboard'),(235,'Nuevo dashboard','dashboard'),(237,'Nuevo dashboard','dashboard'),(238,'Nuevo dashboard','dashboard'),(239,'Nuevo dashboard','dashboard'),(240,'Nuevo dashboard','dashboard'),(241,'Nuevo dashboard','dashboard'),(242,'Nuevo dashboard','dashboard'),(243,'Nuevo dashboard','dashboard'),(244,'Nuevo dashboard','dashboard'),(245,'Nuevo dashboard','dashboard'),(246,'Nuevo dashboard','dashboard'),(247,'New Dashboard','icon.png'),(248,'Nuevo dashboard','dashboard'),(249,'Nuevo dashboard','dashboard'),(250,'Edited Dashboard','new_icon.png'),(251,'Nuevo dashboard','dashboard'),(252,'Nuevo dashboard','dashboard'),(254,'Nuevo dashboard','dashboard'),(255,'Nuevo dashboard','dashboard'),(256,'Nuevo dashboard','dashboard'),(257,'Nuevo dashboard','dashboard'),(258,'Nuevo dashboard','dashboard'),(259,'Nuevo dashboard','dashboard'),(260,'Nuevo dashboard','dashboard'),(261,'Nuevo dashboard','dashboard'),(262,'Nuevo dashboard','dashboard'),(263,'Nuevo dashboard','dashboard'),(264,'New Dashboard','icon.png'),(265,'Nuevo dashboard','dashboard'),(266,'Nuevo dashboard','dashboard'),(267,'Edited Dashboard','new_icon.png'),(268,'Nuevo dashboard','dashboard'),(269,'Nuevo dashboard','dashboard'),(271,'Nuevo dashboard','dashboard'),(272,'Nuevo dashboard','dashboard'),(273,'Nuevo dashboard','dashboard'),(274,'Nuevo dashboard','dashboard'),(275,'Nuevo dashboard','dashboard'),(276,'Nuevo dashboard','dashboard'),(277,'Nuevo dashboard','dashboard'),(278,'Nuevo dashboard','dashboard'),(279,'Nuevo dashboard','dashboard'),(280,'New Dashboard','icon.png'),(281,'Nuevo dashboard','dashboard'),(282,'Nuevo dashboard','dashboard'),(283,'Edited Dashboard','new_icon.png'),(284,'Nuevo dashboard','dashboard'),(285,'Nuevo dashboard','dashboard'),(287,'Nuevo dashboard','dashboard'),(288,'Nuevo dashboard','dashboard'),(289,'Nuevo dashboard','dashboard'),(290,'Nuevo dashboard','dashboard'),(291,'Nuevo dashboard','dashboard'),(292,'Nuevo dashboard','dashboard'),(293,'Nuevo dashboard','dashboard'),(294,'Nuevo dashboard','dashboard'),(295,'Nuevo dashboard','dashboard'),(296,'New Dashboard','icon.png'),(297,'Nuevo dashboard','dashboard'),(298,'Nuevo dashboard','dashboard'),(299,'Edited Dashboard','new_icon.png'),(300,'Nuevo dashboard','dashboard'),(301,'Nuevo dashboard','dashboard'),(303,'Nuevo dashboard','dashboard'),(304,'Nuevo dashboard','dashboard'),(305,'Nuevo dashboard','dashboard'),(306,'Nuevo dashboard','dashboard'),(307,'Nuevo dashboard','dashboard'),(308,'Nuevo dashboard','dashboard'),(309,'Nuevo dashboard','dashboard'),(310,'Nuevo dashboard','dashboard'),(311,'Nuevo dashboard','dashboard'),(312,'New Dashboard','icon.png'),(313,'Nuevo dashboard','dashboard'),(314,'Nuevo dashboard','dashboard'),(315,'Edited Dashboard','new_icon.png'),(316,'Nuevo dashboard','dashboard'),(317,'Nuevo dashboard','dashboard'),(319,'Nuevo dashboard','dashboard'),(320,'Nuevo dashboard','dashboard'),(321,'Nuevo dashboard','dashboard'),(322,'Nuevo dashboard','dashboard'),(323,'Nuevo dashboard','dashboard'),(324,'Nuevo dashboard','dashboard'),(325,'Nuevo dashboard','dashboard'),(326,'Nuevo dashboard','dashboard'),(327,'Nuevo dashboard','dashboard'),(328,'New Dashboard','icon.png'),(329,'Nuevo dashboard','dashboard'),(330,'Nuevo dashboard','dashboard'),(331,'Edited Dashboard','new_icon.png'),(332,'Nuevo dashboard','dashboard'),(333,'Nuevo dashboard','dashboard'),(335,'Nuevo dashboard','dashboard'),(336,'Nuevo dashboard','dashboard'),(337,'Nuevo dashboard','dashboard'),(338,'Nuevo dashboard','dashboard'),(339,'Nuevo dashboard','dashboard'),(340,'Nuevo dashboard','dashboard'),(341,'Nuevo dashboard','dashboard'),(342,'Nuevo dashboard','dashboard'),(343,'Nuevo dashboard','dashboard'),(344,'New Dashboard','icon.png'),(345,'Nuevo dashboard','dashboard'),(346,'Nuevo dashboard','dashboard'),(347,'Edited Dashboard','new_icon.png'),(348,'Nuevo dashboard','dashboard'),(349,'Nuevo dashboard','dashboard'),(351,'Nuevo dashboard','dashboard'),(352,'Nuevo dashboard','dashboard'),(353,'Nuevo dashboard','dashboard'),(354,'Nuevo dashboard','dashboard'),(355,'Nuevo dashboard','dashboard'),(356,'Nuevo dashboard','dashboard'),(357,'Nuevo dashboard','dashboard'),(358,'Nuevo dashboard','dashboard'),(359,'Nuevo dashboard','dashboard'),(360,'Nuevo dashboard','dashboard'),(361,'Nuevo dashboard','dashboard'),(362,'New Dashboard','icon.png'),(363,'Nuevo dashboard','dashboard'),(364,'Nuevo dashboard','dashboard'),(365,'Edited Dashboard','new_icon.png'),(366,'Nuevo dashboard','dashboard'),(367,'Nuevo dashboard','dashboard'),(369,'Nuevo dashboard','dashboard'),(370,'Nuevo dashboard','dashboard'),(371,'Nuevo dashboard','dashboard'),(372,'Nuevo dashboard','dashboard'),(373,'Nuevo dashboard','dashboard'),(374,'Nuevo dashboard','dashboard'),(375,'Nuevo dashboard','dashboard'),(376,'Nuevo dashboard','dashboard'),(377,'Nuevo dashboard','dashboard'),(378,'Nuevo dashboard','dashboard'),(379,'New Dashboard','icon.png'),(380,'Nuevo dashboard','dashboard'),(381,'Nuevo dashboard','dashboard'),(382,'Edited Dashboard','new_icon.png'),(383,'Nuevo dashboard','dashboard'),(384,'Nuevo dashboard','dashboard'),(386,'Nuevo dashboard','dashboard'),(387,'Nuevo dashboard','dashboard'),(388,'Nuevo dashboard','dashboard'),(389,'Nuevo dashboard','dashboard'),(390,'Nuevo dashboard','dashboard'),(391,'Nuevo dashboard','dashboard'),(392,'Nuevo dashboard','dashboard'),(393,'Nuevo dashboard','dashboard'),(394,'Nuevo dashboard','dashboard'),(395,'Nuevo dashboard','dashboard'),(396,'New Dashboard','icon.png'),(397,'Nuevo dashboard','dashboard'),(398,'Nuevo dashboard','dashboard'),(399,'Edited Dashboard','new_icon.png'),(400,'Nuevo dashboard','dashboard'),(401,'Nuevo dashboard','dashboard'),(403,'Nuevo dashboard','dashboard'),(404,'Nuevo dashboard','dashboard'),(405,'Nuevo dashboard','dashboard'),(406,'Nuevo dashboard','dashboard'),(407,'Nuevo dashboard','dashboard'),(408,'Nuevo dashboard','dashboard'),(409,'Nuevo dashboard','dashboard'),(410,'Nuevo dashboard','dashboard'),(411,'Nuevo dashboard','dashboard'),(412,'Nuevo dashboard','dashboard'),(413,'New Dashboard','icon.png'),(414,'Nuevo dashboard','dashboard'),(415,'Nuevo dashboard','dashboard'),(416,'Edited Dashboard','new_icon.png'),(417,'Nuevo dashboard','dashboard'),(418,'Nuevo dashboard','dashboard'),(420,'Nuevo dashboard','dashboard'),(421,'Nuevo dashboard','dashboard'),(422,'Nuevo dashboard','dashboard'),(423,'Nuevo dashboard','dashboard'),(424,'Nuevo dashboard','dashboard'),(425,'Nuevo dashboard','dashboard'),(426,'Nuevo dashboard','dashboard'),(427,'Nuevo dashboard','dashboard'),(428,'Nuevo dashboard','dashboard'),(429,'Nuevo dashboard','dashboard'),(430,'Nuevo dashboard','dashboard'),(431,'Nuevo dashboard','dashboard'),(432,'New Dashboard','icon.png'),(433,'Nuevo dashboard','dashboard'),(434,'Nuevo dashboard','dashboard'),(435,'Edited Dashboard','new_icon.png'),(436,'Nuevo dashboard','dashboard'),(437,'Nuevo dashboard','dashboard'),(439,'Nuevo dashboard','dashboard'),(440,'Nuevo dashboard','dashboard'),(441,'Nuevo dashboard','dashboard'),(442,'Nuevo dashboard','dashboard'),(443,'Nuevo dashboard','dashboard'),(444,'Nuevo dashboard','dashboard'),(445,'Nuevo dashboard','dashboard'),(446,'Nuevo dashboard','dashboard'),(447,'Nuevo dashboard','dashboard'),(448,'Nuevo dashboard','dashboard');
/*!40000 ALTER TABLE `dashboards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dispositivo-grupo`
--

DROP TABLE IF EXISTS `dispositivo-grupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispositivo-grupo` (
  `id-dispositivo` varchar(255) NOT NULL,
  `id-grupo` int NOT NULL,
  PRIMARY KEY (`id-dispositivo`,`id-grupo`),
  KEY `fk_idgrupo_dispositivo_idx` (`id-grupo`),
  CONSTRAINT `fk_iddispositivo_grupo` FOREIGN KEY (`id-dispositivo`) REFERENCES `dispositivos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_idgrupo_dispositivo` FOREIGN KEY (`id-grupo`) REFERENCES `grupos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispositivo-grupo`
--

LOCK TABLES `dispositivo-grupo` WRITE;
/*!40000 ALTER TABLE `dispositivo-grupo` DISABLE KEYS */;
INSERT INTO `dispositivo-grupo` VALUES ('Shelly1',2),('Shelly2',2),('Shelly3',2),('Shelly1',5),('Shelly2',5),('Shelly3',5),('Shelly1',6),('Shelly2',6),('Shelly3',6);
/*!40000 ALTER TABLE `dispositivo-grupo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dispositivos`
--

DROP TABLE IF EXISTS `dispositivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispositivos` (
  `id` varchar(255) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `icono` varchar(255) DEFAULT NULL,
  `topic` varchar(255) NOT NULL,
  `ubicacion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `nombre_UNIQUE` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispositivos`
--

LOCK TABLES `dispositivos` WRITE;
/*!40000 ALTER TABLE `dispositivos` DISABLE KEYS */;
INSERT INTO `dispositivos` VALUES ('Dispositivo actuador','Dispositivo actuador',NULL,'shelly1/events/rpc','LD3'),('Nuevo','Nuevo',NULL,'shelly2/events/rpc','Aula F0.1'),('Shelly 1','Shelly 1',NULL,'shelly1/events/rpc','Aula F0.1'),('Shelly 6','Shelly 6',NULL,'shelly2/events/rpc','Aula F1.1'),('Shelly TRV ','Shelly trv 4',NULL,'shelly/nomeacuerdo','Aula A1.1'),('Shelly1','Shelly aula x','home','shelly1/events/rpc','Aula A1.2'),('Shelly2','Shelly aula y','home','shelly2/events/rpc','Aula A2.1'),('Shelly3','Shelly aula z',NULL,'shelly3/events/rpc','Aula A2.2'),('Shelly4','Otro shelly',NULL,'shelly3/events/rpc','Salón de actos');
/*!40000 ALTER TABLE `dispositivos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dispositivos-integraciones`
--

DROP TABLE IF EXISTS `dispositivos-integraciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispositivos-integraciones` (
  `iddispositivos` varchar(255) NOT NULL,
  `idintegraciones` int NOT NULL,
  PRIMARY KEY (`iddispositivos`,`idintegraciones`),
  KEY `fk_idintegraciones_dispositivo_idx` (`idintegraciones`),
  CONSTRAINT `fk_iddispositivo_integraciones` FOREIGN KEY (`iddispositivos`) REFERENCES `dispositivos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_idintegraciones_dispositivo` FOREIGN KEY (`idintegraciones`) REFERENCES `integraciones` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispositivos-integraciones`
--

LOCK TABLES `dispositivos-integraciones` WRITE;
/*!40000 ALTER TABLE `dispositivos-integraciones` DISABLE KEYS */;
INSERT INTO `dispositivos-integraciones` VALUES ('Nuevo',2),('Shelly TRV ',101),('Dispositivo actuador',110),('Shelly 1',160);
/*!40000 ALTER TABLE `dispositivos-integraciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grupos`
--

DROP TABLE IF EXISTS `grupos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grupos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `icono` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos`
--

LOCK TABLES `grupos` WRITE;
/*!40000 ALTER TABLE `grupos` DISABLE KEYS */;
INSERT INTO `grupos` VALUES (2,'ShellyHT','home'),(5,'ShellyHT','null'),(6,'Shellies','home');
/*!40000 ALTER TABLE `grupos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `integraciones`
--

DROP TABLE IF EXISTS `integraciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `integraciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `script` varchar(45) NOT NULL,
  `tipo_dispositivo` varchar(1) NOT NULL DEFAULT 's',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `nombre_UNIQUE` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=282 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `integraciones`
--

LOCK TABLES `integraciones` WRITE;
/*!40000 ALTER TABLE `integraciones` DISABLE KEYS */;
INSERT INTO `integraciones` VALUES (2,'CO2','ERSCO2','s'),(45,'Shellar HT','ShelladoHT','s'),(46,'actua HT','actua','s'),(48,'actuaa HT','actuaa','s'),(49,'actuaaa HT','actuaaa','s'),(50,'actuaaaa HT','actuaaaa','s'),(51,'actuaaaaa HT','actuaaaaa','a'),(52,'actuaaaaaa HT','actuaaaaaa','a'),(54,'actuaaaaaaa HT','actuaaaaaaa','a'),(56,'actuaaaaaaaa HT','actuaaaaaaaa','a'),(58,'actuaaaaaaaaa HT','actuaaaaaaaaa','a'),(60,'actuaaaaaaaaaa HT','actuaaaaaaaaaa','a'),(62,'actuaaaaaaaaaaa HT','actuaaaaaaaaaaa','a'),(63,'Prueba normal','Prueba normal','a'),(65,'Prueba actuador','Prueba varios actuables','a'),(66,'Prueba actuador error','Prueba varios actuables','a'),(68,'Prueba actuador edición','Prueba','a'),(69,'Prueba web','Integracion web 1','s'),(70,'Integracion web 2','Integracion web 2','s'),(71,'Ole','wedxw','s'),(72,'sqdx','xaxXw','s'),(81,'asxdasw','dwew','s'),(83,'asxdaswcdxs','dw','s'),(84,'asxdaswcdxsa','dw','s'),(86,'awqxdwadxw','xawex','s'),(87,'xwecas','cxewc','s'),(88,'xwecaswx','cxewc','a'),(92,'xwecaswxasd','cxewc','a'),(101,'Shelly TRV','ShellyTRV','a'),(110,'Prueba actuador edición 2','Prueba varios actuables 2','a'),(129,'Prueba de esto','Otro script distinto','s'),(132,'Prueba de eswto','Otro script distifnto','s'),(133,'Prueba de ','Otro  distifnto','s'),(136,'Pruebsefa de ','Otro      ','s'),(137,'Pruebsefa vawevazde ','Otro    er2qwa  ','a'),(140,'Prueba en la web','Prueba en la weeeebb','s'),(160,'ShellyHT','ShellyHT.py','s');
/*!40000 ALTER TABLE `integraciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `integraciones-atributos`
--

DROP TABLE IF EXISTS `integraciones-atributos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `integraciones-atributos` (
  `idintegracion` int NOT NULL,
  `idatributo` int NOT NULL,
  PRIMARY KEY (`idintegracion`,`idatributo`),
  KEY `fk_integracion_idatributo_idx` (`idatributo`),
  CONSTRAINT `fk_integracion_idatributo` FOREIGN KEY (`idatributo`) REFERENCES `atributos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_integracion_idintegracion` FOREIGN KEY (`idintegracion`) REFERENCES `integraciones` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `integraciones-atributos`
--

LOCK TABLES `integraciones-atributos` WRITE;
/*!40000 ALTER TABLE `integraciones-atributos` DISABLE KEYS */;
INSERT INTO `integraciones-atributos` VALUES (2,1),(45,1),(46,1),(48,1),(49,1),(50,1),(51,1),(101,1),(160,1),(2,2),(2,3),(160,3),(2,4),(2,8),(101,8),(160,8),(56,49),(58,49),(63,53),(65,53),(66,53),(68,53),(65,55),(66,55),(68,55),(65,56),(65,57),(68,57),(110,57),(65,58),(68,58),(110,58),(65,59),(68,59),(110,59),(69,66),(70,68),(71,70),(72,72),(83,74),(83,75),(88,76),(92,76),(88,77),(92,77),(88,78),(92,78),(101,87),(110,197),(110,198),(129,200),(132,202),(133,203),(136,205),(137,206),(140,207),(140,208);
/*!40000 ALTER TABLE `integraciones-atributos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reglas`
--

DROP TABLE IF EXISTS `reglas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reglas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `usuario_id` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_usuario_id_reglas_idx` (`usuario_id`),
  CONSTRAINT `fk_usuario_id_reglas` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reglas`
--

LOCK TABLES `reglas` WRITE;
/*!40000 ALTER TABLE `reglas` DISABLE KEYS */;
INSERT INTO `reglas` VALUES (8,'Prueba 1','528ac3a8-b8ed-4a8a-a6fb-5106de7e10e1'),(9,'Prueba 2','528ac3a8-b8ed-4a8a-a6fb-5106de7e10e1'),(11,'Prueba 1','528ac3a8-b8ed-4a8a-a6fb-5106de7e10e1');
/*!40000 ALTER TABLE `reglas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL,
  `Nombre` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Nombre_UNIQUE` (`Nombre`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Admin'),(2,'User');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `secciones`
--

DROP TABLE IF EXISTS `secciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `secciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(25) NOT NULL,
  `icono` varchar(255) DEFAULT NULL,
  `layout` varchar(1) NOT NULL DEFAULT 'g',
  `numFilas` tinyint NOT NULL DEFAULT '3',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=483 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `secciones`
--

LOCK TABLES `secciones` WRITE;
/*!40000 ALTER TABLE `secciones` DISABLE KEYS */;
INSERT INTO `secciones` VALUES (1,'Plano en grid',NULL,'g',3),(2,'hey','dashboard','g',5),(3,'Plano en sidebar',NULL,'s',3),(4,'Nuevo dashboard',NULL,'s',3),(5,'Pruena','mano','g',6),(6,'Sidebar',NULL,'g',4),(7,'Seccion nueva','info','g',4),(8,'a',NULL,'g',3),(9,'Plano',NULL,'c',3),(10,'holita holita','2','g',3),(11,'Grafico',NULL,'c',3),(12,'Nueva sección','home','g',4),(13,'Sección 1','info','g',3),(14,'Grafico2',NULL,'c',3),(15,'Sección 1',NULL,'g',3),(16,'asdxa',NULL,'g',3),(17,'a',NULL,'c',3),(18,'Sidebar',NULL,'s',4),(19,'Sección nueva card',NULL,'c',3),(20,'Nuevo','info','g',3),(21,'Nueva secciónzaca',NULL,'c',3),(22,'Pruebasss','home','g',3),(23,'Creo que es este el que','home','g',3),(24,'sidebar',NULL,'g',3),(25,'Shellies',NULL,'g',3),(26,'Necesito un nombre mucho','home','g',3),(27,'Sección 1','home','g',3),(28,'card',NULL,'c',3),(29,'Otro','home','g',3),(30,'Nueva sección','default','g',3),(31,'Nueva sección','default','g',3),(32,'Sidebar',NULL,'s',3),(33,'Card',NULL,'c',3),(34,'Card 2',NULL,'c',3),(35,'Grid',NULL,'g',3),(36,'Grid 2',NULL,'g',3),(37,'Grid popover',NULL,'g',3),(38,'Card Popover',NULL,'c',3),(39,'Sidebar popover',NULL,'s',3),(40,'Card 3',NULL,'c',3),(41,'Grid 3',NULL,'g',3),(42,'Sidebar 2',NULL,'s',3),(43,'Mas',NULL,'g',3),(44,'Add card',NULL,'c',3),(45,'Nueva prueba',NULL,'s',3),(46,'Nueva sección','default','g',3),(47,'Nueva sección','default','g',3),(48,'Nueva sección','default','g',3),(49,'Nueva sección','default','g',3),(50,'Nueva sección','default','g',3),(51,'Nueva sección','default','g',3),(52,'Nueva sección','default','g',3),(53,'Nueva sección','default','g',3),(54,'Nueva sección','default','g',3),(55,'Nueva sección','default','g',3),(56,'Nueva sección','default','g',3),(57,'Nueva sección','default','g',3),(58,'Nueva sección','default','g',3),(59,'Nueva sección','default','g',3),(60,'Nueva sección','default','g',3),(61,'Nueva sección','default','g',3),(62,'Nueva sección','default','g',3),(63,'Nueva sección','default','g',3),(64,'Nueva sección','default','g',3),(65,'Nueva sección','default','g',3),(66,'Nueva sección','default','g',3),(67,'Nueva sección','default','g',3),(68,'Nueva sección','default','g',3),(69,'Nueva sección','default','g',3),(70,'Nueva sección','default','g',3),(71,'Nueva sección','default','g',3),(72,'Nueva sección','default','g',3),(73,'Nueva sección','default','g',3),(74,'Nueva sección','default','g',3),(75,'Nueva sección','default','g',3),(76,'Nueva sección','default','g',3),(77,'Nueva sección','default','g',3),(78,'Nueva sección','default','g',3),(79,'Nueva sección','default','g',3),(80,'Nueva sección','default','g',3),(81,'Nueva sección','default','g',3),(82,'Nueva sección','default','g',3),(83,'Nueva sección','default','g',3),(84,'Nueva sección','default','g',3),(85,'Nueva sección','default','g',3),(86,'Nueva sección','default','g',3),(87,'Nueva sección','default','g',3),(88,'Nueva sección','default','g',3),(89,'Nueva sección','default','g',3),(90,'Nueva sección','default','g',3),(91,'Nueva sección','default','g',3),(92,'Nueva sección','default','g',3),(93,'Nueva sección','default','g',3),(94,'Nueva sección','default','g',3),(95,'Nueva sección','default','g',3),(96,'Nueva sección','default','g',3),(97,'Nueva sección','default','g',3),(98,'Nueva sección','default','g',3),(99,'Nueva sección','default','g',3),(100,'Nueva sección','default','g',3),(101,'Nueva sección','default','g',3),(102,'Nueva sección','default','g',3),(103,'Nueva sección','default','g',3),(104,'Nueva sección','default','g',3),(105,'Nueva sección','default','g',3),(106,'Nueva sección','default','g',3),(107,'Nueva sección','default','g',3),(108,'Nueva sección','default','g',3),(109,'Nueva sección','default','g',3),(110,'Nueva sección','default','g',3),(111,'Nueva sección','default','g',3),(112,'Nueva sección','default','g',3),(113,'Nueva sección','default','g',3),(114,'Nueva sección','default','g',3),(115,'Nueva sección','default','g',3),(116,'Nueva sección','default','g',3),(117,'Nueva sección','default','g',3),(118,'Nueva sección','default','g',3),(119,'Nueva sección','default','g',3),(120,'Nueva sección','default','g',3),(121,'Nueva sección','default','g',3),(122,'Nueva sección','default','g',3),(123,'Nueva sección','default','g',3),(124,'Nueva sección','default','g',3),(125,'Nueva sección','default','g',3),(126,'Nueva sección','default','g',3),(127,'Nueva sección','default','g',3),(128,'Nueva sección','default','g',3),(129,'Nueva sección','default','g',3),(130,'Nueva sección','default','g',3),(131,'Nueva sección','default','g',3),(132,'Nueva sección','default','g',3),(133,'Nueva sección','default','g',3),(134,'Nueva sección','default','g',3),(135,'Nueva sección','default','g',3),(136,'Nueva sección','default','g',3),(137,'Nueva sección','default','g',3),(138,'Nueva sección','default','g',3),(139,'Nueva sección','default','g',3),(140,'Nueva sección','default','g',3),(141,'Nueva sección','default','g',3),(142,'Nueva sección','default','g',3),(143,'Nueva sección','default','g',3),(144,'Nueva sección','default','g',3),(145,'Nueva sección','default','g',3),(146,'Nueva sección','default','g',3),(147,'Nueva sección','default','g',3),(148,'Nueva sección','default','g',3),(149,'Nueva sección','default','g',3),(150,'Nueva sección','default','g',3),(151,'Nueva sección','default','g',3),(152,'Nueva sección','default','g',3),(153,'Nueva sección','default','g',3),(154,'Nueva sección','default','g',3),(155,'Nueva sección','default','g',3),(156,'Nueva sección','default','g',3),(157,'Nueva sección','default','g',3),(158,'Nueva sección','default','g',3),(159,'Nueva sección','default','g',3),(160,'Nueva sección','default','g',3),(161,'Nueva sección','default','g',3),(162,'Nueva sección','default','g',3),(163,'Nueva sección','default','g',3),(164,'Nueva sección','default','g',3),(165,'Nueva sección','default','g',3),(166,'Nueva sección','default','g',3),(167,'Nueva sección','default','g',3),(168,'Nueva sección','default','g',3),(169,'Nueva sección','default','g',3),(170,'Nueva sección','default','g',3),(171,'Nueva sección','default','g',3),(172,'Nueva sección','default','g',3),(173,'Nueva sección','default','g',3),(174,'Nueva sección','default','g',3),(175,'Nueva sección','default','g',3),(176,'Nueva sección','default','g',3),(177,'Nueva sección','default','g',3),(178,'Nueva sección','default','g',3),(179,'Nueva sección','default','g',3),(180,'Nueva sección','default','g',3),(181,'Nueva sección','default','g',3),(182,'Nueva sección','default','g',3),(183,'Nueva sección','default','g',3),(184,'Nueva sección','default','g',3),(185,'Nueva sección','default','g',3),(186,'Nueva sección','default','g',3),(187,'Nueva sección','default','g',3),(188,'Nueva sección','default','g',3),(189,'Nueva sección','default','g',3),(190,'Nueva sección','default','g',3),(191,'Nueva sección','default','g',3),(192,'Nueva sección','default','g',3),(193,'Nueva sección','default','g',3),(194,'Nueva sección','default','g',3),(195,'Nueva sección','default','g',3),(196,'Nueva sección','default','g',3),(197,'Nueva sección','default','g',3),(198,'Nueva sección','default','g',3),(199,'Nueva sección','default','g',3),(200,'Nueva sección','default','g',3),(201,'Nueva sección','default','g',3),(202,'Nueva sección','default','g',3),(203,'Nueva sección','default','g',3),(204,'Nueva sección','default','g',3),(205,'Nueva sección','default','g',3),(206,'Nueva sección','default','g',3),(207,'Nueva sección','default','g',3),(208,'Nueva sección','default','g',3),(209,'Nueva sección','default','g',3),(210,'Nueva sección','default','g',3),(211,'Nueva sección','default','g',3),(212,'Nueva sección','default','g',3),(213,'Nueva sección','default','g',3),(214,'Nueva sección','default','g',3),(215,'Nueva sección','default','g',3),(216,'Nueva sección','default','g',3),(217,'Nueva sección','default','g',3),(218,'Nueva sección','default','g',3),(219,'Nueva sección','default','g',3),(220,'Nueva sección','default','g',3),(221,'Nueva sección','default','g',3),(222,'Nueva sección','default','g',3),(223,'Nueva sección','default','g',3),(224,'Nueva sección','default','g',3),(225,'Nueva sección','default','g',3),(226,'Nueva sección','default','g',3),(227,'Nueva sección','default','g',3),(228,'New Section','icon.png','g',3),(229,'Nueva sección','default','g',3),(230,'Nueva sección','default','g',3),(231,'Nueva sección','default','g',3),(232,'Nueva sección','default','g',3),(233,'Nueva sección','default','g',3),(234,'Nueva sección','default','g',3),(235,'Nueva sección','default','g',3),(236,'Nueva sección','default','g',3),(237,'Nueva sección','default','g',3),(238,'Nueva sección','default','g',3),(239,'Nueva sección','default','g',3),(240,'Nueva sección','default','g',3),(241,'Nueva sección','default','g',3),(242,'Nueva sección','default','g',3),(243,'Nueva sección','default','g',3),(244,'New Section','icon.png','g',3),(245,'Nueva sección','default','g',3),(246,'Edited Section','new_icon.png','g',3),(247,'Nueva sección','default','g',3),(248,'Nueva sección','default','g',3),(249,'Nueva sección','default','g',3),(250,'Nueva sección','default','g',3),(251,'Nueva sección','default','g',3),(252,'Nueva sección','default','g',3),(253,'Nueva sección','default','g',3),(254,'Nueva sección','default','g',3),(255,'Nueva sección','default','g',3),(256,'Nueva sección','default','g',3),(257,'Nueva sección','default','g',3),(258,'Nueva sección','default','g',3),(259,'Nueva sección','default','g',3),(260,'Nueva sección','default','g',3),(261,'Nueva sección','default','g',3),(262,'New Section','icon.png','g',3),(263,'Nueva sección','default','g',3),(264,'Edited Section','new_icon.png','g',3),(265,'Nueva sección','default','g',3),(266,'Nueva sección','default','g',3),(267,'Nueva sección','default','g',3),(268,'Nueva sección','default','g',3),(269,'Nueva sección','default','g',3),(270,'Nueva sección','default','g',3),(271,'Nueva sección','default','g',3),(272,'Nueva sección','default','g',3),(273,'Nueva sección','default','g',3),(274,'Nueva sección','default','g',3),(275,'Nueva sección','default','g',3),(276,'Nueva sección','default','g',3),(277,'Nueva sección','default','g',3),(278,'Nueva sección','default','g',3),(279,'Nueva sección','default','g',3),(280,'New Section','icon.png','g',3),(281,'Nueva sección','default','g',3),(282,'Edited Section','new_icon.png','g',3),(283,'Nueva sección','default','g',3),(284,'Nueva sección','default','g',3),(285,'Nueva sección','default','g',3),(286,'Nueva sección','default','g',3),(287,'Nueva sección','default','g',3),(288,'Nueva sección','default','g',3),(289,'Nueva sección','default','g',3),(290,'Nueva sección','default','g',3),(291,'Nueva sección','default','g',3),(292,'Nueva sección','default','g',3),(293,'Nueva sección','default','g',3),(294,'Nueva sección','default','g',3),(295,'Nueva sección','default','g',3),(296,'Nueva sección','default','g',3),(297,'Nueva sección','default','g',3),(298,'New Section','icon.png','g',3),(299,'Nueva sección','default','g',3),(300,'Edited Section','new_icon.png','g',3),(301,'Nueva sección','default','g',3),(302,'Nueva sección','default','g',3),(303,'Nueva sección','default','g',3),(304,'Nueva sección','default','g',3),(305,'Nueva sección','default','g',3),(306,'Nueva sección','default','g',3),(307,'Nueva sección','default','g',3),(308,'Nueva sección','default','g',3),(309,'Nueva sección','default','g',3),(310,'Nueva sección','default','g',3),(311,'Nueva sección','default','g',3),(312,'Nueva sección','default','g',3),(313,'Nueva sección','default','g',3),(314,'Nueva sección','default','g',3),(315,'New Section','icon.png','g',3),(316,'Nueva sección','default','g',3),(317,'Edited Section','new_icon.png','g',3),(318,'Nueva sección','default','g',3),(319,'Nueva sección','default','g',3),(320,'Nueva sección','default','g',3),(321,'Nueva sección','default','g',3),(322,'Nueva sección','default','g',3),(323,'Nueva sección','default','g',3),(324,'Nueva sección','default','g',3),(325,'Nueva sección','default','g',3),(326,'Nueva sección','default','g',3),(327,'Nueva sección','default','g',3),(328,'Nueva sección','default','g',3),(329,'Nueva sección','default','g',3),(330,'Nueva sección','default','g',3),(331,'Nueva sección','default','g',3),(332,'New Section','icon.png','g',3),(333,'Nueva sección','default','g',3),(334,'Edited Section','new_icon.png','g',3),(335,'Nueva sección','default','g',3),(336,'Nueva sección','default','g',3),(337,'Nueva sección','default','g',3),(338,'Nueva sección','default','g',3),(339,'Nueva sección','default','g',3),(340,'Nueva sección','default','g',3),(341,'Nueva sección','default','g',3),(342,'Nueva sección','default','g',3),(343,'Nueva sección','default','g',3),(344,'Nueva sección','default','g',3),(345,'Nueva sección','default','g',3),(346,'Nueva sección','default','g',3),(347,'Nueva sección','default','g',3),(348,'Nueva sección','default','g',3),(349,'New Section','icon.png','g',3),(350,'Nueva sección','default','g',3),(351,'Edited Section','new_icon.png','g',3),(352,'Nueva sección','default','g',3),(353,'Nueva sección','default','g',3),(354,'Nueva sección','default','g',3),(355,'Nueva sección','default','g',3),(356,'Nueva sección','default','g',3),(357,'Nueva sección','default','g',3),(358,'Nueva sección','default','g',3),(359,'Nueva sección','default','g',3),(360,'Nueva sección','default','g',3),(361,'Nueva sección','default','g',3),(362,'Nueva sección','default','g',3),(363,'Nueva sección','default','g',3),(364,'Nueva sección','default','g',3),(365,'Nueva sección','default','g',3),(366,'New Section','icon.png','g',3),(367,'Nueva sección','default','g',3),(368,'Edited Section','new_icon.png','g',3),(369,'Nueva sección','default','g',3),(370,'Nueva sección','default','g',3),(371,'Nueva sección','default','g',3),(372,'Nueva sección','default','g',3),(373,'Nueva sección','default','g',3),(374,'Nueva sección','default','g',3),(375,'Nueva sección','default','g',3),(376,'Nueva sección','default','g',3),(377,'Nueva sección','default','g',3),(378,'Nueva sección','default','g',3),(379,'Nueva sección','default','g',3),(380,'Nueva sección','default','g',3),(381,'Nueva sección','default','g',3),(382,'Nueva sección','default','g',3),(383,'New Section','icon.png','g',3),(384,'Nueva sección','default','g',3),(385,'Edited Section','new_icon.png','g',3),(386,'Nueva sección','default','g',3),(387,'Nueva sección','default','g',3),(388,'Nueva sección','default','g',3),(389,'Nueva sección','default','g',3),(390,'Nueva sección','default','g',3),(391,'Nueva sección','default','g',3),(392,'Nueva sección','default','g',3),(393,'Nueva sección','default','g',3),(394,'Nueva sección','default','g',3),(395,'Nueva sección','default','g',3),(396,'Nueva sección','default','g',3),(397,'Nueva sección','default','g',3),(398,'Nueva sección','default','g',3),(399,'Nueva sección','default','g',3),(400,'Nueva sección','default','g',3),(401,'Nueva sección','default','g',3),(402,'New Section','icon.png','g',3),(403,'Nueva sección','default','g',3),(404,'Edited Section','new_icon.png','g',3),(405,'Nueva sección','default','g',3),(406,'Nueva sección','default','g',3),(407,'Nueva sección','default','g',3),(408,'Nueva sección','default','g',3),(409,'Nueva sección','default','g',3),(410,'Nueva sección','default','g',3),(411,'Nueva sección','default','g',3),(412,'Nueva sección','default','g',3),(413,'Nueva sección','default','g',3),(414,'Nueva sección','default','g',3),(415,'Nueva sección','default','g',3),(416,'Nueva sección','default','g',3),(417,'Nueva sección','default','g',3),(418,'Nueva sección','default','g',3),(419,'Nueva sección','default','g',3),(420,'New Section','icon.png','g',3),(421,'Nueva sección','default','g',3),(422,'Edited Section','new_icon.png','g',3),(423,'Nueva sección','default','g',3),(424,'Nueva sección','default','g',3),(425,'Nueva sección','default','g',3),(426,'Nueva sección','default','g',3),(427,'Nueva sección','default','g',3),(428,'Nueva sección','default','g',3),(429,'Nueva sección','default','g',3),(430,'Nueva sección','default','g',3),(431,'Nueva sección','default','g',3),(432,'Nueva sección','default','g',3),(433,'Nueva sección','default','g',3),(434,'Nueva sección','default','g',3),(435,'Nueva sección','default','g',3),(436,'Nueva sección','default','g',3),(437,'Nueva sección','default','g',3),(438,'New Section','icon.png','g',3),(439,'Nueva sección','default','g',3),(440,'Edited Section','new_icon.png','g',3),(441,'Nueva sección','default','g',3),(442,'Nueva sección','default','g',3),(443,'Nueva sección','default','g',3),(444,'Nueva sección','default','g',3),(445,'Nueva sección','default','g',3),(446,'Nueva sección','default','g',3),(447,'Nueva sección','default','g',3),(448,'Nueva sección','default','g',3),(449,'Nueva sección','default','g',3),(450,'Nueva sección','default','g',3),(451,'Nueva sección','default','g',3),(452,'Nueva sección','default','g',3),(453,'Nueva sección','default','g',3),(454,'Nueva sección','default','g',3),(455,'Nueva sección','default','g',3),(456,'New Section','icon.png','g',3),(457,'Nueva sección','default','g',3),(458,'Edited Section','new_icon.png','g',3),(459,'Nueva sección','default','g',3),(460,'Nueva sección','default','g',3),(461,'Nueva sección','default','g',3),(462,'Nueva sección','default','g',3),(463,'Nueva sección','default','g',3),(464,'Nueva sección','default','g',3),(465,'Nueva sección','default','g',3),(466,'Nueva sección','default','g',3),(467,'Nueva sección','default','g',3),(468,'Nueva sección','default','g',3),(469,'Nueva sección','default','g',3),(470,'Nueva sección','default','g',3),(471,'Nueva sección','default','g',3),(472,'Nueva sección','default','g',3),(473,'Nueva sección','default','g',3),(474,'Nueva sección','default','g',3),(475,'Nueva sección','default','g',3),(476,'New Section','icon.png','g',3),(477,'Nueva sección','default','g',3),(478,'Edited Section','new_icon.png','g',3),(479,'Nueva sección','default','g',3),(480,'Nueva sección','default','g',3),(481,'Nueva sección','default','g',3),(482,'Nueva sección','default','g',3);
/*!40000 ALTER TABLE `secciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tarjetas`
--

DROP TABLE IF EXISTS `tarjetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tarjetas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(45) NOT NULL,
  `posicion` varchar(3) NOT NULL,
  `contenido` mediumtext,
  `imagen` varchar(255) DEFAULT NULL,
  `tipo-grafico` varchar(45) DEFAULT NULL,
  `tiempo-grafico` varchar(45) DEFAULT NULL,
  `id-seccion` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_seccion_tarjeta_idx` (`id-seccion`),
  CONSTRAINT `fk_seccion_tarjeta` FOREIGN KEY (`id-seccion`) REFERENCES `secciones` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=156 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarjetas`
--

LOCK TABLES `tarjetas` WRITE;
/*!40000 ALTER TABLE `tarjetas` DISABLE KEYS */;
INSERT INTO `tarjetas` VALUES (4,'Imagen','2x3',NULL,'link',NULL,NULL,7),(7,'Texto','0x0','Creada en Postman',NULL,NULL,NULL,10),(19,'Texto','0x0','Hola mundo',NULL,NULL,NULL,2),(20,'Imagen','0x1',NULL,'logo-sin-fondo.png',NULL,NULL,2),(23,'Estado','1x0',NULL,NULL,NULL,NULL,2),(24,'Texto','0x0','Nuevo',NULL,NULL,NULL,20),(25,'Estado','0x1',NULL,NULL,NULL,NULL,20),(26,'Estado','0x2',NULL,NULL,NULL,NULL,20),(27,'Texto','2x0','Prueba',NULL,NULL,NULL,2),(28,'Texto','0x0','Funciona',NULL,NULL,NULL,12),(29,'Texto','0x0','Texto',NULL,NULL,NULL,27),(30,'Estado','0x1',NULL,NULL,NULL,NULL,27),(31,'Texto','0x0','a',NULL,NULL,NULL,13),(32,'Estado','0x1',NULL,NULL,NULL,NULL,13),(33,'Termostato','1x1',NULL,NULL,NULL,NULL,2),(35,'Imagen','2x2',NULL,'logo-sin-fondo.png',NULL,NULL,2),(37,'Imagen','0x0',NULL,'logo.png',NULL,NULL,18),(41,'Texto','0x0','aerq',NULL,NULL,NULL,5),(42,'Imagen','0x0',NULL,'logo.png',NULL,NULL,19),(43,'Texto','0x0','Vamos a escribir aqui',NULL,NULL,NULL,21),(44,'Estado','0x0',NULL,NULL,NULL,NULL,25),(45,'Estado','0x1',NULL,NULL,NULL,NULL,25),(46,'Estado','0x2',NULL,NULL,NULL,NULL,25),(47,'Estado','1x0',NULL,NULL,NULL,NULL,25),(48,'Estado','1x1',NULL,NULL,NULL,NULL,25),(49,'Estado','1x2',NULL,NULL,NULL,NULL,25),(50,'Termostato','2x0',NULL,NULL,NULL,NULL,7),(51,'Texto','0x0','1',NULL,NULL,NULL,15),(52,'Imagen','0x1',NULL,'esi.jpg',NULL,NULL,15),(53,'Estado','0x2',NULL,NULL,NULL,NULL,15),(54,'Imagen','3x1',NULL,'esi.jpg',NULL,NULL,2),(55,'Texto','0x1','En clasica',NULL,NULL,NULL,10),(56,'Texto','0x1','Second round',NULL,NULL,NULL,7),(57,'Texto','3x0','Hoki',NULL,NULL,NULL,7),(58,'Estado','2x2',NULL,NULL,NULL,NULL,5),(59,'Estado','2x2',NULL,NULL,NULL,NULL,5),(60,'Estado','2x2',NULL,NULL,NULL,NULL,5),(62,'Grafico','0x1',NULL,NULL,'Lineal','30d',5),(63,'Grafico','1x1',NULL,NULL,'Lineal','30d',5),(64,'Grafico','1x0',NULL,NULL,'Lineal','30d',5),(65,'Grafico','0x0',NULL,NULL,'Barra','365d',11),(66,'Grafico','0x0',NULL,NULL,'Lineal','30d',14),(67,'Plano','0x0',NULL,NULL,NULL,NULL,9),(68,'Plano','0x0',NULL,NULL,NULL,NULL,3),(69,'Plano','0x0',NULL,NULL,NULL,NULL,1),(70,'Plano','0x2',NULL,NULL,NULL,NULL,2),(71,'Grafico','1x2',NULL,NULL,'Barra','365d',2),(72,'Texto','2x1','Hola mundo',NULL,NULL,NULL,2),(85,'Estado','0x1',NULL,NULL,NULL,NULL,12),(86,'Estado','3x0',NULL,NULL,NULL,NULL,2),(87,'Texto','3x2','a',NULL,NULL,NULL,2),(88,'Texto','4x0','Prueba de nueva fila',NULL,NULL,NULL,2),(89,'Texto','0x1','Prueba de tarjeta de texto',NULL,NULL,NULL,1),(90,'Imagen','0x2',NULL,'esi.jpg',NULL,NULL,1),(91,'Grafico','1x0',NULL,NULL,'Barra','365d',1),(93,'Termostato','1x1',NULL,NULL,NULL,NULL,1),(94,'Grafico','0x1',NULL,NULL,'Barra','365d',3),(100,'Estado','1x0',NULL,NULL,NULL,NULL,12),(101,'Termostato','0x2',NULL,NULL,NULL,NULL,12),(108,'Plano','1x1',NULL,NULL,NULL,NULL,12),(109,'Grafico','1x2',NULL,NULL,'Lineal','365d',12),(110,'Texto','0x2','Contenido',NULL,NULL,NULL,10),(111,'Imagen','1x0',NULL,'logo.png',NULL,NULL,10),(112,'Estado','1x1',NULL,NULL,NULL,NULL,10),(113,'Grafico','1x2',NULL,NULL,'Lineal','24h',10),(114,'Plano','2x0',NULL,NULL,NULL,NULL,10),(116,'Estado','0x0',NULL,NULL,NULL,NULL,7),(117,'Texto','2x0','Hola',NULL,NULL,NULL,12),(118,'Estado','0x0',NULL,NULL,NULL,NULL,31),(123,'Grupo','0x1',NULL,NULL,NULL,NULL,31),(125,'Grupo','0x0',NULL,NULL,NULL,NULL,33),(126,'Texto','0x0','hola',NULL,NULL,NULL,43),(127,'Texto','0x0','Prueba del popover',NULL,NULL,NULL,37),(128,'Texto','0x1','cosas',NULL,NULL,NULL,37),(129,'Texto','0x2','Prueba',NULL,NULL,NULL,31),(130,'Grupo','1x0',NULL,NULL,NULL,NULL,31),(131,'Grupo','0x2',NULL,NULL,NULL,NULL,37),(132,'Grupo','1x0',NULL,NULL,NULL,NULL,37),(133,'Grupo','1x1',NULL,NULL,NULL,NULL,37),(134,'Texto','0x0','Holi',NULL,NULL,NULL,50),(135,'Texto','0x1','Tarjeta',NULL,NULL,NULL,50),(136,'Texto','1x1','Tarjeta',NULL,NULL,NULL,31),(137,'Texto','1x2','Tarjeta',NULL,NULL,NULL,31),(138,'Grupo','2x0',NULL,NULL,NULL,NULL,31),(139,'Imagen','2x1',NULL,'plano_esi (1).svg',NULL,NULL,31),(140,'Grafico','2x2',NULL,NULL,'Barra','365d',31),(141,'Grupo','0x2',NULL,NULL,NULL,NULL,50),(142,'Texto','1x0','Texto',NULL,NULL,NULL,50),(143,'Plano','1x1',NULL,NULL,NULL,NULL,50),(144,'Grupo','0x0',NULL,NULL,NULL,NULL,51),(145,'Grupo','0x1',NULL,NULL,NULL,NULL,51),(146,'Texto','0x2','a',NULL,NULL,NULL,51),(147,'Texto','1x0','Prueba',NULL,NULL,NULL,51),(148,'Texto','1x1','Texto de prueba',NULL,NULL,NULL,387),(149,'Texto','1x1','Texto de prueba',NULL,NULL,NULL,406),(150,'Texto','1x1','Texto de prueba',NULL,NULL,NULL,424),(151,'Texto','1x1','Texto de prueba',NULL,NULL,NULL,442),(152,'Texto','1x1','Texto de prueba',NULL,NULL,NULL,460),(153,'Texto','1x1','Texto de prueba',NULL,NULL,NULL,461),(154,'Texto','1x1','Texto de prueba',NULL,NULL,NULL,480),(155,'Texto','1x1','Texto de prueba',NULL,NULL,NULL,481);
/*!40000 ALTER TABLE `tarjetas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tarjetas-atributos`
--

DROP TABLE IF EXISTS `tarjetas-atributos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tarjetas-atributos` (
  `id-tarjeta` int NOT NULL,
  `id-atributo` int NOT NULL,
  `id-dispositivo` varchar(255) NOT NULL,
  KEY `fk_atributo_tarjeta-id_idx` (`id-atributo`),
  KEY `fk_dispositivo_tarjeta-id_idx` (`id-dispositivo`),
  KEY `fk_tarjeta-id_idx` (`id-tarjeta`),
  CONSTRAINT `fk_atributo_tarjeta-id` FOREIGN KEY (`id-atributo`) REFERENCES `atributos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_dispositivo_tarjeta-id` FOREIGN KEY (`id-dispositivo`) REFERENCES `dispositivos` (`id`),
  CONSTRAINT `fk_tarjeta-id` FOREIGN KEY (`id-tarjeta`) REFERENCES `tarjetas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarjetas-atributos`
--

LOCK TABLES `tarjetas-atributos` WRITE;
/*!40000 ALTER TABLE `tarjetas-atributos` DISABLE KEYS */;
INSERT INTO `tarjetas-atributos` VALUES (23,1,'Shelly1'),(25,3,'Shelly2'),(26,1,'Shelly2'),(30,1,'Shelly2'),(32,1,'Shelly1'),(33,87,'Shelly TRV '),(44,1,'Shelly1'),(45,1,'Shelly2'),(46,8,'Shelly3'),(47,1,'Shelly2'),(48,3,'Shelly2'),(49,8,'Shelly2'),(50,87,'Shelly TRV '),(53,1,'Shelly1'),(58,1,'Shelly1'),(59,1,'Shelly1'),(60,1,'Shelly1'),(62,1,'Shelly2'),(62,1,'Shelly1'),(63,1,'Shelly2'),(63,1,'Shelly1'),(64,1,'Shelly3'),(64,1,'Shelly1'),(64,1,'Shelly TRV '),(64,1,'Shelly2'),(65,1,'Shelly2'),(65,1,'Shelly3'),(65,1,'Shelly1'),(65,1,'Shelly TRV '),(66,1,'Shelly2'),(66,1,'Shelly1'),(71,1,'Shelly1'),(71,1,'Shelly3'),(71,1,'Shelly2'),(85,1,'Shelly1'),(85,3,'Shelly2'),(85,1,'Shelly3'),(86,1,'Shelly1'),(86,3,'Shelly2'),(91,1,'Shelly2'),(91,1,'Shelly3'),(91,1,'Shelly1'),(91,1,'Shelly TRV '),(93,87,'Shelly TRV '),(94,1,'Shelly2'),(94,1,'Shelly3'),(94,1,'Shelly1'),(94,1,'Shelly TRV '),(100,1,'Shelly1'),(101,87,'Shelly TRV '),(109,1,'Shelly2'),(109,1,'Shelly3'),(109,1,'Shelly1'),(109,1,'Shelly TRV '),(112,1,'Shelly1'),(112,3,'Shelly2'),(113,1,'Shelly2'),(113,1,'Shelly3'),(113,1,'Shelly1'),(113,1,'Shelly TRV '),(116,1,'Shelly1'),(116,3,'Shelly2'),(118,1,'Shelly1'),(118,1,'Shelly2'),(118,1,'Shelly3'),(140,1,'Shelly1');
/*!40000 ALTER TABLE `tarjetas-atributos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tarjetas-grupos`
--

DROP TABLE IF EXISTS `tarjetas-grupos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tarjetas-grupos` (
  `idtarjeta` int NOT NULL,
  `idgrupo` int NOT NULL,
  KEY `fk_idgrupo_tarjeta_idx` (`idgrupo`),
  KEY `fk_idtarjeta_grupo_idx` (`idtarjeta`),
  CONSTRAINT `fk_idgrupo_tarjeta` FOREIGN KEY (`idgrupo`) REFERENCES `grupos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_idtarjeta_grupo` FOREIGN KEY (`idtarjeta`) REFERENCES `tarjetas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarjetas-grupos`
--

LOCK TABLES `tarjetas-grupos` WRITE;
/*!40000 ALTER TABLE `tarjetas-grupos` DISABLE KEYS */;
INSERT INTO `tarjetas-grupos` VALUES (123,6),(125,6),(130,6),(131,6),(132,6),(133,6),(138,6),(141,6),(144,6),(145,6);
/*!40000 ALTER TABLE `tarjetas-grupos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipos_atributos`
--

DROP TABLE IF EXISTS `tipos_atributos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipos_atributos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `nombre_UNIQUE` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_atributos`
--

LOCK TABLES `tipos_atributos` WRITE;
/*!40000 ALTER TABLE `tipos_atributos` DISABLE KEYS */;
INSERT INTO `tipos_atributos` VALUES (1,'Sensor'),(2,'Termostato');
/*!40000 ALTER TABLE `tipos_atributos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario-dashboard`
--

DROP TABLE IF EXISTS `usuario-dashboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario-dashboard` (
  `id-usuario` varchar(255) NOT NULL,
  `id-dashboard` int NOT NULL,
  PRIMARY KEY (`id-usuario`,`id-dashboard`),
  KEY `fk_id_dashboard_usuario_idx` (`id-dashboard`),
  CONSTRAINT `fk_id_dashboard_usuario` FOREIGN KEY (`id-dashboard`) REFERENCES `dashboards` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_id_usuario` FOREIGN KEY (`id-usuario`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario-dashboard`
--

LOCK TABLES `usuario-dashboard` WRITE;
/*!40000 ALTER TABLE `usuario-dashboard` DISABLE KEYS */;
INSERT INTO `usuario-dashboard` VALUES ('619b52f2-bf25-4daf-b776-c8cb8b7953a1',1),('06aa37a5-5133-4fae-b312-7e4365b4037e',2),('428a564b-57b9-4280-b304-2ce93704c785',4),('528ac3a8-b8ed-4a8a-a6fb-5106de7e10e1',5),('528ac3a8-b8ed-4a8a-a6fb-5106de7e10e1',6),('1e0146e2-64ff-49d0-a2a1-6c8fd521f435',7),('528ac3a8-b8ed-4a8a-a6fb-5106de7e10e1',8),('1e0146e2-64ff-49d0-a2a1-6c8fd521f435',9),('1e0146e2-64ff-49d0-a2a1-6c8fd521f435',10),('bd47278e-8b69-41aa-bd97-ed9dbbc01304',11),('55ee01cf-73a6-4884-920f-f5f45d60f17b',14),('528ac3a8-b8ed-4a8a-a6fb-5106de7e10e1',15),('528ac3a8-b8ed-4a8a-a6fb-5106de7e10e1',21);
/*!40000 ALTER TABLE `usuario-dashboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario-grupo`
--

DROP TABLE IF EXISTS `usuario-grupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario-grupo` (
  `id-usuario` varchar(255) NOT NULL,
  `id-grupo` int NOT NULL,
  PRIMARY KEY (`id-usuario`,`id-grupo`),
  KEY `fk_idgrupo_usuario_idx` (`id-grupo`),
  CONSTRAINT `fk_idgrupo_usuario` FOREIGN KEY (`id-grupo`) REFERENCES `grupos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_idusuario_grupo` FOREIGN KEY (`id-usuario`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario-grupo`
--

LOCK TABLES `usuario-grupo` WRITE;
/*!40000 ALTER TABLE `usuario-grupo` DISABLE KEYS */;
INSERT INTO `usuario-grupo` VALUES ('428a564b-57b9-4280-b304-2ce93704c785',2),('428a564b-57b9-4280-b304-2ce93704c785',5),('528ac3a8-b8ed-4a8a-a6fb-5106de7e10e1',6);
/*!40000 ALTER TABLE `usuario-grupo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` varchar(255) NOT NULL,
  `nombre` varchar(25) NOT NULL,
  `correo` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_roles_idx` (`rol_id`),
  CONSTRAINT `fk_roles` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES ('06aa37a5-5133-4fae-b312-7e4365b4037e','Prueba previa','pre@pre.com','a389a638dec32538f55b0c8dc5c84f84aad65bcd5aacd5f05d36f30b71271a6b',2),('09eae340-a73e-437e-9189-bfbec25a4182','Raul','raulcalzado02@gmail.com','a389a638dec32538f55b0c8dc5c84f84aad65bcd5aacd5f05d36f30b71271a6b',2),('1e0146e2-64ff-49d0-a2a1-6c8fd521f435','Prueba','prueba@form.com','a389a638dec32538f55b0c8dc5c84f84aad65bcd5aacd5f05d36f30b71271a6b',2),('428a564b-57b9-4280-b304-2ce93704c785','Fede','Fede.Valverde@alu.uclm.es','a389a638dec32538f55b0c8dc5c84f84aad65bcd5aacd5f05d36f30b71271a6b',2),('528ac3a8-b8ed-4a8a-a6fb-5106de7e10e1','Raúl','raul.calzado@alu.uclm.es','a389a638dec32538f55b0c8dc5c84f84aad65bcd5aacd5f05d36f30b71271a6b',1),('55ee01cf-73a6-4884-920f-f5f45d60f17b','Dashboard','dashboard@a.com','a389a638dec32538f55b0c8dc5c84f84aad65bcd5aacd5f05d36f30b71271a6b',2),('619b52f2-bf25-4daf-b776-c8cb8b7953a1','Nuevo usuario','nuevo@nuevo.com','a389a638dec32538f55b0c8dc5c84f84aad65bcd5aacd5f05d36f30b71271a6b',2),('64c9d693-ebf8-4f3c-b561-bf8f29f7c921','Vinicius','Vinicius.Junior@uclm.es','a389a638dec32538f55b0c8dc5c84f84aad65bcd5aacd5f05d36f30b71271a6b',2),('847f912e-e505-4a73-ae33-c606d529ee90','CR7','Cristiano.Ronaldo@uclm.es','da1b6aaf7d73dfb21a16e077581e33207c2d59a0413754ae9710eb6d6161504a',2),('bd47278e-8b69-41aa-bd97-ed9dbbc01304','Nombre','nombre@correo.com','a389a638dec32538f55b0c8dc5c84f84aad65bcd5aacd5f05d36f30b71271a6b',2);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valores_actuales`
--

DROP TABLE IF EXISTS `valores_actuales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valores_actuales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `valor` varchar(255) DEFAULT NULL,
  `id-dispositivo` varchar(255) NOT NULL,
  `id-atributo` int NOT NULL,
  `topic-actuacion` varchar(255) DEFAULT NULL,
  `plantilla` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_valor_dispositivo_idx` (`id-dispositivo`),
  KEY `fk_valor_atributo_idx` (`id-atributo`),
  CONSTRAINT `fk_valor_atributo` FOREIGN KEY (`id-atributo`) REFERENCES `atributos` (`id`),
  CONSTRAINT `fk_valor_dispositivo` FOREIGN KEY (`id-dispositivo`) REFERENCES `dispositivos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=189 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valores_actuales`
--

LOCK TABLES `valores_actuales` WRITE;
/*!40000 ALTER TABLE `valores_actuales` DISABLE KEYS */;
INSERT INTO `valores_actuales` VALUES (2,'19.40','Shelly2',1,NULL,NULL),(3,'19.40','Shelly3',1,NULL,NULL),(4,'49.30','Shelly3',3,NULL,NULL),(5,'5.29','Shelly3',8,NULL,NULL),(6,'76.0','Shelly1',1,NULL,NULL),(7,'88.2','Shelly1',3,NULL,NULL),(8,'26.0','Shelly1',8,NULL,NULL),(9,'47.30','Shelly2',3,NULL,NULL),(10,'64.00','Shelly2',8,NULL,NULL),(96,'29.00','Shelly TRV ',1,NULL,NULL),(97,'4.00','Shelly TRV ',8,NULL,NULL),(98,'22.30','Shelly TRV ',87,'shellies/shellytrv4/thermostat/0/command/target_t','{{ valor }}'),(111,NULL,'Dispositivo actuador',57,'/a','{{ e }}'),(112,NULL,'Dispositivo actuador',58,NULL,NULL),(113,NULL,'Dispositivo actuador',59,'/a','{{ e }}'),(114,NULL,'Dispositivo actuador',197,NULL,NULL),(115,NULL,'Dispositivo actuador',198,'/a','{{ e }}'),(116,'18.00','Shelly4',1,NULL,NULL),(117,'14.00','Shelly4',3,NULL,NULL),(118,'22.00','Shelly4',8,NULL,NULL),(125,NULL,'Shelly 6',1,NULL,NULL),(126,NULL,'Shelly 6',3,NULL,NULL),(127,NULL,'Shelly 6',8,NULL,NULL),(128,NULL,'Nuevo',1,NULL,NULL),(129,NULL,'Nuevo',2,NULL,NULL),(130,NULL,'Nuevo',3,NULL,NULL),(131,NULL,'Nuevo',4,NULL,NULL),(132,NULL,'Nuevo',8,NULL,NULL),(133,NULL,'Shelly 1',1,NULL,NULL),(134,NULL,'Shelly 1',3,NULL,NULL),(135,NULL,'Shelly 1',8,NULL,NULL);
/*!40000 ALTER TABLE `valores_actuales` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-04  0:20:22
