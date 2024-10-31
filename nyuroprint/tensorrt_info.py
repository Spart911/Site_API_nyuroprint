import tensorrt as trt


def print_bindings_info(engine):
    # Получаем количество входных и выходных тензоров
    num_io_tensors = engine.num_io_tensors

    # Проходим по всем тензорам
    for idx in range(num_io_tensors):
        name = engine.get_tensor_name(idx)  # Получаем имя тензора
        shape = engine.get_tensor_shape(name)  # Получаем форму тензора
        dtype = engine.get_tensor_dtype(name)  # Получаем тип данных тензора
        location = engine.get_tensor_location(name)  # Получаем местоположение тензора

        # Выводим информацию о тензорах
        print(f'Tensor ID: {idx}   Name: {name}   Shape: {shape}   Type: {dtype}   Location: {location}')


def main():
    model_path = "model.trt"

    # Создаем логгер TensorRT
    logger = trt.Logger(trt.Logger.INFO)

    # Загружаем модель
    with open(model_path, "rb") as f, trt.Runtime(logger) as runtime:
        engine = runtime.deserialize_cuda_engine(f.read())

        # Печатаем информацию о привязках
        print_bindings_info(engine)


if __name__ == "__main__":
    main()
