import os
import pickle
import cv2
import numpy as np
from PIL import Image

from fake_feature_extraction import extract_fake_features


def load_fake_model():

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    model_path = os.path.join(base_dir, "fake_model.pkl")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return model


def predict_fake(image_path):

    model = load_fake_model()

    img = Image.open(image_path)
    img = img.convert("RGB")

    img = np.array(img)
    img = cv2.resize(img, (256,128))

    feature = extract_fake_features(img)

    prediction = model.predict([feature])

    return prediction[0]


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    test_path = os.path.join(base_dir, "Dataset_Fake", "data")

    print("\nTesting fake detection...\n")

    count = 0

    for label in ["real", "fake"]:

        label_path = os.path.join(test_path, label)

        for denom in os.listdir(label_path):

            denom_path = os.path.join(label_path, denom)

            for file in os.listdir(denom_path):

                image_path = os.path.join(denom_path, file)

                result = predict_fake(image_path)

                print(file, "->", result)

                count += 1

                if count >= 20:
                    exit()