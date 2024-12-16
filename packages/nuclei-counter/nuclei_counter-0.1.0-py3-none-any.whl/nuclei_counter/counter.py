import logging
import cv2
import matplotlib.pyplot as plt

VALID_FILE_EXTENSIONS = [".png", ".jpg", ".tif"]

logger = logging.getLogger(__file__)


def count_objects(args):
    file_name, img_dir, save_path, save_images = args
    if not any(file_name.endswith(ext) for ext in VALID_FILE_EXTENSIONS):
        return None
    try:
        img = cv2.imread(str(img_dir / file_name))
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply thresholding
        thresh = cv2.threshold(gray, 11, 255, cv2.THRESH_OTSU)[1]
        # Apply morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # Find contours
        contours, _ = cv2.findContours(
            opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        marked_img = cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

        plt.imshow(marked_img)
        if save_images:
            cv2.imwrite(str(save_path / f"marked_{file_name}"), marked_img)

        # Count the number of contours
        num_objects = len(contours)

        # print(f"Number of objects found: {num_objects} ({file_name})")
        return {"file_name": file_name, "count": num_objects}
    except Exception as e:
        logger.error(f"Exception: {e}, {file_name}")
