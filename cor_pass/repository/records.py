from sqlalchemy import and_
from sqlalchemy.orm import Session


from cor_pass.database.models import User, Record, Tag
from cor_pass.config.config import settings

import os



async def create_record(
    db: Session, record_name: str, user_id: int, website: str, username: str, password: str, notes: str, tag_names: list = None,  
) -> Record:

    user = db.query(User).filter_by(id=user_id).first()

    if not user:
        raise Exception("User not found")

    record = Record(record_name=record_name, 
                   user_id=user_id, 
                   website = website, 
                   username = username,
                   password = password,
                   notes = notes)

    if tag_names:
        for tag_name in tag_names:
            tag = db.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            record.tags.append(tag)

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


async def get_record_by_id(user: User, db: Session, record_id: int):

    record = (
        db.query(Record)
        .filter(
            and_(
                Record.record_id == record_id,
                # Image.user_id == user.id
            )
        )
        .first()
    )
    return record


async def get_all_records(db: Session):

    images = db.query(Record).all()
    return images


async def update_record(
    user: User, db: Session, record_id: int, record_name: str, website: str, username: str, password: str,  notes: str):

    record = (
        db.query(Record)
        .filter(
            and_(
                Record.record_id == record_id,
                # Image.user_id == user.id
            )
        )
        .first()
    )
    if record:
        record_name=record_name,  
        website = website, 
        username = username,
        password = password,
        notes = notes
        db.commit()
    return record


async def delete_record(user: User, db: Session, record_id: int):

    record = (
        db.query(Record)
        .filter(and_(Record.record_id == record_id, Record.user_id == user.id))
        .first()
    )
    if not record:
        return False, {"message": "image not found"}
    if record:
        db.delete(record)
        db.commit()
        print("Record deleted")
    return record
