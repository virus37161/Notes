from bot.core.config import settings
from sqlalchemy.ext.asyncio import (async_sessionmaker,
                                	create_async_engine,
                                	AsyncSession, AsyncEngine, AsyncConnection)

from typing import Union, Callable

db_url = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
    f"db:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

engine = create_async_engine(db_url)

class InternalError(Exception):
	pass

# Функция get_async_session используется для получения асинхронной сессии SQLAlchemy
async def get_async_session() -> AsyncSession:
	async with async_session() as session:
		try:
			yield session
		except InternalError:
			await session.rollback()

# Функция create_sessionmaker создаёт фабрику сессий для асинхронной работы с базой данных
def create_sessionmaker(
    	bind_engine: Union[AsyncEngine, AsyncConnection]
) -> Callable[..., async_sessionmaker]:
	# Возвращается фабрика сессий, определённая с заданными параметрами
	return async_sessionmaker(
    	bind=bind_engine,
    	expire_on_commit=False,
    	class_=AsyncSession,
	)

# Создание асинхронного движка SQLAlchemy для работы с PostgreSQL
engine = create_async_engine(db_url)

# Создание фабрики для сессий
async_session = create_sessionmaker(engine)

# Создание зависимости для работы с базой данных
