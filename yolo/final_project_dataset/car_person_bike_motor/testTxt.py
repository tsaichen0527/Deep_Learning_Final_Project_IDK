import os

image_files = []
os.chdir(os.path.join("images", "test"))
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg"):
        image_files.append("A:/FinalProject/Deep_Learning_Final_Project_IDK/yolo/final_project_dataset/car_person_bike_motor/test/" + filename)
os.chdir("../..")
with open("test.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()
os.chdir("..")