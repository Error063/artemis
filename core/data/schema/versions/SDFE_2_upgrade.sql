ALTER TABLE wacca_score_stageup CHANGE season version int(11) DEFAULT NULL NULL;
UPDATE wacca_score_stageup SET version = 4 WHERE version = 3;
UPDATE wacca_score_stageup SET version = 3 WHERE version = 2;
