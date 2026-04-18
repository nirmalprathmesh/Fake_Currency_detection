import os
import cv2

def load_fake_dataset(dataset_path):

    images = []
    labels = []

    data_path = os.path.join(dataset_path, "data")

    for label in ["real", "fake"]:

        label_path = os.path.join(data_path, label)

        if not os.path.exists(label_path):
            continue

        # go inside denomination folders (10, 20, 50...)
        for denom in os.listdir(label_path):

            denom_path = os.path.join(label_path, denom)

            if not os.path.isdir(denom_path):
                continue

            for img_name in os.listdir(denom_path):

                img_path = os.path.join(denom_path, img_name)

                img = cv2.imread(img_path)

                if img is None:
                    continue

                img = cv2.resize(img, (256,128))

                images.append(img)
                labels.append(label)   # ONLY real / fake

    return images, labels