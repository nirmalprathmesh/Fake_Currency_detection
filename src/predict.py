import cv2
import pickle
import os
import numpy as np
from PIL import Image

from feature_extraction import extract_features


def load_model():

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    model_path = os.path.join(base_dir, "currency_model.pkl")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return model


def predict_note(image_path):

    model = load_model()

    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        img = np.array(img)

    except:
        print("Error loading image:", image_path)
        return None

    img = cv2.resize(img, (256,128))

    feature = extract_features(img)

    prediction = model.predict([feature])

    return prediction[0]


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    test_folder = os.path.join(base_dir, "Dataset", "test1")

    files = [f for f in os.listdir(test_folder) if not f.startswith("Background")]

    correct = 0
    total = 0

    for file in files:

        image_path = os.path.join(test_folder, file)

        prediction = predict_note(image_path)

        true_label = file.split("_")[0]

        if prediction == true_label:
            correct += 1

        total += 1

    print("\nAccuracy:", (correct/total)*100, "%")