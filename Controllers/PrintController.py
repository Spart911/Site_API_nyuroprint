import os
import aiofiles
import aiohttp
from fastapi import HTTPException, UploadFile, Form
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from Models.Print import Print, PrintSchema
import aiofiles.os


class PrintController:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    @staticmethod
    def allowed_file(filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in PrintController.ALLOWED_EXTENSIONS

    @staticmethod
    async def get_prints(session: AsyncSession):
        try:
            result = await session.execute(select(Print))
            prints = result.scalars().all()
            print_schema = PrintSchema(many=True)
            return {"message": "OK", "data": print_schema.dump(prints)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_print(session: AsyncSession, item_id: int):
        try:
            result = await session.execute(select(Print).filter(Print.id == item_id))
            selected_print = result.scalar_one_or_none()
            if not selected_print:
                raise HTTPException(status_code=404, detail="Print not found")
            print_schema = PrintSchema()
            return {"message": "OK", "data": print_schema.dump(selected_print)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def add_print(
            file: UploadFile,
            session: AsyncSession,
            upload_folder: str,
            printer_id: int = Form(...),
            quality: str = Form(...)
    ):
        # Проверка файла
        if not file:
            raise HTTPException(status_code=400, detail="No image part")

        if file.filename == "":
            raise HTTPException(status_code=400, detail="No selected image")

        if not PrintController.allowed_file(file.filename):
            raise HTTPException(status_code=400, detail="Invalid file type")

        try:
            # Создание безопасного имени файла
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)

            # Проверка существования файла и генерация уникального имени
            while await aiofiles.os.path.exists(filepath):
                name, ext = filename.rsplit('.', 1)
                filename = f"{name}1.{ext}"
                filepath = os.path.join(upload_folder, filename)

            # Асинхронное сохранение файла
            async with aiofiles.open(filepath, 'wb') as f:
                content = await file.read()
                await f.write(content)

            # Асинхронный запрос к сервису обработки изображений
            async with aiohttp.ClientSession() as session_http:
                form = aiohttp.FormData()
                form.add_field('image',
                               content,
                               filename=filename,
                               content_type=file.content_type)

                async with session_http.post('http://nyuroprint:3000/process_images', data=form) as response:
                    response_data = await response.json()
                    is_defected_image = response_data.get('defect')

            # Создание записи в базе данных
            new_print = Print(
                printer_id=printer_id,
                defect=is_defected_image,
                img_path=filepath,
                quality=quality
            )
            session.add(new_print)
            await session.commit()

            return {
                "message": "Print added successfully",
                "print_id": new_print.id,
                "defect": is_defected_image
            }

        except Exception as e:
            await session.rollback()
            # Удаление файла в случае ошибки
            if await aiofiles.os.path.exists(filepath):
                await aiofiles.os.remove(filepath)
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def secure_filename(filename: str) -> str:
        """
        Безопасное преобразование имени файла
        """
        filename = filename.replace(" ", "_")
        filename = "".join(c for c in filename if c.isalnum() or c in "._-")
        return filename