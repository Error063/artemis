ALTER TABLE diva_profile_shop DROP COLUMN c_itm_eqp_ary;
ALTER TABLE diva_profile_shop DROP COLUMN ms_itm_flg_ary;

ALTER TABLE diva_profile DROP COLUMN use_pv_mdl_eqp;
ALTER TABLE diva_profile DROP COLUMN use_mdl_pri;
ALTER TABLE diva_profile DROP COLUMN use_pv_skn_eqp;
ALTER TABLE diva_profile DROP COLUMN use_pv_btn_se_eqp;
ALTER TABLE diva_profile DROP COLUMN use_pv_sld_se_eqp;
ALTER TABLE diva_profile DROP COLUMN use_pv_chn_sld_se_eqp;
ALTER TABLE diva_profile DROP COLUMN use_pv_sldr_tch_se_eqp;
ALTER TABLE diva_profile ADD COLUMN use_pv_mdl_eqp VARCHAR(8) NOT NULL DEFAULT "true" AFTER sort_kind;
ALTER TABLE diva_profile ADD COLUMN use_pv_btn_se_eqp VARCHAR(8) NOT NULL DEFAULT "true" AFTER use_pv_mdl_eqp;
ALTER TABLE diva_profile ADD COLUMN use_pv_sld_se_eqp VARCHAR(8) NOT NULL DEFAULT "false" AFTER use_pv_btn_se_eqp;
ALTER TABLE diva_profile ADD COLUMN use_pv_chn_sld_se_eqp VARCHAR(8) NOT NULL DEFAULT "false" AFTER use_pv_sld_se_eqp;
ALTER TABLE diva_profile ADD COLUMN use_pv_sldr_tch_se_eqp VARCHAR(8) NOT NULL DEFAULT "false" AFTER use_pv_chn_sld_se_eqp;

DROP TABLE IF EXISTS `diva_profile_pv_customize`;