SET FOREIGN_KEY_CHECKS = 0;

ALTER TABLE chuni_score_playlog
    ADD COLUMN regionId INT,
    ADD COLUMN machineType INT;

ALTER TABLE chuni_static_events
    ADD COLUMN startDate TIMESTAMP NOT NULL DEFAULT current_timestamp();

ALTER TABLE chuni_profile_data
    ADD COLUMN rankUpChallengeResults JSON;

ALTER TABLE chuni_static_login_bonus
    DROP FOREIGN KEY chuni_static_login_bonus_ibfk_1;

ALTER TABLE chuni_static_login_bonus_preset
    CHANGE COLUMN id presetId INT NOT NULL;
ALTER TABLE chuni_static_login_bonus_preset
    DROP PRIMARY KEY;
ALTER TABLE chuni_static_login_bonus_preset
    DROP INDEX chuni_static_login_bonus_preset_uk;
ALTER TABLE chuni_static_login_bonus_preset
    ADD CONSTRAINT chuni_static_login_bonus_preset_pk PRIMARY KEY (presetId, version);

ALTER TABLE chuni_static_login_bonus
    ADD CONSTRAINT chuni_static_login_bonus_ibfk_1 FOREIGN KEY (presetId, version)
    REFERENCES chuni_static_login_bonus_preset(presetId, version) ON UPDATE CASCADE ON DELETE CASCADE;

SET FOREIGN_KEY_CHECKS = 1;