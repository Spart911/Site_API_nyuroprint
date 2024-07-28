from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import zipfile
from cryptography.fernet import Fernet
import os


def underextrusion(input_path):
    # Загружаем модель
    model = load_model("keras_model.h5", compile=False)

    # # Удаляем расшифрованный архив
    # os.remove('decrypted_model.zip')

    # # Удаляем файл модели
    # os.remove('keras_model.h5')


    # Загружаем метки классов
    class_names = open("labels.txt", "r").readlines()

    # Создаем массив правильной формы для передачи в модель Keras
    # 'length' или количество изображений, которые можно поместить в массив,
    # определяется первой позицией в кортеже формы, в данном случае 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Получаем путь к директории
    input_directory = input_path

    # Получаем список файлов в директории
    files_in_directory = os.listdir(input_directory)

    # Ищем первый файл в директории (вам может потребоваться более сложную логику, в зависимости от вашего случая)
    first_file = next((f for f in files_in_directory if os.path.isfile(os.path.join(input_directory, f))), None)
    full_path_to_file = os.path.join(input_directory, first_file)

    # Замените это на путь к вашему изображению
    image = Image.open(full_path_to_file).convert("RGB")

    # изменение размера изображения до 224x224 и обрезка по центру
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # преобразование изображения в массив numpy
    image_array = np.asarray(image)

    # Нормализация изображения
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Загрузка изображения в массив
    data[0] = normalized_image_array

    # Прогнозирование модели
    prediction = model.predict(data, verbose=0)
    index = np.argmax(prediction)
    class_name = class_names[index]
    return class_name
    # print("Class:", class_name[2:], end="")
    # print("defect =", defect)
    # print("Confidence Score:", confidence_score)
    # return defect,confidence_score
