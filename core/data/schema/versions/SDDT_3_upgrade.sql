SET FOREIGN_KEY_CHECKS=0;

ALTER TABLE ongeki_profile_data ADD COLUMN isDialogWatchedSuggestMemory BOOLEAN;
ALTER TABLE ongeki_score_best ADD COLUMN platinumScoreMax INTEGER;
ALTER TABLE ongeki_score_playlog ADD COLUMN platinumScore INTEGER;
ALTER TABLE ongeki_score_playlog ADD COLUMN platinumScoreMax INTEGER;

CREATE TABLE ongeki_user_memorychapter (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user INT NOT NULL,
    chapterId INT NOT NULL,
    gaugeId INT NOT NULL,
    gaugeNum INT NOT NULL,
    jewelCount INT NOT NULL,
    isStoryWatched BOOLEAN NOT NULL,
    isBossWatched BOOLEAN NOT NULL,
    isDialogWatched BOOLEAN NOT NULL,
    isEndingWatched BOOLEAN NOT NULL,
    isClear BOOLEAN NOT NULL,
    lastPlayMusicId INT NOT NULL,
    lastPlayMusicLevel INT NOT NULL,
    lastPlayMusicCategory INT NOT NULL,
    UNIQUE KEY ongeki_user_memorychapter_uk (user, chapterId),
    CONSTRAINT ongeki_user_memorychapter_ibfk_1 FOREIGN KEY (user) REFERENCES aime_user (id) ON DELETE CASCADE ON UPDATE CASCADE
);

SET FOREIGN_KEY_CHECKS=1;
