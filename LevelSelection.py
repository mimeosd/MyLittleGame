import pygame
# NOT IMPLEMENTED PROPERLY


class LevelGameScreen:
    def __init__(self, screen, screen_width, screen_height, level):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

        return self

    def update(self):
        self.screen.fill((0, 0, 0)) 


class LevelSelectionScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.levels = ["Level 1", "Level 2", "Level 3"] 

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, level in enumerate(self.levels):
                    level_rect = self.font.render(level, True, (255, 255, 255)).get_rect(center=(self.screen_width // 2, 200 + i * 50))
                    if level_rect.collidepoint(mouse_pos):
                        return LevelGameScreen(self.screen, self.screen_width, self.screen_height, level)

        return self

    def update(self):
        self.screen.fill((0, 0, 0))

        text = self.font.render("Select a level:", True, (255, 255, 255))
        self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, 100))

        for i, level in enumerate(self.levels):
            level_text = self.font.render(level, True, (255, 255, 255))
            level_rect = level_text.get_rect(center=(self.screen_width // 2, 200 + i * 50))
            self.screen.blit(level_text, level_rect)


class UpgradeScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

        return self

    def update(self):
        self.screen.fill((0, 0, 0))
