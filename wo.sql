-- MySQL dump 10.13  Distrib 5.1.61, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: django_track
-- ------------------------------------------------------
-- Server version	5.1.61-0ubuntu0.11.10.1

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
-- Table structure for table `workout`
--

DROP TABLE IF EXISTS `workout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workout` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workout`
--

LOCK TABLES `workout` WRITE;
/*!40000 ALTER TABLE `workout` DISABLE KEYS */;
INSERT INTO `workout` VALUES (2,'2012-02-20 23:19:24'),(3,'2012-02-18 23:19:58'),(4,'2012-02-22 23:21:38'),(5,'2012-02-25 23:24:25'),(6,'2012-02-27 23:35:13'),(7,'2012-02-29 23:38:40'),(8,'2012-03-02 23:39:08'),(9,'2012-03-04 23:41:21'),(10,'2012-04-02 23:43:06'),(11,'2012-03-10 23:44:55');
/*!40000 ALTER TABLE `workout` ENABLE KEYS */;
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
  KEY `set_2799bae2` (`exercise_id`)
) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exweight`
--

LOCK TABLES `exweight` WRITE;
/*!40000 ALTER TABLE `exweight` DISABLE KEYS */;
INSERT INTO `exweight` VALUES (1,3,209,82),(2,3,199,77),(3,3,179,67),(4,3,225,90),(5,6,77,16),(6,8,50,25),(7,6,65,10),(8,2,-80,-40),(9,2,-50,-25),(10,7,121,38),(11,3,125,40),(12,6,89,22),(13,5,89,22),(14,3,135,45),(15,2,0,0),(16,9,90,45),(17,5,67,11),(18,9,70,35),(19,7,135,45),(20,7,125,40),(28,7,137,46),(22,3,177,66),(23,5,99,27),(27,7,139,47),(25,2,-60,-30),(26,6,95,25),(29,3,185,70),(30,6,109,32);
/*!40000 ALTER TABLE `exweight` ENABLE KEYS */;
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
) ENGINE=MyISAM AUTO_INCREMENT=88 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `set`
--

LOCK TABLES `set` WRITE;
/*!40000 ALTER TABLE `set` DISABLE KEYS */;
INSERT INTO `set` VALUES (1,12,5,5,''),(2,12,5,5,''),(3,12,5,5,''),(4,13,5,5,''),(5,13,5,5,''),(6,13,5,5,''),(7,14,5,5,''),(8,14,5,5,''),(9,9,5,5,''),(10,15,5,3,''),(11,16,5,5,''),(12,16,5,5,''),(13,16,5,5,''),(14,5,2,5,''),(15,5,2,5,''),(16,5,2,5,''),(31,5,3,5,''),(33,6,3,5,''),(32,5,3,5,''),(21,17,2,5,''),(22,17,2,5,''),(23,17,2,5,''),(24,17,2,5,''),(25,8,2,5,''),(26,9,2,5,''),(27,9,2,5,''),(28,9,2,5,''),(30,5,3,5,''),(34,5,4,5,''),(35,5,4,5,''),(36,5,4,5,''),(37,10,4,5,''),(38,10,4,5,''),(39,10,4,5,''),(40,11,4,5,''),(41,11,4,5,''),(42,11,4,5,''),(43,5,6,5,''),(44,5,6,5,''),(45,5,6,5,''),(46,19,6,5,''),(47,20,6,5,''),(48,20,6,5,''),(49,22,6,5,''),(50,22,6,5,''),(51,12,7,5,''),(52,12,7,5,''),(53,12,7,5,''),(54,23,7,5,''),(72,15,9,8,''),(56,9,7,8,''),(57,15,7,4,''),(58,25,7,5,''),(59,26,8,5,''),(60,26,8,5,''),(61,26,8,5,''),(62,19,8,5,''),(63,19,8,5,''),(64,19,8,5,''),(65,3,8,5,''),(66,26,9,5,''),(67,26,9,5,''),(68,26,9,5,''),(69,23,9,5,''),(70,23,9,5,''),(71,23,9,5,''),(73,15,9,4,''),(74,3,9,5,''),(75,26,10,5,''),(76,26,10,5,''),(77,26,10,5,''),(78,27,10,5,''),(79,28,10,5,''),(80,28,10,5,''),(81,29,10,5,''),(82,30,11,5,'heavy!'),(83,30,11,5,''),(84,30,11,5,''),(85,23,11,5,''),(86,23,11,5,''),(87,23,11,5,'');
/*!40000 ALTER TABLE `set` ENABLE KEYS */;
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
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exercise`
--

LOCK TABLES `exercise` WRITE;
/*!40000 ALTER TABLE `exercise` DISABLE KEYS */;
INSERT INTO `exercise` VALUES (3,'Deadlift',1,''),(2,'Pullup',0,''),(4,'Clean',1,''),(5,'Press',1,''),(6,'Squat',1,''),(7,'Bench Press',1,''),(8,'dumbell row',0,''),(9,'row machine',0,'');
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
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exercise_pmuscles`
--

LOCK TABLES `exercise_pmuscles` WRITE;
/*!40000 ALTER TABLE `exercise_pmuscles` DISABLE KEYS */;
INSERT INTO `exercise_pmuscles` VALUES (3,3,16),(2,2,1),(4,5,27),(5,6,19),(6,7,35);
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-04-03  8:16:40
