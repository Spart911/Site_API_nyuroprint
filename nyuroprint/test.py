import numpy as np
import tensorflow as tf
from tensorflow.python.compiler.tensorrt import trt_convert as trt

# Diagnostic and configuration print
print("TensorFlow Version:", tf.__version__)
print("TensorRT Imported Successfully")

# Parameters
INPUT_SHAPE = (1, 224, 224, 3)  # Adjust to your model's input shape
MAX_BATCH_SIZE = 32  # Adjust based on your GPU memory

try:
    # Ensure the saved model directory exists
    import os
    if not os.path.exists("keras_model_saved_model"):
        raise FileNotFoundError("Saved model directory not found. Please save your model first.")

    # TensorRT Converter (removed max_batch_size)
    converter = trt.TrtGraphConverterV2(
        input_saved_model_dir="keras_model_saved_model",
        precision_mode=trt.TrtPrecisionMode.FP16  # Using FP16 for performance
    )

    # Input generation function
    def input_fn():
        x = np.random.rand(1, *INPUT_SHAPE[1:]).astype(np.float32)  # Changed to single batch
        yield [x]

    # Conversion process with detailed logging
    print("Starting TensorRT conversion...")
    converter.convert()
    print("Conversion completed. Building TensorRT graph...")

    # Build the TensorRT-optimized graph
    converter.build(input_fn=input_fn)
    print("TensorRT graph built successfully.")

    # Save the optimized model
    OUTPUT_SAVED_MODEL_DIR = "tensorrt_optimized_model"
    converter.save(output_saved_model_dir=OUTPUT_SAVED_MODEL_DIR)
    print(f"Optimized model saved to: {OUTPUT_SAVED_MODEL_DIR}")

except Exception as e:
    print(f"TensorRT Conversion Error: {e}")
    import traceback
    traceback.print_exc()

# Optional: Verify the converted model
try:
    loaded_trt_model = tf.saved_model.load(OUTPUT_SAVED_MODEL_DIR)
    concrete_func = loaded_trt_model.signatures['serving_default']

    # Test inference
    test_input = np.random.rand(1, *INPUT_SHAPE[1:]).astype(np.float32)
    predictions = concrete_func(tf.constant(test_input))
    print("Model loaded and inference test completed successfully.")
except Exception as e:
    print(f"Model verification error: {e}")