import pygame


class TextPanel:
    def __init__(self, text, x, y, width, height):
        self.x = x
        self.y = y
        self.is_rounded = False
        self.centre_text = False
        self.width = width
        self.height = height
        self.font = pygame.font.Font("fonts/IBMPlexMono-Regular.ttf", 16)
        self.texts = []
        for line in text.split("\n"):
            self.texts.append(self.font.render(line, True, (0, 0, 0)))
        self.colour = (251, 139, 30)

    def draw(self, screen):
        pygame.draw.rect(#
            screen,
            self.colour,
            [self.x, self.y, self.width, self.height],
            border_radius=5 if self.is_rounded else 0
        )

        if self.centre_text:
            total_line_height = len(self.texts) * self.font.get_height()
            start_y = self.y + (self.height - total_line_height) // 2

            for i, line in enumerate(self.texts):
                screen.blit(line, (self.x + (self.width - line.get_width()) // 2, start_y + i * self.font.get_height()))
        else:
            for i, line in enumerate(self.texts):
                screen.blit(line, (self.x + 10, 8 + self.y + i * 20))

    def change_text(self, new_text):
        self.texts = []
        for line in new_text.split("\n"):
            self.texts.append(self.font.render(line, True, (0,0,0)))
