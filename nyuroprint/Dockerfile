# Используем образ с предустановленными инструментами для разработки
FROM python:3.10-buster AS builder

# Обновление и установка дополнительных пакетов
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    openjdk-11-jdk \
    bazel \
    && rm -rf /var/lib/apt/lists/*

# Клонируем репозиторий TensorFlow
WORKDIR /tensorflow
RUN git clone https://github.com/tensorflow/tensorflow.git .
RUN git checkout v2.12.0  # Выберите нужную версию

# Настраиваем сборку без AVX
RUN echo "build --copt=-march=x86-64" >> .bazelrc
RUN echo "build --copt=-mno-avx" >> .bazelrc
RUN echo "build --copt=-mno-avx2" >> .bazelrc
RUN echo "build --copt=-mno-fma" >> .bazelrc
RUN echo "build --copt=-mno-avx512f" >> .bazelrc

# Конфигурируем и собираем TensorFlow
RUN python3 configure.py
RUN bazel build --config=opt //tensorflow/tools/pip_package:build_pip_package

# Создаем wheel-файл
RUN ./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg

# Начинаем новый этап для финального образа
FROM python:3.10-slim-buster

# Копируем собранный wheel-файл из предыдущего этапа
COPY --from=builder /tmp/tensorflow_pkg/tensorflow-*.whl /tmp/

# Устанавливаем необходимые зависимости
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем TensorFlow из wheel-файла
RUN pip install /tmp/tensorflow-*.whl

# Копируем остальные файлы приложения
COPY ./requirements.txt /ai/requirements.txt
WORKDIR /ai
RUN pip install --no-cache-dir -r requirements.txt
COPY . /ai

EXPOSE 3000

ENTRYPOINT ["python"]
CMD ["main.py"]
