import numpy as np
from PIL import Image
import os
import asyncio
import aiofiles
import io

async def enhance_image(image):
    """Улучшает изображение, преобразуя его в черно-белый формат."""
    enhanced_image = await asyncio.to_thread(image.convert, "L")
    return enhanced_image

async def process_image(file_name, input_folder, output_folder, max_image_size=(224, 224)):
    """Обрабатывает одно изображение и сохраняет его в выходную папку."""
    input_path = os.path.join(input_folder, file_name)
    output_path = os.path.join(output_folder, file_name)


    # Чтение файла в байты, затем открытие с использованием io.BytesIO
    async with aiofiles.open(input_path, 'rb') as f:
        image_data = await f.read()
        image = await asyncio.to_thread(Image.open, io.BytesIO(image_data))

        await asyncio.to_thread(image.thumbnail, max_image_size, Image.LANCZOS)

        # Улучшаем изображение
        enhanced_image = await enhance_image(image)

        # Сохраняем результат
        async with aiofiles.open(output_path, 'wb') as out_f:
            output_data = io.BytesIO()
            await asyncio.to_thread(enhanced_image.save, output_data, format="JPEG")
            await out_f.write(output_data.getvalue())

async def process_single_image(input_folder, output_folder, file_name, max_image_size=(224, 224)):
    """Обрабатывает одно изображение, указанное пользователем."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    await process_image(file_name, input_folder, output_folder, max_image_size)
