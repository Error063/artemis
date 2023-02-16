SET FOREIGN_KEY_CHECKS=0;

ALTER TABLE wacca_profile DROP COLUMN season;
ALTER TABLE wacca_profile DROP COLUMN playcount_stageup_season;
ALTER TABLE wacca_profile DROP COLUMN playcount_multi_coop_season;
ALTER TABLE wacca_profile DROP COLUMN playcount_multi_vs_season;
ALTER TABLE wacca_profile DROP COLUMN playcount_single_season;
ALTER TABLE wacca_profile DROP COLUMN xp_season;
ALTER TABLE wacca_profile DROP COLUMN wp_season;
ALTER TABLE wacca_profile DROP COLUMN wp_spent_season;
ALTER TABLE wacca_item DROP COLUMN use_count_season;

ALTER TABLE wacca_profile ADD gate_tutorial_flags JSON NULL;

SET FOREIGN_KEY_CHECKS=1;
