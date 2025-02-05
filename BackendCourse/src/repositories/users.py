from pydantic import EmailStr
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import UserSchema, UserWithHashedPasswordSchema


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = UserSchema

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPasswordSchema.model_validate(model)
