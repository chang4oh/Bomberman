# menu.py
import pygame

class Menu:
    def __init__(self, font, items):
        self.items = items
        self.selected_item = 0
        self.font = font
        self.visible = True

    def draw(self, screen):
        if self.visible:
            for i, item in enumerate(self.items):
                color = (255, 0, 0) if i == self.selected_item else (255, 255, 255)
                label = self.font.render(item, True, color)
                screen.blit(label, (100, 100 + i * 30))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.items)
            elif event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.items)
            elif event.key == pygame.K_RETURN:
                return self.items[self.selected_item]
        return None