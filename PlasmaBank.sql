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


INSERT INTO `USER_ACCOUNTS` VALUES ('ved', 'ved');
INSERT INTO `USER_ACCOUNTS` VALUES ('nachi', 'nachi');
INSERT INTO `USER_ACCOUNTS` VALUES ('paras', 'paras');

DROP TABLE IF EXISTS `ADMIN_ACCOUNTS`;
CREATE TABLE `ADMIN_ACCOUNTS` (
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Insert some example user accounts
INSERT INTO `ADMIN_ACCOUNTS` VALUES ('admin', 'admin');







-- Tables without foreign key references
DROP TABLE IF EXISTS `DONORS`;
CREATE TABLE `DONORS` (
  `donor_id` int(11) NOT NULL AUTO_INCREMENT,
  `donor_name` varchar(255) NOT NULL,
  `blood_type` varchar(10) NOT NULL,
  `date_of_donation` date NOT NULL,
  PRIMARY KEY (`donor_id`,`date_of_donation`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



INSERT INTO `DONORS` (`donor_name`, `blood_type`, `date_of_donation`) 
VALUES ('John Doe', 'A+', '2023-11-01');

INSERT INTO `DONORS` (`donor_name`, `blood_type`, `date_of_donation`) 
VALUES ('Jane Smith', 'B-', '2023-11-02');

INSERT INTO `DONORS` (`donor_name`, `blood_type`, `date_of_donation`) 
VALUES ('Robert Johnson', 'O+', '2023-11-03');

INSERT INTO `DONORS` (`donor_name`, `blood_type`, `date_of_donation`) 
VALUES ('Alice Williams', 'AB+', '2023-11-04');

INSERT INTO `DONORS` (`donor_name`, `blood_type`, `date_of_donation`) 
VALUES ('David Miller', 'A-', '2023-11-05');

INSERT INTO `DONORS` (`donor_name`, `blood_type`, `date_of_donation`) 
VALUES ('Sophia Davis', 'B+', '2023-11-06');

INSERT INTO `DONORS` (`donor_name`, `blood_type`, `date_of_donation`) 
VALUES ('Michael Brown', 'O-', '2023-11-07');

INSERT INTO `DONORS` (`donor_name`, `blood_type`, `date_of_donation`) 
VALUES ('Emma Wilson', 'AB-', '2023-11-08');

INSERT INTO `DONORS` (`donor_name`, `blood_type`, `date_of_donation`) 
VALUES ('William Jones', 'A+', '2023-11-09');

INSERT INTO `DONORS` (`donor_name`, `blood_type`, `date_of_donation`) 
VALUES ('Olivia White', 'B+', '2023-11-10');




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
INSERT INTO `BLOOD` VALUES (2,'B+','40',5.0);
INSERT INTO `BLOOD` VALUES (3,'O+','65',3.0);
INSERT INTO `BLOOD` VALUES (4,'AB+','13',2.5);
INSERT INTO `BLOOD` VALUES (5,'A-','27',7.0);
INSERT INTO `BLOOD` VALUES (6,'B-','39',4.5);
INSERT INTO `BLOOD` VALUES (7,'AB-','7',2.5);
INSERT INTO `BLOOD` VALUES (8,'O-','15',3.0);


DROP TABLE IF EXISTS `BLOOD_COST`;
CREATE TABLE `BLOOD_COST` (
  `plasma_bag_number` int(11) NOT NULL,
  `cost` int(11) DEFAULT NULL,
  PRIMARY KEY (`plasma_bag_number`),
  CONSTRAINT `BLOOD_COST_ibfk_1` FOREIGN KEY (`plasma_bag_number`) REFERENCES `BLOOD` (`plasma_bag_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Insert data into the BLOOD_COST table
INSERT INTO `BLOOD_COST` VALUES (1,5000);









-- Tables with foreign key references
DROP TABLE IF EXISTS `RECIPIENT`;
CREATE TABLE `RECIPIENT` (
  `rec_id` int(11) NOT NULL,
  `blood_type` varchar(10) DEFAULT NULL,
  `quantity_needed` int(11) DEFAULT NULL,
  `date_of_request` date DEFAULT NULL,
  `recipient_name` varchar(30) DEFAULT NULL,
  `dOB` date DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  `address` char(30) DEFAULT NULL,
  PRIMARY KEY (`rec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Insert data into the RECIPIENT table
INSERT INTO `RECIPIENT` VALUES (1, 'A+', 23, '2023-10-10', 'Veeral Agarwal', '1998-10-10', 'M', 23, 'C102, Raj Vihar, Mumbai');
INSERT INTO `RECIPIENT` VALUES (2, 'B-', 30, '2023-05-15', 'Sara Johnson', '1991-08-25', 'F', 30, 'D45, Park Avenue, New York');
INSERT INTO `RECIPIENT` VALUES (3, 'O+', 28, '2023-12-03', 'Alexandra Smith', '1993-07-12', 'F', 28, 'A22, Green Street, London');
INSERT INTO `RECIPIENT` VALUES (4, 'AB-', 35, '2023-03-21', 'Michael Brown', '1986-09-18', 'M', 35, 'B12, Sunshine Apartments, Sydney');
INSERT INTO `RECIPIENT` VALUES (5, 'B+', 25, '2023-08-02', 'Emily Wilson', '1997-04-05', 'F', 25, 'E78, Orchard Lane, Toronto');
INSERT INTO `RECIPIENT` VALUES (6, 'A-', 27, '2023-11-14', 'Daniel Kim', '1995-02-28', 'M', 27, 'F56, Cherry Hills, Seoul');
INSERT INTO `RECIPIENT` VALUES (7, 'O-', 22, '2023-06-08', 'Sophie Davis', '2000-01-15', 'F', 22, 'G89, Maple Grove, Berlin');
INSERT INTO `RECIPIENT` VALUES (8, 'AB+', 32, '2023-09-30', 'Christopher Lee', '1988-12-12', 'M', 32, 'H33, Redwood Lane, Paris');
INSERT INTO `RECIPIENT` VALUES (9, 'A+', 29, '2023-04-18', 'Amanda White', '1992-11-23', 'F', 29, 'I67, Ocean View, Barcelona');
INSERT INTO `RECIPIENT` VALUES (10, 'B-', 26, '2023-01-05', 'Joshua Miller', '1996-06-19', 'M', 26, 'J44, Riverside Drive, Tokyo');











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
  `address1` varchar(50) DEFAULT NULL,
  `phone_no` varchar(15) DEFAULT NULL,
  `salary` int(11) DEFAULT NULL,
  PRIMARY KEY (`emp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Insert data into the STAFF table
INSERT INTO `STAFF` VALUES (1,'Def Gef','Sandy','23 A','9090909090',23411);

-- 





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








CREATE TABLE REQUESTS (
  request_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(30),  -- Match the length with the primary key in USER_ACCOUNTS
  blood_type VARCHAR(10),
  quantity_needed INT,
  date_of_request DATE,
  status VARCHAR(10) DEFAULT 'Pending',
  admin_comment VARCHAR(255) DEFAULT 'ToBeGiven',
  FOREIGN KEY (username) REFERENCES USER_ACCOUNTS(username)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `REQUESTS` (username, blood_type, quantity_needed, date_of_request) VALUES ("ved", 'O+', 5, '2023-11-03');

select * from REQUESTS where username='ved';










/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


