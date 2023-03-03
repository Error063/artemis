SET FOREIGN_KEY_CHECKS=0;
ALTER TABLE ongeki_profile_data DROP COLUMN isDialogWatchedSuggestMemory;
ALTER TABLE ongeki_score_best DROP COLUMN platinumScoreMax;
ALTER TABLE ongeki_score_playlog DROP COLUMN platinumScore;
ALTER TABLE ongeki_score_playlog DROP COLUMN platinumScoreMax;
DROP TABLE IF EXISTS `ongeki_user_memorychapter`;
SET FOREIGN_KEY_CHECKS=1;
