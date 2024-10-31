from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageOps
import remove_bg as rb
import image_editor as ie
import Underextrusion as un
import os
import logging

# Конфигурация логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

detector = un.UnderextrusionDetector(
            model_path="tensorrt_optimized_model",
            labels_path="labels.txt"
        )

# Создание директории для входящих изображений
script_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(script_dir, 'input')
os.makedirs(input_dir, exist_ok=True)


@app.route('/process_images', methods=['POST'])
def process_images():
    # Проверяем, было ли передано изображение
    if 'image' not in request.files:
        logger.error('No image provided')
        return jsonify({'error': 'No image provided'}), 400

    # Получаем файл из запроса
    image = request.files['image']
    image_path = os.path.join(input_dir, image.filename)

    # Сохраняем изображение
    image.save(image_path)

    try:
        # Изменяем размер изображения до 224x224
        resize_image(image_path)

        # Выполняем обработку изображений
        rb.Dremove_bg(input_dir, input_dir)
        ie.process_images(input_dir, input_dir)

        prediction_result = detector.predict(input_dir)

        # Извлекаем имя файла из prediction_result и предсказание для этого файла
        file_name = os.path.basename(image_path)
        file_prediction = prediction_result.get(file_name)

        # Проверка на наличие предсказания и ключа 'class_name'
        if file_prediction and 'class_name' in file_prediction:
            defect = file_prediction['class_name']
        else:
            logger.error(f'Prediction result for "{file_name}" does not contain "class_name": {prediction_result}')
            return jsonify({'error': f'Prediction result for "{file_name}" does not contain "class_name": {prediction_result}'}), 500

        # Удаляем изображение после обработки
        os.remove(image_path)

        defect_str = str(defect)
        print("defect_str =")
        print(defect_str)
        defect_int = int(defect_str[0]) if defect_str else 0

        logger.info('Images processed successfully')
        return jsonify({'message': 'Images processed successfully', 'defect': defect_int}), 200
    except Exception as e:
        logger.error(f'Error processing image: {str(e)}')
        return jsonify({'error': str(e)}), 500


def resize_image(image_path):
    """Изменяет размер изображения до 224x224."""
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    resized_image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    resized_image.save(image_path)


# Запускаем Flask-приложение
if __name__ == "__main__":
    # Запуск с помощью Gunicorn
    app.run(host='0.0.0.0', port=3000, debug=False)  # Убедитесь, что debug=False для продакшена

