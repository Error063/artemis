SET FOREIGN_KEY_CHECKS = 0;

ALTER TABLE chuni_score_playlog
    DROP COLUMN regionId,
    DROP COLUMN machineType;

ALTER TABLE chuni_static_events
    DROP COLUMN startDate;

ALTER TABLE chuni_profile_data
    DROP COLUMN rankUpChallengeResults;

ALTER TABLE chuni_static_login_bonus
    DROP FOREIGN KEY chuni_static_login_bonus_ibfk_1;

ALTER TABLE chuni_static_login_bonus_preset
    DROP PRIMARY KEY;

ALTER TABLE chuni_static_login_bonus_preset
    CHANGE COLUMN presetId id INT NOT NULL;
ALTER TABLE chuni_static_login_bonus_preset
    ADD PRIMARY KEY(id);
ALTER TABLE chuni_static_login_bonus_preset
    ADD CONSTRAINT chuni_static_login_bonus_preset_uk UNIQUE(id, version);

ALTER TABLE chuni_static_login_bonus
    ADD CONSTRAINT chuni_static_login_bonus_ibfk_1 FOREIGN KEY(presetId)
    REFERENCES chuni_static_login_bonus_preset(id) ON UPDATE CASCADE ON DELETE CASCADE;

SET FOREIGN_KEY_CHECKS = 1;