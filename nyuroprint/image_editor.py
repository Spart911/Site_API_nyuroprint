import numpy as np
from PIL import Image
import os
import asyncio
import aiofiles
import io

async def enhance_image(image):
    """Улучшает изображение, преобразуя его в черно-белый формат."""
    print("Преобразование изображения в черно-белый формат...")
    enhanced_image = await asyncio.to_thread(image.convert, "L")
    print("Преобразование завершено.")
    return enhanced_image

async def process_image(file_name, input_folder, output_folder, max_image_size=(224, 224)):
    """Обрабатывает одно изображение и сохраняет его в выходную папку."""
    input_path = os.path.join(input_folder, file_name)
    output_path = os.path.join(output_folder, file_name)

    print(f"Начало обработки файла: {file_name}")
    print(f"Загрузка изображения из: {input_path}")

    # Чтение файла в байты, затем открытие с использованием io.BytesIO
    async with aiofiles.open(input_path, 'rb') as f:
        print("Чтение файла изображения...")
        image_data = await f.read()
        image = await asyncio.to_thread(Image.open, io.BytesIO(image_data))
        print("Файл изображения прочитан.")

        print(f"Изменение размера изображения до {max_image_size}...")
        await asyncio.to_thread(image.thumbnail, max_image_size, Image.LANCZOS)
        print("Изменение размера завершено.")

        # Улучшаем изображение
        print("Начало улучшения изображения...")
        enhanced_image = await enhance_image(image)
        print("Улучшение изображения завершено.")

        # Сохраняем результат
        print(f"Сохранение обработанного изображения в: {output_path}")
        async with aiofiles.open(output_path, 'wb') as out_f:
            output_data = io.BytesIO()
            await asyncio.to_thread(enhanced_image.save, output_data, format="JPEG")
            await out_f.write(output_data.getvalue())
        print(f"Изображение сохранено: {output_path}")

async def process_images(input_folder, output_folder, max_image_size=(224, 224)):
    """Обрабатывает изображения из входной папки и сохраняет в выходную папку."""
    if not os.path.exists(output_folder):
        print(f"Создание выходной папки: {output_folder}")
        os.makedirs(output_folder)

    file_list = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    print(f"Найдено {len(file_list)} изображений для обработки.")

    tasks = [process_image(file_name, input_folder, output_folder, max_image_size) for file_name in file_list]
    print("Запуск задач на обработку изображений...")
    await asyncio.gather(*tasks)

    print("Обработка всех изображений завершена.")
