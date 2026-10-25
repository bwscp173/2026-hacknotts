import pygame
from gui.button import Button
from gui.game import Game
from gui.text_panel import TextPanel


class StartMenu:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.title_font = pygame.font.Font("fonts/IBMPlexMono-Regular.ttf", 48)


        pygame.display.set_caption("Bonzi's Big Bubble")

        self.running = False

        self.difficulties = ["Easy", "Medium", "Hard"]
        self.selected_difficulty = None

        def set_difficulty(difficulty):
            self.selected_difficulty = difficulty
            print(f"Selected difficulty: {difficulty}")
            self.play_game()

        self.to_draw = []
        self.title_box = TextPanel(
            "temp", 100, 100, 600, 100)
        self.title_box.centre_text = True
        self.title_box.font = self.title_font
        self.title_box.change_text("Bonzi's Big Bubble")
        self.to_draw.append(self.title_box)

        for i, difficulty in enumerate(self.difficulties):
            x_pos = 150 + (i * 180)  # Spawns buttons side by side
            y_pos = 400
            button = Button(x_pos, y_pos, 150, 80, str(difficulty), lambda d=difficulty: set_difficulty(d))
            button.centre_text = True
            self.to_draw.append(button)

    def play_game(self):
        print(f"Starting game with difficulty: {self.selected_difficulty}")
        game = Game(self.width, self.height, self.selected_difficulty)
        game.run()


    def run(self):
        self.running = True
        while self.running:
            mouse_pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pressed = True

            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill((30, 30, 30))

            for element in self.to_draw:
                if isinstance(element, Button):
                    element.draw(self.screen, mouse_pos, mouse_pressed)
                elif isinstance(element, TextPanel):
                    element.draw(self.screen)
                else:
                    raise ValueError(f"Unknown element type: {type(element)}")

            pygame.display.flip()

        pygame.quit()
