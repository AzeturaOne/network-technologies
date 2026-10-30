from fastapi import APIRouter, HTTPException, status, Request, Depends
from sqlmodel import Session, select
from app.database.connection import get_session
from app.models.users import User, NewUser, UserSignIn

user_router = APIRouter(tags=["User"])


def get_current_user(request: Request, session: Session = Depends(get_session)) -> User:
    user_email = request.session.get("user")
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Необходима авторизация (выполните вход /signin)."
        )
    user = session.exec(select(User).where(User.email == user_email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден."
        )
    return user


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_new_user(data: NewUser, session: Session = Depends(get_session)) -> dict:
    existing_user = session.exec(select(User).where(User.email == data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует.",
        )
    new_user = User.model_validate(data)
    session.add(new_user)
    session.commit()
    return {"message": "Пользователь успешно зарегистрирован!"}


@user_router.post("/signin")
async def sign_user_in(user_data: UserSignIn, request: Request, session: Session = Depends(get_session)) -> dict:
    user = session.exec(select(User).where(User.email == user_data.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не существует.",
        )
    if user.password != user_data.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Переданы неверные учетные данные.",
        )
    request.session["user"] = user.email
    return {"message": "Вход выполнен успешно."}


@user_router.post("/signout")
async def sign_user_out(request: Request) -> dict:
    if "user" not in request.session:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы не авторизованы.",
        )
    request.session.pop("user", None)
    return {"message": "Выход выполнен успешно."}