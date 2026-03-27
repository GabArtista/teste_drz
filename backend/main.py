from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Infrastructure.Database.connection import create_tables
from app.Http.Controllers import auth_controller, knowledge_controller, chat_controller
from app.Exceptions.handlers import register_exception_handlers
from config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="DRZ Chat API",
    version="1.0.0",
    description="API para chat com IA baseado em texto fornecido",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router, prefix="/auth", tags=["Auth"])
app.include_router(knowledge_controller.router, prefix="/knowledge", tags=["Knowledge"])
app.include_router(chat_controller.router, prefix="/chat", tags=["Chat"])

register_exception_handlers(app)


@app.get("/health")
async def health():
    return {"status": "ok"}
