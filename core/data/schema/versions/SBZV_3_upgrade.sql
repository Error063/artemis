ALTER TABLE diva_profile_shop ADD COLUMN c_itm_eqp_ary varchar(59) DEFAULT "-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999";
ALTER TABLE diva_profile_shop ADD COLUMN ms_itm_flg_ary varchar(59) DEFAULT "-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1";

ALTER TABLE diva_profile DROP COLUMN use_pv_mdl_eqp;
ALTER TABLE diva_profile DROP COLUMN use_pv_btn_se_eqp;
ALTER TABLE diva_profile DROP COLUMN use_pv_sld_se_eqp;
ALTER TABLE diva_profile DROP COLUMN use_pv_chn_sld_se_eqp;
ALTER TABLE diva_profile DROP COLUMN use_pv_sldr_tch_se_eqp;
ALTER TABLE diva_profile ADD COLUMN use_pv_mdl_eqp BOOLEAN NOT NULL DEFAULT true AFTER sort_kind;
ALTER TABLE diva_profile ADD COLUMN use_mdl_pri BOOLEAN NOT NULL DEFAULT false AFTER use_pv_mdl_eqp;
ALTER TABLE diva_profile ADD COLUMN use_pv_skn_eqp BOOLEAN NOT NULL DEFAULT false AFTER use_mdl_pri;
ALTER TABLE diva_profile ADD COLUMN use_pv_btn_se_eqp BOOLEAN NOT NULL DEFAULT true AFTER use_pv_skn_eqp;
ALTER TABLE diva_profile ADD COLUMN use_pv_sld_se_eqp BOOLEAN NOT NULL DEFAULT false AFTER use_pv_btn_se_eqp;
ALTER TABLE diva_profile ADD COLUMN use_pv_chn_sld_se_eqp BOOLEAN NOT NULL DEFAULT false AFTER use_pv_sld_se_eqp;
ALTER TABLE diva_profile ADD COLUMN use_pv_sldr_tch_se_eqp BOOLEAN NOT NULL DEFAULT false AFTER use_pv_chn_sld_se_eqp;


CREATE TABLE diva_profile_pv_customize (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user INT NOT NULL,
    version INT NOT NULL,
    pv_id INT NOT NULL,
    mdl_eqp_ary VARCHAR(14) DEFAULT '-999,-999,-999',
    c_itm_eqp_ary VARCHAR(59) DEFAULT '-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999',
    ms_itm_flg_ary VARCHAR(59) DEFAULT '-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1',
    skin INT DEFAULT '-1',
    btn_se INT DEFAULT '-1',
    sld_se INT DEFAULT '-1',
    chsld_se INT DEFAULT '-1',
    sldtch_se INT DEFAULT '-1',
    UNIQUE KEY diva_profile_pv_customize_uk (user, version, pv_id),
    CONSTRAINT diva_profile_pv_customize_ibfk_1 FOREIGN KEY (user) REFERENCES aime_user (id) ON DELETE CASCADE ON UPDATE CASCADE
);
