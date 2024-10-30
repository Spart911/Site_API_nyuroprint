import tensorflow as tf
import tf2onnx

# Загрузка Keras-модели
model = tf.keras.models.load_model("keras_model.h5")

# Конвертация Keras модели в ONNX формат
model_proto, _ = tf2onnx.convert.from_keras(model, opset=13)

# Сохранение ONNX-модели
with open("model.onnx", "wb") as f:
    f.write(model_proto.SerializeToString())
