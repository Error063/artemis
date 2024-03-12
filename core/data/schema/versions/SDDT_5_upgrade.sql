ALTER TABLE ongeki_static_events
ADD COLUMN startDate TIMESTAMP NOT NULL DEFAULT current_timestamp();