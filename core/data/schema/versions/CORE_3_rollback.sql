CREATE TABLE `frontend_session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `ip` varchar(15) DEFAULT NULL,
  `session_cookie` varchar(32) NOT NULL,
  `expires` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `session_cookie` (`session_cookie`),
  KEY `user` (`user`),
  CONSTRAINT `frontend_session_ibfk_1` FOREIGN KEY (`user`) REFERENCES `aime_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;