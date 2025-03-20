from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep, DatabaseDep
from src.exceptions.exceptions import UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException, \
    EmailIsNotRegisteredException, EmailIsNotRegisteredHTTPException, IncorrectPasswordException, \
    IncorrectPasswordHTTPException
from src.schemas.users import UserRequestAddSchema
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserRequestAddSchema, db: DatabaseDep):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"Status": "OK"}


@router.post("/login")
async def login_user(data: UserRequestAddSchema, response: Response, db: DatabaseDep):
    try:
        access_token = await AuthService(db).login_user(data, response)
    except EmailIsNotRegisteredException:
        raise EmailIsNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    return {"access_token": access_token}


@router.get("/me")
async def get_auth(user_id: UserIdDep, db: DatabaseDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")

    return {"Status": "Ok"}
