# assets.py
import pygame

def load_assets():
    return {
        "player_image": pygame.image.load("player.png"),
        "enemy_image": pygame.image.load("enemy.png"),
        "bomb_image": pygame.image.load("bomb.png"),
        "wall_image": pygame.image.load("wall.png"),
        "explosion_images": [
            pygame.image.load("explosion_frame1.png"),
            pygame.image.load("explosion_frame2.png"),
            pygame.image.load("explosion_frame3.png")
        ],
        "menu_music": pygame.mixer.Sound("menu_music.ogg"),
        "background_music": pygame.mixer.Sound("background_music.ogg"),
        "explosion_sound": pygame.mixer.Sound("explosion.ogg")
    }