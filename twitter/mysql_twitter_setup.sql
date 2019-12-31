 CREATE TABLE `sentimentDB`.`tweets` (
  `entry_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(20) NULL,
  `user_name` VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `keyword` VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `latitude` DOUBLE NULL,
  `longitude` DOUBLE NULL,
  `keyword_or_latlong` VARCHAR(7) NULL,
  `tweet` VARCHAR(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `post_time` DATETIME NULL,
  `crawled_time` DATETIME NULL,
  PRIMARY KEY (`entry_id`));
  
CREATE TABLE `sentimentDB`.`twitter_users` (
  `user_index` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_name` VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `raw_home_location` VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `image_url` VARCHAR(1000) NULL,
  `crawled_time` DATETIME NULL,
  `cleaned_home_location` VARCHAR(1000) NULL,
  PRIMARY KEY (`user_index`, `user_id`));