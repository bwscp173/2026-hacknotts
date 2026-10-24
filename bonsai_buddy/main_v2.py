from PIL import Image
from random import randint
from time import sleep
from pyautogui import moveTo
import shutil
import os
import pygame
import datetime
from time import sleep

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
    def __init__(self, screen):
        self.surface = pygame.image.load("bonsai_buddy/images/bonsai-buddy-0.png")
        self.surface.convert()
        self.frame_index = 0
        self.location = [0, 0]
        self.screen = screen

    def set_location(self, location:tuple):
        self.location = location

    def set_x(self, x:int):
        self.location = (x, self.location[1])

    def set_y(self, y:int):
        self.location = (self.location[0], y)
    
    def draw(self, screen):
        screen.blit(self.surface, self.location)

    def set_frame(self, frame_index:int):
        self.frame_index = (frame_index) % 343
        self.surface = pygame.image.load(f"bonsai_buddy/images/bonsai-buddy-{self.frame_index}.png")
        self.surface.convert()

    def increment_frame(self):
        self.frame_index = (self.frame_index+1) % 343
        self.surface = pygame.image.load(f"bonsai_buddy/images/bonsai-buddy-{self.frame_index}.png")
        self.surface.convert()

    def steal_mouse(self, screen_size:tuple, time2=2):
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=time2)
        while datetime.datetime.now() < end_time:
            x = randint(0,screen_size[0])
            y = randint(0,screen_size[1])

            moveTo(x, y, 1)
            sleep(0.5)
        print(end_time)


    def moveTo(self, x, y, slow=0.003):
        steps = 100

        target_x = x
        target_y = y

        x, y = pygame.mouse.get_pos()
        dy = (y - target_y)/steps
        dx = (x - target_x)/steps

        for _ in range(steps):
            x -= dx
            y -= dy
            pygame.mouse.set_pos(x, y)
            self.set_location((x, y))

            self.draw(self.screen)
            pygame.display.flip()

            sleep(slow)


if __name__ == "__main__":
    # generate_bonsai_buddy_images()
    pass
    moveTo(0,0)
    #steal_mouse((500,500))