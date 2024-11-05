from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Depends, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uvicorn
from Controllers.PrinterController import PrinterController
from Controllers.PrintController import PrintController
from Models.Printer import Printer
from Models.Print import Print
from database import DataBase, AsyncSessionLocal, engine, get_db  # Импортируйте engine и AsyncSessionLocal
from fastapi.responses import JSONResponse


UPLOAD_FOLDER = 'uploads'

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
async def add_print(
    img: UploadFile,
    printer_id: int = Form(...),  # Добавлено получение printer_id из формы
    quality: int = Form(...),      # Добавлено получение quality из формы
    session: AsyncSession = Depends(get_db)
):
    try:
        response = await PrintController.add_print(img, printer_id, quality, session, UPLOAD_FOLDER)
        return JSONResponse(content=response, status_code=201)  # Успешный ответ с кодом 201
    except HTTPException as http_ex:
        raise http_ex  # Повторно выбрасываем HTTP исключения
    except Exception as ex:
        return JSONResponse(content={"message": str(ex)}, status_code=500)  # Обработка общих исключений

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
