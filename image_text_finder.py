import os
import pytesseract
import streamlit as st
from PIL import Image, ImageOps
from pytesseract import Output

def get_rotated_images(image_path):
    rotated_images = []
    images_paths = []        
    for root, _, files in os.walk(image_path):

        for file in files:
            image_file = os.path.join(root, file)
            image = Image.open(image_file)

            for angle in [0, 90, 180, 270]:
                rotated_image = ImageOps.exif_transpose(image.rotate(angle))
                rotated_images.append(rotated_image)
                images_paths.append(file)
    return rotated_images, images_paths

def ocr_and_search_text(rotated_images, search_string, images_paths):
    found_in_images = []
    for image, file in zip(rotated_images, images_paths):
        text = pytesseract.image_to_string(image, config='--psm 6', output_type=Output.STRING)
        if search_string.lower() in text.lower():
            found_in_images.append(file)
        else:
            continue

    return set(found_in_images)

def main():
    st.title("OCR Text Search Application:sleuth_or_spy::open_file_folder:")

    image_directory = st.text_input("Enter your image directory:", "test_images")
    search_string = st.text_input("Enter the substring you want to search for:", "RC")
    
    if st.button('Start OCR and Text Search'):
        try:
            rotated_images, images_paths = get_rotated_images(image_directory)
            found_in_images = ocr_and_search_text(rotated_images, search_string, images_paths)
            if found_in_images:
                st.success(f"Substring '{search_string}' found in the following images: ")
                for image in found_in_images:
                    st.write("- ",  os.path.join(image_directory, image))
            else:
                st.warning(f"Substring '{search_string}' not found in any image.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
