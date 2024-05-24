import tensorflow as tf 
import numpy as np
from PIL import Image
import os

# Load the custom trained model
model_path = 'car_classifier.h5'
angle_model = tf.keras.models.load_model('angle_classifier.h5')

if not os.path.exists(model_path): #Control Flow : If statement
    raise FileNotFoundError(f"Model file not found at {model_path}")

try:
    model = tf.keras.models.load_model(model_path)
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

def preprocess_image(image_path): #Function
    try: #Exception Handling : try block
        img = Image.open(image_path).resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array / 255.0
    except Exception as e: #Exception Handling : except block
        raise RuntimeError(f"Error preprocessing image: {e}")

def classify_image(image_path): #Function
    try: #Exception Handling : try block
        processed_image = preprocess_image(image_path)
        prediction = model.predict(processed_image)
        return prediction[0][0] < 0.5  # Thresholding
    except Exception as e: #Exception Handling : except block
        raise RuntimeError(f"Error during classification: {e}")
    
def classify_angle(image_path): #Function
    processed_image = preprocess_image(image_path)
    prediction = angle_model.predict(processed_image)
    angles = ['front', 'left', 'right', 'back']
    return angles[np.argmax(prediction)]
