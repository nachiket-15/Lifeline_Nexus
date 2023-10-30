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



DROP DATABASE IF EXISTS `PLASMABANK`;
CREATE SCHEMA `PLASMABANK`;
USE `PLASMABANK`;






-- Create a table for user accounts
DROP TABLE IF EXISTS `USER_ACCOUNTS`;
CREATE TABLE `USER_ACCOUNTS` (
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Insert some example user accounts
INSERT INTO `USER_ACCOUNTS` VALUES ('admin', 'admin');







-- Tables without foreign key references
DROP TABLE IF EXISTS `DONORS`;
CREATE TABLE `DONORS` (
  `donor_id` int(11) NOT NULL AUTO_INCREMENT,
  `date_of_donation` date NOT NULL,
  PRIMARY KEY (`donor_id`,`date_of_donation`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;






DROP TABLE IF EXISTS `BLOOD`;
CREATE TABLE `BLOOD` (
  `plasma_bag_number` int(11) NOT NULL,
  `blood_type` varchar(10) DEFAULT NULL,
  `blood_amount` varchar(10) DEFAULT NULL,
  `platelets_count` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`plasma_bag_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Insert data into the BLOOD table
INSERT INTO `BLOOD` VALUES (1,'A+','23',2.20);





DROP TABLE IF EXISTS `BLOOD_COST`;
CREATE TABLE `BLOOD_COST` (
  `plasma_bag_number` int(11) NOT NULL,
  `cost` int(11) DEFAULT NULL,
  PRIMARY KEY (`plasma_bag_number`),
  CONSTRAINT `BLOOD_COST_ibfk_1` FOREIGN KEY (`plasma_bag_number`) REFERENCES `BLOOD` (`plasma_bag_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Insert data into the BLOOD_COST table
INSERT INTO `BLOOD_COST` VALUES (1,50);









-- Tables with foreign key references
DROP TABLE IF EXISTS `RECIPIENT`;
CREATE TABLE `RECIPIENT` (
  `rec_id` int(11) NOT NULL,
  `blood_type` varchar(10) DEFAULT NULL,
  `quantity_needed` int(11) DEFAULT NULL,
  `date_of_request` date DEFAULT NULL,
  `fname` varchar(10) DEFAULT NULL,
  `lname` varchar(10) DEFAULT NULL,
  `dOB` date DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `address` char(30) DEFAULT NULL,
  PRIMARY KEY (`rec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;






-- Insert data into the RECIPIENT table
INSERT INTO `RECIPIENT` VALUES (1,'A+',23,'1999-10-10','Veeral','Agarwal','1998-10-10','M',23,'C102, Raj Vihar, Mumbai');



DROP TABLE IF EXISTS `REGISTERS`;
CREATE TABLE `REGISTERS` (
  `donor_id` int(11) DEFAULT NULL,
  `rec_id` int(11) DEFAULT NULL,
  KEY `rec_id` (`rec_id`),
  KEY `donor_id` (`donor_id`),
  CONSTRAINT `REGISTERS_ibfk_1` FOREIGN KEY (`rec_id`) REFERENCES `RECIPIENT` (`rec_id`),
  CONSTRAINT `REGISTERS_ibfk_2` FOREIGN KEY (`donor_id`) REFERENCES `DONORS` (`donor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;






-- Tables with foreign key references
DROP TABLE IF EXISTS `STAFF`;
CREATE TABLE `STAFF` (
  `emp_id` int(11) NOT NULL,
  `fname` varchar(10) DEFAULT NULL,
  `supervisor` varchar(20) DEFAULT NULL,
  `address1` varchar(10) DEFAULT NULL,
  `phone_no` int(11) DEFAULT NULL,
  `salary` int(11) DEFAULT NULL,
  PRIMARY KEY (`emp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Insert data into the STAFF table
INSERT INTO `STAFF` VALUES (1,'Def Gef','Sandy','23 A','1234567890',23411);






DROP TABLE IF EXISTS `COMPANION`;
CREATE TABLE `COMPANION` (
  `donor_id` int(11) DEFAULT NULL,
  `companion_name` varchar(10) DEFAULT NULL,
  `relationship` varchar(10) DEFAULT NULL,
  KEY `donor_id` (`donor_id`),
  CONSTRAINT `COMPANION_ibfk_1` FOREIGN KEY (`donor_id`) REFERENCES `DONORS` (`donor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- No need to lock/unlock tables for this operation







DROP TABLE IF EXISTS `DONOR_INFO`;
CREATE TABLE `DONOR_INFO` (
  `donor_id` int(11) NOT NULL,
  `fname` varchar(30) NOT NULL,
  `lName` varchar(30) DEFAULT NULL,
  `blood_type` varchar(30) DEFAULT NULL,
  `phone_no` varchar(11) DEFAULT NULL,
  `dOB` date DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  `address` char(30) DEFAULT NULL,
  PRIMARY KEY (`donor_id`),
  CONSTRAINT `DONOR_INFO_ibfk_1` FOREIGN KEY (`donor_id`) REFERENCES `DONORS` (`donor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- No need to lock/unlock tables for this operation












DROP TABLE IF EXISTS `PAYMENT_TRANSACTION`;
CREATE TABLE `PAYMENT_TRANSACTION` (
  `rec_id` int(11) DEFAULT NULL,
  `payment_amt` int(11) DEFAULT NULL,
  KEY `rec_id` (`rec_id`),
  CONSTRAINT `PAYMENT_TRANSACTION_ibfk_1` FOREIGN KEY (`rec_id`) REFERENCES `RECIPIENT` (`rec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- No need to lock/unlock tables for this operation










DROP TABLE IF EXISTS `RECIEVES`;
CREATE TABLE `RECIEVES` (
  `emp_id` int(11) DEFAULT NULL,
  `rec_id` int(11) DEFAULT NULL,
  KEY `rec_id` (`rec_id`),
  KEY `emp_id` (`emp_id`),
  CONSTRAINT `RECIEVES_ibfk_1` FOREIGN KEY (`rec_id`) REFERENCES `RECIPIENT` (`rec_id`),
  CONSTRAINT `RECIEVES_ibfk_2` FOREIGN KEY (`emp_id`) REFERENCES `STAFF` (`emp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- No need to lock/unlock tables for this operation



















/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


