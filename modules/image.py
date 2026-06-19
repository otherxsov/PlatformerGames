import pygame
import os
from .settings import screen

class Sprite:
    def __init__(self, width: int, height: int, image_name: str, x: int, y: int):
        self.WIDTH = width
        self.HEIGTH = height
        self.X = x
        self.Y = y
        self.IMAGE = self.img_load(image_name)
    def img_load(self,image_name, flip_x = False):
        path = os.path.join(__file__, "..", "..", "images",image_name)
        path = os.path.abspath(path)
        image = pygame.image.load(path)
        image = pygame.transform.scale(image,(self.WIDTH, self.HEIGTH))
        if flip_x == True:
            image = pygame.transform.flip(image,True,False)
        return image
    def create_animation_list(self, folder_name, count_image, flip_x = False):
        list_image = []
        for count in range(count_image):
            image = self.img_load(f"{folder_name}/{count}.png", flip_x)
            list_image.append(image)
        return list_image
    def show_image(self):
        screen.blit(self.IMAGE, (self.X, self.Y))
object = Sprite(width = 1500, height = 700, image_name = "bg.png", x = 0, y = 0)