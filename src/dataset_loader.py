import os
import cv2

def load_dataset(dataset_path):

    images = []
    labels = []

    for label in os.listdir(dataset_path):

        # ignore background images
        if label.lower().startswith("background"):
            continue

        folder_path = os.path.join(dataset_path, label)

        if not os.path.isdir(folder_path):
            continue

        for img_name in os.listdir(folder_path):

            img_path = os.path.join(folder_path, img_name)

            img = cv2.imread(img_path)

            if img is None:
                continue

            # better resolution for HOG
            img = cv2.resize(img, (256,128))

            images.append(img)
            labels.append(label)

    return images, labels