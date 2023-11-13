SET FOREIGN_KEY_CHECKS=0;

ALTER TABLE ongeki_user_event_point DROP COLUMN version;
ALTER TABLE ongeki_user_event_point DROP COLUMN rank;
ALTER TABLE ongeki_user_event_point DROP COLUMN type;
ALTER TABLE ongeki_user_event_point DROP COLUMN date;

ALTER TABLE ongeki_user_tech_event DROP COLUMN version;

ALTER TABLE ongeki_user_mission_point DROP COLUMN version;

ALTER TABLE ongeki_static_event DROP COLUMN endDate;

DROP TABLE ongeki_tech_event_ranking;
DROP TABLE ongeki_static_music_ranking_list;
DROP TABLE ongeki_static_rewards;
DROP TABLE ongeki_static_present_list;
DROP TABLE ongeki_static_tech_music;
DROP TABLE ongeki_static_client_testmode;
DROP TABLE ongeki_static_game_point;

SET FOREIGN_KEY_CHECKS=1;
