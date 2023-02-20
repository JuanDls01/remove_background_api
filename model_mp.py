import cv2
from PIL import Image
import mediapipe as mp
import numpy as np


mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

def remove_background_mediapipe(input_file, background_file):
    with mp_selfie_segmentation.SelfieSegmentation(
        model_selection=0) as selfie_segmentation:
        image_file = Image.open(input_file.file)
        bg_file = Image.open(background_file.file)
        # Convert the PIL image to a NumPy array
        image = np.array(image_file)
        bg = np.array(bg_file)

        # Compute the average color of the background image
        bg_avg_color = bg.mean(axis=(0,1)).astype(int)

        # Define a custom background color
        bg_color = tuple(bg_avg_color)
    
        # Convert the BGR image to RGB before processing.
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        bg_rgb = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
        bg_resized = cv2.resize(bg_rgb, (image.shape[1], image.shape[0]))

        results = selfie_segmentation.process(image_rgb)

        blurred_image = cv2.GaussianBlur(image,(55,55),0)
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        output_image = np.where(condition, image, bg_resized)

        return output_image

# def remove_background_mediapipe(input_file):
#     with mp_selfie_segmentation.SelfieSegmentation(model_selection=0) as selfie_segmentation:
#         image_file = Image.open(input_file.file)
#         # Convert the PIL image to a NumPy array
#         image = np.array(image_file)
#         # Convert the BGR image to RGB before processing.
#         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         results = selfie_segmentation.process(image_rgb)
#         condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
#         output_image = np.where(condition, image, 1)
#         return output_image
    
def custom_background(background_file, foreground):
    background = Image.open(background_file.file)
    # Convert the NumPy array to a PIL image object
    foreground_image = Image.fromarray(foreground)
    x = (background.size[0]-foreground_image.size[0])/2 + 0.5
    y = (background.size[1]-foreground_image.size[1])/2 + 0.5
    box = (x, y, foreground_image.size[0] + x, foreground_image.size[1] + y)
    crop = background.crop(box)
    final_image = crop.copy()
    # put the foreground in the centre of the background
    paste_box = (0, final_image.size[1] - foreground_image.size[1], final_image.size[0], final_image.size[1])
    final_image.paste(foreground_image, paste_box, mask=foreground_image)
    # Convert the PIL image object to a NumPy array
    final_array = np.array(final_image)
    return final_array

# def custom_background(background_file, foreground):
#   final_foreground = Image.fromarray(foreground)
#   background = Image.open(background_file)
#   x = (background.size[0]-final_foreground.size[0])/2 + 0.5
#   y = (background.size[1]-final_foreground.size[1])/2 + 0.5
#   box = (x, y, final_foreground.size[0] + x, final_foreground.size[1] + y)
#   crop = background.crop(box)
#   final_image = crop.copy()
#   # put the foreground in the centre of the background
#   paste_box = (0, final_image.size[1] - final_foreground.size[1], final_image.size[0], final_image.size[1])
#   final_image.paste(final_foreground, paste_box, mask=final_foreground)
#   return final_image