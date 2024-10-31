import os
import requests
from flask import jsonify, request
from Models.Print import Print, PrintSchema, db
from werkzeug.utils import secure_filename

class PrintController:
    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def get_prints():
        prints = Print.query.all()
        print_schema = PrintSchema(many=True)
        return jsonify({'message': 'OK', 'data': print_schema.dump(prints)})

    @staticmethod
    def get_print(item_id):
        selected_print = Print.query.get(item_id)
        if selected_print:
            print_schema = PrintSchema()
            return jsonify({'message': 'OK', 'data': print_schema.dump(selected_print)})
        else:
            return jsonify({'message': 'Print not found'}), 404

    @staticmethod
    def add_print(app):
        print_schema = PrintSchema()
        request_data = request.form.to_dict()

        # Проверка наличия обязательных полей в запросе
        required_fields = ['printer_id', 'quality']
        missing_fields = [field for field in required_fields if field not in request_data]

        if missing_fields:
            return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        try:
            new_print_data = print_schema.load(request_data)
        except Exception as e:
            return jsonify({'message': 'Validation error', 'errors': str(e)}), 400

        if 'img' not in request.files:
            return jsonify({'message': 'No image part'}), 400

        file = request.files['img']

        if file.filename == '':
            return jsonify({'message': 'No selected image'}), 400

        if file and PrintController.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            while os.path.exists(filepath):
                filename = filename.rsplit('.', 1)[0] + '1' + '.' + filename.rsplit('.', 1)[1]
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(filepath)
        else:
            return jsonify({'message': 'Invalid file type'}), 400

        with open(filepath, 'rb') as f:
            file_content = f.read()
        files = {'image': (str(filename), file_content)}
        response = requests.post('http://nyuroprint:3000/process_images', files=files)
        isDefectedImage = response.json().get('defect')

        try:
            new_print = Print(
                printer_id=new_print_data['printer_id'],
                defect=isDefectedImage,
                img_path=filepath,
                quality=new_print_data['quality']
            )
            db.session.add(new_print)
            db.session.commit()
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'message': str(e)}), 400
        return jsonify({'message': 'Print added successfully', 'print_id': new_print.id, 'defect': isDefectedImage}), 201
