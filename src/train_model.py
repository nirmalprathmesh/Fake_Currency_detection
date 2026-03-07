import pickle
from sklearn.svm import SVC
from dataset_loader import load_dataset
from feature_extraction import extract_features

print("Loading training dataset...")

images, labels = load_dataset("Dataset/training")

features = []

print("Extracting features...")

for img in images:

    feature = extract_features(img)

    features.append(feature)

print("Training model...")

model = SVC(kernel="rbf", C=10, gamma="scale")

model.fit(features, labels)

with open("currency_model.pkl","wb") as f:
    pickle.dump(model,f)

print("Model trained successfully")