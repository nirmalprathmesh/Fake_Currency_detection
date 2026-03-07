from skimage.feature import hog
from preprocessing import preprocess_image

def extract_features(image):

    processed = preprocess_image(image)

    features = hog(
        processed,
        orientations=9,
        pixels_per_cell=(8,8),
        cells_per_block=(2,2),
        block_norm='L2-Hys'
    )

    return features