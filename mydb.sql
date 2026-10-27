-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `guest_records`
--

DROP TABLE IF EXISTS `guest_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guest_records` (
  `id` int DEFAULT NULL,
  `guest_name` varchar(50) DEFAULT NULL,
  `qr_code_id` varchar(50) DEFAULT NULL,
  `room_id` int DEFAULT NULL,
  `check_in_time` datetime DEFAULT NULL,
  `check_out_time` datetime DEFAULT NULL,
  `guest_status` enum('Pending','Checked In','Checked Out') DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guest_records`
--

LOCK TABLES `guest_records` WRITE;
/*!40000 ALTER TABLE `guest_records` DISABLE KEYS */;
INSERT INTO `guest_records` VALUES (12345,'Tyrese Haliburton','QR-HOTEL-0002',2,'2026-10-27 19:31:51','2026-10-27 19:37:29','Checked Out'),(123456,'Steph Curry','QR-HOTEL-0003',3,'2026-10-27 16:47:06','2026-10-27 16:45:58','Pending'),(1234567,'Corazon Aswang','QR-HOTEL-0004',4,NULL,NULL,'Pending'),(12345678,'Bob De belder','QR-HOTEL-0005',5,'2026-10-27 17:35:24','2026-10-27 17:35:49','Pending'),(1234,'John Doe','QR-HOTEL-0001',1,'2026-10-27 19:30:00','2026-10-27 20:38:12','Checked Out');
/*!40000 ALTER TABLE `guest_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `history_transactions`
--

DROP TABLE IF EXISTS `history_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `history_transactions` (
  `id` int DEFAULT NULL,
  `guest_name` varchar(100) DEFAULT NULL,
  `qr_code_id` varchar(100) DEFAULT NULL,
  `room_id` int DEFAULT NULL,
  `check_in_time` datetime DEFAULT NULL,
  `check_out_time` datetime DEFAULT NULL,
  `guest_status` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history_transactions`
--

LOCK TABLES `history_transactions` WRITE;
/*!40000 ALTER TABLE `history_transactions` DISABLE KEYS */;
INSERT INTO `history_transactions` VALUES (12345,'Tyrese Haliburton','QR-HOTEL-0002',2,'2026-10-27 19:31:51','2026-10-27 19:37:29','Checked Out'),(1234,'John Doe','QR-HOTEL-0001',1,'2026-10-27 19:30:00','2026-10-27 20:38:12','Checked Out');
/*!40000 ALTER TABLE `history_transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rooms`
--

DROP TABLE IF EXISTS `rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rooms` (
  `room_id` varchar(100) DEFAULT NULL,
  `room_status` enum('Available','Occupied','Reserved','Maintenance') DEFAULT 'Available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rooms`
--

LOCK TABLES `rooms` WRITE;
/*!40000 ALTER TABLE `rooms` DISABLE KEYS */;
INSERT INTO `rooms` VALUES ('1','Available'),('2','Available'),('3','Occupied'),('4','Reserved'),('5','Available'),('6','Maintenance');
/*!40000 ALTER TABLE `rooms` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-27 21:01:51
