ALTER TABLE diva_profile DROP COLUMN passwd_stat;
ALTER TABLE diva_profile DROP COLUMN passwd;
ALTER TABLE diva_profile MODIFY player_name VARCHAR(8);
