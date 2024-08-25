CREATE TABLE IF NOT EXISTS Books (
    id INTEGER PRIMARY KEY,
    identifier VARCHAR(255) NOT NULL,  -- internal UUID-like identifier

    name TEXT,
    description TEXT,
    image TEXT,
    url TEXT,
    badges TEXT,  -- Semicolon-separated list of badge names
    -- alternate_name TEXT,

    abstract TEXT,
    comment TEXT,
    content_location TEXT,  -- The location depicted or described in the content
    content_rating TEXT,  -- Official rating of a piece of content—for example, 'MPAA PG-13'
    content_reference_time TEXT,  -- The location depicted or described in the content
    country_of_origin VARCHAR(255),  -- ISO country code
    date_created TIMESTAMP,
    date_modified TIMESTAMP,
    date_published TIMESTAMP,
    genres TEXT,  -- Semicolon-separated list of genres
    -- has_part: list or CreativeWork  -- Indicates an item or CreativeWork that is part of this item
    in_language VARCHAR(255),  -- ISO language code
    is_accessible_for_free BOOLEAN,
    is_family_friendly BOOLEAN,
    is_in_original_language BOOLEAN,
    is_abridged BOOLEAN,  -- Indicates whether the book is an abridged edition
    part_of INTEGER,  -- Indicates an item or CreativeWork that this item is part of
    keywords TEXT,  -- Semicolon-separated list of keywords
    license TEXT,  -- url
    position INTEGER,  -- The position of an item in a series or sequence of items
    thumbnail TEXT,  -- URL of the thumbnail
    translation_of INTEGER,
    -- work_translation INTEGER,  -- A work that is a translation of the content of this work
    -- about: Thing  # The subject matter of the content
    -- aggregate_rating TEXT,
    -- alternative_headline TEXT,
    -- citations: list
    -- headline TEXT,
    location_created TEXT,
    -- size TEXT,  # Physical size of the creative work
    -- time_required INTEGER,  # Approximate or typical time it usually takes to work with
    -- typical_age_range TEXT,  # The typical expected age range, e.g. '7-9', '11-'

    book_edition TEXT,  -- The edition of the book
    book_format VARCHAR(255),  -- The format of the book: AudiobookFormat, EBook, GraphicNovel, Hardcover, Paperback
    isbn VARCHAR(255),  -- The ISBN of the book
    number_of_pages INTEGER,  -- The number of pages in the book

    file_size INTEGER,
    file_type VARCHAR(255),  -- pdf, docx etc.

    FOREIGN KEY (part_of) REFERENCES Books (id) ON DELETE SET NULL,
    FOREIGN KEY (translation_of) REFERENCES Books (id) ON DELETE SET NULL
);