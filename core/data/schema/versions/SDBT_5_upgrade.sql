SET FOREIGN_KEY_CHECKS = 0;

ALTER TABLE chuni_score_playlog
  CHANGE COLUMN isClear isClear TINYINT(6) NULL DEFAULT NULL;

ALTER TABLE chuni_score_best
  CHANGE COLUMN isSuccess isSuccess INT(11) NULL DEFAULT NULL ;

ALTER TABLE chuni_score_playlog
  ADD COLUMN ticketId INT(11) NULL AFTER machineType;

SET FOREIGN_KEY_CHECKS = 1;