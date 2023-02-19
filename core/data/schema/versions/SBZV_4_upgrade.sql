ALTER TABLE diva_profile ADD COLUMN passwd_stat INTEGER NOT NULL DEFAULT 0;
ALTER TABLE diva_profile ADD COLUMN passwd VARCHAR(12) NOT NULL DEFAULT "**********";
ALTER TABLE diva_profile MODIFY player_name VARCHAR(10);
