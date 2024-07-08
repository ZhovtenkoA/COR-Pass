from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Security,
    BackgroundTasks,
    Request,
    Query,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from cor_pass.database.db import get_db
from cor_pass.schemas import (
    UserModel,
    ResponseUser,
    LoginResponseModel,
    TokenModel,
    EmailSchema,
    ChangePasswordModel,
)
from cor_pass.repository import users as repository_users
from cor_pass.services.auth import auth_service
from cor_pass.config.config import settings
from cor_pass.services.logger import logger

router = APIRouter(prefix="/auth", tags=["Authorization"])
security = HTTPBearer()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

@router.post("/signup", response_model=ResponseUser, status_code=status.HTTP_201_CREATED)
async def signup(
    body: UserModel,
    db: Session = Depends(get_db),
):
    """
    The signup function creates a new user in the database.
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        logger.debug(f"{body.email} user already exist")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    logger.debug(f"{body.email} user successfully created")
    return {"user": new_user, "detail": "User successfully created"}

@router.post("/login", response_model=LoginResponseModel)
async def login(
    request: Request,
    body: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    The login function is used to authenticate a user.
    """
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found / invalid email",
        )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    access_token = await auth_service.create_access_token(
        data={"oid": user.id}, expires_delta=3600
    )
    refresh_token = await auth_service.create_refresh_token(data={"oid": user.id})
    await repository_users.update_token(user, refresh_token, db)
    logger.debug(f"{user.email} login success")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    """
    The refresh_token function is used to refresh the access token.
    """
    token = credentials.credentials
    id = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_uuid(id, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await auth_service.create_access_token(data={"oid": user.id})
    refresh_token = await auth_service.create_refresh_token(data={"oid": user.id})
    user.refresh_token = refresh_token
    db.commit()
    await repository_users.update_token(user, refresh_token, db)
    logger.debug(f"{user.email}'s refresh token updated")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post("/forgot_password")
async def forgot_password_send_verification_code(
    body: EmailSchema,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    The forgot_password_send_verification_code function sends a verification code to the user's email.
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # логика восстановления пароля с помощью ключа/пользовательского файла

    return {"message": "Verification code sent"}

@router.patch("/change_password")
async def change_password(body: ChangePasswordModel, db: Session = Depends(get_db)):
    """
    The change_password function allows a user to change their password.
    """
    user = await repository_users.get_user_by_email(body.email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    else:
        if body.password:
            await repository_users.change_user_password(body.email, body.password, db)
            logger.debug(f"{body.email} changed their password")
            return {"message": f"User '{body.email}' changed their password"}
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Incorrect password input",
            )