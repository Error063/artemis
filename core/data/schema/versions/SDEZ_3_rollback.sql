ALTER TABLE mai2_profile_option
DROP COLUMN tapSe;

ALTER TABLE mai2_score_best
DROP COLUMN extNum1;

ALTER TABLE mai2_profile_extend
DROP COLUMN playStatusSetting;

ALTER TABLE mai2_playlog
DROP COLUMN extNum4;

ALTER TABLE mai2_static_event
DROP COLUMN startDate;

ALTER TABLE mai2_item_map
CHANGE COLUMN mapId map_id INT NOT NULL,
CHANGE COLUMN isLock is_lock BOOLEAN NOT NULL DEFAULT 0,
CHANGE COLUMN isClear is_clear BOOLEAN NOT NULL DEFAULT 0,
CHANGE COLUMN isComplete is_complete BOOLEAN NOT NULL DEFAULT 0;

ALTER TABLE mai2_item_friend_season_ranking
CHANGE COLUMN seasonId season_d INT NOT NULL,
CHANGE COLUMN rewardGet reward_get BOOLEAN NOT NULL,
CHANGE COLUMN userName user_name VARCHAR(8) NOT NULL,
CHANGE COLUMN recordDate record_date VARCHAR(255) NOT NULL;

ALTER TABLE mai2_item_login_bonus
CHANGE COLUMN bonusId bonus_id INT NOT NULL,
CHANGE COLUMN isCurrent is_currentBoolean NOT NULL DEFAULT 0,
CHANGE COLUMN isComplete is_complete Boolean NOT NULL DEFAULT 0;