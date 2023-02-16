SET FOREIGN_KEY_CHECKS=0;

ALTER TABLE wacca_profile ADD season int(11) NOT NULL;
ALTER TABLE wacca_profile ADD playcount_stageup_season int(11) NULL;
ALTER TABLE wacca_profile ADD playcount_multi_coop_season int(11) NULL;
ALTER TABLE wacca_profile ADD playcount_multi_vs_season int(11) NULL;
ALTER TABLE wacca_profile ADD playcount_single_season int(11) NULL;
ALTER TABLE wacca_profile ADD xp_season int(11) NULL;
ALTER TABLE wacca_profile ADD wp_season int(11) NULL;
ALTER TABLE wacca_profile ADD wp_spent_season int(11) NULL;
ALTER TABLE wacca_item ADD use_count_season int(11) NULL;

ALTER TABLE wacca_profile DROP COLUMN gate_tutorial_flags;


SET FOREIGN_KEY_CHECKS=1;