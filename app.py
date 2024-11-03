from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import select
import uvicorn
from Controllers.PrinterController import PrinterController
from Controllers.PrintController import PrintController
from Models.Printer import Printer
from Models.Print import Print

UPLOAD_FOLDER = 'uploads'
DATABASE_URL = "postgresql+asyncpg://root:root@db:5432/PrintersProject"

# Создаем асинхронный движок и сессию
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
from database import DataBase


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(DataBase.metadata.create_all)

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Printer))
        if not result.scalars().first():
            await PrinterController.create_default_printers(session)
        await session.commit()

    yield

    await engine.dispose()

# Создаем приложение FastAPI с жизненным циклом
app = FastAPI(lifespan=lifespan)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nyuroprint.vercel.app", "https://nyuroprint.ru"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware для CSP
@app.middleware("http")
async def add_csp_header(request, call_next):
    response = await call_next(request)
    csp = (
        "upgrade-insecure-requests; default-src 'self'; script-src 'self' 'unsafe-inline' "
        "'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
        "connect-src 'self' http: https:;"
    )
    response.headers['Content-Security-Policy'] = csp
    return response

# Dependency для получения сессии базы данных
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Роуты для принтеров
@app.get("/api/printers/")
async def get_printers(session: AsyncSession = Depends(get_db)):
    return await PrinterController.get_printers(session)

@app.post("/api/printers/")
async def add_printer(session: AsyncSession = Depends(get_db)):
    return await PrinterController.add_printer(session)

@app.get("/api/printers/{item_id}")
async def get_printer(item_id: int, session: AsyncSession = Depends(get_db)):
    return await PrinterController.get_printer(session, item_id)

# Роуты для печати
@app.get("/api/prints/")
async def get_prints(session: AsyncSession = Depends(get_db)):
    return await PrintController.get_prints(session)

@app.post("/api/prints/")
async def add_print(file: UploadFile = File(...), session: AsyncSession = Depends(get_db)):
    return await PrintController.add_print(file, session, UPLOAD_FOLDER)

@app.get("/api/prints/{item_id}")
async def get_print(item_id: int, session: AsyncSession = Depends(get_db)):
    return await PrintController.get_print(session, item_id)

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        ssl_keyfile='ssl/certificate.key.pem',
        ssl_certfile='ssl/certificate.crt.pem'
    )
