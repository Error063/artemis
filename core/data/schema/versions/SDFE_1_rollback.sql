UPDATE wacca_score_stageup SET version = 2 WHERE version = 3;
UPDATE wacca_score_stageup SET version = 3 WHERE version = 4;
ALTER TABLE wacca_score_stageup CHANGE version season int(11) DEFAULT NULL NULL;
