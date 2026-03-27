from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables():
    from app.Models.base import Base
    import app.Models.user_model  # noqa
    import app.Models.knowledge_base_model  # noqa
    import app.Models.chat_session_model  # noqa
    import app.Models.message_model  # noqa

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
