import numpy as np
import cv2
from object_detector import *

# Load Object Detector
detector = HomogeneousBgDetector()

# Load Cap
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Fixed pixel to cm ratio for demonstration (replace with actual calibration)
pixel_cm_ratio = 20.0  # Replace with your calibration value

# Example field of view values (replace with your actual values)
hfov_degrees = 60  # Horizontal field of view in degrees
total_pixels_width = 1280  # Total width of the image in pixels

while True:
    _, img = cap.read()

    contours = detector.detect_objects(img)

    # Draw objects boundaries
    for cnt in contours:
        # Get rect
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect

        # Get Width and Height of the Objects by applying the fixed Ratio pixel to cm
        object_width = w / pixel_cm_ratio
        object_height = h / pixel_cm_ratio

        # Calculate angle using the formula
        angle = x * hfov_degrees / total_pixels_width

        # Display rectangle
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
        cv2.polylines(img, [box], True, (255, 0, 0), 2)
        cv2.putText(img, "Width: {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)),
                    cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
        cv2.putText(img, "Height: {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)),
                    cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

        # Display angle
        cv2.putText(img, "Angle: {} degrees".format(round(angle, 1)), (int(x - 100), int(y + 50)),
                    cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
