FROM nvcr.io/nvidia/tensorflow:24.01-tf2-py3

# Обновляем пакеты и устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libhdf5-dev \
    python3-dev \
    libhdf5-serial-dev \
    hdf5-tools \
    libhdf5-dev \
    zlib1g-dev

# Устанавливаем переменные среды для HDF5 и pkg-config
ENV HDF5_DIR=/usr/include/hdf5/serial
ENV PKG_CONFIG_PATH=/usr/lib/pkgconfig

# install libgl1-mesa-glx and libglib2.0-0
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# copy the requirements file into the image
COPY ./requirements.txt /ai/requirements.txt

# switch working directory
WORKDIR /ai

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# copy every content from the local file to the image
COPY . /ai

EXPOSE 3000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000", "--workers", "10", "--proxy-headers", "--forwarded-allow-ips", "*", "--reload"]
