import zipfile
from cryptography.fernet import Fernet  # Убедитесь, что у вас установлен пакет cryptography

# Генерируем ключ для шифрования
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Создаем зашифрованный архив
with zipfile.ZipFile('encrypted_model.zip', 'w') as zipf:
    # Добавляем файл модели в архив
    zipf.write('keras_Model.h5')

# Шифруем архив
with open('encrypted_model.zip', 'rb') as file:
    encrypted_data = cipher_suite.encrypt(file.read())

# Сохраняем зашифрованный архив
with open('encrypted_model.zip', 'wb') as file:
    file.write(encrypted_data)
print(key)
