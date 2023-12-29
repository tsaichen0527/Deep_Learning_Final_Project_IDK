import os

image_files = []
os.chdir(os.path.join("images", "train"))
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg"):
        image_files.append("A:/FinalProject/Deep_Learning_Final_Project_IDK/yolo/final_project_dataset/car_person_bike_motor/images/train/" + filename)

os.chdir("../..")

os.chdir(os.path.join("labels", "train"))
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".txt"):
        image_files.append(
            "A:/FinalProject/Deep_Learning_Final_Project_IDK/yolo/final_project_dataset/car_person_bike_motor/labels/train/" + filename)

os.chdir("../..")

with open("train.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()





