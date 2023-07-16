ALTER TABLE diva_profile
    ADD cnp_cid INT NOT NULL DEFAULT -1,
    ADD cnp_val INT NOT NULL DEFAULT -1,
    ADD cnp_rr INT NOT NULL DEFAULT -1,
    ADD cnp_sp VARCHAR(255) NOT NULL DEFAULT "",
    ADD btn_se_eqp INT NOT NULL DEFAULT -1,
    ADD sld_se_eqp INT NOT NULL DEFAULT -1,
    ADD chn_sld_se_eqp INT NOT NULL DEFAULT -1,
    ADD sldr_tch_se_eqp INT NOT NULL DEFAULT -1;