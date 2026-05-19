from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

db_uri = settings.DATABASE_URI
if db_uri.startswith("postgresql://"):
    db_uri = db_uri.replace("postgresql://", "postgresql+asyncpg://", 1)
elif db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql+asyncpg://", 1)

engine = create_async_engine(db_uri, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
