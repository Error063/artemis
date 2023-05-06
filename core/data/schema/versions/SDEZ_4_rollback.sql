DELETE FROM mai2_static_event WHERE version < 13;
UPDATE mai2_static_event SET version = version - 13 WHERE version >= 13;

DELETE FROM mai2_static_music WHERE version < 13;
UPDATE mai2_static_music SET version = version - 13 WHERE version >= 13;

DELETE FROM mai2_static_ticket WHERE version < 13;
UPDATE mai2_static_ticket SET version = version - 13 WHERE version >= 13;

DELETE FROM mai2_static_cards WHERE version < 13;
UPDATE mai2_static_cards SET version = version - 13 WHERE version >= 13;

DELETE FROM mai2_profile_detail WHERE version < 13;
UPDATE mai2_profile_detail SET version = version - 13 WHERE version >= 13;

DELETE FROM mai2_profile_extend WHERE version < 13;
UPDATE mai2_profile_extend SET version = version - 13 WHERE version >= 13;

DELETE FROM mai2_profile_option WHERE version < 13;
UPDATE mai2_profile_option SET version = version - 13 WHERE version >= 13;

DELETE FROM mai2_profile_ghost WHERE version < 13;
UPDATE mai2_profile_ghost SET version = version - 13 WHERE version >= 13;

DELETE FROM mai2_profile_rating WHERE version < 13;
UPDATE mai2_profile_rating SET version = version - 13 WHERE version >= 13;
