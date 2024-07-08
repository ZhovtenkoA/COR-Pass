from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from cor_pass.database.db import get_db
from cor_pass.services.auth import auth_service
from cor_pass.database.models import User, Role
from cor_pass.schemas import UserDb
from cor_pass.repository import users
from pydantic import EmailStr

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/get_all", response_model=list[UserDb]
)
async def get_all_users(
    skip: int = 0,
    limit: int = 10,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    **Get a list of users.**
    This route allows to get a list of pagination-aware users.
    Level of Access:
    - Current authorized user
    :param skip: int: Number of users to skip.
    :param limit: int: Maximum number of users to return.
    :param current_user: User: Current authenticated user.
    :param db: Session: Database session.
    :return: List of users.
    :rtype: List[UserDb]
    """
    list_users = await users.get_users(skip, limit, db)
    return list_users
