import glob
import os

folder_path = "/Users/tiagocoutinho/Desktop/Programação/Software/Modelos ML/yolov3 models/2º modelo/Dataset/images/"

# Loop through all .txt files in the folder
for file_path in glob.glob(os.path.join(folder_path, "*.txt")):
    with open(file_path, "r") as file:
        # Read all lines of the file into a list
        lines = file.readlines()

    # Loop through each line of the file
    for i in range(len(lines)):
        # Split the line into a list of numbers
        numbers = lines[i].strip().split()

        # Replace the first number with zero
        numbers[0] = "0"

        # Join the list of numbers back into a string with spaces
        new_line = " ".join(numbers)

        # Replace the old line with the new line
        lines[i] = new_line + "\n"

    with open(file_path, "w") as file:
        # Write the modified lines back to the file
        file.writelines(lines)
