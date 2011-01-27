-- MySQL dump 10.13  Distrib 5.1.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: xrquiz
-- ------------------------------------------------------
-- Server version	5.1.41-3ubuntu12.6

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
-- Table structure for table `answers`
--

DROP TABLE IF EXISTS `answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `answers` (
  `id` mediumint(4) unsigned NOT NULL AUTO_INCREMENT,
  `question_id` mediumint(4) unsigned NOT NULL DEFAULT '0',
  `text` varchar(4096) NOT NULL DEFAULT '',
  `author_id` mediumint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answers`
--

LOCK TABLES `answers` WRITE;
/*!40000 ALTER TABLE `answers` DISABLE KEYS */;
INSERT INTO `answers` VALUES (1,1,'Mark Zuckerberg',1),(2,2,'Blogger',1),(3,3,'50 million',1),(4,4,'Retweet',1),(5,5,'The restrictive size of text messages.',1),(6,6,'Group text messaging.',1),(7,7,'You and your friends',1),(8,8,'.edu',1),(9,9,'Google',1),(10,10,'5000',1),(11,11,'False',1),(12,12,'Newsweek',1),(13,13,'New York City',1),(14,14,'Like it',1),(15,15,'Theme',1),(16,16,'Matt Mullenweg',1),(17,17,'Plugin',1),(18,18,'Content Management System',1),(19,19,'Open Source',1),(20,20,'PHP',1);
/*!40000 ALTER TABLE `answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categories` (
  `id` mediumint(4) unsigned NOT NULL AUTO_INCREMENT,
  `text` varchar(256) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `distractors`
--

DROP TABLE IF EXISTS `distractors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `distractors` (
  `id` mediumint(4) unsigned NOT NULL AUTO_INCREMENT,
  `question_id` mediumint(4) unsigned NOT NULL DEFAULT '0',
  `text` varchar(4096) NOT NULL DEFAULT '',
  `author_id` mediumint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distractors`
--

LOCK TABLES `distractors` WRITE;
/*!40000 ALTER TABLE `distractors` DISABLE KEYS */;
INSERT INTO `distractors` VALUES (1,1,'Steve Jobs',1),(2,2,'Wordpress',1),(3,3,'5 million',1),(4,4,'Right Thinking',1),(5,5,'It is arbitrary.',1),(6,6,'It was developed for the military to monitor troops.',1),(7,7,'You',1),(8,8,'.com',1),(9,9,'Twitter',1),(10,10,'1000',1),(11,11,'True',1),(12,12,'Entertainment Weekly',1),(13,13,'Austin',1),(14,14,'Love it',1),(15,15,'Stylings',1),(16,16,'Om Malik',1),(17,17,'Adapter',1),(18,18,'Customer Relationship Manager',1),(19,19,'Complicated',1),(20,20,'Java',1),(21,1,'Sergey Brin',1),(22,2,'Flickr',1),(23,3,'800,000',1),(24,4,'Rethread',1),(25,5,'It was a coding error that turned into a feature.',1),(26,6,'Celebrity microblogging.',1),(27,7,'Your friends',1),(28,8,'.org',1),(29,9,'Tumblr',1),(30,10,'10,000',1),(31,12,'Time',1),(32,13,'Boston',1),(33,14,'Hug it',1),(34,15,'Template',1),(35,16,'Biz Stone',1),(36,17,'Tool',1),(37,18,'Content Production Developer',1),(38,19,'DOS',1),(39,20,'Python',1),(40,1,'Bill Gates',1),(41,2,'Google',1),(42,3,'75 million',1),(43,4,'Retalk',1),(44,5,'To limit the cost the cost of bandwidth.',1),(45,6,'It was developed for the NYSE.',1),(46,7,'Facebook',1),(47,8,'.biz',1),(48,9,'Myspace',1),(49,10,'Unlimited',1),(50,12,'Playboy',1),(51,13,'San Francisco',1),(52,14,'Kiss it',1),(53,15,'Format',1),(54,16,'Dennis Crowley',1),(55,17,'Widget',1),(56,18,'Coded Content Silo',1),(57,19,'Linux',1),(58,20,'Ruby',1);
/*!40000 ALTER TABLE `distractors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `questions` (
  `id` mediumint(4) unsigned NOT NULL AUTO_INCREMENT,
  `quiz_id` mediumint(4) unsigned NOT NULL DEFAULT '0',
  `author_id` mediumint(4) unsigned NOT NULL DEFAULT '0',
  `text` varchar(4096) NOT NULL DEFAULT '',
  `ranking` mediumint(4) unsigned NOT NULL DEFAULT '0',
  `rd` mediumint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `quiz_id` (`quiz_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (1,2,1,'Who is the CEO of Facebook?',1500,350),(2,1,1,'Which company did the founders of Twitter found before Twitter?',1500,350),(3,1,1,'How many daily tweets are there?',1500,350),(4,1,1,'What does RT stand for?',1500,350),(5,1,1,'What is the reason for the 140 character limit?',1500,350),(6,1,1,'What was Twitter originally created for?',1500,350),(7,2,1,'Who is responsible for your privacy on Facebook?',1500,350),(8,2,1,'Before being opened to the public, Facebook was only available to people with this type of email address.',1500,350),(9,2,1,'Facebook considers who to be their main competitor?',1500,350),(10,2,1,'From a personal Facebook account, what is the maximum number of people you may friend?',1500,350),(11,9,1,'There is a limit to the number of Tumblr blogs you can administrate.',1500,350),(12,9,1,'Which magazine received recognition for having the best Tumblr blog?',1500,350),(13,9,1,'What city is home to the largest Tumblr community?',1500,350),(14,9,1,'To show appreciation for a post, what can you do to it?',1500,350),(15,9,1,'When you want to change the way your Tumblr blog looks, you change your. . .',1500,350),(16,10,1,'Who founded Wordpress?',1500,350),(17,10,1,'Users can easily add functionality to their Wordpress blog by adding a. . .',1500,350),(18,10,1,'Wordpress is a . . .',1500,350),(19,10,1,'Wordpress is an example of what type of software?',1500,350),(20,10,1,'Wordpress is written in. . .',1500,350);
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quizzes`
--

DROP TABLE IF EXISTS `quizzes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quizzes` (
  `id` mediumint(4) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL DEFAULT '',
  `author_id` mediumint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quizzes`
--

LOCK TABLES `quizzes` WRITE;
/*!40000 ALTER TABLE `quizzes` DISABLE KEYS */;
INSERT INTO `quizzes` VALUES (1,'Twitter',1),(2,'Facebook',1),(3,'Flickr',1),(4,'FourSquare',1),(5,'iTunes',1),(6,'Linked In',1),(7,'Shareaholic',1),(8,'YouTube',1),(9,'Tumblr',1),(10,'Wordpress',1),(11,'Reddit',1);
/*!40000 ALTER TABLE `quizzes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sessions` (
  `id` mediumint(4) unsigned NOT NULL AUTO_INCREMENT,
  `session_id` char(128) NOT NULL DEFAULT '',
  `cache` varchar(8192) NOT NULL DEFAULT '',
  `user_id` mediumint(4) unsigned NOT NULL DEFAULT '0',
  `date_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `session_id` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tags` (
  `id` mediumint(4) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` mediumint(4) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(40) NOT NULL DEFAULT '',
  `password` varchar(28) NOT NULL DEFAULT '',
  `status` varchar(4) NOT NULL DEFAULT 'OK',
  `ranking` mediumint(4) unsigned NOT NULL DEFAULT '0',
  `rd` mediumint(4) unsigned NOT NULL DEFAULT '0',
  -- `date_created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `date_created` timestamp NULL DEFAULT NULL,
  `date_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TRIGGER new_users BEFORE INSERT ON `users` FOR EACH ROW SET
NEW.date_created = IFNULL(NEW.date_created, NOW());

-- NEW.updated = IFNULL(NEW.updated, '0000-00-00 00:00:00');


--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`,`email`,`status`) VALUES (1, 'support@xpertrank.com', 'SYS');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `versions`
--

DROP TABLE IF EXISTS `versions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `versions` (
  `id` mediumint(4) unsigned NOT NULL AUTO_INCREMENT,
  `subversion` mediumint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


CREATE TABLE `quizzes_categories` (
  `quiz_id` mediumint(4) unsigned NOT NULL DEFAULT '0',
  `category_id` mediumint(4) unsigned NOT NULL DEFAULT '0',
  KEY `quiz_id` (`quiz_id`),
  KEY `category_id` (`category_id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `versions`
--

LOCK TABLES `versions` WRITE;
/*!40000 ALTER TABLE `versions` DISABLE KEYS */;
/*!40000 ALTER TABLE `versions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-10-21 11:38:04
