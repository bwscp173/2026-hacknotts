import pygame


class Button:
    def __init__(self, x, y, width, height, text, call_on_click):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.call_on_click = call_on_click
        font = pygame.font.Font("fonts/IBMPlexMono-Regular.ttf", 16)
        self.text = font.render(text, True, (200, 200, 200))

    def draw(self, screen, mouse, is_left_clicking: bool):
        if (
            self.x <= mouse[0] <= self.x + self.width
            and self.y <= mouse[1] <= self.y + self.height
        ):
            if is_left_clicking:
                pygame.draw.rect(
                    screen, (0, 0, 255), [self.x, self.y, self.width, self.height],
                    border_radius=5
                )
                self.call_on_click()
            else:
                pygame.draw.rect(
                    screen, (255, 0, 0), [self.x, self.y, self.width, self.height],
                    border_radius=5
                )

        else:
            pygame.draw.rect(
                screen, (0, 0, 255), [self.x, self.y, self.width, self.height],
                    border_radius=5
            )

        screen.blit(self.text, (self.x + 10, self.y + self.height // 4))
