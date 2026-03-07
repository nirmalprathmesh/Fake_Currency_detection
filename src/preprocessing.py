import cv2

def preprocess_image(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.equalizeHist(gray)

    gray = cv2.GaussianBlur(gray,(5,5),0)

    return gray