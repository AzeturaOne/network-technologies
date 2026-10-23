from fastapi import APIRouter, HTTPException, status, Request, Depends
from app.models.users import NewUser, UserSignIn

user_router = APIRouter(tags=["User"])
users: dict[str, NewUser] = {}

# Зависимость для проверки, вошел ли пользователь
def get_current_user(request: Request) -> str:
    user_email = request.session.get("user")
    if not user_email or user_email not in users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Необходима авторизация (выполните вход /signin)."
        )
    return user_email


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_new_user(data: NewUser) -> dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует.",
        )
    users[data.email] = data
    return {"message": "Пользователь успешно зарегистрирован!"}


@user_router.post("/signin")
async def sign_user_in(user: UserSignIn, request: Request) -> dict:
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не существует.",
        )
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Переданы неверные учетные данные.",
        )
    # Сохраняем email пользователя в сессию (в cookies браузера)
    request.session["user"] = user.email
    return {"message": "Вход выполнен успешно."}


@user_router.post("/signout")
async def sign_user_out(request: Request) -> dict:
    if "user" not in request.session:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы не авторизованы.",
        )
    # Удаляем пользователя из сессии
    request.session.pop("user", None)
    return {"message": "Выход выполнен успешно."}