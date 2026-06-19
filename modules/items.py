import pygame
from .image import Sprite
from .characters import hero
class Items(Sprite):
    def __init__(self, width, height, image_name, x, y):
        Sprite.__init__(self, width, height, image_name, x, y)
        self.IMAGE_NAME = image_name
        
        
    def collect(self):
        item = pygame.Rect(self.X, self.Y, self.WIDTH, self.HEIGTH)
        if hero.RECT_HERO.colliderect(item):
            items.remove(self)
            if "battery" in self.IMAGE_NAME and hero.BATTERY_COUNT < 5:
                hero.BATTERY_COUNT += 1
                hero.BATTERY_IMG.IMAGE = hero.BATTERY_IMG.ANIMATION_BATTERY[hero.BATTERY_COUNT]
            elif "heart" in self.IMAGE_NAME and hero.HEART < 3:
                hero.HEART += 1
            elif "key" in self.IMAGE_NAME:
                hero.HAS_KEY = True
            elif "protect" in self.IMAGE_NAME :
                hero.PROTECT = True

items = [
    Items(width=25, height=25, image_name="heart.png", x=425, y=625),
    Items(width=25, height=25, image_name="heart.png", x=375, y=275),
    Items(width=25, height=25, image_name="protect.png", x=625, y=425),
    Items(width=50, height=50, image_name="battery1.png", x=350, y=500),
    Items(width=50, height=50, image_name="battery2.png", x=450, y=500),
    Items(width=25, height=25, image_name="key.png", x=325, y=275)
]

             