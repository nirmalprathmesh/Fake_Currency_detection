import cv2
import pickle
import os
import numpy as np
from PIL import Image

from feature_extraction import extract_features
from predict_fake import predict_fake   # import fake model


def load_model():

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    model_path = os.path.join(base_dir, "currency_model.pkl")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return model


def predict_note_and_authenticity(image_path):

    model = load_model()

    img = Image.open(image_path)
    img = img.convert("RGB")
    img = np.array(img)

    img = cv2.resize(img, (256,128))

    feature = extract_features(img)

    denomination = model.predict([feature])[0]

    # 🔥 Only check fake for high-value notes
    if denomination in ["500", "2000"]:
        authenticity = predict_fake(image_path)
    else:
        authenticity = "real"

    return denomination, authenticity