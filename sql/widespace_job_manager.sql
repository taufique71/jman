DROP DATABASE IF EXISTS `widespace_job_manager`;
CREATE DATABASE `widespace_job_manager`;
USE `widespace_job_manager`;

DROP TABLE IF EXISTS `job_log`;
CREATE TABLE `job_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_key` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `exec_time` int(11) NOT NULL,
  `amount_of_data` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
