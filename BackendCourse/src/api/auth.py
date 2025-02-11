from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, get_token
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAddSchema, UserAddSchema
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


@router.post('/register')
async def register_user(
        data: UserRequestAddSchema
):
    hashed_password = AuthService().hash_password(password=data.password)
    new_user_data = UserAddSchema(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {'Status': 'OK'}


@router.post('/login')
async def login_user(
        data: UserRequestAddSchema,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким Email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {'access_token': access_token}


@router.get('/me')
async def get_auth(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie("access_token")

    return {"Status": "Ok"}
