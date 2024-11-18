import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
import os
import asyncio
from tensorflow.python.compiler.tensorrt import trt_convert as trt
import aiofiles
import shutil
cache_path = "/tmp/tensorrt/"
if os.path.exists(cache_path):
    shutil.rmtree(cache_path)
    print("Cleared TensorRT cache.")

class UnderextrusionDetector:
    def __init__(self, model_path="tensorrt_optimized_model", labels_path="labels.txt"):
        # Удаляем старую оптимизированную модель, если она существует
        optimized_model_path = model_path + "_optimized"

        # Инициализация конвертера TensorRT
        self.converter = trt.TrtGraphConverterV2(
            input_saved_model_dir=model_path,
            precision_mode=trt.TrtPrecisionMode.FP16,
            use_calibration=True,
            allow_build_at_runtime=True
        )

        # Конвертация и сохранение модели
        print("Converting model to TensorRT...")
        self.converter.convert()

        # Сохранение оптимизированной модели
        print("Saving optimized model...")
        self.converter.save(optimized_model_path)

        # Загрузка оптимизированной модели
        print("Loading optimized model...")
        self.model = tf.saved_model.load(optimized_model_path)
        self.predict_fn = self.model.signatures['serving_default']

        # Загрузка меток классов
        print("Loading class labels...")
        with open(labels_path, "r") as f:
            self.class_names = [line.strip() for line in f.readlines()]

    def predict(self, image_path, confidence_threshold=0.5):
        """Предсказание для одного изображения."""

        # Предобработка изображения
        data = self.preprocess_image(image_path)
        data = np.expand_dims(data, axis=0)

        # Выполнение предсказания
        try:
            predictions = self.predict_fn(tf.constant(data))
            output = next(iter(predictions.values())).numpy().flatten()

            # Получение индекса класса и уверенности
            confidence = float(np.max(output))
            class_index = np.argmax(output)

            if confidence < confidence_threshold:
                return {
                    'status': 'low_confidence',
                    'confidence': confidence,
                    'message': 'Prediction confidence too low'
                }

            return {
                'status': 'success',
                'class_name': self.class_names[class_index],
                'confidence': confidence,
                'predictions': {
                    self.class_names[i]: float(output[i])
                    for i in range(len(self.class_names))
                }
            }

        except Exception as e:
            print(f"ошибка предсказания {str(e)}")
            return {
                'status': 'error',
                'message': f'Prediction failed: {str(e)}'
            }

    def preprocess_image(self, image_path):
        """Предобработка изображения для модели."""
        try:
            size = (224, 224)
            image = Image.open(image_path).convert("RGB")
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            image_array = np.asarray(image).astype(np.float32)
            normalized_image_array = (image_array / 127.5) - 1
            return normalized_image_array
        except Exception as e:
            print(f"Exception ----- {str(e)}")
            raise Exception(f"Error preprocessing image: {str(e)}")
detector = UnderextrusionDetector(
            model_path="tensorrt_optimized_model",
            labels_path="labels.txt"
        )