CREATE TABLE IF NOT EXISTS Organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    alternate_name TEXT,
    image TEXT,
    url TEXT,
    address TEXT,
    email TEXT,
    founding_date TIMESTAMP,
    founding_location VARCHAR(255),  -- ISO country code
    is_non_profit BOOLEAN,
    phone TEXT
);