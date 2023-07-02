UPDATE mai2_static_event SET version = version + 13 WHERE version < 1000;

UPDATE mai2_static_music SET version = version + 13 WHERE version < 1000;

UPDATE mai2_static_ticket SET version = version + 13 WHERE version < 1000;

UPDATE mai2_static_cards SET version = version + 13 WHERE version < 1000;

UPDATE mai2_profile_detail  SET version = version + 13 WHERE version < 1000;

UPDATE mai2_profile_extend  SET version = version + 13 WHERE version < 1000;

UPDATE mai2_profile_option  SET version = version + 13 WHERE version < 1000;

UPDATE mai2_profile_ghost  SET version = version + 13 WHERE version < 1000;

UPDATE mai2_profile_rating  SET version = version + 13 WHERE version < 1000;

ALTER TABLE mai2_item_character ADD point int(11) NULL;

ALTER TABLE mai2_item_card MODIFY COLUMN cardId int(11) NULL;
ALTER TABLE mai2_item_card MODIFY COLUMN cardTypeId int(11) NULL;
ALTER TABLE mai2_item_card MODIFY COLUMN charaId int(11) NULL;
ALTER TABLE mai2_item_card MODIFY COLUMN mapId int(11) NULL;

ALTER TABLE mai2_item_character MODIFY COLUMN characterId int(11) NULL;
ALTER TABLE mai2_item_character MODIFY COLUMN level int(11) NULL;
ALTER TABLE mai2_item_character MODIFY COLUMN awakening int(11) NULL;
ALTER TABLE mai2_item_character MODIFY COLUMN useCount int(11) NULL;

ALTER TABLE mai2_item_charge MODIFY COLUMN chargeId int(11) NULL;
ALTER TABLE mai2_item_charge MODIFY COLUMN stock int(11) NULL;

ALTER TABLE mai2_item_favorite MODIFY COLUMN itemKind int(11) NULL;

ALTER TABLE mai2_item_friend_season_ranking MODIFY COLUMN seasonId int(11) NULL;
ALTER TABLE mai2_item_friend_season_ranking MODIFY COLUMN point int(11) NULL;
ALTER TABLE mai2_item_friend_season_ranking MODIFY COLUMN rank int(11) NULL;
ALTER TABLE mai2_item_friend_season_ranking MODIFY COLUMN rewardGet tinyint(1) NULL;
ALTER TABLE mai2_item_friend_season_ranking MODIFY COLUMN userName varchar(8) NULL;

ALTER TABLE mai2_item_item MODIFY COLUMN itemId int(11) NULL;
ALTER TABLE mai2_item_item MODIFY COLUMN itemKind int(11) NULL;
ALTER TABLE mai2_item_item MODIFY COLUMN stock int(11) NULL;
ALTER TABLE mai2_item_item MODIFY COLUMN isValid tinyint(1) NULL;

ALTER TABLE mai2_item_login_bonus MODIFY COLUMN bonusId int(11) NULL;
ALTER TABLE mai2_item_login_bonus MODIFY COLUMN point int(11) NULL;
ALTER TABLE mai2_item_login_bonus MODIFY COLUMN isCurrent tinyint(1) NULL;
ALTER TABLE mai2_item_login_bonus MODIFY COLUMN isComplete tinyint(1) NULL;

ALTER TABLE mai2_item_map MODIFY COLUMN mapId int(11) NULL;
ALTER TABLE mai2_item_map MODIFY COLUMN distance int(11) NULL;
ALTER TABLE mai2_item_map MODIFY COLUMN isLock tinyint(1) NULL;
ALTER TABLE mai2_item_map MODIFY COLUMN isClear tinyint(1) NULL;
ALTER TABLE mai2_item_map MODIFY COLUMN isComplete tinyint(1) NULL;

ALTER TABLE mai2_item_print_detail MODIFY COLUMN printDate timestamp DEFAULT current_timestamp() NULL;
ALTER TABLE mai2_item_print_detail MODIFY COLUMN serialId varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL;
ALTER TABLE mai2_item_print_detail MODIFY COLUMN placeId int(11) NULL;
ALTER TABLE mai2_item_print_detail MODIFY COLUMN clientId varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL;
ALTER TABLE mai2_item_print_detail MODIFY COLUMN printerSerialId varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL;