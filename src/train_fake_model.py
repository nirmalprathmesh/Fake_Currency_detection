import pickle
from sklearn.svm import SVC
from fake_dataset_loader import load_fake_dataset
from fake_feature_extraction import extract_fake_features

print("Loading fake dataset...")

images, labels = load_fake_dataset("Dataset_Fake")

features = []

print("Extracting features...")

for img in images:
    features.append(extract_fake_features(img))

print("Training fake detection model...")

model = SVC(kernel="rbf", C=10, gamma="scale")

model.fit(features, labels)

with open("fake_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Fake detection model trained successfully")