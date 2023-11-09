SET FOREIGN_KEY_CHECKS=0;

ALTER TABLE ongeki_user_event_point ADD COLUMN version INTEGER NOT NULL;
ALTER TABLE ongeki_user_event_point ADD COLUMN rank INTEGER;
ALTER TABLE ongeki_user_event_point ADD COLUMN type INTEGER NOT NULL;
ALTER TABLE ongeki_user_event_point ADD COLUMN date VARCHAR(25);

ALTER TABLE ongeki_user_tech_event ADD COLUMN version INTEGER NOT NULL;

ALTER TABLE ongeki_user_mission_point ADD COLUMN version INTEGER NOT NULL;

ALTER TABLE ongeki_static_events ADD COLUMN endDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE ongeki_tech_event_ranking (
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	user INT NOT NULL,
	version INT NOT NULL,
	date VARCHAR(25),
	eventId INT NOT NULL,
	rank INT,
	totalPlatinumScore INT NOT NULL,
	totalTechScore INT NOT NULL,
	UNIQUE KEY ongeki_tech_event_ranking_uk (user, eventId),
	CONSTRAINT ongeki_tech_event_ranking_ibfk1 FOREIGN KEY (user) REFERENCES aime_user(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE ongeki_static_music_ranking_list (
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	version INT NOT NULL,
	musicId INT NOT NULL,
	point INT NOT NULL,
	userName VARCHAR(255),
	UNIQUE KEY ongeki_static_music_ranking_list_uk (version, musicId)
);

CREATE TABLE ongeki_static_rewards (
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	version INT NOT NULL,
	rewardId INT NOT NULL,
	rewardName VARCHAR(255) NOT NULL,
	itemKind INT NOT NULL,
	itemId INT NOT NULL,
	UNIQUE KEY ongeki_tech_event_ranking_uk (version, rewardId)
);

CREATE TABLE ongeki_static_present_list (
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	version INT NOT NULL,
	presentId INT NOT NULL,
	presentName VARCHAR(255) NOT NULL,
	rewardId INT NOT NULL,
	stock INT NOT NULL,
	message VARCHAR(255),
	startDate VARCHAR(25) NOT NULL,
	endDate VARCHAR(25) NOT NULL,
	UNIQUE KEY ongeki_static_present_list_uk (version, presentId, rewardId)
);

CREATE TABLE ongeki_static_tech_music (
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	version INT NOT NULL,
	eventId INT NOT NULL,
	musicId INT NOT NULL,
	level INT NOT NULL,
	UNIQUE KEY ongeki_static_tech_music_uk (version, musicId, eventId)
);

CREATE TABLE ongeki_static_client_testmode (
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	regionId INT NOT NULL,
	placeId INT NOT NULL,
	clientId VARCHAR(11) NOT NULL,
	updateDate TIMESTAMP NOT NULL,
	isDelivery BOOLEAN NOT NULL,
	groupId INT NOT NULL,
	groupRole INT NOT NULL,
	continueMode INT NOT NULL,
	selectMusicTime INT NOT NULL,
	advertiseVolume INT NOT NULL,
	eventMode INT NOT NULL,
	eventMusicNum INT NOT NULL,
	patternGp INT NOT NULL,
	limitGp INT NOT NULL,
	maxLeverMovable INT NOT NULL,
	minLeverMovable INT NOT NULL,
	UNIQUE KEY ongeki_static_client_testmode_uk (clientId)
);
SET FOREIGN_KEY_CHECKS=1;
