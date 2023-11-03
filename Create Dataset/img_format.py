import os

from PIL import Image

# Define the folder path where the images are located
folder_path = "/Users/tiagocoutinho/Desktop/Programação/Software/Modelos ML/yolov3 models/2º modelo/Dataset/images/"

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is an image
    if (
        filename.endswith(".jpg")
        or filename.endswith(".jpeg")
        or filename.endswith(".png")
    ):
        # Open the image file using Pillow
        image = Image.open(os.path.join(folder_path, filename))

        # Change the image format to JPEG
        new_filename = os.path.splitext(filename)[0] + ".jpg"
        image.save(os.path.join(folder_path, new_filename), "jpg")

        # Close the image file
        image.close()

        # Delete the original image file
        os.remove(os.path.join(folder_path, filename))
