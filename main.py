import asyncio
import threading
import pygame
import sys
from settings import WIDTH, HEIGHT, BACKGROUND_COLOR
from assets import load_assets
from menu import Menu
from levels import create_level, update_bombs
from entities import player, enemies, walls, player_bombs, update_enemies, handle_player_input, handle_game_over_screen
# from async_tasks import start_asyncio_loop

# Initialize Pygame and load assets
pygame.init()
pygame.mixer.init()
assets = load_assets()
font = pygame.font.Font(None, 36)  # Create a font object for the menu

async def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bomberman Game")

    # Define menu items
    menu_items = ["Start Game", "Options", "Credits", "Quit Game"]
    menu = Menu(font, menu_items)

    # Initialize variables
    in_menu = True
    game_over = False
    retry_selected = True
    current_level = 1
    game_started = False
    game_elements_visible = False
    can_drop_bomb = True

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if in_menu:
                # Handle menu navigation
                selected_option = menu.handle_event(event)
                if selected_option == "Start Game":
                    in_menu = False
                    game_started = True
                    game_elements_visible = True
                    create_level(current_level, enemies, walls, assets)
                # Add logic for other menu options (Options, Credits, Quit)

        if game_elements_visible:
            # Game logic and drawing
            update_bombs(player_bombs, assets)
            update_enemies(enemies, assets)
            handle_player_input(player, assets)
            screen.fill(BACKGROUND_COLOR)
            # Drawing game elements
            for wall in walls:
                screen.blit(assets['wall_image'], (wall.x, wall.y))
            for enemy in enemies:
                screen.blit(assets['enemy_image'], (enemy.x, enemy.y))
            screen.blit(assets['player_image'], (player.x, player.y))

        elif in_menu:
            # Drawing the menu
            screen.fill(BACKGROUND_COLOR)
            menu.draw(screen)

        elif game_over:
            # Handle game over logic
            handle_game_over_screen(screen, assets, retry_selected)

        # Update the display
        pygame.display.update()

    await asyncio.sleep(0)
    if not running:
        pygame.quit()
        return