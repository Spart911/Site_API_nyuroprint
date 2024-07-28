import os

def create_file(path):
    try:
        # Проверяем, существует ли директория, если нет, создаем ее
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'w') as file:
            # Можно записать что-то в файл, если это необходимо
            file.write("Пример текста в файле\n")

        print(f"Файл успешно создан по пути: {path}")
    except OSError as e:
        print(f"Ошибка при создании файла: {e}")

create_file('C:/Users/79509/Desktop/printerAPI/nyuroprint/input⁠/text.jpeg')