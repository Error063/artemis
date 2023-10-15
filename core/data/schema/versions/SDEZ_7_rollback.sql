ALTER TABLE mai2_profile_detail
    DROP COLUMN mapStock;

ALTER TABLE mai2_profile_extend
    DROP COLUMN selectResultScoreViewType;

ALTER TABLE mai2_profile_option
    DROP COLUMN outFrameType,
    DROP COLUMN touchVolume,
    DROP COLUMN breakSlideVolume;
