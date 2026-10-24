from PIL import Image
from enum import Enum
import shutil
import pygame
import os
import random

class Animation(Enum):
    DEFAULT = 0
    SURF = [0,9]
    CLAP = [10,14]
    SURFF = [15,39]
    HOLD_HAND = 48
    SPINNING_GLOBE = [40,87]
    BEATING = [101,108]
    SUN_GLASSES = [108,136]

    WEED = 344

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
        self.animation = Animation.WEED
        self.set_animation(self.animation)

    def set_location(self, location:tuple):
        self.location = location

    def set_x(self, x:int):
        self.location = (x, self.location[1])

    def set_y(self, y:int):
        self.location = (self.location[0], y)
    
    def draw(self, screen):
        screen.blit(self.surface, self.location)

    def set_frame(self, frame_index:int):
        self.frame_index = (frame_index) % 345
        self.surface = pygame.image.load(f"bonsai_buddy/images/bonsai-buddy-{self.frame_index}.png")
        self.surface.convert()

    def increment_frame(self):
        self.frame_index = (self.frame_index+1) % 345
        self.surface = pygame.image.load(f"bonsai_buddy/images/bonsai-buddy-{self.frame_index}.png")
        self.surface.convert()
        print(self.frame_index)

    def set_animation(self, animation:Animation):
        print("ANIMATION VALUE:",animation, animation.value)
        self.animation = animation
        if type(animation.value) == int:
            self.animation_start_frame = animation.value
            self.animation_end_frame = animation.value

            self.frame_index = self.animation_start_frame
            return
        self.animation_start_frame = animation.value[0]
        self.animation_end_frame = animation.value[1]

        self.frame_index = self.animation_start_frame

    def handle_animation(self):
        """run after set_animation() for start frame to be set"""
        #print("handle_animation", self.animation, self.frame_index, self.animation_start_frame, self.animation_end_frame)
        self.set_frame(self.frame_index)

        if self.animation in  [Animation.DEFAULT, Animation.WEED, Animation.HOLD_HAND]:
            return
        
        self.set_frame(self.frame_index)
        self.frame_index += 1
        if self.frame_index > self.animation_end_frame:
            self.frame_index = self.animation_start_frame

    def select_random_animation(self):
        self.set_animation(random.choice([Animation.SURFF,Animation.BEATING,Animation.SURF,Animation.CLAP,Animation.SPINNING_GLOBE,Animation.SUN_GLASSES]))

if __name__ == "__main__":
    # generate_bonsai_buddy_images()
    pass