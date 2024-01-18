import pygame
import sys
from settings import WIDTH, HEIGHT, BACKGROUND_COLOR
from assets import load_assets
from menu import Menu
from levels import create_level, update_bombs
from entities import player, enemies, walls, player_bombs, update_enemies, handle_player_input, handle_game_over_screen
from async_tasks import start_asyncio_loop

# Initialize Pygame and load assets
pygame.init()
pygame.mixer.init()
assets = load_assets()

# Main game loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bomberman Game")

    menu = Menu(assets)
    current_level = 1
    in_menu = True
    game_started = False
    game_elements_visible = False
    current_level = 1
    can_drop_bomb = True
    last_frame_time = pygame.time.get_ticks()
    retry_selected = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if in_menu:
            menu.handle_event(event, screen)
            if menu.selected_item == 0 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_started = True
                in_menu = False
                game_elements_visible = True
                current_level = 1
                create_level(current_level, enemies, walls, assets)

        if game_elements_visible:
            update_bombs(player_bombs, assets)
            screen.fill(BACKGROUND_COLOR)
            update_enemies(enemies, assets)
            handle_player_input(player, assets)

            # Render game elements
            for wall in walls:
                screen.blit(assets['wall_image'], (wall.x, wall.y))
            for enemy in enemies:
                screen.blit(assets['enemy_image'], (enemy.x, enemy.y))
            screen.blit(assets['player_image'], (player.x, player.y))

            pygame.display.update()

        if game_over and not menu.visible:
            handle_game_over_screen(screen, assets, retry_selected)

if __name__ == "__main__":
    # Start the asyncio loop in a separate thread
    asyncio_thread = threading.Thread(target=start_asyncio_loop, daemon=True)
    asyncio_thread.start()

    main()