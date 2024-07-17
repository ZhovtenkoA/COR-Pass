from typing import List

from sqlalchemy.orm import Session

from cor_pass.database.models import Tag
from cor_pass.schemas import TagModel, TagResponse


async def get_tags(skip: int, limit: int, db: Session) -> List[Tag]:
    """
    Get a list of tags from the database.

    :param skip: The number of tags to skip.
    :param limit: The maximum number of tags to retrieve.
    :param db: The database session used to interact with the database.
    :return: A list of tag objects.
    """
    tags = db.query(Tag).offset(skip).limit(limit).all()
    tag_dicts = [{"name": tag.name, "id": tag.id} for tag in tags]
    return tag_dicts


async def get_tag(tag_id: int, db: Session) -> Tag:
    """
    Get a tag from the database by its ID.

    :param tag_id: The ID of the tag to retrieve.
    :param db: The database session used to interact with the database.
    :return: The retrieved tag object.
    """
    return db.query(Tag).filter(Tag.id == tag_id).first()


async def create_tag(body: TagModel, db: Session) -> TagResponse:
    """
    Create a new tag in the database.

    :param body: The tag data used to create the tag.
    :param db: The database session used to interact with the database.
    :return: The created tag response object.
    """
    tag = Tag(name=body.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return TagResponse(id=tag.id, name=tag.name)


async def update_tag(tag_id: int, body: TagModel, db: Session) -> Tag | None:
    """
    Update an existing tag in the database.

    :param tag_id: The ID of the tag to update.
    :param body: The updated tag data.
    :param db: The database session used to interact with the database.
    :return: The updated tag object if found, else None.
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.name = body.name
        db.commit()
    return tag


async def remove_tag(tag_id: int, db: Session) -> Tag | None:
    """
    Remove a tag from the database.

    :param tag_id: The ID of the tag to remove.
    :param db: The database session used to interact with the database.
    :return: The removed tag object if found, else None.
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag