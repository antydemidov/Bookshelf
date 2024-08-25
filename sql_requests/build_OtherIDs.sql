CREATE TABLE IF NOT EXISTS OtherIDs (
    id INTEGER PRIMARY KEY,
    book_id INTEGER,
    type VARCHAR(255) NOT NULL,  -- type of identifier: ISSN, DOI, OLID, etc.
    identifier VARCHAR(255),  -- value of identifier

    FOREIGN KEY (book_id) REFERENCES Books (id) ON DELETE CASCADE
);