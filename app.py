import types
from typing import Any
import pygame
from pygame.display import flip
import math
import random
import os  # Import the os module to list files in a directory
import sys
import platform


# Tuple representing width and height in pixels
screen_size = (1024, 768)
game_state = "start_menu"
window_width = 1024
window_height = 768


bullet_hitbox_fix = 0
vangvogel_fix_X = 0
vangvogel_fix_Y = 0
text_height_fix_x = 0
text_height_fix_y = 0
text_height_fix_x_2 = 0
text_height_fix_y_2 = 0
enemy_outside_screen_fix_X = 0

# Darwin
if platform.system() == "Darwin":
    bullet_hitbox_fix = 52
    vangvogel_fix_X = 52
    vangvogel_fix_Y = 29
    text_height_fix_x = 30
    text_height_fix_y = 10
    text_height_fix_x_2 = 7
    text_height_fix_y_2 = 12
    enemy_outside_screen_fix_X = 15

# CLASSES


class HighScoreCounter:
    def __init__(self):
        self.filePath = "highScore.txt"
        self.read_high_score()
        self.font = pygame.font.SysFont("Franklin Gothic Medium", 20, bold=True)

    def read_high_score(self):
        with open(self.filePath, "r") as file:
            self.currentHighScore = int(file.readline().rstrip())

    def update(self, new_score):
        if new_score > self.currentHighScore:
            self.currentHighScore = new_score
            with open(self.filePath, "w") as file:
                file.write(str(new_score))

    def render(self, window):
        high_score = str(self.currentHighScore)
        high_score = self.font.render(high_score, 1, pygame.Color("BLACK"))
        window.blit(high_score, (120, 7))


class Health:
    def __init__(self):
        self.health = 5
        self.hearth = pygame.transform.scale(
            pygame.image.load("assets/images/hearth.png"),
            (30, 30),
        )
        self.hearth_empty = pygame.transform.scale(
            pygame.image.load("assets/images/hearth_empty.png"),
            (30, 30),
        )
        self.positionX1 = 970
        self.positionX2 = 930
        self.positionX3 = 890
        self.positionX4 = 850
        self.positionX5 = 810

    def decrease_health(self):
        self.health -= 1
        print(self.health)

    def render(self, window):
        if self.health == 5:
            window.blit(self.hearth, (self.positionX1, 10))
            window.blit(self.hearth, (self.positionX2, 10))
            window.blit(self.hearth, (self.positionX3, 10))
            window.blit(self.hearth, (self.positionX4, 10))
            window.blit(self.hearth, (self.positionX5, 10))

        if self.health == 4:
            window.blit(self.hearth_empty, (self.positionX1, 10))
            window.blit(self.hearth, (self.positionX2, 10))
            window.blit(self.hearth, (self.positionX3, 10))
            window.blit(self.hearth, (self.positionX4, 10))
            window.blit(self.hearth, (self.positionX5, 10))

        if self.health == 3:
            window.blit(self.hearth_empty, (self.positionX1, 10))
            window.blit(self.hearth_empty, (self.positionX2, 10))
            window.blit(self.hearth, (self.positionX3, 10))
            window.blit(self.hearth, (self.positionX4, 10))
            window.blit(self.hearth, (self.positionX5, 10))

        if self.health == 2:
            window.blit(self.hearth_empty, (self.positionX1, 10))
            window.blit(self.hearth_empty, (self.positionX2, 10))
            window.blit(self.hearth_empty, (self.positionX3, 10))
            window.blit(self.hearth, (self.positionX4, 10))
            window.blit(self.hearth, (self.positionX5, 10))

        if self.health == 1:
            window.blit(self.hearth_empty, (self.positionX1, 10))
            window.blit(self.hearth_empty, (self.positionX2, 10))
            window.blit(self.hearth_empty, (self.positionX3, 10))
            window.blit(self.hearth_empty, (self.positionX4, 10))
            window.blit(self.hearth, (self.positionX5, 10))


class GameInfo:
    def __init__(self):
        self.font = pygame.font.SysFont("Franklin Gothic Medium", 40, bold=True)
        self.render_text = False
        self.timer = 0
        self.text_position = (359, 0)  # Position of the text
        self.lock_timer = False
        self.color = (247, 233, 173)

    def render(self, window, clock):
        if not self.lock_timer:
            if self.render_text:
                waveText = "Wave completed!"
                waveText_surface = self.font.render(waveText, 1, pygame.Color("BLACK"))
                window.blit(waveText_surface, self.text_position)

                # Get the time since last frame in seconds
                self.timer += clock.get_time() / 1000
                if self.timer > 2:
                    self.render_text = False  # Disable text rendering after 2 seconds
                    self.timer = 0  # Reset the timer
                    # Clear the area where the text was rendered
                    window.fill(
                        (0, 0, 0),
                        (
                            self.text_position[0],
                            self.text_position[1],
                            waveText_surface.get_width(),
                            waveText_surface.get_height(),
                        ),
                    )
                    self.lock_timer = True


class BorderHitbox:
    def __init__(self, health):
        self.location = (1024, 786)
        self.boundingBox = pygame.Rect(0, 828, 1024, 1)
        self.health = health

    def check_collision(self, enemy_manager):
        for enemy in enemy_manager.enemies:
            if self.boundingBox.colliderect(enemy.bounding_box):
                self.health.decrease_health()

                enemy_manager.enemies.remove(enemy)

    def render_bounding_box(self, window):
        pygame.draw.rect(window, (255, 0, 0), self.boundingBox, 1)


# CLASS FOR GAME OVER SCREEN
class GameOver:
    def __init__(self) -> None:
        self.game_over_screen = pygame.transform.scale(
            pygame.image.load("assets/images/backgrounds/background_game_over.jpg"),
            (window_width, window_height),
        )
        self.font = pygame.font.SysFont("Franklin Gothic Medium", 36, True)
        self.button_rect = pygame.Rect(362, 323, 300, 50)
        self.button_text = self.font.render("Return to menu", True, (109, 136, 245))
        self.button_text = self.font.render("Return to menu", True, (109, 136, 245))

    def render(self, window):
        window.blit(self.game_over_screen, (0, 0))
        pygame.draw.rect(window, (247, 233, 173), self.button_rect, 0, 10)
        window.blit(
            self.button_text,
            (
                self.button_rect.x + 25 + text_height_fix_x,
                self.button_rect.y + 2 + text_height_fix_y,
            ),
        )

    def check_click(self, x, y):
        return self.button_rect.collidepoint(x, y)


# CLASS FOR START MENU
class StartMenu:
    def __init__(self):
        self.font = pygame.font.SysFont("Franklin Gothic Medium", 36, True)
        self.button_rect = pygame.Rect(412, 323, 200, 50)
        self.button_text = self.font.render("Start", True, (109, 136, 245))
        self.background = pygame.transform.scale(
            pygame.image.load("assets/images/backgrounds/background_menu.png"),
            (window_width, window_height),
        )

    def render(self, window):
        window.blit(self.background, (0, 0))
        pygame.draw.rect(window, (247, 233, 173), self.button_rect, 0, 10)
        window.blit(
            self.button_text,
            (
                self.button_rect.x + 65 + text_height_fix_x_2,
                self.button_rect.y + 2 + text_height_fix_y_2,
            ),
        )

    def check_click(self, x, y):
        return self.button_rect.collidepoint(x, y)


# CLASS FOR SOUNDS
class Sounds:
    def __init__(self):
        self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosions/turkey.mp3")

    def play(self):
        pygame.mixer.Sound.play(self.explosion_sound)


class FPS_Counter:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 18, bold=True)

    def render(self, window, clock):
        fps = "FPS: " + str(int(clock.get_fps()))
        fps_surface = self.font.render(fps, 1, pygame.Color("BLACK"))
        window.blit(fps_surface, (2, 745))


# CLASS FOR KILCOUNTER
class KillCounter:
    def __init__(self):
        self.count = 0
        self.font = pygame.font.SysFont("Franklin Gothic Medium", 22, True)
        self.icons = pygame.transform.scale(
            pygame.image.load("assets/images/GUI.png"),
            (11 * 10, 3 * 10),
        )

    def update(self):
        self.count += 1

    def render(self, window):
        kills_surface = self.font.render(str(self.count), 1, pygame.Color("BLACK"))
        window.blit(kills_surface, (40, 5))
        window.blit(self.icons, (2, 2))


# CLASS FOR COOLDOWN
class Cooldown:
    def __init__(self, time_between_shots):
        self.time_between_shots = time_between_shots
        self.elapsed_time = 0

    def update(self, elapsed_seconds):
        self.elapsed_time += elapsed_seconds

    @property
    def ready(self):
        return self.elapsed_time >= self.time_between_shots

    def reset(self):
        self.elapsed_time = 0


# CLASS FOR EXPLOSION
class Explosion:
    def __init__(self):
        self.__explosion_frames = []
        self.frame_index = 0
        self.__load_explosion_frames()
        self.position = (-100, -100)  # Initial position off-screen
        self.visible = False
        self.__animation_duration = 0.3
        self.__time_left = self.__animation_duration  # Set the initial time

    def __load_explosion_frames(self):
        explosion_path = "assets/images/sprites/explosion/"
        # Get a list of all files in the explosion path
        explosion_files = os.listdir(explosion_path)
        # Sort the files to ensure the correct order
        explosion_files.sort()

        for filename in explosion_files:
            frame = pygame.transform.scale(
                pygame.image.load(os.path.join(explosion_path, filename)),
                (80, 80),
            )
            self.__explosion_frames.append(frame)

    def render(self, window):
        if self.visible:
            window.blit(self.__explosion_frames[self.frame_index], self.position)

    def explode_at(self, x, y):
        self.position = (x, y)
        self.visible = True
        self.frame_index = 0
        self.__time_left = (
            self.__animation_duration
        )  # Reset the time when a new explosion occurs

    def update(self, elapsed_seconds):
        # Update the frame index based on elapsed time and animation duration
        time_per_frame = self.__animation_duration / len(self.__explosion_frames)
        time_per_frame = self.__animation_duration / len(self.__explosion_frames)
        frames_elapsed = int(
            (self.__animation_duration - self.__time_left) / time_per_frame
        )
        self.frame_index = min(frames_elapsed, len(self.__explosion_frames) - 1)
        self.frame_index = min(frames_elapsed, len(self.__explosion_frames) - 1)

        # Subtract elapsed time from the remaining time
        self.__time_left -= elapsed_seconds
        # Set visibility to False when time is up
        self.visible = self.__time_left > 0

    @property
    def disposed(self):
        return not self.visible


# CLASS FOR BULLETS
class Bullets:
    def __init__(self, positionX, positionY):
        self.__bullet = pygame.transform.scale(
            pygame.image.load("assets/images/sprites/bullets/spek.png"),
            (15, 35.25),
        )
        self.positionX = positionX + bullet_hitbox_fix
        self.positionY = positionY
        self.__speed = 200
        self.__time_left = 5
        self.bounding_box = pygame.Rect(self.positionX, self.positionY, 15, 35.25)
        self.bounding_box = pygame.Rect(self.positionX, self.positionY, 15, 35.25)

    def update(self, elapsed_seconds):
        self.positionY -= self.__speed * elapsed_seconds
        self.__time_left -= elapsed_seconds
        self.bounding_box.x = self.positionX + 36.5
        self.bounding_box.y = self.positionY

    def render(self, window):
        window.blit(self.__bullet, (self.positionX + 36.5, self.positionY))
        # pygame.draw.rect(window, (250, 0, 0), self.bounding_box, 2)

    @property
    def disposed(self):
        return self.__time_left <= 0


# CLASS FOR BACKGROUND
class Background:
    def __init__(self):
        self.__image = self.__create_image()
        self.__y = -768
        self.__h = 1536

    def __create_image(self):
        background = pygame.image.load("assets/images/backgrounds/background.png")
        background = pygame.image.load("assets/images/backgrounds/background.png")

        return background

    def render(self, window):
        window.blit(self.__image, (0, self.__y))
        window.blit(self.__image, (0, self.__y - self.__h))

    def update(self, elapsed_seconds, speed):
        # Move the background down
        self.__y += speed * elapsed_seconds

        if self.__y >= self.__h:
            self.__y -= self.__h


# CLASS THAT MANAGES AL THE SPAWNED KALKOENEN
class EnemyManager:
    def __init__(self, screen_width, screen_height, kill_counter):
        self.enemies = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spawn_cooldown = Cooldown(random.uniform(1.0, 3.0))
        self.kill_counter = kill_counter

    def spawn_enemy(self, enemy_sprite):
        if self.spawn_cooldown.ready:
            x = random.randint(0, self.screen_width - 60 - enemy_outside_screen_fix_X)
            y = random.randint(-60, -60)
            new_enemy = Enemy(
                x, y, self, self.kill_counter, enemy_sprite
            )  # Pass the kill_counter
            self.enemies.append(new_enemy)
            self.spawn_cooldown.reset()
            self.spawn_cooldown.time_between_shots = random.uniform(1, 3)

    def update(self, elapsed_seconds):
        self.spawn_cooldown.update(elapsed_seconds)
        for enemy in self.enemies:
            enemy.update(elapsed_seconds)

    def render(self, window):
        for enemy in self.enemies:
            enemy.render(window)


# CLASS FOR KALKOEN
class Enemy:
    def __init__(self, initial_x, initial_y, enemy_manager, kill_counter, sprite_path):
        self.sprite_path = sprite_path
        self.enemy = pygame.transform.scale(
            pygame.image.load(self.sprite_path),
            (60, 60),
        )
        self.__x = initial_x
        self.__y = initial_y
        self.bounding_box = pygame.Rect(self.__x, self.__y, 60, 60)
        self.__time_left = 15
        self.enemy_manager = enemy_manager  # Pass the manager reference
        self.kill_counter = kill_counter
        self.explosion_sound = Sounds()

    def update(self, elapsed_seconds):
        self.__y += 1.5
        # Update bounding box position
        self.bounding_box.x = self.__x
        self.bounding_box.y = self.__y
        self.__time_left -= elapsed_seconds

    def render(self, window):
        window.blit(self.enemy, (self.__x, self.__y))
        # pygame.draw.rect(window, (250, 0, 0), self.bounding_box, 2)

    @property
    def disposed(self):
        return self.__time_left <= 0

    def check_collisions(self, bullets, explosion):
        for bullet in bullets:
            if bullet.bounding_box.colliderect(self.bounding_box):
                self.kill_counter.update()  # Update the kill counter
                self.enemy_manager.enemies.remove(self)
                bullets.remove(bullet)
                explosion.explode_at(self.__x, self.__y)
                self.explosion_sound.play()


# CLASS FOR VANGVOGEL PLAYER
class Vangvogel:
    def __init__(self, state, kill_counter, window):
        self.load_images()  # Load all frames for the animation
        self.animation_speed = 0.2  # Set the animation speed
        self.animation_timer = 0
        self.animation_frame = 0
        self.state = state
        self.speed = 500
        self.bounding_box = pygame.Rect(
            self.state.positionX, self.state.positionY, 86, 76
        )
        self.kill_counter = kill_counter
        self.highScoreCounter = HighScoreCounter()
        self.health = state.health
        self.window = window

    def load_images(self):
        self.animation_frames = []
        base_path = "assets/images/sprites/"
        for i in range(
            1, 3
        ):  # Assuming you have vangvogelpixel1.png and vangvogelpixel2.png
            image_path = os.path.join(base_path, f"vangvogel{i}.png")
            image = pygame.transform.scale(pygame.image.load(image_path), (86, 76))
            self.animation_frames.append(image)

    @property
    def position(self):
        return (self.state.positionX, self.state.positionY)

    def update_position(self, dx, dy):
        # Ensure Vangvogel stays within screen boundaries
        new_x = max(
            0,
            min(
                self.state.positionX + dx,
                screen_size[0] - self.animation_frames[0].get_width(),
            ),
        )
        new_y = max(
            0,
            min(
                self.state.positionY + dy,
                screen_size[1] - self.animation_frames[0].get_height(),
            ),
        )

        self.state.positionX = new_x
        self.state.positionY = new_y
        # Update bounding box position
        self.bounding_box.x = self.position[0] + vangvogel_fix_X
        self.bounding_box.y = self.position[1] + vangvogel_fix_Y

    def render(self, window):
        # DRAWS VANGVOGEL
        current_frame = self.animation_frames[self.animation_frame]
        window.blit(current_frame, self.position)
        # pygame.draw.rect(window, (250, 0, 0), self.bounding_box, 2)
        self.highScoreCounter.render(window)

        # Update the animation frame based on elapsed time
        self.animation_timer += self.state.clock.get_time() / 1000.0
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(
                self.animation_frames
            )

    def check_collision(self, enemy_manager):
        for enemy in enemy_manager.enemies:
            if self.bounding_box.colliderect(enemy.bounding_box):
                if not self.colliding:
                    self.colliding = True
                    self.health.decrease_health()

                # Play explosion sound at the enemy's position
                explosion_sound = Sounds()
                explosion_sound.play()

                # Create an explosion at the enemy's position
                self.state.explosion.explode_at(
                    enemy.bounding_box.x, enemy.bounding_box.y
                )

                # Remove the defeated enemy from the manager
                enemy_manager.enemies.remove(enemy)
                self.colliding = False  # Reset colliding flag after enemy removal

            else:
                self.colliding = False

            if self.health.health == 0:
                self.highScoreCounter.update(self.kill_counter.count)
                self.handle_collision()

    def handle_collision(self):
        # Additional logic to handle collision
        # For example, reset some game state variables, play sound effects, etc.

        # Set the game state to "start_menu"
        global game_state
        game_state = "game_over"

        # Stop the game music
        pygame.mixer.music.stop()
        start_music_game_over()

        # Additional logic to reset game state variables
        # For example, reset the kill counter
        self.state.kill_counter = KillCounter()


class State:
    def __init__(self, window):
        self.positionX = 468
        self.positionY = 650
        self.kill_counter = KillCounter()
        self.health = Health()
        self.enemy_manager = EnemyManager(
            screen_size[0], screen_size[1], self.kill_counter
        )
        self.vangvogel = Vangvogel(self, self.kill_counter, window)
        self.__Background = Background()
        self.enemy = Enemy(
            -100,
            -100,
            self.enemy_manager,
            self.kill_counter,
            "assets/images/sprites/kalkoen.png",
        )
        self.__bullets = []  # List to store bullets
        # Example cooldown time (adjust as needed)
        self.__fire_cooldown = Cooldown(0.5)
        self.FPS_Counter = FPS_Counter()
        self.explosion = Explosion()  # Initialize an instance of Explosion
        self.gameinfo = GameInfo()

        self.borderHitbox = BorderHitbox(self.health)
        self.clock = pygame.time.Clock()  # Add this line to initialize the clock

    def render(self, window, clock):
        self.__Background.render(window)

        self.enemy.render(window)
        for bullet in self.__bullets:
            bullet.render(window)
        self.enemy_manager.render(window)

        self.vangvogel.render(window)
        self.FPS_Counter.render(window, clock)
        self.explosion.render(window)  # Render the explosion
        self.kill_counter.render(window)
        self.borderHitbox.render_bounding_box(window)

        self.clock = clock
        self.window = window
        self.health.render(window)

    def update(self, elapsed_seconds):
        self.__Background.update(elapsed_seconds, 200)
        self.enemy.update(elapsed_seconds)
        self.__fire_cooldown.update(elapsed_seconds)

        # Check if enough time has passed to fire a new bullet
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.__fire_cooldown.ready:
            self.fire_bullet(elapsed_seconds)  # Pass elapsed_seconds here

        # Update existing bullets and remove disposed ones
        updated_bullets = []
        for bullet in self.__bullets:
            bullet.update(elapsed_seconds)
            if not bullet.disposed:
                updated_bullets.append(bullet)

        self.__bullets = updated_bullets

        self.enemy_manager.update(elapsed_seconds)

        self.explosion.update(elapsed_seconds)  # Update the explosion position

        if self.kill_counter.count > 10:
            self.enemy_manager.spawn_enemy("assets/images/sprites/suikerspinwalvis.png")
            self.gameinfo.render_text = True

        elif self.kill_counter.count <= 10:
            self.enemy_manager.spawn_enemy("assets/images/sprites/kalkoen.png")

        if self.kill_counter.count == 10:
            self.gameinfo.render_text = True
            self.gameinfo.render(self.window, self.clock)

    def fire_bullet(self, elapsed_seconds):
        # Add a new bullet to the list
        new_bullet = Bullets(
            self.vangvogel.state.positionX, self.vangvogel.state.positionY
        )
        self.__bullets.append(new_bullet)
        # Reset the cooldown
        self.__fire_cooldown.reset()

        # Update existing bullets and remove disposed ones
        updated_bullets = []
        for bullet in self.__bullets:
            bullet.update(elapsed_seconds)
            if not bullet.disposed:
                updated_bullets.append(bullet)

        self.__bullets = updated_bullets

        self.enemy_manager.update(elapsed_seconds)

        if self.kill_counter.count > 10:
            self.enemy_manager.spawn_enemy("assets/images/sprites/suikerspinwalvis.png")

        elif self.kill_counter.count <= 10:
            self.enemy_manager.spawn_enemy("assets/images/sprites/kalkoen.png")

    @property
    def bullets(self):
        return (
            self.__bullets
        )  # Provide a property to access the bullets outside the class


# FUNCTIONS


# FUNCTION FOR RESSETTING THE GAME
def reset_game(state):
    state.kill_counter = KillCounter()
    state.vangvogel.state.positionX = 468
    state.vangvogel.state.positionY = 650
    state.enemy_manager = EnemyManager(
        screen_size[0], screen_size[1], state.kill_counter
    )
    state.__bullets = []
    state.explosion = Explosion()
    state.health.health = 5


# FUNCTION FOR GAME OVER SCREEN
def start_music_game_over():
    # Initialize the music for the menu
    pygame.mixer.music.load("assets/music/game_over.mp3")
    pygame.mixer.music.play(1)


# FUNCTION FOR MENU
def start_music_menu():
    # Initialize the music for the menu
    pygame.mixer.music.load("assets/music/intro.mp3")
    pygame.mixer.music.play(-1)


# FUNCTION TO START THE GAME
def start_music_game():
    # Initialize the music for the game
    pygame.mixer.music.load("assets/music/1.mp3")
    pygame.mixer.music.play(-1)


# FUNCTION FOR START MENU
def draw_start_menu(window, start_menu):
    clear_surface(window)
    start_menu.render(window)
    pygame.display.flip()


# FUNCTION FOR GAME OVER
def draw_game_over(window, game_over_screen):
    clear_surface(window)
    game_over_screen.render(window)
    pygame.display.flip()


# FUNCTION THAT CHECKS FOR COLLISIONS
def process_collisions(enemy_manager, bullets, state, border, enemy):
    # Check for collisions between Vangvogel and Kalkoen instances
    state.vangvogel.check_collision(enemy_manager)

    for enemy in enemy_manager.enemies:
        enemy.check_collisions(bullets, state.explosion)
        border.check_collision(enemy_manager)


# FUNCTION THAT HANDLES KEY PRESSES


def process_key_input(state, elapsed_seconds, speed):
    keys = pygame.key.get_pressed()
    straight_speed = speed * elapsed_seconds
    diagonal_speed = (speed / math.sqrt(2)) * elapsed_seconds

    # Check for arrow key presses
    move_left = keys[pygame.K_LEFT]
    move_right = keys[pygame.K_RIGHT]
    move_up = keys[pygame.K_UP]
    move_down = keys[pygame.K_DOWN]

    dx = 0
    dy = 0

    # Todo: case van maken?

    # Diagonal movement
    if move_left and move_up:
        dx = -diagonal_speed
        dy = -diagonal_speed
    elif move_left and move_down:
        dx = -diagonal_speed
        dy = diagonal_speed
    elif move_right and move_up:
        dx = diagonal_speed
        dy = -diagonal_speed
    elif move_right and move_down:
        dx = diagonal_speed
        dy = diagonal_speed
    # Straight movement
    elif move_left:
        dx = -straight_speed
    elif move_right:
        dx = straight_speed
    elif move_up:
        dy = -straight_speed
    elif move_down:
        dy = straight_speed

    state.vangvogel.update_position(dx, dy)

    # Check for quit key press
    if keys[pygame.K_ESCAPE]:
        pygame.quit()


# FUNCTION THAT HANDLES EVENTS


def event():
    for event in pygame.event.get():
        # CHECKS IF WINDOW CLOSES
        if event.type == pygame.QUIT:
            pygame.quit()


# FUNCTION THAT CLEARS SCREEN
def clear_surface(window):
    # CLEAR FRAME
    window.fill((0, 0, 0))


# FUNCTION THAT CREATES DISPLAY
def create_main_surface():
    # Create window with given size
    return pygame.display.set_mode(screen_size)


# FUNCTION THAT RENDERS CIRCLES
def render_frame(window, state, elapsed_seconds, speed, clock):
    # CALL RENDER FUNCTION
    state.render(window, clock)

    state.update(elapsed_seconds)

    # CALL COLLISION FUNCTION
    process_collisions(
        state.enemy_manager, state.bullets, state, state.borderHitbox, state.enemy
    )

    # UPDATES FRONT SCREEN
    pygame.display.flip()

    # CALL KEY PRES FUNCTION
    process_key_input(state, elapsed_seconds, speed)

    # CALL EVENT FUNCTION
    event()

    # CLEAR FRAME
    clear_surface(window)


# FUNCTION THAT CREATES MAIN GAME


def main():
    # Initialize Pygame
    pygame.init()

    # INITIALIZE THE MUSIC
    pygame.mixer.init()

    # BOSS FIGHT MUSIC

    # MAIN MENU MUSIC
    start_music_menu()
    # START DISPLAY
    window = create_main_surface()

    # INITIALIZE STATE
    state = State(window)

    # INITIALIZE CLOCK FOR FPS
    clock = pygame.time.Clock()

    # INITIALIZE START MENU
    start_menu = StartMenu()
    in_start_menu = True

    # INITIALIZE GAME OVER MENU
    game_over_screen = GameOver()
    in_game_over_screen = True

    global game_state  # Declare game_state as a global variable

    # INFINTE LOOP TO KEEP CODE RUNNING
    while True:
        if game_state == "start_menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and in_start_menu:
                    x, y = pygame.mouse.get_pos()
                    if start_menu.check_click(x, y):
                        game_state = "playing"
                        in_start_menu = False
                        start_music_game()  # Start playing the game music

            if in_start_menu:
                draw_start_menu(window, start_menu)
        elif game_state == "playing":
            elapsed_seconds = clock.tick() / 1000.0
            render_frame(window, state, elapsed_seconds, state.vangvogel.speed, clock)

        if game_state == "game_over":
            reset_game(state)
            in_game_over_screen = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and in_game_over_screen:
                    x, y = pygame.mouse.get_pos()
                    if game_over_screen.check_click(x, y):
                        game_state = "start_menu"
                        in_game_over_screen = False
                        in_start_menu = True
                        start_music_menu()  # Start playing the game music

            if in_game_over_screen:
                draw_game_over(window, game_over_screen)


# RUNS MAIN
main()
