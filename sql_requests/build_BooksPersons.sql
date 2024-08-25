CREATE TABLE IF NOT EXISTS BooksPersons (
    id INTEGER PRIMARY KEY,
    book_id INTEGER,
    person_id INTEGER,
    type VARCHAR(255) NOT NULL,  -- Author, Translator, Illustrator, Character etc.

    FOREIGN KEY (book_id) REFERENCES Books (id) ON DELETE CASCADE,
    FOREIGN KEY (person_id) REFERENCES Persons (id) ON DELETE CASCADE
);