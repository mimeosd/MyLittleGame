import pygame
import sys
import random
import os
import pygame.sprite
from MainScreen import MainScreen
from LevelSelection import LevelSelectionScreen
from MapScreen import MapScreen

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

background = pygame.image.load("assets/background-1.png")

game_over = False
font = pygame.font.Font(None, 36)

main_screen = MainScreen(screen, screen_width, screen_height)
main_screen.run()

selected_level = main_screen.run()


pygame.mixer.init()
pygame.mixer.music.load("bgmusic.mp3")  
pygame.mixer.music.play(-1)

def spawning_enemies():
    if len(enemy_group) < 1:
        for i in range(3):
            for j in range(10):
                enemy_group.add(Enemy(j * 50, i, 2 ))


class Game:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clock = pygame.time.Clock()

        # Create screens
        self.main_screen = MainScreen(self.screen, self.screen_width, self.screen_height)
        self.level_selection_screen = LevelSelectionScreen(self.screen, self.screen_width, self.screen_height)
        # Add more screens if you need here

        self.current_screen = self.main_screen

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))

            next_screen = self.current_screen.handle_events()

            if next_screen is not None:
                self.current_screen = next_screen

            self.current_screen.update()

            pygame.display.flip()  
            self.clock.tick(60)  


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("assets/antmaker.png")
        self.width = self.original_image.get_width() // 2
        self.height = self.original_image.get_height() // 2
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.x = screen_width // 2
        self.y = screen_height - 50
        self.speed = 5
        self.move_left_flag = False
        self.move_right_flag = False
        self.hit_points = 10

    def update(self):
        if self.move_left_flag:
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
        if self.move_right_flag:
            self.x += self.speed
            if self.x > screen_width:
                self.x = screen_width

    def draw(self):
        screen.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))




class Enemy(Ship):
    def __init__(self, x_pos, row, level):
        super().__init__()
        enemy_images = os.listdir("assets/enemies")
        random_image = random.choice(enemy_images)
        image_path = os.path.join("assets/enemies", random_image)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.y = (row + 1) * 50
        self.x = x_pos
        self.direction = 1
        
        # Will remove this once you fix colliders for bullets and ships
        self.width = 40
        self.height = 40
        self.hit_points = 3 * level
        self.health_bar = HealthBar(self.x, self.y - 10, self.width, 5, self.hit_points)

        

    def update(self):
        super().update()
        self.x += self.direction
        self.health_bar.x = self.x - self.width // 2
        self.health_bar.y = self.y - 10
        if self.x <= 0 or self.x >= screen_width:
            self.direction *= -1

class Bullet:
    def __init__(self, x, y, player_bullet=True):
        self.image = pygame.image.load("assets/bullet.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.speed = 10
        
        # Correct this for coliderect
        self.width = 5
        self.height = 15
        self.player_bullet = player_bullet

        self.shoot_sound = pygame.mixer.Sound("assets/sounds/alienshoot1.wav")
        self.shoot_sound.set_volume(0.5)
        self.shoot_sound.play()

    def move(self):
        self.y -= self.speed

    def draw(self):
        screen.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))


class EnemyBullet(Bullet):
    def __init__(self, x, y, ship, player_bullet=False):
        super().__init__(x, y, player_bullet=player_bullet)

        
        self.flipped_image = pygame.transform.flip(self.image, False, True)

        self.rect = self.flipped_image.get_rect()
        self.x = x
        self.y = y
        self.speed = 10
        self.ship = ship

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.flipped_image, (self.x - self.flipped_image.get_width() // 2, self.y - self.flipped_image.get_height() // 2))


class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health

    def update(self, health):
        self.current_health = health

    def draw(self, screen):
        # Calculate the width of the health bar based on the current health
        health_ratio = self.current_health / self.max_health
        bar_width = int(self.width * health_ratio)

        # Draw the health bar outline
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)

        # Draw the filled portion of the health bar
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, bar_width, self.height))

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((7, 7))
        self.image.fill((255, 255, 255))  # Set the particle color
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity_x = random.uniform(-2, 2)  # Set the initial velocity
        self.velocity_y = random.uniform(-2, 2)
        self.gravity = 0.1

    def update(self):
        self.velocity_y += self.gravity
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        if self.rect.y > screen_height:
            self.kill()


ship = Ship()

ship_group = pygame.sprite.Group()
ship_group.draw(screen)

enemy_group = pygame.sprite.Group()

# Create a health bar for the player
player_health_bar = HealthBar(50, screen_height - 30, 200, 20, ship.hit_points)

bullets = []
enemy_bullet_timer = 0

# Bullet particles Sprite group
particle_group = pygame.sprite.Group()


while not game_over:
    screen.fill((0, 0, 0))  

    screen.blit(background, (0, 0))

    elapsed_time = clock.tick(60)  
    enemy_bullet_timer += elapsed_time


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(ship.x, ship.y)
                bullets.append(bullet)
            elif event.key == pygame.K_LEFT:
                ship.move_left_flag = True
            elif event.key == pygame.K_RIGHT:
                ship.move_right_flag = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                ship.move_left_flag = False
            elif event.key == pygame.K_RIGHT:
                ship.move_right_flag = False

    # Update ship and bullet positions
    ship.update()
    for bullet in bullets:
        bullet.move()
        if bullet.y < 0:
            bullets.remove(bullet)

    # Draw ship and bullets
    ship.draw()

    bullets_to_remove = []  # New list to store bullets to remove

    for bullet in bullets:
        if isinstance(bullet, EnemyBullet):
            if pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height).colliderect(
                pygame.Rect(ship.x, ship.y, ship.width, ship.height)
            ):
                bullets.remove(bullet)
                ship.hit_points -= 1
                if ship.hit_points == 0:
                    game_over = True
        else:
            for enemy in enemy_group:
                if pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height).colliderect(
                    pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                ):
                    bullets.remove(bullet)
                    enemy.hit_points -= 1
                    if enemy.hit_points == 0:
                        enemy.kill()
                        for i in range(10):
                            particle = Particle(enemy.x, enemy.y)
                            particle_group.add(particle)
                        break


    # Remove the bullets outside the loop
    for bullet in bullets_to_remove:
        bullets.remove(bullet)


    for particle in particle_group:
        particle.update()
        screen.blit(particle.image, particle.rect)


    spawning_enemies()

    if enemy_bullet_timer >= 500:
        random_enemy = random.choice(enemy_group.sprites())
        bullet = EnemyBullet(random_enemy.x + random_enemy.width // 2, random_enemy.y + random_enemy.height, ship)

        bullets.append(bullet)
        enemy_bullet_timer = 0


    for bullet in bullets:
        bullet.draw()

    particle_group.update()  # Update the particles
    particle_group.draw(screen)  # Draw the particles
    particle_group.remove(particle_group.sprites())  # Remove particles that are off-screen

    # Drawing enemies and their health bars 
    for enemy in enemy_group :
        enemy.draw()
        enemy.update()
        enemy.health_bar.update(enemy.hit_points)
        enemy.health_bar.draw(screen)
    
    ship_group.draw(screen)
    player_health_bar.update(ship.hit_points)
    player_health_bar.draw(screen)

    
    pygame.display.flip()
    
    clock.tick(60)
    spawning_enemies()
    



while game_over:
    screen.fill((0, 0, 0))

    
    game_over_text = font.render("Game over!", True, (255, 255, 255))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))

    pygame.display.flip()  # Update the display

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
