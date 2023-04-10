ALTER TABLE mai2_profile_option
ADD COLUMN tapSe INT NOT NULL DEFAULT 0 AFTER tapDesign;

ALTER TABLE mai2_score_best
ADD COLUMN extNum1 INT NOT NULL DEFAULT 0;

ALTER TABLE mai2_profile_extend
ADD COLUMN playStatusSetting INT NOT NULL DEFAULT 0;

ALTER TABLE mai2_playlog
ADD COLUMN extNum4 INT NOT NULL DEFAULT 0;

ALTER TABLE mai2_static_event
ADD COLUMN startDate TIMESTAMP NOT NULL DEFAULT current_timestamp();

ALTER TABLE mai2_item_map
CHANGE COLUMN map_id mapId INT NOT NULL,
CHANGE COLUMN is_lock isLock BOOLEAN NOT NULL DEFAULT 0,
CHANGE COLUMN is_clear isClear BOOLEAN NOT NULL DEFAULT 0,
CHANGE COLUMN is_complete isComplete BOOLEAN NOT NULL DEFAULT 0;

ALTER TABLE mai2_item_friend_season_ranking
CHANGE COLUMN season_id seasonId INT NOT NULL,
CHANGE COLUMN reward_get rewardGet BOOLEAN NOT NULL,
CHANGE COLUMN user_name userName VARCHAR(8) NOT NULL,
CHANGE COLUMN record_date recordDate TIMESTAMP NOT NULL;

ALTER TABLE mai2_item_login_bonus
CHANGE COLUMN bonus_id bonusId INT NOT NULL,
CHANGE COLUMN is_current isCurrent Boolean NOT NULL DEFAULT 0,
CHANGE COLUMN is_complete isComplete Boolean NOT NULL DEFAULT 0;
