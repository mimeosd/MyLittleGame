import pygame
import sys

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class MainScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = pygame.image.load("assets/background-1.png")
        self.title = "Star shooter"
        self.options = ["New Game", "Options"]
        self.selected_option = 0
        self.is_running = False

        # Initialize the font
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

        pygame.mixer.music.load("assets/sounds/Savfk-The Travelling Symphony.mp3")


    def draw_title(self):
        title_text = self.font.render(self.title, True, WHITE, RED)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(title_text, title_rect)


    def draw_options(self):
        # TODO add rectangle over selected options and allow mouse and keyboard choosing
        for i, option in enumerate(self.options):
            option_text = self.font.render(option, True, WHITE)
            option_rect = option_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + i * 50))
            self.screen.blit(option_text, option_rect)

            if option_rect.collidepoint(pygame.mouse.get_pos()):
            # Define the rectangle's position and size based on the option's rect
                rect_width = option_rect.width + 10
                rect_height = option_rect.height + 10
                rect_pos = (option_rect.centerx - rect_width // 2, option_rect.centery - rect_height // 2)
                rect = pygame.Rect(rect_pos, (rect_width, rect_height))
                pygame.draw.rect(self.screen, RED, rect, 2)  # Draw the rectangle with a red border

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    for i in range(len(self.options)):
                        option_rect = self.font.render(self.options[i], True, WHITE).get_rect(center=(self.screen_width // 2, self.screen_height // 2 + i * 50))
                        if option_rect.collidepoint(mouse_pos):
                            if i == 0:  # New Game option
                                self.is_running = True
                            elif i == 1:  # Options option
                                pass

    def run(self):
        pygame.mixer.music.play(-1)
        while not self.is_running:
            self.screen.fill(BLACK)
            self.screen.blit(self.background, (0, 0))

            self.draw_title()
            self.draw_options()

            self.handle_events()

            pygame.display.flip()
