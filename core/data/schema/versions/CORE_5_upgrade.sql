ALTER TABLE machine ADD memo varchar(255) NULL;
ALTER TABLE machine ADD is_blacklisted tinyint(1) NULL;
ALTER TABLE machine ADD `data` longtext NULL;
