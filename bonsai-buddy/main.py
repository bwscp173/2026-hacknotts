from PIL import Image
import shutil
import os

if os.path.isdir("bonsai-buddy/images"):
    shutil.rmtree("bonsai-buddy/images")
    print("cleared images folder")
os.mkdir("bonsai-buddy/images")
print("made images folder")

sheet = Image.open("bonsai-buddy/sprite_sheet.png")
count = 0

sheet_size = (3400, 3360)
colums = 17
rows = 21
width = sheet_size[0]/colums
height = sheet_size[1]/rows

print(f"height={height}")
print(f"width={width}")
for y in range(rows):
    for x in range(colums):

        a = (x + 1) * width
        b = (y + 1) * height
        icon = sheet.crop((a - width, b - height, a, b))  # Problem here
        icon.save("bonsai-buddy/images/bonsai-buddy-{}.png".format(count))
        count += 1