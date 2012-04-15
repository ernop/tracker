-- MySQL dump 10.13  Distrib 5.1.49, for debian-linux-gnu (x86_64)
--
-- Host: mysql.fuseki.net    Database: django_track
-- ------------------------------------------------------
-- Server version	5.1.53-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_fbfc09f1` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(45,'Can delete exercise',15,'delete_exercise'),(44,'Can change exercise',15,'change_exercise'),(43,'Can add exercise',15,'add_exercise'),(16,'Can add content type',6,'add_contenttype'),(17,'Can change content type',6,'change_contenttype'),(18,'Can delete content type',6,'delete_contenttype'),(19,'Can add session',7,'add_session'),(20,'Can change session',7,'change_session'),(21,'Can delete session',7,'delete_session'),(22,'Can add site',8,'add_site'),(23,'Can change site',8,'change_site'),(24,'Can delete site',8,'delete_site'),(25,'Can add domain',9,'add_domain'),(26,'Can change domain',9,'change_domain'),(27,'Can delete domain',9,'delete_domain'),(28,'Can add source',10,'add_source'),(29,'Can change source',10,'change_source'),(30,'Can delete source',10,'delete_source'),(31,'Can add product',11,'add_product'),(32,'Can change product',11,'change_product'),(33,'Can delete product',11,'delete_product'),(34,'Can add currency',12,'add_currency'),(35,'Can change currency',12,'change_currency'),(36,'Can delete currency',12,'delete_currency'),(37,'Can add purchase',13,'add_purchase'),(38,'Can change purchase',13,'change_purchase'),(39,'Can delete purchase',13,'delete_purchase'),(40,'Can add person',14,'add_person'),(41,'Can change person',14,'change_person'),(42,'Can delete person',14,'delete_person'),(46,'Can add muscle',16,'add_muscle'),(47,'Can change muscle',16,'change_muscle'),(48,'Can delete muscle',16,'delete_muscle'),(49,'Can add set',17,'add_set'),(50,'Can change set',17,'change_set'),(51,'Can delete set',17,'delete_set'),(52,'Can add ex weight',18,'add_exweight'),(53,'Can change ex weight',18,'change_exweight'),(54,'Can delete ex weight',18,'delete_exweight'),(55,'Can add workout',19,'add_workout'),(56,'Can change workout',19,'change_workout'),(57,'Can delete workout',19,'delete_workout'),(58,'Can add measurement',20,'add_measurement'),(59,'Can change measurement',20,'change_measurement'),(60,'Can delete measurement',20,'delete_measurement'),(61,'Can add measuring spot',21,'add_measuringspot'),(62,'Can change measuring spot',21,'change_measuringspot'),(63,'Can delete measuring spot',21,'delete_measuringspot');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'djangotrack','','','ernestfrench@gmail.com','sha1$60af5$a360ac1d5b1fb97ff864fd1a6306b857b64b8689',1,1,1,'2012-04-01 23:12:31','2012-04-01 23:12:31'),(2,'ernie','','','ernestfrench@gmail.com','pbkdf2_sha256$10000$NUe6R6UeMcPr$j3nnv3xZGu40kFec06pTsbOy2UrXuwftH2czyjZsXm8=',1,1,1,'2012-04-11 16:20:46','2012-04-01 23:13:09');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `currency`
--

DROP TABLE IF EXISTS `currency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `currency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `symbol` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `currency`
--

LOCK TABLES `currency` WRITE;
/*!40000 ALTER TABLE `currency` DISABLE KEYS */;
INSERT INTO `currency` VALUES (1,'RMB','元'),(2,'USD','$'),(3,'SGD','s$'),(4,'Euro','€'),(5,'Vnd','vnd'),(6,'HKD','HKD');
/*!40000 ALTER TABLE `currency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=349 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2012-04-02 19:24:13',2,9,'1','Food',1,''),(2,'2012-04-02 19:24:16',2,11,'1','Steak',1,''),(3,'2012-04-02 19:24:36',2,12,'1','rmb',1,''),(4,'2012-04-02 19:24:55',2,10,'1','fairwood',1,''),(5,'2012-04-02 19:25:09',2,13,'1','Steak 1 for 47.00元 each, total 47.000000',1,''),(6,'2012-04-02 19:25:25',2,9,'2','Transportation',1,''),(7,'2012-04-02 19:25:28',2,11,'2','parking',1,''),(8,'2012-04-02 19:25:41',2,10,'2','YingZuo',1,''),(9,'2012-04-02 19:25:44',2,13,'2','parking 1 for 1.00元 each, total 1.000000',1,''),(10,'2012-04-02 19:32:54',2,12,'2','USD',1,''),(11,'2012-04-02 19:33:07',2,12,'1','RMB',2,'Changed name.'),(12,'2012-04-02 20:01:52',2,9,'3','House',1,''),(13,'2012-04-02 20:02:01',2,11,'3','Ayi',1,''),(14,'2012-04-02 20:02:16',2,10,'3','home',1,''),(15,'2012-04-02 20:02:20',2,13,'3','Ayi 3 for 20.00元 each, total 60.000000',1,''),(16,'2012-04-02 20:03:32',2,10,'4','wallet',1,''),(17,'2012-04-02 20:04:05',2,9,'4','cash',1,''),(18,'2012-04-02 20:04:07',2,11,'4','cash in wallet',1,''),(19,'2012-04-02 20:04:10',2,13,'4','cash in wallet 1 for -930.00元 each, total -930.000000',1,''),(20,'2012-04-02 20:12:24',2,11,'5','cash',1,''),(21,'2012-04-02 20:12:35',2,13,'5','cash 1 for 432.00$ each, total 432.000000',1,''),(22,'2012-04-02 20:13:14',2,12,'3','SGD',1,''),(23,'2012-04-02 20:13:21',2,13,'6','cash 1 for 20.00s$ each, total 20.000000',1,''),(24,'2012-04-02 20:13:58',2,12,'4','Euro',1,''),(25,'2012-04-02 20:15:02',2,13,'7','cash 1 for 35.00€ each, total 35.000000',1,''),(26,'2012-04-02 20:16:12',2,12,'5','Vnd',1,''),(27,'2012-04-02 20:16:23',2,13,'8','cash 1 for 17000000.00vnd each, total 17000000.000000',1,''),(28,'2012-04-02 20:16:46',2,13,'8','cash 1 for -17000000.00vnd each, total -17000000.000000',2,'Changed cost.'),(29,'2012-04-02 20:16:50',2,13,'6','cash 1 for -20.00s$ each, total -20.000000',2,'Changed cost.'),(30,'2012-04-02 20:16:57',2,13,'7','cash 1 for -35.00€ each, total -35.000000',2,'Changed cost.'),(31,'2012-04-02 20:22:40',2,12,'6','HKD',1,''),(32,'2012-04-02 20:22:44',2,13,'9','cash 1 for -2950.00HKD each, total -2950.000000',1,''),(33,'2012-04-02 20:27:03',2,13,'5','cash 1 for -432.00$ each, total -432.000000',2,'Changed cost.'),(34,'2012-04-03 09:26:46',2,9,'5','health',1,''),(35,'2012-04-03 09:26:48',2,11,'6','ZMA',1,''),(36,'2012-04-03 09:27:05',2,10,'5','taobao',1,''),(37,'2012-04-03 09:27:08',2,13,'10','ZMA 1 for 48.00元 each, total 48.00',1,''),(38,'2012-04-03 09:59:59',2,11,'7','Vitamins',1,''),(39,'2012-04-03 10:00:10',2,13,'11','Vitamins 1 for 154.00元 each, total 154.00',1,''),(40,'2012-04-03 15:32:11',2,10,'6','salary',1,''),(41,'2012-04-03 15:32:14',2,13,'12','cash 1 for -9000.00元 each, total -9000.00',1,''),(42,'2012-04-03 22:27:34',2,11,'8','coconut cream',1,''),(43,'2012-04-03 22:28:02',2,10,'7','Kevin\'s shop',1,''),(44,'2012-04-03 22:28:11',2,13,'13','coconut cream 1 for 11.50元 each, total 11.50',1,''),(45,'2012-04-03 22:28:29',2,11,'9','KerryGold Cheese',1,''),(46,'2012-04-03 22:28:49',2,13,'14','KerryGold Cheese 2 for 29.00元 each, total 58.00',1,''),(47,'2012-04-03 22:29:16',2,11,'10','black olives',1,''),(48,'2012-04-03 22:29:34',2,13,'15','black olives 1 for 17.50元 each, total 17.50',1,''),(49,'2012-04-04 15:38:23',2,13,'16','Steak 1 for 47.00元 each, total 47.00',1,''),(50,'2012-04-04 20:25:11',2,18,'31','Squat 105',1,''),(51,'2012-04-04 20:25:22',2,18,'32','Press 99',1,''),(52,'2012-04-04 16:00:57',2,19,'12','2012-04-04',1,''),(53,'2012-04-04 16:01:44',2,18,'33','Clean 100 (27.5)',1,''),(54,'2012-04-04 16:05:09',2,18,'32','Press 99 (27.0)',3,''),(55,'2012-04-04 16:06:31',2,18,'34','Clean 90 (22.5)',1,''),(56,'2012-04-04 16:08:23',2,19,'12','2012-04-04',2,'Added set \"Squat 3@105 lb\". Added set \"Clean 3@100 lb\". Added set \"Clean 4@100 lb\". Added set \"Clean 4@100 lb\". Changed note for set \"Press 5@99 lb\". Changed exweight and note for set \"Press 5@99 lb\". Changed count for set \"Squat 6@105 lb\".'),(57,'2012-04-04 16:09:14',2,19,'12','2012-04-04',2,'Changed count for set \"Clean 5@100 lb\".'),(58,'2012-04-04 16:12:23',2,19,'2','2012-02-21',2,'Deleted set \"Press 5@67 lb\".'),(59,'2012-04-04 16:12:56',2,19,'9','2012-03-05',2,'Changed exweight for set \"Press 5@89 lb\". Changed exweight for set \"Press 5@89 lb\".'),(60,'2012-04-04 16:14:23',2,19,'13','2012-03-07',1,''),(61,'2012-04-04 16:14:36',2,19,'13','2012-03-07',2,'Added set \"Deadlift 5@185 lb\".'),(62,'2012-04-04 16:15:35',2,18,'35','Press 95 (25.0)',1,''),(63,'2012-04-04 16:15:46',2,19,'14','2012-03-10',1,''),(64,'2012-04-04 16:16:28',2,19,'14','2012-03-10',2,'Added set \"Press 5@95 lb\". Added set \"Deadlift 5@179 lb\". Added set \"Deadlift 5@185 lb\".'),(65,'2012-04-04 16:17:43',2,15,'10','DB Bench Press',1,''),(66,'2012-04-04 16:18:39',2,18,'36','DB Bench Press 80',1,''),(67,'2012-04-04 16:20:15',2,18,'37','Bench Press 89 (22.0)',1,''),(68,'2012-04-04 16:20:25',2,18,'38','Bench Press 111 (33.0)',1,''),(69,'2012-04-04 16:21:50',2,19,'11','2012-03-10',2,'Changed date. Changed exweight for set \"Press 5@95 lb\". Changed exweight for set \"Press 5@95 lb\". Changed exweight for set \"Press 5@95 lb\".'),(70,'2012-04-04 16:22:02',2,19,'11','2012-03-10',2,'No fields changed.'),(71,'2012-04-04 16:22:17',2,19,'14','2012-03-10',3,''),(72,'2012-04-04 16:23:29',2,19,'15','2012-03-12',1,''),(73,'2012-04-04 16:24:07',2,19,'15','2012-03-12',2,'Added set \"DB Bench Press 5@80 lb\". Added set \"Deadlift 5@185 lb\". Added set \"Bench Press 5@89 lb\". Added set \"Bench Press 5@111 lb\".'),(74,'2012-04-04 16:25:08',2,19,'16','2012-03-14',1,''),(75,'2012-04-04 16:25:40',2,15,'11','DB rows',1,''),(76,'2012-04-04 16:26:02',2,18,'39','DB rows 30',1,''),(77,'2012-04-04 16:26:12',2,18,'40','DB rows 40',1,''),(78,'2012-04-04 16:26:52',2,19,'16','2012-03-14',2,'Added set \"Press 5@89 lb\". Added set \"DB rows 5@30 lb\". Added set \"DB rows 5@40 lb\". Added set \"DB rows 5@40 lb\".'),(79,'2012-04-04 16:28:53',2,19,'17','2012-03-17',1,''),(80,'2012-04-04 16:29:10',2,18,'41','Deadlift 201 (78.0)',1,''),(81,'2012-04-04 16:29:45',2,19,'17','2012-03-17',2,'Added set \"Bench Press 5@139 lb\". Added set \"Deadlift 5@201 lb\".'),(82,'2012-04-04 16:30:07',2,19,'18','3012-03-19',1,''),(83,'2012-04-04 16:30:51',2,19,'19','2012-03-21',1,''),(84,'2012-04-04 16:31:18',2,19,'19','2012-03-21',2,'Added set \"Press 4@95 lb\". Added set \"Deadlift 5@201 lb\".'),(85,'2012-04-04 16:31:46',2,18,'42','Bench Press 145 (50.0)',1,''),(86,'2012-04-04 16:32:07',2,19,'20','2012-03-24',1,''),(87,'2012-04-04 16:32:37',2,19,'20','2012-03-24',2,'Added set \"Bench Press 5@145 lb\". Added set \"Bench Press 5@145 lb\". Added set \"Bench Press 5@145 lb\". Added set \"Pullup 3@0 lb\". Added set \"Pullup 4@0 lb\".'),(88,'2012-04-04 16:35:10',2,19,'20','2012-03-24',2,'Added set \"Pullup 3@0 lb\". Added set \"Deadlift 5@135 lb\". Added set \"Deadlift 5@135 lb\".'),(89,'2012-04-04 16:36:18',2,18,'43','Press 101 (28.0)',1,''),(90,'2012-04-04 16:36:34',2,19,'21','2012-03-26',1,''),(91,'2012-04-04 16:37:37',2,19,'21','2012-03-26',2,'Added set \"Press 5@101 lb\". Added set \"Press 5@99 lb\". Added set \"Press 5@99 lb\". Added set \"Clean 3@90 lb\".'),(92,'2012-04-04 16:38:44',2,19,'22','2012-03-28',1,''),(93,'2012-04-04 16:40:57',2,19,'23','2012-03-29',1,''),(94,'2012-04-04 16:43:52',2,19,'10','2012-04-04',2,'Changed date. Changed exweight for set \"Bench Press 5@145 lb\". Changed exweight for set \"Bench Press 5@145 lb\". Changed exweight for set \"Bench Press 5@139 lb\".'),(95,'2012-04-04 16:45:00',2,19,'12','2012-04-04',2,'No fields changed.'),(96,'2012-04-04 16:45:23',2,19,'10','2012-04-04',3,''),(97,'2012-04-05 00:47:29',2,19,'12','2012-04-04',2,'Changed date.'),(98,'2012-04-05 00:47:59',2,19,'18','2012-03-19',2,'Changed date.'),(99,'2012-04-05 11:02:04',2,19,'23','2012-03-30',2,'Changed date.'),(100,'2012-04-05 19:05:22',2,11,'11','sashimi',1,''),(101,'2012-04-05 19:09:30',2,13,'17','sashimi 8 for 6.00元 each, total 48.00',1,''),(102,'2012-04-05 19:09:38',2,10,'8','kaitensushi yingzuo',1,''),(103,'2012-04-05 19:09:58',2,13,'17','sashimi 8 for 6.00元 each, total 48.00',2,'Changed source.'),(104,'2012-04-05 20:13:25',2,11,'12','mustard',1,''),(105,'2012-04-05 20:13:36',2,10,'9','april gourmet',1,''),(106,'2012-04-05 20:13:39',2,13,'18','mustard 1 for 17.50元 each, total 17.50',1,''),(107,'2012-04-05 20:15:06',2,13,'19','parking 1 for 1.00元 each, total 1.00',1,''),(108,'2012-04-05 20:15:26',2,11,'13','coconut milk',1,''),(109,'2012-04-05 20:15:33',2,13,'20','coconut milk 1 for 10.00元 each, total 10.00',1,''),(110,'2012-04-05 20:20:28',2,11,'14','nurnberger sausage',1,''),(111,'2012-04-05 20:20:39',2,13,'21','nurnberger sausage 1 for 30.00元 each, total 30.00',1,''),(112,'2012-04-05 20:47:41',2,11,'15','sausages',1,''),(113,'2012-04-05 20:48:37',2,13,'22','sausages 1 for 27.50元 each, total 27.50',1,''),(114,'2012-04-05 20:48:50',2,11,'16','turkey',1,''),(115,'2012-04-05 20:49:10',2,11,'17','turkey 100g',1,''),(116,'2012-04-05 20:49:18',2,13,'23','turkey 100g 3 for 26.67元 each, total 80.00',1,''),(117,'2012-04-05 20:49:27',2,11,'18','cheddar 100g',1,''),(118,'2012-04-05 20:49:38',2,13,'24','cheddar 100g 3 for 9.67元 each, total 29.00',1,''),(119,'2012-04-06 09:39:16',2,19,'12','2012-04-04',2,'Changed count for set \"Clean 3@100 lb\". Changed count for set \"Clean 4@100 lb\". Changed count for set \"Squat 5@105 lb\".'),(120,'2012-04-06 09:39:52',2,19,'23','2012-03-30',2,'Deleted set \"Press 5@89 lb\". Deleted set \"Press 4@89 lb\".'),(121,'2012-04-06 09:41:03',2,19,'23','2012-03-30',2,'Changed exweight for set \"Bench Press 4@139 lb\". Changed exweight for set \"Bench Press 3@139 lb\". Changed exweight for set \"Bench Press 3@139 lb\". Changed exweight for set \"Deadlift 3@199 lb\". Changed exweight for set \"Deadlift 5@209 lb\". Changed exweight for set \"Pullup 5@0 lb\". Deleted set \"Pullup 5@0 lb\".'),(122,'2012-04-06 13:39:48',2,19,'23','2012-03-30',2,'Deleted set \"Clean 6@90 lb\".'),(123,'2012-04-06 13:44:40',2,13,'25','Steak 1 for 47.00元 each, total 47.00',1,''),(124,'2012-04-06 19:27:05',2,19,'23','2012-03-30',2,'Changed exweight and count for set \"Bench Press 5@145 lb\". Changed exweight and count for set \"Bench Press 4@145 lb\". Changed exweight and count for set \"Bench Press 6@135 lb\". Changed exweight for set \"Deadlift 5@199 lb\". Changed exweight for set \"Deadlift 3@209 lb\".'),(125,'2012-04-06 19:28:10',2,18,'44','Press 80 (17.5)',1,''),(126,'2012-04-06 19:29:19',2,18,'45','Squat 100 (27.5)',1,''),(127,'2012-04-06 19:29:29',2,19,'24','2012-03-29',1,''),(128,'2012-04-06 19:29:58',2,19,'24','2012-03-29',2,'Added set \"Squat 5@100 lb\". Added set \"Squat 5@100 lb\".'),(129,'2012-04-06 19:31:30',2,19,'23','2012-03-31',2,'Changed date.'),(130,'2012-04-06 21:04:54',2,18,'46','Bench Press 147 (51.0)',1,''),(131,'2012-04-06 21:05:53',2,18,'47','Deadlift 205 (80.0)',1,''),(132,'2012-04-06 21:06:03',2,19,'25','2012-04-06',1,''),(133,'2012-04-06 21:06:41',2,18,'48','Deadlift 215 (85.0)',1,''),(134,'2012-04-06 21:07:05',2,19,'25','2012-04-06',2,'Added set \"Deadlift 5@215 lb\".'),(135,'2012-04-06 21:08:56',2,19,'25','2012-04-06',2,'Added set \"Pullup 3@0 lb\". Added set \"Pullup 4@0 lb\". Added set \"Pullup 3@0 lb\".'),(136,'2012-04-07 06:01:10',2,13,'26','parking 1 for 1.00元 each, total 1.00',1,''),(137,'2012-04-07 08:12:48',2,9,'6','fee',1,''),(138,'2012-04-07 08:12:51',2,11,'19','park membership',1,''),(139,'2012-04-07 08:13:13',2,10,'10','chaoyang park',1,''),(140,'2012-04-07 08:13:16',2,13,'27','park membership 1 for 8.50元 each, total 8.50',1,''),(141,'2012-04-07 09:57:21',2,9,'3','house',2,'Changed name.'),(142,'2012-04-08 10:38:10',2,21,'1','weight',1,''),(143,'2012-04-08 10:40:17',2,20,'3','weight 2012-04-08:90.40',1,''),(144,'2012-04-08 10:40:26',2,20,'3','weight 2012-04-08:90.40',3,''),(145,'2012-04-08 10:40:26',2,20,'2','weight 2012-04-08:90.00',3,''),(146,'2012-04-08 10:48:28',2,20,'4','weight 2012-04-08:90.40',1,''),(147,'2012-04-08 10:48:36',2,20,'1','weight 2012-04-08:90.40',3,''),(148,'2012-04-08 10:49:14',2,21,'2','stomach caliper',1,''),(149,'2012-04-08 10:49:19',2,20,'5','stomach caliper 2012-04-08:24.50',1,''),(150,'2012-04-08 10:50:18',2,21,'3','chest caliper',1,''),(151,'2012-04-08 10:50:48',2,20,'6','chest caliper 2012-04-08:10.80',1,''),(152,'2012-04-08 10:51:18',2,21,'4','midaxillary',1,''),(153,'2012-04-08 10:51:24',2,20,'7','midaxillary 2012-04-08:17.90',1,''),(154,'2012-04-08 10:52:03',2,21,'5','bicep caliper',1,''),(155,'2012-04-08 10:52:19',2,20,'8','bicep caliper 2012-04-08:3.30',1,''),(156,'2012-04-08 10:57:04',2,21,'4','midaxillary caliper',2,'Changed name.'),(157,'2012-04-08 11:02:34',2,21,'6','abdominal vertical caliper',1,''),(158,'2012-04-08 11:03:26',2,20,'5','abdominal vertical caliper 2012-04-08: <b>38.20</b>',2,'Changed place and amount.'),(159,'2012-04-08 11:04:14',2,21,'7','abdominal caliper',1,''),(160,'2012-04-08 11:04:18',2,20,'9','abdominal caliper 2012-04-08: <b>35.70</b>',1,''),(161,'2012-04-08 11:04:58',2,21,'7','suprailiac',2,'Changed name.'),(162,'2012-04-08 11:05:16',2,21,'2','stomach caliper',3,''),(163,'2012-04-08 11:06:50',2,21,'8','thigh caliper',1,''),(164,'2012-04-08 11:07:03',2,20,'10','thigh caliper 2012-04-08: <b>33.00</b>',1,''),(165,'2012-04-08 11:08:25',2,21,'9','inside calf',1,''),(166,'2012-04-08 11:08:30',2,20,'11','inside calf 2012-04-08: <b>9.50</b>',1,''),(167,'2012-04-08 11:08:55',2,20,'10','thigh caliper 2012-04-08: <b>18.90</b>',2,'Changed amount.'),(168,'2012-04-08 11:09:12',2,20,'9','suprailiac 2012-04-08: <b>17.00</b>',2,'Changed amount.'),(169,'2012-04-08 11:09:54',2,20,'5','abdominal vertical caliper 2012-04-08: <b>19.50</b>',2,'Changed amount.'),(170,'2012-04-08 11:10:28',2,20,'6','chest caliper 2012-04-08: <b>13.50</b>',2,'Changed amount.'),(171,'2012-04-08 11:10:57',2,20,'7','midaxillary caliper 2012-04-08: <b>23.90</b>',2,'Changed amount.'),(172,'2012-04-08 11:11:38',2,20,'8','bicep caliper 2012-04-08: <b>3.70</b>',2,'Changed amount.'),(173,'2012-04-08 11:55:49',2,21,'10','tricep caliper',1,''),(174,'2012-04-08 11:56:25',2,20,'12','tricep caliper 2012-04-08: <b>11.90</b>',1,''),(175,'2012-04-08 11:57:47',2,21,'11','lower back',1,''),(176,'2012-04-08 11:57:56',2,20,'13','lower back 2012-04-08: <b>22.30</b>',1,''),(177,'2012-04-08 11:59:00',2,21,'12','waist mm',1,''),(178,'2012-04-08 11:59:10',2,20,'14','waist mm 2012-04-08: <b>950.00</b>',1,''),(179,'2012-04-08 11:59:31',2,21,'13','chest mm',1,''),(180,'2012-04-08 11:59:36',2,20,'15','chest mm 2012-04-08: <b>990.00</b>',1,''),(181,'2012-04-08 12:00:31',2,21,'14','thigh mm',1,''),(182,'2012-04-08 12:00:44',2,20,'16','thigh mm 2012-03-29: <b>550.00</b>',1,''),(183,'2012-04-08 12:00:50',2,20,'15','chest mm 2012-03-29: <b>990.00</b>',2,'Changed date.'),(184,'2012-04-08 12:00:56',2,20,'14','waist mm 2012-03-29: <b>950.00</b>',2,'Changed date.'),(185,'2012-04-08 20:07:55',2,13,'28','parking for 元1.00',1,''),(186,'2012-04-08 20:08:09',2,11,'20','avocado',1,''),(187,'2012-04-08 20:08:26',2,10,'11','dongjiao market',1,''),(188,'2012-04-08 20:08:33',2,13,'29','avocado(6) for 元10.00',1,''),(189,'2012-04-08 20:08:52',2,13,'30','avocado(3) for 元24.00',1,''),(190,'2012-04-08 20:09:13',2,13,'31','Steak for 元49.00',1,''),(191,'2012-04-08 20:10:37',2,11,'21','water',1,''),(192,'2012-04-08 20:10:53',2,13,'32','water for 元3.50',1,''),(193,'2012-04-08 20:19:31',2,10,'12','jenny lou\'s',1,''),(194,'2012-04-08 20:19:48',2,13,'33','sausages(6) for 元145.00',1,''),(195,'2012-04-09 10:57:04',2,20,'17','weight 2012-04-09: <b>90.80</b>',1,''),(196,'2012-04-09 13:14:47',2,13,'34','Steak for 元47.00',1,''),(197,'2012-04-09 13:18:55',2,11,'22','salary',1,''),(198,'2012-04-09 13:19:03',2,10,'13','vericant',1,''),(199,'2012-04-09 13:19:07',2,13,'35','salary for 元-9000.00',1,''),(200,'2012-04-09 13:20:32',2,11,'16','turkey',3,''),(201,'2012-04-09 13:21:01',2,13,'29','avocado(6) for 元60.00',2,'Changed cost.'),(202,'2012-04-09 16:02:48',2,11,'23','wine',1,''),(203,'2012-04-09 16:02:59',2,13,'36','wine for 元58.00',1,''),(204,'2012-04-09 19:12:41',2,13,'37','parking for 元1.00',1,''),(205,'2012-04-09 21:26:22',2,18,'49','Press 26 (-9.5)',1,''),(206,'2012-04-09 21:26:35',2,18,'50','Press 97 (26.0)',1,''),(207,'2012-04-09 21:27:26',2,18,'51','Clean 95 (25.0)',1,''),(208,'2012-04-09 21:27:47',2,18,'52','Clean 117 (36.0)',1,''),(209,'2012-04-09 21:29:54',2,19,'26','2012-04-09',1,''),(210,'2012-04-09 21:39:26',2,13,'38','water(2) for 元7.00',1,''),(211,'2012-04-09 21:39:46',2,11,'24','yogurt',1,''),(212,'2012-04-09 21:40:39',2,13,'39','yogurt(4) for 元7.20',1,''),(213,'2012-04-09 22:05:35',2,9,'1','food',2,'Changed name.'),(214,'2012-04-09 22:05:35',2,9,'2','transportation',2,'Changed name.'),(215,'2012-04-10 06:54:40',2,20,'18','weight 2012-04-10: <b>91.20</b>',1,''),(216,'2012-04-10 06:56:25',2,20,'19','chest caliper 2012-04-10: <b>17.50</b>',1,''),(217,'2012-04-10 06:57:08',2,20,'20','midaxillary caliper 2012-04-10: <b>23.10</b>',1,''),(218,'2012-04-10 06:58:12',2,20,'21','bicep caliper 2012-04-10: <b>4.10</b>',1,''),(219,'2012-04-10 06:59:00',2,20,'22','tricep caliper 2012-04-10: <b>12.20</b>',1,''),(220,'2012-04-10 06:59:33',2,20,'23','lower back 2012-04-10: <b>23.40</b>',1,''),(221,'2012-04-10 07:00:30',2,20,'24','thigh mm 2012-04-10: <b>18.00</b>',1,''),(222,'2012-04-10 07:01:30',2,20,'25','inside calf 2012-04-10: <b>11.40</b>',1,''),(223,'2012-04-10 07:02:25',2,20,'26','abdominal vertical caliper 2012-04-10: <b>19.20</b>',1,''),(224,'2012-04-10 07:03:04',2,20,'27','suprailiac 2012-04-10: <b>19.60</b>',1,''),(225,'2012-04-10 07:03:33',2,20,'24','thigh caliper 2012-04-10: <b>18.00</b>',2,'Changed place.'),(226,'2012-04-10 07:32:20',2,21,'6','vertical caliper',2,'Changed name.'),(227,'2012-04-10 07:32:25',2,21,'9','calf caliper',2,'Changed name.'),(228,'2012-04-10 07:32:29',2,21,'11','back caliper',2,'Changed name.'),(229,'2012-04-10 07:32:32',2,21,'7','suprailiac caliper',2,'Changed name.'),(230,'2012-04-10 07:41:20',2,21,'15','thigh cord',1,''),(231,'2012-04-10 07:41:27',2,20,'28','thigh cord 2012-04-10: <b>3.58</b>',1,''),(232,'2012-04-10 07:42:35',2,21,'16','bicep cord',1,''),(233,'2012-04-10 07:42:42',2,20,'29','bicep cord 2012-04-10: <b>2.60</b>',1,''),(234,'2012-04-10 07:44:04',2,21,'17','waist cord',1,''),(235,'2012-04-10 07:44:15',2,20,'30','waist cord 2012-04-10: <b>6.35</b>',1,''),(236,'2012-04-10 07:50:56',2,20,'31','waist cord 2012-03-29: <b>6.45</b>',1,''),(237,'2012-04-10 07:51:57',2,21,'18','chest cord',1,''),(238,'2012-04-10 07:52:01',2,20,'32','chest cord 2012-03-29: <b>6.67</b>',1,''),(239,'2012-04-10 07:52:19',2,20,'31','waist cord 2012-03-29: <b>6.40</b>',2,'Changed amount.'),(240,'2012-04-10 07:52:52',2,20,'33','thigh cord 2012-03-26: <b>3.70</b>',1,''),(241,'2012-04-10 07:53:14',2,20,'14','waist mm 2012-03-29: <b>950.00</b>',3,''),(242,'2012-04-10 07:53:14',2,20,'15','chest mm 2012-03-29: <b>990.00</b>',3,''),(243,'2012-04-10 07:53:14',2,20,'16','thigh mm 2012-03-29: <b>550.00</b>',3,''),(244,'2012-04-10 07:54:10',2,21,'6','abdominal caliper',2,'Changed name.'),(245,'2012-04-10 07:55:34',2,20,'34','chest mm 2012-04-10: <b>6.83</b>',1,''),(246,'2012-04-10 07:56:06',2,21,'12','waist mm',3,''),(247,'2012-04-10 07:56:06',2,21,'14','thigh mm',3,''),(248,'2012-04-10 07:56:47',2,20,'34','chest cord 2012-04-10: <b>6.83</b>',2,'Changed place.'),(249,'2012-04-10 07:57:00',2,21,'13','chest mm',3,''),(250,'2012-04-10 18:12:31',2,13,'40','Vitamins for 元120.00',1,''),(251,'2012-04-10 18:12:40',2,13,'41','Vitamins for 元138.00',1,''),(252,'2012-04-10 18:52:12',2,13,'42','parking for 元1.00',1,''),(253,'2012-04-10 22:25:21',2,20,'35','bicep caliper 2012-04-10: <b>4.50</b>',1,''),(254,'2012-04-10 22:26:03',2,20,'36','tricep caliper 2012-04-10: <b>9.40</b>',1,''),(255,'2012-04-10 22:27:47',2,20,'37','suprailiac caliper 2012-04-10: <b>34.30</b>',1,''),(256,'2012-04-10 22:28:38',2,20,'38','abdominal caliper 2012-04-10: <b>18.80</b>',1,''),(257,'2012-04-10 22:29:32',2,20,'39','chest caliper 2012-04-10: <b>10.40</b>',1,''),(258,'2012-04-10 22:31:58',2,20,'40','thigh caliper 2012-04-10: <b>22.80</b>',1,''),(259,'2012-04-10 22:32:53',2,20,'41','calf caliper 2012-04-10: <b>12.60</b>',1,''),(260,'2012-04-10 22:34:02',2,20,'42','waist cord 2012-04-10: <b>6.33</b>',1,''),(261,'2012-04-10 22:38:26',2,20,'43','bicep cord 2012-04-10: <b>2.42</b>',1,''),(262,'2012-04-10 22:40:25',2,21,'19','wrist cord',1,''),(263,'2012-04-10 22:40:30',2,20,'44','wrist cord 2012-04-10: <b>1.20</b>',1,''),(264,'2012-04-10 22:47:38',2,20,'37','suprailiac caliper 2012-04-10: <b>34.30</b>',3,''),(265,'2012-04-10 22:47:44',2,20,'27','suprailiac caliper 2012-04-10: <b>22.10</b>',2,'Changed amount.'),(266,'2012-04-11 07:52:35',2,11,'25','protein 5lb',1,''),(267,'2012-04-11 07:52:51',2,13,'43','protein 5lb(2) for 元474.00',1,''),(268,'2012-04-11 16:21:26',2,11,'26','eyedrops',1,''),(269,'2012-04-11 16:24:19',2,10,'14','xinli eye clinic',1,''),(270,'2012-04-11 16:24:23',2,13,'44','eyedrops(2) for 元36.50',1,''),(271,'2012-04-11 16:24:48',2,11,'27','eye exam',1,''),(272,'2012-04-11 16:24:55',2,13,'45','eye exam for 元500.00',1,''),(273,'2012-04-11 16:25:18',2,11,'28','LASIK visx4s IR',1,''),(274,'2012-04-11 16:25:28',2,13,'46','LASIK visx4s IR(2) for 元16800.00',1,''),(275,'2012-04-11 19:17:36',2,13,'47','park membership for 元1.00',1,''),(276,'2012-04-11 22:26:58',2,19,'27','2012-04-11',1,''),(277,'2012-04-11 22:39:33',2,20,'45','weight 2012-04-11: <b>92.00</b>',1,''),(278,'2012-04-11 22:40:29',2,20,'46','abdominal caliper 2012-04-11: <b>23.40</b>',1,''),(279,'2012-04-11 22:41:00',2,20,'47','chest caliper 2012-04-11: <b>12.90</b>',1,''),(280,'2012-04-11 22:41:23',2,20,'48','suprailiac caliper 2012-04-11: <b>22.70</b>',1,''),(281,'2012-04-11 22:41:58',2,20,'49','back caliper 2012-04-11: <b>25.60</b>',1,''),(282,'2012-04-11 22:43:07',2,20,'50','thigh caliper 2012-04-11: <b>20.10</b>',1,''),(283,'2012-04-11 22:43:39',2,20,'51','calf caliper 2012-04-11: <b>11.30</b>',1,''),(284,'2012-04-11 22:44:32',2,20,'52','bicep caliper 2012-04-11: <b>4.40</b>',1,''),(285,'2012-04-11 22:45:33',2,20,'53','bicep cord 2012-04-11: <b>2.42</b>',1,''),(286,'2012-04-11 22:46:36',2,20,'54','waist cord 2012-04-11: <b>6.38</b>',1,''),(287,'2012-04-11 22:48:12',2,20,'55','thigh cord 2012-04-11: <b>3.56</b>',1,''),(288,'2012-04-11 22:49:25',2,21,'20','stomach cord',1,''),(289,'2012-04-11 22:49:31',2,20,'56','stomach cord 2012-04-11: <b>6.57</b>',1,''),(290,'2012-04-12 17:25:07',2,13,'46','LASIK visx4s IR(2) for 元16396.00',2,'Changed cost.'),(291,'2012-04-12 17:25:33',2,11,'29','bank account',1,''),(292,'2012-04-12 17:25:47',2,11,'30','bank of china',1,''),(293,'2012-04-12 17:25:55',2,11,'31','HSBK',1,''),(294,'2012-04-12 17:26:33',2,10,'15','old',1,''),(295,'2012-04-12 17:26:38',2,13,'48','bank of china for 元-2293.00',1,''),(296,'2012-04-13 13:02:19',2,13,'49','Steak for 元47.00',1,''),(297,'2012-04-14 07:35:49',2,20,'57','weight 2012-04-14: <b>90.90</b>',1,''),(298,'2012-04-14 07:37:46',2,20,'58','bicep caliper 2012-04-14: <b>3.20</b>',1,''),(299,'2012-04-14 07:38:16',2,20,'59','thigh caliper 2012-04-14: <b>18.70</b>',1,''),(300,'2012-04-14 07:39:25',2,20,'60','calf caliper 2012-04-14: <b>11.10</b>',1,''),(301,'2012-04-14 07:40:30',2,20,'61','suprailiac caliper 2012-04-14: <b>21.40</b>',1,''),(302,'2012-04-14 07:41:01',2,20,'62','abdominal caliper 2012-04-14: <b>23.70</b>',1,''),(303,'2012-04-14 07:41:37',2,20,'63','back caliper 2012-04-14: <b>20.30</b>',1,''),(304,'2012-04-14 07:42:25',2,20,'64','tricep caliper 2012-04-14: <b>11.10</b>',1,''),(305,'2012-04-14 07:43:38',2,20,'65','chest caliper 2012-04-14: <b>9.50</b>',1,''),(306,'2012-04-14 07:44:57',2,20,'66','waist cord 2012-04-14: <b>6.25</b>',1,''),(307,'2012-04-14 07:45:47',2,20,'67','bicep cord 2012-04-14: <b>2.45</b>',1,''),(308,'2012-04-14 07:46:40',2,20,'68','thigh cord 2012-04-14: <b>3.66</b>',1,''),(309,'2012-04-14 07:49:20',2,20,'69','midaxillary caliper 2012-04-14: <b>19.50</b>',1,''),(310,'2012-04-14 13:41:22',2,11,'32','phone card',1,''),(311,'2012-04-14 13:41:43',2,10,'16','xiaomaibu',1,''),(312,'2012-04-14 13:41:51',2,13,'50','phone card(2) for 元200.00',1,''),(313,'2012-04-14 13:49:30',2,11,'33','vegetables',1,''),(314,'2012-04-14 13:50:09',2,13,'51','vegetables for 元10.00',1,''),(315,'2012-04-14 19:38:19',2,18,'53','Squat 111 (33.0)',1,''),(316,'2012-04-14 19:38:53',2,18,'54','Clean 115 (35.0)',1,''),(317,'2012-04-14 19:39:56',2,19,'28','2012-04-14',1,''),(318,'2012-04-14 19:40:51',2,19,'28','2012-04-14',2,'Changed exweight for set \"Squat 7@111 lb\".'),(319,'2012-04-14 19:48:40',2,9,'7','clothes',1,''),(320,'2012-04-14 19:48:44',2,11,'34','sunglasses',1,''),(321,'2012-04-14 19:48:59',2,10,'17','nanluoguxiang',1,''),(322,'2012-04-14 19:49:09',2,13,'52','sunglasses for 元30.00',1,''),(323,'2012-04-14 19:49:27',2,10,'18','shuangjing',1,''),(324,'2012-04-14 19:49:33',2,13,'53','water for 元2.00',1,''),(325,'2012-04-15 01:24:47',2,11,'35','taxi',1,''),(326,'2012-04-15 01:25:01',2,10,'19','home',1,''),(327,'2012-04-15 01:25:06',2,13,'54','taxi for 元29.00',1,''),(328,'2012-04-15 01:25:23',2,13,'55','taxi for 元29.00',1,''),(329,'2012-04-15 01:25:34',2,13,'56','taxi for 元30.00',1,''),(330,'2012-04-15 11:14:34',2,20,'70','abdominal caliper 2012-04-15: <b>19.00</b>',1,''),(331,'2012-04-15 11:15:41',2,20,'71','abdominal caliper 2012-04-15: <b>22.40</b>',1,''),(332,'2012-04-15 11:16:00',2,20,'70','suprailiac caliper 2012-04-15: <b>19.00</b>',2,'Changed place.'),(333,'2012-04-15 11:16:47',2,20,'72','bicep caliper 2012-04-15: <b>4.10</b>',1,''),(334,'2012-04-15 11:17:40',2,20,'73','back caliper 2012-04-15: <b>19.60</b>',1,''),(335,'2012-04-15 11:18:12',2,20,'74','midaxillary caliper 2012-04-15: <b>21.50</b>',1,''),(336,'2012-04-15 11:18:40',2,20,'75','calf caliper 2012-04-15: <b>9.50</b>',1,''),(337,'2012-04-15 11:19:17',2,20,'76','weight 2012-04-15: <b>91.10</b>',1,''),(338,'2012-04-15 11:46:37',2,20,'77','waist cord 2012-04-15: <b>6.33</b>',1,''),(339,'2012-04-15 11:47:38',2,20,'78','bicep cord 2012-04-15: <b>2.45</b>',1,''),(340,'2012-04-15 11:50:34',2,20,'79','stomach cord 2012-04-15: <b>6.38</b>',1,''),(341,'2012-04-15 11:51:05',2,20,'80','stomach cord 2012-04-15: <b>6.38</b>',1,''),(342,'2012-04-15 12:20:23',2,13,'57','Ayi(3) for 元70.00',1,''),(343,'2012-04-15 12:23:11',2,11,'36','eggs',1,''),(344,'2012-04-15 12:29:07',2,10,'20','ayi',1,''),(345,'2012-04-15 12:29:31',2,13,'58','eggs(45) for 元42.00',1,''),(346,'2012-04-15 12:30:04',2,11,'37','milk 500ml',1,''),(347,'2012-04-15 12:30:20',2,13,'59','milk 500ml(10) for 元42.00',1,''),(348,'2012-04-15 18:55:42',2,11,'29','bank account',3,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(15,'exercise','workout','exercise'),(6,'content type','contenttypes','contenttype'),(7,'session','sessions','session'),(8,'site','sites','site'),(9,'domain','buy','domain'),(10,'source','buy','source'),(11,'product','buy','product'),(12,'currency','buy','currency'),(13,'purchase','buy','purchase'),(14,'person','buy','person'),(16,'muscle','workout','muscle'),(17,'set','workout','set'),(18,'ex weight','workout','exweight'),(19,'workout','workout','workout'),(20,'measurement','workout','measurement'),(21,'measuring spot','workout','measuringspot');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('01926ca2d5fa0ceadfe515a487741e8b','MjQ0OTFkZjI2YTUyZGNkYWQyNWM5NmEzZGY3YWZhNzhjNTQ4OWQ5ODqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-04-18 15:47:55'),('c3f1fdb9dacef8264e4e3ef5412d11bd','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS4xNGI0OGY2YWI0NDY2NDA3MTMy\nYjExNTVjNjM3NWUzMw==\n','2012-04-17 09:26:00'),('5b1a5513651f54301baf3d01f928f5a6','MjQ0OTFkZjI2YTUyZGNkYWQyNWM5NmEzZGY3YWZhNzhjNTQ4OWQ5ODqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-04-19 10:58:49'),('66bce63cc0909f847b1f798a2a424168','MjQ0OTFkZjI2YTUyZGNkYWQyNWM5NmEzZGY3YWZhNzhjNTQ4OWQ5ODqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-04-19 08:44:31'),('03dc75f5906c14385e9a03dd0eba7159','MjQ0OTFkZjI2YTUyZGNkYWQyNWM5NmEzZGY3YWZhNzhjNTQ4OWQ5ODqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-04-25 16:20:46');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domain`
--

DROP TABLE IF EXISTS `domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `created` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domain`
--

LOCK TABLES `domain` WRITE;
/*!40000 ALTER TABLE `domain` DISABLE KEYS */;
INSERT INTO `domain` VALUES (1,'food','2012-04-02'),(2,'transportation','2012-04-02'),(3,'house','2012-04-02'),(4,'cash','2012-04-02'),(5,'health','2012-04-03'),(6,'fee','2012-04-07'),(7,'clothes','2012-04-14');
/*!40000 ALTER TABLE `domain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exercise`
--

DROP TABLE IF EXISTS `exercise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exercise` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `barbell` tinyint(1) NOT NULL,
  `note` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exercise`
--

LOCK TABLES `exercise` WRITE;
/*!40000 ALTER TABLE `exercise` DISABLE KEYS */;
INSERT INTO `exercise` VALUES (3,'Deadlift',1,''),(2,'Pullup',0,''),(4,'Clean',1,''),(5,'Press',1,''),(6,'Squat',1,''),(7,'Bench Press',1,''),(8,'dumbell row',0,''),(9,'row machine',0,''),(10,'DB Bench Press',0,''),(11,'DB rows',0,'');
/*!40000 ALTER TABLE `exercise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exercise_pmuscles`
--

DROP TABLE IF EXISTS `exercise_pmuscles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exercise_pmuscles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exercise_id` int(11) NOT NULL,
  `muscle_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `exercise_id` (`exercise_id`,`muscle_id`),
  KEY `exercise_pmuscles_2799bae2` (`exercise_id`),
  KEY `exercise_pmuscles_375ece13` (`muscle_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exercise_pmuscles`
--

LOCK TABLES `exercise_pmuscles` WRITE;
/*!40000 ALTER TABLE `exercise_pmuscles` DISABLE KEYS */;
INSERT INTO `exercise_pmuscles` VALUES (3,3,16),(2,2,1),(4,5,27),(5,6,19),(6,7,35),(7,10,35),(8,10,14);
/*!40000 ALTER TABLE `exercise_pmuscles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exercise_smuscles`
--

DROP TABLE IF EXISTS `exercise_smuscles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exercise_smuscles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exercise_id` int(11) NOT NULL,
  `muscle_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `exercise_id` (`exercise_id`,`muscle_id`),
  KEY `exercise_smuscles_2799bae2` (`exercise_id`),
  KEY `exercise_smuscles_375ece13` (`muscle_id`)
) ENGINE=MyISAM AUTO_INCREMENT=50 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exercise_smuscles`
--

LOCK TABLES `exercise_smuscles` WRITE;
/*!40000 ALTER TABLE `exercise_smuscles` DISABLE KEYS */;
INSERT INTO `exercise_smuscles` VALUES (8,2,6),(7,2,5),(10,2,9),(4,2,2),(5,2,3),(9,2,8),(11,2,10),(12,2,11),(13,2,12),(14,2,14),(15,2,15),(16,3,17),(17,3,18),(18,3,19),(19,3,21),(20,3,22),(21,3,23),(22,3,13),(23,3,24),(24,3,10),(25,3,11),(26,3,25),(27,3,26),(28,5,28),(29,5,29),(30,5,30),(31,5,12),(32,5,13),(33,5,31),(34,5,32),(35,5,33),(36,5,24),(37,5,34),(38,6,17),(39,6,18),(40,6,21),(41,6,22),(42,6,23),(43,6,16),(44,6,25),(45,6,26),(46,7,36),(47,7,27),(48,7,29),(49,7,33);
/*!40000 ALTER TABLE `exercise_smuscles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exweight`
--

DROP TABLE IF EXISTS `exweight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exweight` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exercise_id` int(11) NOT NULL,
  `weight` int(11) NOT NULL,
  `side` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `exweightindex` (`exercise_id`,`weight`),
  KEY `set_2799bae2` (`exercise_id`)
) ENGINE=MyISAM AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exweight`
--

LOCK TABLES `exweight` WRITE;
/*!40000 ALTER TABLE `exweight` DISABLE KEYS */;
INSERT INTO `exweight` VALUES (1,3,209,82),(2,3,199,77),(3,3,179,67),(4,3,225,90),(5,6,77,16),(6,8,50,25),(7,6,65,10),(8,2,-80,-40),(9,2,-50,-25),(10,7,121,38),(11,3,125,40),(12,6,89,22),(13,5,89,22),(14,3,135,45),(15,2,0,0),(16,9,90,45),(17,5,67,11),(18,9,70,35),(19,7,135,45),(20,7,125,40),(28,7,137,46),(22,3,177,66),(23,5,99,27),(27,7,139,47),(25,2,-60,-30),(26,6,95,25),(29,3,185,70),(30,6,109,32),(31,6,105,30),(33,4,100,27),(34,4,90,22),(35,5,95,25),(36,10,80,40),(37,7,89,22),(38,7,111,33),(39,11,30,15),(40,11,40,20),(41,3,201,78),(42,7,145,50),(43,5,101,28),(44,5,80,17),(45,6,100,27),(46,7,147,51),(47,3,205,80),(48,3,215,85),(49,5,26,-9),(50,5,97,26),(51,4,95,25),(52,4,117,36),(53,6,111,33),(54,4,115,35);
/*!40000 ALTER TABLE `exweight` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measurement`
--

DROP TABLE IF EXISTS `measurement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `measurement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `place_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `amount` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `measurement_c4391d6c` (`place_id`)
) ENGINE=MyISAM AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measurement`
--

LOCK TABLES `measurement` WRITE;
/*!40000 ALTER TABLE `measurement` DISABLE KEYS */;
INSERT INTO `measurement` VALUES (5,6,'2012-04-08 00:00:00',19.5),(6,3,'2012-04-08 00:00:00',13.5),(4,1,'2012-04-08 10:48:24',90.4),(7,4,'2012-04-08 00:00:00',23.9),(8,5,'2012-04-08 00:00:00',3.7),(9,7,'2012-04-08 00:00:00',17),(10,8,'2012-04-08 00:00:00',18.9),(11,9,'2012-04-08 00:00:00',9.5),(12,10,'2012-04-08 00:00:00',11.9),(13,11,'2012-04-08 00:00:00',22.3),(36,10,'2012-04-10 00:00:00',9.4),(35,5,'2012-04-10 00:00:00',4.5),(34,18,'2012-04-10 00:00:00',6.83),(17,1,'2012-04-09 00:00:00',90.8),(18,1,'2012-04-10 00:00:00',91.2),(19,3,'2012-04-10 00:00:00',17.5),(20,4,'2012-04-10 00:00:00',23.1),(21,5,'2012-04-10 00:00:00',4.1),(22,10,'2012-04-10 00:00:00',12.2),(23,11,'2012-04-10 00:00:00',23.4),(24,8,'2012-04-10 00:00:00',18),(25,9,'2012-04-10 00:00:00',11.4),(26,6,'2012-04-10 00:00:00',19.2),(27,7,'2012-04-10 00:00:00',22.1),(28,15,'2012-04-10 00:00:00',3.58),(29,16,'2012-04-10 00:00:00',2.6),(30,17,'2012-04-10 00:00:00',6.35),(31,17,'2012-03-29 00:00:00',6.4),(32,18,'2012-03-29 00:00:00',6.67),(33,15,'2012-03-26 00:00:00',3.7),(45,1,'2012-04-11 00:00:00',92),(38,6,'2012-04-10 00:00:00',18.8),(39,3,'2012-04-10 00:00:00',10.4),(40,8,'2012-04-10 00:00:00',22.8),(41,9,'2012-04-10 00:00:00',12.6),(42,17,'2012-04-10 00:00:00',6.33),(43,16,'2012-04-10 00:00:00',2.42),(44,19,'2012-04-10 00:00:00',1.2),(46,6,'2012-04-11 00:00:00',23.4),(47,3,'2012-04-11 00:00:00',12.9),(48,7,'2012-04-11 00:00:00',22.7),(49,11,'2012-04-11 00:00:00',25.6),(50,8,'2012-04-11 00:00:00',20.1),(51,9,'2012-04-11 00:00:00',11.3),(52,5,'2012-04-11 00:00:00',4.4),(53,16,'2012-04-11 00:00:00',2.42),(54,17,'2012-04-11 00:00:00',6.375),(55,15,'2012-04-11 00:00:00',3.5625),(56,20,'2012-04-11 00:00:00',6.565),(57,1,'2012-04-14 00:00:00',90.9),(58,5,'2012-04-14 00:00:00',3.2),(59,8,'2012-04-14 00:00:00',18.7),(60,9,'2012-04-14 00:00:00',11.1),(61,7,'2012-04-14 00:00:00',21.4),(62,6,'2012-04-14 00:00:00',23.7),(63,11,'2012-04-14 00:00:00',20.3),(64,10,'2012-04-14 00:00:00',11.1),(65,3,'2012-04-14 00:00:00',9.5),(66,17,'2012-04-14 00:00:00',6.25),(67,16,'2012-04-14 00:00:00',2.45),(68,15,'2012-04-14 00:00:00',3.66),(69,4,'2012-04-14 00:00:00',19.5),(70,7,'2012-04-15 00:00:00',19),(71,6,'2012-04-15 00:00:00',22.4),(72,5,'2012-04-15 00:00:00',4.1),(73,11,'2012-04-15 00:00:00',19.6),(74,4,'2012-04-15 00:00:00',21.5),(75,9,'2012-04-15 00:00:00',9.5),(76,1,'2012-04-15 00:00:00',91.1),(77,17,'2012-04-15 00:00:00',6.33),(78,16,'2012-04-15 00:00:00',2.45),(79,20,'2012-04-15 00:00:00',6.38),(80,20,'2012-04-15 00:00:00',6.38);
/*!40000 ALTER TABLE `measurement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measuringspot`
--

DROP TABLE IF EXISTS `measuringspot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `measuringspot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measuringspot`
--

LOCK TABLES `measuringspot` WRITE;
/*!40000 ALTER TABLE `measuringspot` DISABLE KEYS */;
INSERT INTO `measuringspot` VALUES (1,'weight'),(8,'thigh caliper'),(3,'chest caliper'),(4,'midaxillary caliper'),(5,'bicep caliper'),(6,'abdominal caliper'),(7,'suprailiac caliper'),(9,'calf caliper'),(10,'tricep caliper'),(11,'back caliper'),(20,'stomach cord'),(19,'wrist cord'),(15,'thigh cord'),(16,'bicep cord'),(17,'waist cord'),(18,'chest cord');
/*!40000 ALTER TABLE `measuringspot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `muscle`
--

DROP TABLE IF EXISTS `muscle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `muscle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=37 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `muscle`
--

LOCK TABLES `muscle` WRITE;
/*!40000 ALTER TABLE `muscle` DISABLE KEYS */;
INSERT INTO `muscle` VALUES (1,'Latissimus Dorsi'),(2,'Brachialis'),(3,'Brachioradialis'),(5,'Biceps Brachii'),(6,'Teres Major'),(8,'Infraspinatus'),(9,'Teres Minor'),(10,'Rhomboids'),(11,'Levator Scapulae'),(12,'Lower Trapezius'),(13,'Middle Trapezius'),(14,'Pectoralis Minor'),(15,'Long Head Triceps'),(16,'Erector Spinae'),(17,'Gluteus Maximus'),(18,'Adductor Magnus'),(19,'Quadriceps'),(27,'Anterior Deltoid'),(21,'Soleus'),(22,'Hamstrings'),(23,'Gastrocnemius'),(24,'Upper Trapezius'),(25,'Rectus Abdominis'),(26,'Obliques'),(28,'Clavicular Pectoralis Major'),(29,'Triceps Brachii'),(30,'Lateral Deltoid'),(31,'Serratus Anterior, Inferior Digitations'),(32,'Triceps, Long Head'),(33,'Biceps Brachii, Short Head'),(34,'Levator Scapulae'),(35,'Sternal Pectoralis Major'),(36,'Clavicular Pectoralis Major');
/*!40000 ALTER TABLE `muscle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `birthday` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person_met_through`
--

DROP TABLE IF EXISTS `person_met_through`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person_met_through` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_person_id` int(11) NOT NULL,
  `to_person_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `from_person_id` (`from_person_id`,`to_person_id`),
  KEY `person_met_through_55b0c02d` (`from_person_id`),
  KEY `person_met_through_97bd00dc` (`to_person_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person_met_through`
--

LOCK TABLES `person_met_through` WRITE;
/*!40000 ALTER TABLE `person_met_through` DISABLE KEYS */;
/*!40000 ALTER TABLE `person_met_through` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `created` date NOT NULL,
  `domain_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `product_a2431ea` (`domain_id`)
) ENGINE=MyISAM AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'Steak','2012-04-02',1),(2,'parking','2012-04-02',2),(3,'Ayi','2012-04-02',3),(4,'cash in wallet','2012-04-02',4),(5,'cash','2012-04-02',4),(6,'ZMA','2012-04-03',5),(7,'Vitamins','2012-04-03',5),(8,'coconut cream','2012-04-03',1),(9,'KerryGold Cheese','2012-04-03',1),(10,'black olives','2012-04-03',1),(11,'sashimi','2012-04-05',1),(12,'mustard','2012-04-05',1),(13,'coconut milk','2012-04-05',1),(14,'nurnberger sausage','2012-04-05',1),(15,'sausages','2012-04-05',1),(23,'wine','2012-04-09',1),(17,'turkey 100g','2012-04-05',1),(18,'cheddar 100g','2012-04-05',1),(19,'park membership','2012-04-07',6),(20,'avocado','2012-04-08',1),(21,'water','2012-04-08',1),(22,'salary','2012-04-09',4),(24,'yogurt','2012-04-09',1),(25,'protein 5lb','2012-04-11',5),(26,'eyedrops','2012-04-11',5),(27,'eye exam','2012-04-11',5),(28,'LASIK visx4s IR','2012-04-11',5),(30,'bank of china','2012-04-12',4),(31,'HSBK','2012-04-12',4),(32,'phone card','2012-04-14',6),(33,'vegetables','2012-04-14',1),(34,'sunglasses','2012-04-14',7),(35,'taxi','2012-04-15',2),(36,'eggs','2012-04-15',1),(37,'milk 500ml','2012-04-15',1);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase`
--

DROP TABLE IF EXISTS `purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `created` date NOT NULL,
  `quantity` float NOT NULL,
  `cost` double NOT NULL,
  `currency_id` int(11) NOT NULL,
  `source_id` int(11) NOT NULL,
  `hour` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_bb420c12` (`product_id`),
  KEY `purchase_41f657b3` (`currency_id`),
  KEY `purchase_89f89e85` (`source_id`)
) ENGINE=MyISAM AUTO_INCREMENT=60 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase`
--

LOCK TABLES `purchase` WRITE;
/*!40000 ALTER TABLE `purchase` DISABLE KEYS */;
INSERT INTO `purchase` VALUES (1,1,'2012-04-02',1,47,1,1,0),(2,2,'2012-04-02',1,1,1,2,0),(3,3,'2012-04-02',3,60,1,3,0),(4,4,'2012-04-02',1,-930,1,4,0),(5,5,'2012-04-02',1,-432,2,3,0),(6,5,'2012-04-02',1,-20,3,3,0),(7,5,'2012-04-02',1,-35,4,3,0),(8,5,'2012-04-02',1,-17000000,5,3,0),(9,5,'2012-04-02',1,-2950,6,3,0),(10,6,'2012-04-03',1,48,1,5,0),(11,7,'2012-04-03',1,154,1,5,0),(12,5,'2012-04-03',1,-9000,1,6,0),(13,8,'2012-04-03',1,11.5,1,7,0),(14,9,'2012-04-03',2,58,1,7,0),(15,10,'2012-04-03',1,17.5,1,7,0),(16,1,'2012-04-04',1,47,1,1,0),(17,11,'2012-04-05',8,48,1,8,0),(18,12,'2012-04-05',1,17.5,1,9,0),(19,2,'2012-04-05',1,1,1,2,0),(20,13,'2012-04-05',1,10,1,9,0),(21,14,'2012-04-05',1,30,1,9,0),(22,15,'2012-04-05',1,27.5,1,9,0),(23,17,'2012-04-05',3,80,1,9,0),(24,18,'2012-04-05',3,29,1,9,0),(25,1,'2012-04-06',1,47,1,1,0),(26,2,'2012-04-07',1,1,1,2,0),(27,19,'2012-04-07',1,8.5,1,10,0),(28,2,'2012-04-08',1,1,1,2,0),(29,20,'2012-04-08',6,60,1,11,0),(30,20,'2012-04-08',3,24,1,11,0),(31,1,'2012-04-08',1,49,1,1,0),(32,21,'2012-04-08',1,3.5,1,2,0),(33,15,'2012-04-08',6,145,1,12,0),(34,1,'2012-04-09',1,47,1,1,0),(35,22,'2012-04-09',1,-9000,1,13,0),(36,23,'2012-04-09',1,58,1,9,0),(37,2,'2012-04-09',1,1,1,2,0),(38,21,'2012-04-09',2,7,1,7,0),(39,24,'2012-04-09',4,7.2,1,7,0),(40,7,'2012-04-10',1,120,1,5,0),(41,7,'2012-04-10',1,138,1,5,0),(42,2,'2012-04-10',1,1,1,2,0),(43,25,'2012-04-11',2,474,1,5,0),(44,26,'2012-04-11',2,36.5,1,14,0),(45,27,'2012-04-11',1,500,1,14,0),(46,28,'2012-04-11',2,16396,1,14,0),(47,19,'2012-04-11',1,1,1,2,0),(48,30,'2012-04-12',1,-2293,1,15,3),(49,1,'2012-04-13',1,47,1,1,1),(50,32,'2012-04-14',2,200,1,16,1),(51,33,'2012-04-14',1,10,1,16,3),(52,34,'2012-04-14',1,30,1,17,2),(53,21,'2012-04-14',1,2,1,18,3),(54,35,'2012-04-15',1,29,1,19,2),(55,35,'2012-04-15',1,29,1,19,4),(56,35,'2012-04-15',1,30,1,19,5),(57,3,'2012-04-15',3,70,1,19,0),(58,36,'2012-04-15',45,42,1,20,1),(59,37,'2012-04-15',10,42,1,20,1);
/*!40000 ALTER TABLE `purchase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_who_with`
--

DROP TABLE IF EXISTS `purchase_who_with`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase_who_with` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `purchase_id` int(11) NOT NULL,
  `person_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `purchase_id` (`purchase_id`,`person_id`),
  KEY `purchase_who_with_eb38737d` (`purchase_id`),
  KEY `purchase_who_with_21b911c5` (`person_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_who_with`
--

LOCK TABLES `purchase_who_with` WRITE;
/*!40000 ALTER TABLE `purchase_who_with` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_who_with` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `set`
--

DROP TABLE IF EXISTS `set`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `set` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exweight_id` int(11) NOT NULL,
  `workout_id` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  `note` varchar(500) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `set_53d7194d` (`exweight_id`),
  KEY `set_41a43c3a` (`workout_id`)
) ENGINE=MyISAM AUTO_INCREMENT=227 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `set`
--

LOCK TABLES `set` WRITE;
/*!40000 ALTER TABLE `set` DISABLE KEYS */;
INSERT INTO `set` VALUES (1,12,5,5,''),(2,12,5,5,''),(3,12,5,5,''),(4,13,5,5,''),(5,13,5,5,''),(6,13,5,5,''),(7,14,5,5,''),(8,14,5,5,''),(9,9,5,5,''),(10,15,5,3,''),(11,16,5,5,''),(12,16,5,5,''),(13,16,5,5,''),(14,5,2,5,''),(15,5,2,5,''),(16,5,2,5,''),(31,5,3,5,''),(33,6,3,5,''),(32,5,3,5,''),(21,17,2,5,''),(22,17,2,5,''),(23,17,2,5,''),(97,26,13,5,''),(25,8,2,5,''),(26,9,2,5,''),(27,9,2,5,''),(28,9,2,5,''),(30,5,3,5,''),(34,5,4,5,''),(35,5,4,5,''),(36,5,4,5,''),(37,10,4,5,''),(38,10,4,5,''),(39,10,4,5,''),(40,11,4,5,''),(41,11,4,5,''),(42,11,4,5,''),(43,5,6,5,''),(44,5,6,5,''),(45,5,6,5,''),(46,19,6,5,''),(47,20,6,5,''),(48,20,6,5,''),(49,22,6,5,''),(50,22,6,5,''),(51,12,7,5,''),(52,12,7,5,''),(53,12,7,5,''),(54,23,7,5,''),(72,15,9,8,''),(56,9,7,8,''),(57,15,7,4,''),(58,25,7,5,''),(59,26,8,5,''),(60,26,8,5,''),(61,26,8,5,''),(62,19,8,5,''),(63,19,8,5,''),(64,19,8,5,''),(65,3,8,5,''),(66,26,9,5,''),(67,26,9,5,''),(68,26,9,5,''),(69,23,9,5,''),(70,13,9,5,''),(71,13,9,5,''),(73,15,9,4,''),(74,3,9,5,''),(184,45,24,5,''),(183,12,24,5,''),(182,5,24,5,''),(181,7,24,5,''),(180,34,24,6,''),(179,33,24,3,''),(178,33,24,3,''),(82,30,11,5,'heavy!'),(83,30,11,5,''),(84,30,11,5,''),(85,35,11,5,''),(86,35,11,5,''),(87,35,11,5,''),(88,23,12,5,'Hard!'),(89,31,12,6,''),(90,31,12,5,''),(91,23,12,5,''),(92,23,12,5,'hard'),(93,31,12,5,''),(94,33,12,4,''),(95,33,12,3,''),(96,33,12,5,''),(98,26,13,5,''),(99,26,13,5,''),(100,27,13,5,''),(101,28,13,5,''),(102,29,13,5,''),(114,36,15,5,''),(113,36,15,5,''),(112,36,15,5,''),(111,26,15,5,''),(110,26,15,5,''),(109,26,15,5,''),(115,29,15,5,''),(116,37,15,5,''),(117,38,15,5,''),(118,26,16,5,''),(119,26,16,5,''),(120,26,16,5,''),(121,13,16,5,''),(122,13,16,5,''),(123,13,16,5,''),(124,39,16,5,''),(125,40,16,5,''),(126,40,16,5,''),(127,26,17,5,''),(128,26,17,5,''),(129,26,17,5,''),(130,27,17,5,''),(131,27,17,5,''),(132,27,17,5,''),(133,41,17,5,''),(134,26,19,5,''),(135,26,19,5,''),(136,26,19,5,''),(137,35,19,5,''),(138,35,19,5,''),(139,35,19,4,''),(140,41,19,5,''),(141,42,20,5,''),(142,42,20,5,''),(143,42,20,5,''),(144,15,20,3,''),(145,15,20,4,''),(146,15,20,3,''),(147,14,20,5,''),(148,14,20,5,''),(149,12,21,5,''),(150,26,21,5,''),(151,26,21,5,''),(152,43,21,5,''),(153,23,21,5,''),(154,23,21,5,''),(155,34,21,3,''),(156,27,22,5,''),(157,27,22,5,''),(158,27,22,5,''),(159,29,22,5,''),(160,15,22,3,''),(161,15,22,5,''),(162,15,22,4,''),(163,15,22,4,''),(177,33,24,3,''),(176,13,24,4,''),(166,42,23,5,''),(167,19,23,6,''),(168,1,23,3,''),(169,42,23,4,''),(174,17,24,5,''),(171,2,23,5,''),(172,15,23,5,''),(175,44,24,4,''),(185,45,24,5,''),(186,45,24,5,''),(187,46,25,5,''),(188,46,25,5,''),(189,46,25,5,'aight, just barely'),(190,47,25,5,''),(191,48,25,5,''),(192,15,25,3,''),(193,15,25,4,''),(194,15,25,3,''),(195,30,26,5,''),(196,30,26,5,''),(197,30,26,5,''),(198,50,26,5,''),(199,50,26,5,''),(200,50,26,5,''),(201,51,26,5,''),(202,51,26,5,''),(203,52,26,5,''),(204,52,26,5,''),(205,52,26,5,''),(206,19,27,5,''),(207,42,27,5,''),(208,42,27,5,''),(209,42,27,5,''),(210,14,27,5,''),(211,22,27,5,''),(212,47,27,5,''),(213,48,27,5,''),(214,15,27,5,''),(215,15,27,4,''),(216,15,27,2,''),(217,53,28,5,''),(218,53,28,5,''),(219,53,28,7,''),(220,23,28,5,''),(221,23,28,5,''),(222,23,28,5,''),(223,54,28,5,''),(224,54,28,5,''),(225,54,28,5,''),(226,54,28,5,'');
/*!40000 ALTER TABLE `set` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `source`
--

DROP TABLE IF EXISTS `source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `created` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `source`
--

LOCK TABLES `source` WRITE;
/*!40000 ALTER TABLE `source` DISABLE KEYS */;
INSERT INTO `source` VALUES (1,'fairwood','2012-04-02'),(2,'YingZuo','2012-04-02'),(3,'home','2012-04-02'),(4,'wallet','2012-04-02'),(5,'taobao','2012-04-03'),(6,'salary','2012-04-03'),(7,'Kevin\'s shop','2012-04-03'),(8,'kaitensushi yingzuo','2012-04-05'),(9,'april gourmet','2012-04-05'),(10,'chaoyang park','2012-04-07'),(11,'dongjiao market','2012-04-08'),(12,'jenny lou\'s','2012-04-08'),(13,'vericant','2012-04-09'),(14,'xinli eye clinic','2012-04-11'),(15,'old','2012-04-12'),(16,'xiaomaibu','2012-04-14'),(17,'nanluoguxiang','2012-04-14'),(18,'shuangjing','2012-04-14'),(19,'home','2012-04-15'),(20,'ayi','2012-04-15');
/*!40000 ALTER TABLE `source` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workout`
--

DROP TABLE IF EXISTS `workout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workout` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workout`
--

LOCK TABLES `workout` WRITE;
/*!40000 ALTER TABLE `workout` DISABLE KEYS */;
INSERT INTO `workout` VALUES (2,'2012-02-20 23:19:24'),(3,'2012-02-18 23:19:58'),(4,'2012-02-22 23:21:38'),(5,'2012-02-25 23:24:25'),(6,'2012-02-27 23:35:13'),(7,'2012-02-29 23:38:40'),(8,'2012-03-02 23:39:08'),(9,'2012-03-04 23:41:21'),(24,'2012-03-29 19:00:00'),(11,'2012-03-10 11:00:00'),(12,'2012-04-04 19:00:00'),(13,'2012-03-07 11:00:00'),(15,'2012-03-12 11:00:00'),(16,'2012-03-14 11:00:00'),(17,'2012-03-17 11:00:00'),(18,'2012-03-19 11:00:00'),(19,'2012-03-21 11:00:00'),(20,'2012-03-24 11:00:00'),(21,'2012-03-26 11:00:00'),(22,'2012-03-28 11:00:00'),(23,'2012-03-31 15:00:00'),(25,'2012-04-06 19:30:00'),(26,'2012-04-09 19:30:00'),(27,'2012-04-11 22:26:58'),(28,'2012-04-14 19:39:56');
/*!40000 ALTER TABLE `workout` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workout_set`
--

DROP TABLE IF EXISTS `workout_set`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workout_set` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exweight_id` int(11) NOT NULL,
  `workout_id` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  `note` varchar(500) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workout_set_53d7194d` (`exweight_id`),
  KEY `workout_set_41a43c3a` (`workout_id`)
) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workout_set`
--

LOCK TABLES `workout_set` WRITE;
/*!40000 ALTER TABLE `workout_set` DISABLE KEYS */;
INSERT INTO `workout_set` VALUES (9,5,2,5,''),(8,5,2,5,''),(10,6,2,5,''),(7,5,2,5,''),(11,7,3,5,''),(12,7,3,5,''),(13,7,3,5,''),(14,8,3,5,''),(15,9,3,5,''),(16,9,3,5,''),(17,9,3,5,''),(18,5,4,5,''),(19,5,4,5,''),(20,5,4,5,''),(21,10,4,5,''),(22,10,4,5,''),(23,10,4,5,''),(24,11,4,5,''),(25,12,5,5,''),(26,12,5,5,''),(27,13,5,5,''),(28,13,5,5,''),(29,13,5,5,''),(30,14,5,5,'');
/*!40000 ALTER TABLE `workout_set` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-04-15  4:39:43
