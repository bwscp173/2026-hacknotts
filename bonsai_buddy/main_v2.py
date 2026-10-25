from PIL import Image
from enum import Enum
import datetime
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
    PRAISE = [158,165]
    SHINY = [177,190]
    BOW = [221,232]
    SAD = [236,241]
    THINK = [233,247]
    WAVE = [248,262]
    JUMP = [302,307]
    FLIP = [331,343]
    WEED = 344

avaliable_animations = [Animation.SURFF,Animation.BEATING,Animation.SURF,Animation.CLAP,Animation.SPINNING_GLOBE,Animation.SUN_GLASSES,Animation.PRAISE,Animation.SHINY,Animation.BOW,Animation.SAD,Animation.THINK,Animation.WAVE,Animation.JUMP,Animation.FLIP,Animation.WEED,]

def get_public_ip():
    try:
        from urllib.request import urlopen
        import re

        data = str(urlopen('http://checkip.dyndns.com/').read())
        ip = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)
    except:
        ip = "127.0.0.1"

    return ip

messages = ["monster yummy! <3", "OOPS", "I Talk!", "I Email!", get_public_ip(), "www.bonzi.com"]

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
        self.animation = Animation.DEFAULT
        self.set_animation(self.animation)
        self.last_event = datetime.datetime.now()
        self.event_interval = 5
        self.difficultys = ["EASY","MEDIUM","HARD"]
        self.difficulty = 0

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

    def set_animation(self, animation:Animation):
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
        self.set_animation(random.choice(avaliable_animations))

    def select_message(self):
        return "Bonzi Buddy says:\n"+random.choice(messages)

    def can_do_event(self):
        next_event = self.last_event + datetime.timedelta(seconds=self.event_interval)
        return next_event < datetime.datetime.now()

    def random_event(self):
        self.last_event = datetime.datetime.now()
        key = random.choice([
            pygame.K_0,"change stock",pygame.K_t,pygame.K_y,pygame.K_g,pygame.K_h,pygame.K_b,pygame.K_s
        ])
        if key == "change stock":
            key = random.choice([pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
            pygame.K_7])
        keyboard_event = pygame.event.Event(pygame.KEYDOWN, {"key": key})
        keyboard_event2 = pygame.event.Event(pygame.KEYUP, {"key": key})
        key_to_gloat_map = {
            pygame.K_0: "Let's sell\nthat!)", # resets pending trade vol to 0
            pygame.K_1: "Let's have a \nlook at this one...",
            pygame.K_2: "Let's have a \nlook at this one...",
            pygame.K_3: "Let's have a \nlook at this one...",
            pygame.K_4: "Let's have a \nlook at this one...",
            pygame.K_5: "Let's have a \nlook at this one...",
            pygame.K_6: "Let's have a \nlook at this one...",
            pygame.K_7: "Let's have a \nlook at this one...",
            pygame.K_t: "Some of this...",
            pygame.K_y: "Some of this...",
            pygame.K_g: "Some of that...",
            pygame.K_h: "Some of that...",
            pygame.K_b: "And buy!\nGod I'm good.",
            pygame.K_s: "And sell!\nCan't believe\nyou bought\nthat.",
        }
        select = random.randint(0,4)
        if self.difficulty < 2: # if not hard - SOFTware
            if select == 0 or select == 1:
                self.select_random_animation()
                self.handle_animation()
            elif select == 2 and self.difficulty != 0: #not easy
                return "STEALMOUSE"
            elif select == 3:
                return self.select_message()
            elif select == 4 and self.difficulty != 0: #not easy
                print(f"posting keyboard event {keyboard_event} for key {key}")
                pygame.event.post(keyboard_event)
                pygame.event.post(keyboard_event2)
                return key_to_gloat_map[key]
        else: # if hard
            if select == 0:
                self.select_random_animation()
                self.handle_animation()
            elif select == 1 or select == 2:
                return "STEALMOUSE"
            elif select == 3:
                return self.select_message()
            elif select == 4:
                print(f"posting keyboard event {keyboard_event} for key {key}")
                pygame.event.post(keyboard_event)
                pygame.event.post(keyboard_event2)
                return key_to_gloat_map[key]

    def select_point(self):
        selection = random.randint(0,5)
        if selection == 0:
            x = random.randint(0,800)
            y = random.randint(0,600)

        elif selection >= 1:
            #more likly to hit buttons
            x = random.randint(400,800)
            y = random.randint(0,400)
        return x,y