ALTER TABLE mai2_item_card 
    CHANGE COLUMN startDate startDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHANGE COLUMN endDate endDate TIMESTAMP NOT NULL;