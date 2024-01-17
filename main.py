import asyncio
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomberman Game")

# Set the background color to dark green
BACKGROUND_COLOR = (0, 100, 0)

# Load game assets (graphics, sounds, music)
player_image = pygame.image.load("player.png")
enemy_image = pygame.image.load("enemy.png")
wall_image = pygame.image.load("wall.png")
bomb_image = pygame.image.load("bomb.png")

# Load menu music
menu_music = pygame.mixer.Sound("menu_music.mp3")  # Replace with your menu music file's path

# Load and play background music
background_music = pygame.mixer.Sound("background_music.mp3")
background_music.play(-1)  # Loop the background music indefinitely

# Load explosion sound
explosion_sound = pygame.mixer.Sound("explosion.wav")  # Replace with your sound file's path

# Load explosion images
explosion_images = [pygame.image.load("explosion_frame1.png"),
                   pygame.image.load("explosion_frame2.png"),
                   pygame.image.load("explosion_frame3.png")]

# Define the sizes of each explosion frame
explosion_frame_sizes = [(32, 32), (48, 48), (64, 64)]  # Adjust the sizes as needed

# Initialize the explosion frame index
explosion_frame_index = 0
explosion_start_time = 0

# Define game entities (player, enemies, walls, bombs, power-ups)
player = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
enemies = []
walls = []
bombs = []
explosion_sound_playing = False  # Flag for explosion sound

# Game variables
score = 0
game_over = False
PLAYER_SPEED = .2  # Reduced player speed
ENEMY_SPEED = 1  # Enemy speed adjusted
explosion_radius = 50
ghost_speed = 1  # Adjust ghost speed

# Bomb variables
BOMB_TIMER = 3000
bomb_timer = BOMB_TIMER
BOMB_COOLDOWN = 1000
can_drop_bomb = True

# Define a font for UI text
font = pygame.font.Font(None, 36)

# Define enemy movement directions (up, down, left, right)
enemy_directions = [(0, -ENEMY_SPEED), (0, ENEMY_SPEED), (-ENEMY_SPEED, 0), (ENEMY_SPEED, 0)]
retry_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 40)
menu_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 40)

# Define a variable for the player's bombs
player_bombs = []

# Create a function to generate non-overlapping walls
def generate_non_overlapping_walls(count):
    walls.clear()
    attempts = 0
    while len(walls) < count and attempts < count * 10:  # Limit attempts to prevent infinite loop
        wall = pygame.Rect(random.randint(0, WIDTH - wall_image.get_width()),
                           random.randint(0, HEIGHT - wall_image.get_height()),
                           wall_image.get_width(),
                           wall_image.get_height())
        # Check if the new wall overlaps with any existing wall
        if not any(wall.colliderect(existing_wall) for existing_wall in walls):
            walls.append(wall)
        attempts += 1

# Function to update bomb timers and handle explosions
def update_bombs():
    global player_bombs, explosion_radius, explosion_sound, explosion_sound_playing

    for bomb in player_bombs:
        # Decrease the bomb timer
        bomb_timer = pygame.time.get_ticks() - bomb['placed_time']
        if bomb_timer >= BOMB_TIMER:
            # Explosion time! Remove the bomb and create an explosion
            player_bombs.remove(bomb)
            explode(bomb['rect'].center)

# Function to create an explosion
def explode(center):
    global enemies, score, explosion_radius, explosion_sound, explosion_sound_playing

    # Play the explosion sound
    if not explosion_sound_playing:
        explosion_sound.play()
        explosion_sound_playing = True

    for enemy in enemies[:]:
        if pygame.Rect(enemy).colliderect(center[0] - explosion_radius, center[1] - explosion_radius,
                                      explosion_radius * 2, explosion_radius * 2):
            enemies.remove(enemy)
            score += 1

# Function to create a new game level with increased difficulty
def create_level(level):
    global player, enemies, walls, ghost_speed
    walls.clear()
    generate_non_overlapping_walls(20 + level * 5)

    enemies.clear()
    for _ in range(level * 2):
        enemy = pygame.Rect(random.randint(0, WIDTH - enemy_image.get_width()),
                            random.randint(0, HEIGHT - enemy_image.get_height()),
                            enemy_image.get_width(),
                            enemy_image.get_height())
        # Ensure enemies don't overlap with walls
        while any(wall.colliderect(enemy) for wall in walls):
            enemy.x = random.randint(0, WIDTH - enemy_image.get_width())
            enemy.y = random.randint(0, HEIGHT - enemy_image.get_height())
        enemies.append(enemy)

    ghost_speed = 1 + level * 0.25

    player.x = WIDTH // 2 - player.width // 2
    player.y = HEIGHT // 2 - player.height // 2
    # Ensure the player doesn't overlap with walls or enemies
    while any(player.colliderect(wall) for wall in walls) or any(player.colliderect(enemy) for enemy in enemies):
        player.x = random.randint(0, WIDTH - player.width)
        player.y = random.randint(0, HEIGHT - player.height)

class Menu:
    def __init__(self):
        self.option_visible = False
        self.esc_cooldown = 0  # Initialize the cooldown timer
        self.items = ["Start Game", "Options", "Credits", "Quit Game"]
        self.selected_item = 0
        self.font = pygame.font.Font(None, 36)
        self.visible = True
        # Load your menu background image
        self.background_image = pygame.image.load("menu_background.jpg")
        # Resize the background image to match the game window size
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

        self.bright_green = (100, 255, 0)  # Define bright green color

        self.menu_music_playing = False
        self.background_music_playing = False
        self.music_on = True  # Added option for music on/off
        self.hard_difficulty = False  # Added option for difficulty
        self.player_skin = "player.png"  # Added option for player skin
        self.default_skin_image = pygame.image.load("player.png")
        self.alternate_skin_image = pygame.image.load("alternate_player.png")
        self.alternate_skin = False  # Track the current skin state

    def draw(self, screen):
        if self.visible:
            screen.blit(self.background_image, (0, 0))  # Draw the menu background image
            for i, item in enumerate(self.items):
                text = self.font.render(item, True, self.bright_green if i == self.selected_item else (100, 100, 100))
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - len(self.items) * 20 + i * 40))

    def handle_event(self, event):
        if self.visible:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.items)
                elif event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.items)
                elif event.key == pygame.K_RETURN:
                    self.select_item()

    def select_item(self):
        if self.selected_item == 0:
            self.start_game()
        elif self.selected_item == 1:
            self.show_options()  # Show options screen
        elif self.selected_item == 2:
            self.show_credits()  # Show credits screen
        elif self.selected_item == 3:
            pygame.quit()
            sys.exit

    def start_game(self):
        self.visible = False
        self.stop_menu_music()
        self.play_background_music()
        resume_game()

    def play_menu_music(self):
        if not self.menu_music_playing:
            pygame.mixer.stop()  # Stop all music (including background music)
            menu_music.play(-1)
            self.menu_music_playing = True

    def stop_menu_music(self):
        pygame.mixer.stop()  # Stop menu music

    def play_background_music(self):
        if not self.background_music_playing:
            background_music.play(-1)  # Play background music
            self.background_music_playing = True

    def show_credits(self):
        self.visible = False  # Hide the menu
        credits_text = "Created by Chang through the use of ChatGPT"

        # Display the credits for 6 seconds
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 6000:  # 6 seconds
            screen.fill(BACKGROUND_COLOR)
            credits = self.font.render(credits_text, True, (255, 255, 255))
            screen.blit(credits, (WIDTH // 2 - credits.get_width() // 2, HEIGHT // 2 - credits.get_height() // 2))
            pygame.display.flip()

        self.visible = True  # Return to the menu

    def toggle_skin(self):
        self.alternate_skin = not self.alternate_skin  # Toggle the skin state in option

    def toggle_music(self):
        self.music_on = not self.music_on
        if self.music_on:
            background_music.play(-1)
        else:
            pygame.mixer.stop()

    def toggle_difficulty(self):
        self.hard_difficulty = not self.hard_difficulty

    def show_options(self):
        self.option_visible = True  # Show the Options menu
        option_items = ["[Music]", "[Difficulty]", "[Skin]"]
        option_selected_item = 0

        while self.option_visible:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        option_selected_item = (option_selected_item + 1) % len(option_items)
                    elif event.key == pygame.K_UP:
                        option_selected_item = (option_selected_item - 1) % len(option_items)
                    elif event.key == pygame.K_RETURN:
                        if option_selected_item == 0:
                            self.toggle_music()
                        elif option_selected_item == 1:
                            self.toggle_difficulty()
                        elif option_selected_item == 2:
                            self.toggle_skin()  # Add this line to toggle the skin
                    elif event.key == pygame.K_ESCAPE:
                        self.option_visible = False  # Hide the Options menu

            screen.fill(BACKGROUND_COLOR)

            # Display "ESC" text in the upper left corner
            esc_text = self.font.render("ESC", True, (255, 255, 255))
            screen.blit(esc_text, (10, 10))

            for i, item in enumerate(option_items):
                text = self.font.render(f"{item}", True,
                                        (255, 255, 255) if i == option_selected_item else (100, 100, 100))
                screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - len(option_items) * 20 + i * 40))

            # Display the current settings next to the options
            music_text = self.font.render("Music On" if self.music_on else "Music Off", True,
                                          (255, 255, 255) if self.music_on else (255, 255, 255))
            screen.blit(music_text, (WIDTH // 2 + 10, HEIGHT // 2 - len(option_items) * 20))
            difficulty_text = self.font.render("Hard Difficulty" if self.hard_difficulty else "Normal Difficulty", True,
                                               (255, 255, 255) if self.hard_difficulty else (255, 255, 255))
            screen.blit(difficulty_text, (WIDTH // 2 + 10, HEIGHT // 2 - len(option_items) * 20 + 40))

            # Display the "Change Skin" checkbox and player image
            change_skin_text = self.font.render("", True,
                                                (255, 255, 255) if option_selected_item == 2 else (100, 100, 100))
            screen.blit(change_skin_text, (WIDTH // 2 - 150, HEIGHT // 2 - len(option_items) * 20 + 80))

            # Display the player skin image based on the current skin state
            if (self.alternate_skin):
                player_skin_image = self.alternate_skin_image
            else:
                player_skin_image = self.default_skin_image
            screen.blit(player_skin_image, (WIDTH // 2 + 20, HEIGHT // 2 - len(option_items) * 20 + 80))

            pygame.display.flip()
def resume_game():
    global game_over
    game_over = False

# Add a new state variable to manage game states
game_state = "menu"

# MAIN GAME LOOP
menu = Menu()
current_level = 1
in_menu = True
game_started = False
game_elements_visible = False
current_level = 1
can_drop_bomb = True
last_frame_time = pygame.time.get_ticks()

# Initialize player position and fractional parts of movement
player_x = 50.0
player_y = 50.0
player_fractional_x = 0.0
player_fractional_y = 0.0

retry_selected = True  # Track which button is selected initially

# MAIN GAME # MAIN GAME# MAIN GAME # MAIN GAME# MAIN GAME # MAIN GAME# MAIN GAME # MAIN GAME
# MAIN GAME # MAIN GAME # MAIN GAME # MAIN GAME # MAIN GAME # MAIN GAME # MAIN GAME # MAIN GAME
# MAKE SURE pygame.display.update() and update_bombs() is in while loop
# Main game loop
while True:
    # DONT REMOVE THIS OR ELSE GREEN SCREEN
    pygame.display.update()
    update_bombs()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.USEREVENT and not can_drop_bomb:
            can_drop_bomb = True  # Reset can_drop_bomb to True after BOMB_COOLDOWN

    for i, enemy in enumerate(enemies):
        # Update each enemy's movement direction independently
        enemy_direction = random.choice(enemy_directions)
        enemies[i] = pygame.Rect(enemy.left + enemy_direction[0] * ENEMY_SPEED,
                                 enemy.top + enemy_direction[1] * ENEMY_SPEED,
                                 enemy.width,
                                 enemy.height)

        if pygame.Rect(int(player_x), int(player_y), player_image.get_width(), player_image.get_height()).colliderect(
                enemy):
            game_over = True

    if in_menu:
        menu.handle_event(event)
        menu.play_menu_music()
        screen.fill(BACKGROUND_COLOR)
        menu.draw(screen)


        if menu.selected_item == 0 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_started = True
            menu.stop_menu_music()
            in_menu = False
            game_elements_visible = True
            current_level = 1
            create_level(current_level)
            background_music.play(-1)  # Background music starts when the game begins

        pygame.display.flip()
        pygame.time.delay(100)

    if game_elements_visible and not game_over:
        screen.fill(BACKGROUND_COLOR)

        for wall in walls:
            screen.blit(wall_image, (wall.x, wall.y))
        for enemy in enemies:
            screen.blit(enemy_image, (enemy.x, enemy.y))
        screen.blit(player_image, (int(player_x), int(player_y)))

        keys = pygame.key.get_pressed()

        # Initialize movement values
        move_x = 0.0
        move_y = 0.0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y = PLAYER_SPEED

        # Update player position
        player_fractional_x += move_x
        player_fractional_y += move_y

        # Translate fractional parts into full steps
        steps_x = int(player_fractional_x)
        steps_y = int(player_fractional_y)

        # Update the player position with integer part
        player_x += steps_x
        player_y += steps_y

        # Update fractional parts with remaining fractional parts
        player_fractional_x -= steps_x
        player_fractional_y -= steps_y

        # Ensure the player stays within the game window
        player_x = max(0.0, min(player_x, float(WIDTH) - float(player_image.get_width())))
        player_y = max(0.0, min(player_y, float(HEIGHT) - float(player_image.get_height())))

        for wall in walls:
            if pygame.Rect(int(player_x), int(player_y), player_image.get_width(), player_image.get_height()).colliderect(
            wall):
                # Adjust the player's position if there is a collision with a wall
                if steps_x > 0:
                    player_x = float(wall.left - player_image.get_width())
                elif steps_x < 0:
                    player_x = float(wall.right)
                if steps_y > 0:
                    player_y = float(wall.top - player_image.get_height())
                elif steps_y < 0:
                    player_y = float(wall.bottom)

        for enemy in enemies:
            enemy_direction = random.choice(enemy_directions)
        enemy.x += enemy_direction[0] * ENEMY_SPEED
        enemy.y += enemy_direction[1] * ENEMY_SPEED
        if pygame.Rect(int(player_x), int(player_y), player_image.get_width(), player_image.get_height()).colliderect(
                enemy):
            game_over = True

        # Check for player input (bomb drop)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and can_drop_bomb:
            bomb = {
                'rect': pygame.Rect(int(player_x), int(player_y), bomb_image.get_width(), bomb_image.get_height()),
                'placed_time': pygame.time.get_ticks()
            }
            player_bombs.append(bomb)
            can_drop_bomb = False  # Set to False when a bomb is placed
            pygame.time.set_timer(pygame.USEREVENT, BOMB_COOLDOWN)  # Set a timer to reset can_drop_bomb

        # Define the sizes of each explosion frame
        explosion_frame_sizes = [(32, 32), (48, 48), (64, 64)]  # Adjust the sizes as needed

        # Initialize the explosion frame index
        explosion_frame_index = 0

        # Inside your game loop:

        for bomb in player_bombs:
            bomb_timer = pygame.time.get_ticks() - bomb['placed_time']

            # Handle bomb explosion
            if bomb_timer >= BOMB_TIMER:
                player_bombs.remove(bomb)
                explosion_sound.play()  # Play the explosion sound
                # Remove enemies near the exploded bomb
                enemies = [enemy for enemy in enemies if
                           pygame.math.Vector2(enemy.center).distance_to(bomb['rect'].center) > explosion_radius]

            if bomb_timer < BOMB_TIMER - 500:  # Show the bomb image until the explosion animation starts
                screen.blit(bomb_image, (bomb['rect'].x, bomb['rect'].y))
            else:
                # Handle bomb explosion animation
                elapsed_time = pygame.time.get_ticks() - bomb['placed_time'] - (BOMB_TIMER - 500)

                if elapsed_time >= 0:
                    explosion_frame_index = min(2,
                                                int(elapsed_time / 500))  # Switch between frames every 500 milliseconds
                    explosion_frame_size = explosion_frame_sizes[explosion_frame_index]
                    explosion_frame = pygame.transform.scale(explosion_images[explosion_frame_index],
                                                             explosion_frame_size)
                    screen.blit(explosion_frame, (bomb['rect'].x, bomb['rect'].y))

        # Allow the player to set a new bomb if they have no bombs
        if not player_bombs:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                bomb = player.copy()
                bomb_timer = BOMB_TIMER
                player_bombs.append({'rect': bomb, 'placed_time': pygame.time.get_ticks()})

        if not enemies:
            # Create a new level
            current_level += 1
            create_level(current_level)
    # Ensure the game continues running if the game hasn't been quit
    if pygame.display.get_init():
        pygame.display.update()
    else:
        break

    if game_over and not menu.visible:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

        final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))

        retry_color = (0, 255, 0) if retry_selected else (255, 255, 255)
        menu_color = (0, 255, 0) if not retry_selected else (255, 255, 255)

        retry_text = font.render("Retry", True, retry_color)
        menu_text = font.render("Menu", True, menu_color)

        screen.blit(retry_text, (WIDTH // 2 - 100, HEIGHT // 2 + 70))
        screen.blit(menu_text, (WIDTH // 2 - 100, HEIGHT // 2 + 110))

        pygame.display.flip()
        pygame.time.delay(100)


        # Check for user input on the "Game Over" screen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] or keys[pygame.K_UP]:
            retry_selected = not retry_selected  # Toggle between Retry and Menu
            pygame.time.delay(150)  # Delay to prevent quick key presses
        if keys[pygame.K_RETURN]:
            if retry_selected:
                # Retry the current level
                create_level(current_level)
                game_over = False
            else:
                # Return to the menu
                in_menu = True
                current_level = 1
                menu.visible = True
                pygame.mixer.stop()  # Turn off the background music
                menu_music.play(-1)
                game_over = False