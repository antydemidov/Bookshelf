CREATE TABLE IF NOT EXISTS BooksOrganizations (
    id INTEGER PRIMARY KEY,
    book_id INTEGER,
    organization_id INTEGER,
    type VARCHAR(255) NOT NULL,  -- Author, Translator, Illustrator, Character etc.

    FOREIGN KEY (book_id) REFERENCES Books (id) ON DELETE CASCADE,
    FOREIGN KEY (organization_id) REFERENCES Organizations (id) ON DELETE CASCADE
);