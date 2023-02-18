SET FOREIGN_KEY_CHECKS=0;
ALTER TABLE diva_score ADD COLUMN edition int(11) DEFAULT 0 AFTER difficulty;
ALTER TABLE diva_playlog ADD COLUMN edition int(11) DEFAULT 0 AFTER difficulty;

ALTER TABLE diva_score DROP FOREIGN KEY diva_score_ibfk_1;
ALTER TABLE diva_score DROP CONSTRAINT diva_score_uk;
ALTER TABLE diva_score ADD CONSTRAINT diva_score_uk UNIQUE (user, pv_id, difficulty, edition);
ALTER TABLE diva_score ADD CONSTRAINT diva_score_ibfk_1 FOREIGN KEY (user) REFERENCES aime_user(id) ON DELETE CASCADE;
SET FOREIGN_KEY_CHECKS=1;