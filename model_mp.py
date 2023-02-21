import cv2
from PIL import Image
import mediapipe as mp
import numpy as np


mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

BG_COLOR = (192, 192, 192) # gray

def remove_background_mediapipe(input_file):
    with mp_selfie_segmentation.SelfieSegmentation(
        model_selection=0) as selfie_segmentation:
        
        # Convert the PIL image to a NumPy array
        image_file = Image.open(input_file.file)
        image = np.array(image_file)

        # Define a custom background color
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        
        # If we want a background blur we can do:
        blurred_image = cv2.GaussianBlur(image,(55,55),0)
    
        # Convert the BGR image to RGB before processing.
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        results = selfie_segmentation.process(image_rgb)

        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5
        output_image = np.where(condition, image, blurred_image)

        return output_image