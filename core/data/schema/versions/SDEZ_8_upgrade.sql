ALTER TABLE mai2_profile_detail
    ADD mapStock INT NULL AFTER playCount;

ALTER TABLE mai2_profile_extend
    ADD selectResultScoreViewType INT NULL AFTER selectResultDetails;

ALTER TABLE mai2_profile_option
    ADD outFrameType INT NULL AFTER dispCenter,
    ADD touchVolume INT NULL AFTER slideVolume,
    ADD breakSlideVolume INT NULL AFTER slideVolume;
