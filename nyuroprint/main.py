from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageOps
import os
import logging
import asyncio
import uvicorn
import aiofiles

import remove_bg as rb
import image_editor as ie
import Underextrusion as un

# Конфигурация логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_detector():
    """Ленивая инициализация детектора"""
    if not hasattr(app.state, "detector"):
        app.state.detector = un.UnderextrusionDetector(
            model_path="tensorrt_optimized_model",
            labels_path="labels.txt"
        )
    return app.state.detector

# Создание директории для входящих изображений
script_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(script_dir, 'input')
os.makedirs(input_dir, exist_ok=True)


@app.post("/process_images")
async def process_images_endpoint(image: UploadFile = File(...)):
    # Сохраняем изображение
    image_path = os.path.join(input_dir, image.filename)
    try:
        print("async file open start")
        async with aiofiles.open(image_path, "wb") as buffer:
            await buffer.write(await image.read())
        print("async file open stop")

        print("async resize_image start")
        await resize_image(image_path)
        print("async resize_image stop")

        print("async обработка изображений start")
        await asyncio.gather(
            rb.Dremove_bg(input_dir, input_dir),
            ie.process_images(input_dir, input_dir)
        )
        print(f"async обработка изображений sto---------------p")

        # Инициализируем детектор при первом обращении
        detector = get_detector()

        # Выполняем предсказание для конкретного изображени
        # prediction_result = detector.predict(image_path)
        prediction_result = await asyncio.to_thread(detector.predict, image_path)  # Изменено на image_path

        # Извлекаем имя файла и предсказание
        file_name = os.path.basename(image_path)
        file_prediction = prediction_result.get('class_name')  # Предполагаем, что возвращается только одно предсказание

        if file_prediction:
            defect_str = str(file_prediction)
            defect_int = int(defect_str[0]) if defect_str else 0

            logger.info('Images processed successfully')
            return JSONResponse(content={'message': 'Images processed successfully', 'defect': defect_int},
                                status_code=200)
        else:
            logger.error(f'No valid prediction found for "{file_name}": {prediction_result}')
            raise HTTPException(status_code=500, detail='No valid prediction found')

    except Exception as e:
        logger.error(f'Error processing image: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


async def resize_image(image_path):
    """Изменяет размер изображения до 224x224 асинхронно."""
    await asyncio.to_thread(_resize_and_save_image, image_path)

def _resize_and_save_image(image_path):
    """Синхронная функция для изменения размера изображения, вызываемая из асинхронного контекста."""
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    resized_image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    resized_image.save(image_path)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
    )
