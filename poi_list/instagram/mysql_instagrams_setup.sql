CREATE TABLE `sentimentDB`.`instagrams` (
  `entry_id` INT(11) NOT NULL AUTO_INCREMENT,
  `number_id` TINYTEXT NULL,
  `user_id` TINYTEXT NULL,
  `keyword` VARCHAR(1000) NULL,
  `posted_time` DATETIME NULL,
  `caption` VARCHAR(15000) NULL,
  PRIMARY KEY (`entry_id`));
