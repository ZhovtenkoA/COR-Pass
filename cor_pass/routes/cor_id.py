from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from cor_pass.database.db import get_db
from cor_pass.services.auth import auth_service
from cor_pass.database.models import User
from cor_pass.services.access import user_access
from cor_pass.schemas import ResponseCorIdModel, CreateCorIdModel
from cor_pass.repository import cor_id as repository_cor_id


router = APIRouter(prefix="/medical/cor_id", tags=["Cor-Id"])


@router.post(
    "/show_corid_info",
    # response_model=ResponseCorIdModel,
    dependencies=[Depends(user_access)],
)
async def read_cor_id(
    cor_id: ResponseCorIdModel,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    **Просмотр своего COR-id** \n

    """
    if cor_id:
        cor_id = repository_cor_id.display_corid_info(cor_id.cor_id)
    if cor_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="COR-Id not found"
        )
    return cor_id


@router.post(
    "/create",
    # response_model=ResponseCorIdModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(user_access)],
)
async def create_cor_id(
    n_patient,
    # body: CreateCorIdModel,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    **Создание COR-id** \n

    """
    birth_year_gender = f"{user.birth}{user.user_sex}"
    if not user.cor_id:
        cor_id = await repository_cor_id.create_corid(n_patient, birth_year_gender)
        print(cor_id)
        return cor_id
    else:
        return {"message": "cor-id already exist", "cor_id": user.cor_id}
