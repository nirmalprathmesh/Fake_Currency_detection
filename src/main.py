from dataset_loader import load_dataset
from feature_extraction import extract_features

images, labels = load_dataset("Dataset/Train")

feature = extract_features(images[0])

print("Feature vector length:", len(feature))
print("Label:", labels[0])