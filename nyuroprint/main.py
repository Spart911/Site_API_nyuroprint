from flask import Flask, request, jsonify
import remove_bg as rb
import image_editor as ie
import Underextrusion as un
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/process_images', methods=['POST'])
def process_images():
    # Проверяем, было ли передано изображение
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    # Получаем файл из запроса
    image = request.files['image']

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, 'input')

    os.makedirs(input_dir, exist_ok=True)

    image.save(os.path.join(input_dir, image.filename))

    try:
        # Выполняем обработку изображений с помощью ваших функций
        rb.Dremove_bg('input/', 'input/')
        ie.process_images('input/', 'input/')
        defect = un.underextrusion('input/')
        defect_str = str(defect)
        defect_int = int(defect_str[0])
        # Удаляем изображение после обработки
        try:
            os.remove('input/' + image.filename)
        except OSError as e:
            print("Ошибка при удалении изображения:", e)
        return jsonify({'message': 'Images processed successfully', 'defect': defect_int}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Запускаем Flask-приложение, только если скрипт запускается напрямую, а не при импортировании
if __name__ == "__main__":
    # Запускаем Flask с помощью Gunicorn
    # Задаем параметры: хост, порт и количество рабочих процессов
    app.run(host='0.0.0.0', port=3000)
