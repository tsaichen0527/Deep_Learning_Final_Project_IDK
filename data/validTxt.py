import os

image_files = []
os.chdir(os.path.join("images", "valid"))
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg"):
        image_files.append("../data/images/valid/" + filename)
os.chdir("../..")
with open("valid.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()


