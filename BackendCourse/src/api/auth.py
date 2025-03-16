from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DatabaseDep
from src.schemas.users import UserRequestAddSchema, UserAddSchema
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


@router.post('/register')
async def register_user(
        data: UserRequestAddSchema,
        db: DatabaseDep
):
    try:
        hashed_password = AuthService().hash_password(password=data.password)
        new_user_data = UserAddSchema(email=data.email, hashed_password=hashed_password)
        await db.users.add(new_user_data)
        await db.commit()
    except:  # noqa: E722
        raise HTTPException(status_code=400)

    return {'Status': 'OK'}


@router.post('/login')
async def login_user(
        data: UserRequestAddSchema,
        response: Response,
        db: DatabaseDep
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким Email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный пароль")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)

    return {'access_token': access_token}


@router.get('/me')
async def get_auth(
        user_id: UserIdDep,
        db: DatabaseDep
):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie("access_token")

    return {"Status": "Ok"}
