# entities.py
import pygame
from settings import PLAYER_SPEED, ENEMY_SPEED, EXPLOSION_RADIUS, BOMB_TIMER

player = pygame.Rect(50, 50, 50, 50)  # Modify dimensions as needed
enemies = []
walls = []
player_bombs = []

def update_enemies(enemies, enemy_directions, ENEMY_SPEED):
    for i, enemy in enumerate(enemies):
        enemy_direction = random.choice(enemy_directions)
        enemies[i] = pygame.Rect(enemy.left + enemy_direction[0] * ENEMY_SPEED,
                                 enemy.top + enemy_direction[1] * ENEMY_SPEED,
                                 enemy.width,
                                 enemy.height)
    # Add collision detection and other logic as needed

def handle_player_input(keys, PLAYER_SPEED):
    move_x, move_y = 0, 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        move_x = -PLAYER_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        move_x = PLAYER_SPEED
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        move_y = -PLAYER_SPEED
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        move_y = PLAYER_SPEED

    # Update player position
    player.x += move_x
    player.y += move_y
    # Add collision detection and boundary checking as needed

def handle_game_over_screen(screen, font, score, retry_selected):
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (50, 50))

    final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    screen.blit(final_score_text, (50, 100))

    retry_color = (0, 255, 0) if retry_selected else (255, 255, 255)
    menu_color = (0, 255, 0) if not retry_selected else (255, 255, 255)

    retry_text = font.render("Retry", True, retry_color)
    menu_text = font.render("Menu", True, menu_color)

    screen.blit(retry_text, (50, 150))
    screen.blit(menu_text, (50, 200))