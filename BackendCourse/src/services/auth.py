from datetime import datetime, timezone, timedelta

import jwt
from fastapi.openapi.models import Response
from passlib.context import CryptContext

from src.config import settings
from src.exceptions.exceptions import ObjectAlreadyExistsException, UserAlreadyExistsException, \
    EmailIsNotRegisteredException, IncorrectPasswordException, IncorrectTokenException
from src.schemas.users import UserRequestAddSchema, UserAddSchema
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException

    async def register_user(self, data: UserRequestAddSchema):
        hashed_password = AuthService().hash_password(password=data.password)
        new_user_data = UserAddSchema(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as exc:
            raise UserAlreadyExistsException from exc

    async def login_user(self, data: UserRequestAddSchema, response: Response):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise EmailIsNotRegisteredException
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)

        return access_token

    async def get_auth(self, user_id):
        user = await self.db.users.get_one_or_none(id=user_id)
        return user

    async def logout(self, response: Response) -> None:
        response.delete_cookie("access_token")

