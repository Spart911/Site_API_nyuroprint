import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
import os
from tensorflow.python.compiler.tensorrt import trt_convert as trt


class UnderextrusionDetector:
    def __init__(self, model_path="tensorrt_optimized_model", labels_path="labels.txt"):
        # Инициализация конвертера TensorRT
        self.converter = trt.TrtGraphConverterV2(
            input_saved_model_dir=model_path,
            precision_mode=trt.TrtPrecisionMode.FP16,
            use_calibration=True
        )

        # Конвертация и сохранение модели
        print("Converting model to TensorRT...")
        self.converter.convert()

        # Сохранение оптимизированной модели
        print("Saving optimized model...")
        self.converter.save(model_path + "_optimized")

        # Загрузка оптимизированной модели
        print("Loading optimized model...")
        self.model = tf.saved_model.load(model_path + "_optimized")
        self.predict_fn = self.model.signatures['serving_default']

        # Загрузка меток классов
        print("Loading class labels...")
        with open(labels_path, "r") as f:
            self.class_names = [line.strip() for line in f.readlines()]

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
            raise Exception(f"Error preprocessing image: {str(e)}")

    def predict(self, input_path, confidence_threshold=0.5):
        """
        Выполняет предсказание для изображения или директории с изображениями.

        Args:
            input_path: путь к изображению или директории
            confidence_threshold: порог уверенности для предсказания

        Returns:
            dict: результаты предсказания
        """
        try:
            if os.path.isfile(input_path):
                return self._predict_single(input_path, confidence_threshold)
            elif os.path.isdir(input_path):
                return self._predict_directory(input_path, confidence_threshold)
            else:
                raise ValueError(f"Invalid input path: {input_path}")

        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")

    def _predict_single(self, image_path, confidence_threshold):
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
            return {
                'status': 'error',
                'message': f'Prediction failed: {str(e)}'
            }

    def _predict_directory(self, directory_path, confidence_threshold):
        """Предсказание для директории с изображениями."""
        results = {}
        for filename in os.listdir(directory_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(directory_path, filename)
                results[filename] = self._predict_single(file_path, confidence_threshold)
        return results


# Пример использования:
if __name__ == "__main__":
    try:
        # Инициализация детектора
        detector = UnderextrusionDetector(
            model_path="tensorrt_optimized_model",
            labels_path="labels.txt"
        )

        # Пример предсказания для одного изображения
        result = detector.predict("def_no.jpg")
        print("Single image prediction:", result)



    except Exception as e:
        print(f"Error: {str(e)}")