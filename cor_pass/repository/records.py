from typing import List, Optional

from sqlalchemy.orm import Session

from cor_pass.database.models import Record
from cor_pass.schemas import RecordModel, CreateRecordModel, ResponseRecord, UserDb
from cor_pass.services.cipher import encrypt_data, decrypt_data, generate_aes_key

async def get_records(skip: int, limit: int, db: Session) -> List[RecordModel]:
    """
    Get a list of records from the database.

    :param skip: The number of records to skip.
    :param limit: The maximum number of records to retrieve.
    :param db: The database session used to interact with the database.
    :return: A list of record models.
    """
    records = db.query(Record).offset(skip).limit(limit).all()
    print(records)
    return [RecordModel(record) for record in records]

async def get_record(record_id: int, db: Session, encryption_key: str) -> Optional[RecordModel]:
    """
    Get a record from the database by its ID.

    :param record_id: The ID of the record to retrieve.
    :param db: The database session used to interact with the database.
    :param encryption_key: The encryption key used to decrypt the record.
    :return: The retrieved record model.
    """
    encryption_key = generate_aes_key(encryption_key)
    record = db.query(Record).filter(Record.id == record_id).first()
    if record:
        decrypted_record_data = decrypt_data(record.password, encryption_key)
        record.password = decrypted_record_data
        return RecordModel(record)
    return None

async def create_record(body: CreateRecordModel, db: Session, encryption_key: str) -> ResponseRecord:
    """
    Create a new record in the database.

    :param body: The record data used to create the record.
    :param db: The database session used to interact with the database.
    :param encryption_key: The encryption key used to encrypt the record.
    :return: The created record response object.
    """
    encryption_key = generate_aes_key(encryption_key)
    encrypted_password = encrypt_data(body.password, encryption_key) if body.password else None
    record = Record(
        user_id=body.user_id,
        record_name=body.record_name,
        website=body.website,
        username=body.username,
        password=encrypted_password,
        attachments=body.attachments,
        notes=body.notes
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return ResponseRecord(record=RecordModel(record), detail="Record successfully created")

async def update_record(record_id: int, body: CreateRecordModel, db: Session, encryption_key: str) -> Optional[ResponseRecord]:
    """
    Update an existing record in the database.

    :param record_id: The ID of the record to update.
    :param body: The updated record data.
    :param db: The database session used to interact with the database.
    :param encryption_key: The encryption key used to encrypt the record.
    :return: The updated record response object if found, else None.
    """
    encryption_key = generate_aes_key(encryption_key)
    record = db.query(Record).filter(Record.id == record_id).first()
    if record:
        record.record_name = body.record_name
        record.website = body.website
        record.username = body.username
        record.password = encrypt_data(body.password, encryption_key) if body.password else record.password
        record.attachments = body.attachments
        record.notes = body.notes
        db.commit()
        return ResponseRecord(record=RecordModel(record), detail="Record successfully updated")
    return None

async def remove_record(record_id: int, db: Session) -> Optional[RecordModel]:
    """
    Remove a record from the database.

    :param record_id: The ID of the record to remove.
    :param db: The database session used to interact with the database.
    :return: The removed record model if found, else None.
    """
    record = db.query(Record).filter(Record.id == record_id).first()
    if record:
        db.delete(record)
        db.commit()
        return RecordModel(record)
    return None