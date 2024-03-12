CREATE TABLE `mai2_profile_consec_logins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `version` int(11) NOT NULL,
  `logins` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mai2_profile_consec_logins_uk` (`user`,`version`),
  CONSTRAINT `mai2_profile_consec_logins_ibfk_1` FOREIGN KEY (`user`) REFERENCES `aime_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;