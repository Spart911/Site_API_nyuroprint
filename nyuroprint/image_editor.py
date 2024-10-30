import numpy as np
from PIL import Image, ImageFilter
import os

def enhance_image(image):
    """Улучшает изображение, преобразуя его в черно-белый формат."""
    bw_image = image.convert("L")  # Преобразование в черно-белый
    return bw_image

def process_images(input_folder, output_folder, max_image_size=(224, 224)):
    """Обрабатывает изображения из входной папки и сохраняет в выходную папку."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_list = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    for file_name in file_list:
        input_path = os.path.join(input_folder, file_name)

        # Открываем изображение
        with Image.open(input_path) as image:
            # Изменяем размер изображения, если необходимо
            image.thumbnail(max_image_size, Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)

            # Улучшаем изображение
            enhanced_image = enhance_image(image)

            # Сохраняем результат
            output_path = os.path.join(output_folder, file_name)
            enhanced_image.save(output_path)

    print("Обработка изображений завершена.")
