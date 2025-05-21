from sqlalchemy import select
from database import Base, async_engine, async_session_factory
from models import UsersOrm, BooksOrm


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для хеширования пароля
def get_password_hash(password):
    return pwd_context.hash(password)


class AsyncORM:
    
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    
    @staticmethod
    async def insert_users(username_, email_):
        async with async_session_factory() as session:
            user = UsersOrm(username = username_, email = email_,)
            session.add_all([user])
            # flush взаимодействует с БД, поэтому пишем await
            await session.flush()
            await session.commit()


    @staticmethod
    async def select_user(email):
        async with async_session_factory() as session:
            query = (
                select(UsersOrm.email)
                .filter_by(email = email)
            )
            res = await session.execute(query)
            result = res.first()
            return result
        
    @staticmethod
    async def select_users_auth(email: str, password):
        async with async_session_factory() as session:
            query = (
                select(UsersOrm.email, UsersOrm.hashed_password)
                .filter_by(email=email)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await session.execute(query)
            result = res.first()
            if result:
                return result
            else:
                raise HTTPException(status_code=401, detail=f"Пользователь с email {email} не зарегистрирован")