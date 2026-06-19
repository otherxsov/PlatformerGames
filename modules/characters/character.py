from ..image import Sprite
import pygame
from ..settings import screen 
from ..map import map


class Character(Sprite):
    def __init__(self, width, height, image_name, x, y, speed, direction= "right"):
        Sprite.__init__(self, width, height, image_name, x, y)
        self.SPEED = speed
        self.JUMP_COUNTER = 0
        self.DIRECTION = direction
        self.IMAGE_COUNTER = 0
        self.CRAWL_COLLISION = False 
        self.ENEMY_DEATH = False
    def check_collision(self):
        self.RECT_HERO = pygame.Rect(self.X + 15, self.Y +10, self.WIDTH - 30, self.HEIGTH - 10)
        if self.CRAWL_COLLISION:
            self.RECT_HERO = pygame.Rect(self.X + 15, self.Y + 25, self.WIDTH - 30, self.HEIGTH - 25 )
        # pygame.draw.rect(screen, "red", self.RECT_HERO)
        self.CAN_STAND_UP = True
        self.CAN_MOVE_RIGHT = True
        self.CAN_MOVE_LEFT = True
        self.CAN_MOVE_DOWN = True
        for platform in map.LIST_COLLISION:
            left_rect = pygame.Rect(platform.x, platform.y + 8, 1 , platform.height - 16)
            # pygame.draw.rect(screen, "blue", left_rect)
            top_rect= pygame.Rect(platform.x + 8, platform.y, platform.width - 16, 1)
            # pygame.draw.rect(screen, "blue", top_rect)
            bottom_rect= pygame.Rect(platform.x + 8, platform.y + platform.height, platform.width - 16, 1)
            # pygame.draw.rect(screen, "blue", bottom_rect)
            right_rect= pygame.Rect(platform.x + platform.width, platform.y + 8, 1, platform.height - 16)
            # pygame.draw.rect(screen, "blue", right_rect)
            if self.RECT_HERO.colliderect(left_rect):
                self.CAN_MOVE_RIGHT = False
            if self.RECT_HERO.colliderect(right_rect):
                self.CAN_MOVE_LEFT = False
            if self.RECT_HERO.colliderect(top_rect):
                self.CAN_MOVE_DOWN = False
                self.Y = platform.y - self.HEIGTH + 1
            if self.RECT_HERO.colliderect(bottom_rect):
                self.JUMP_COUNTER = 0
                self.CAN_STAND_UP = False
    def play_animation(self, time, max_count, list_image, list_image_left = None):
        self.IMAGE_COUNTER += 1
        if self.IMAGE_COUNTER >= max_count:
            self.IMAGE_COUNTER = 0
        if list_image_left and self.DIRECTION == "left":
            self.IMAGE = list_image_left[self.IMAGE_COUNTER // time]
        else:
            self.IMAGE = list_image[self.IMAGE_COUNTER // time]