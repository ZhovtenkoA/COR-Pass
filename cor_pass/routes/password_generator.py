from fastapi import FastAPI, Query, APIRouter, HTTPException, Depends, status
from cor_pass.schemas import PasswordGeneratorSettings


from cor_pass.repository import password_generator as repository_password_generator



router = APIRouter(prefix="/password_generator", tags=["Password Generator"])


@router.post("/generate_password/", status_code=status.HTTP_201_CREATED)
async def generate_password_endpoint(settings: PasswordGeneratorSettings):
    return {"password": repository_password_generator.generate_password(settings)}



@router.get("/generate_word_password/", status_code=status.HTTP_201_CREATED)
async def generate_word_password_endpoint(num_words: int = Query(4, ge=1, le=10)):
    return {"password": repository_password_generator.generate_word_password(num_words)}