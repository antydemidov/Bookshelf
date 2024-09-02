"""A set of models for the Bookshelf."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class OrganizationModel(BaseModel):
    """A model for a organization."""

    id: int

    name: str  # The name of the item
    alternate_name: str | None = None  # An alias for the item
    description: str | None = None  # A description of the item
    image: str | None = None  # An image of the item. This can be a URL
    url: str | None = None  # URL of the item

    address: str | None = None
    email: str | None = None
    founding_date: datetime | None = datetime.min
    founding_location: str | None = None
    is_non_profit: bool | None = False
    phone: str | None = None


class PersonModel(BaseModel):
    """A model for a person."""

    id: int

    full_name: str | None = None
    family_name: str | None = None
    given_name: str | None = None
    additional_name: str | None = None  # for middle names e.g.

    alternate_name: str | None = None  # An alias for the item
    description: str | None = None  # A description of the item
    image: str | None = None  # An image URL
    url: str | None = None  # URL of the item

    birth_date: datetime | None = datetime.min
    birth_place: str | None = None
    death_date: datetime | None = datetime.min
    death_place: str | None = None
    email: str | None = None
    gender: str | None = None
    member_of: OrganizationModel | None = None
    nationality: str | None = None


class BookModel(BaseModel):
    """A model for books."""

    model_config = ConfigDict(validate_default=False)

    identifier: str  # internal UUID-like identifier
    name: str | None = None
    description: str | None = None
    image: str | None = None  # url
    url: str | None = None
    # alternate_name: str | None = None

    abstract: str | None = None
    authors: list | None = Field(default_factory=list)
    comment: str | None = None
    content_location: str | None = None  # The location depicted or described in the content
    content_rating: str | None = None  # Official rating of a piece of content, for example, 'MPAA PG-13'
    content_reference_time: datetime | None = datetime.min  # The location depicted or described in the content
    country_of_origin: str | None = None
    date_created: datetime | None = datetime.min
    date_modified: datetime | None = datetime.min
    date_published: datetime | None = datetime.min
    editors: list | None = Field(default_factory=list)  # Specifies the Person who edited the CreativeWork
    genres: str | None = None
    # has_part: list | CreativeWork  # Indicates an item or CreativeWork that is part of this item
    in_language: str | None = None
    is_accessible_for_free: bool | None = None
    is_family_friendly: bool | None = None
    is_in_original_language: bool | None = None
    is_abridged: bool | None = None  # Indicates whether the book is an abridged edition
    part_of: int | None = None  # Indicates an item or CreativeWork that this item is part of
    keywords: str | None = None
    license: str | None = None  # url
    position: int | str | None = None  # The position of an item in a series or sequence of items
    publishers: list | None = Field(default_factory=list)  # The publisher of the creative work
    thumbnail: str | None = None  # URL of the thumbnail
    translation_of: int | None = None
    translators: list | None = Field(default_factory=list)
    # work_translation: CreativeWork  # A work that is a translation of the content of this work
    # about: Thing  # The subject matter of the content
    # aggregate_rating: str
    # alternative_headline: str
    characters: list | None = Field(default_factory=list)
    # citations: list
    # headline: str
    location_created: str | None = None
    # size: str  # Physical size of the creative work
    # time_required: int  # Approximate or typical time it usually takes to work with
    # typical_age_range: str  # The typical expected age range, e.g. '7-9', '11-'

    book_edition: str | None = None  # The edition of the book
    book_format: str | None = None  # The format of the book: AudiobookFormat, EBook, GraphicNovel, Hardcover, Paperback
    illustrators: list | None = Field(default_factory=list)  # The illustrator of the book
    isbn: str | None = None  # The ISBN of the book
    number_of_pages: int | None = None  # The number of pages in the book

    file_size: int | None = None
    file_type: str | None = None
    other_ids: dict | None = None


class SettingsModel(BaseModel):

    default_picture: str = '../static/person_default.png'
    other_ids_links: dict[str, str] = Field(default_factory=dict)
