CREATE TABLE IF NOT EXISTS Persons (
    id INTEGER PRIMARY KEY,
    alternate_name TEXT,  -- An alias for the item
    description TEXT,  -- A description of the item
    image TEXT,  -- An image of the item. This can be a URL
    name TEXT,  -- The name of the item
    url TEXT,  -- URL of the item
    additional_name TEXT,  -- for middle names e.g.
    birth_date TIMESTAMP,
    birth_place TEXT,
    death_date TIMESTAMP,
    death_place TEXT,
    email TEXT,
    family_name TEXT,
    gender TEXT,
    given_name TEXT,
    full_name TEXT,
    member_of INTEGER,
    nationality VARCHAR(255),  -- ISO country code

    FOREIGN KEY (member_of) REFERENCES Organizations (id) ON DELETE SET NULL
);