from PIL import Image
import shutil
import os
import pygame

def generate_bonsai_buddy_images():
    if os.path.isdir("bonsai_buddy/images"):
        shutil.rmtree("bonsai_buddy/images")
        print("cleared images folder")
    os.mkdir("bonsai_buddy/images")
    print("made images folder")

    sheet = Image.open("bonsai_buddy/sprite_sheet.png")
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
            icon = sheet.crop((a - width, b - height, a, b))
            icon.save(f"bonsai_buddy/images/bonsai-buddy-{count}.png")
            count += 1

class bonsai_buddy:
    def __init__(self):
        pass

    def __init__(self):
        img = pygame.image.load("bonsai_buddy/images/bonsai-buddy-0.png")
        img.convert()
        self.width = 200
        self.height = 160
        self.surface = pygame.Surface((self.width, self.height))

    def draw(self, screen, x, y):
        screen.blit(self.surface, (x, y))


if __name__ == "__main__":
    # generate_bonsai_buddy_images()
    pass