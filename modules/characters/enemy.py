from .character import Character
import pygame
from ..settings import screen
from .hero import hero
from ..map import map
from ..image import Sprite

class Enemy(Character):
    def __init__(self, width, height, x, y, speed, finish_x):
        Character.__init__(self, width, height, "enemy3/move/0.png" ,x, y, speed )
        self.MOVE_LIST = self.create_animation_list(folder_name="enemy3/move", count_image=5)
        self.MOVE_LIST_LEFT = self.create_animation_list(folder_name="enemy3/move", count_image=5, flip_x = True)
        self.START_X = x
        self.FINISH_X = finish_x
        self.SPEED = speed
        self.BULLET = Sprite(width=20, height=20, image_name= "enemy3/bullet.png", x=0, y=0)
        self.BULLET_DELAY = 0
        self.ENEMY_DEATH_LIST = self.create_animation_list("enemy3/death", 4)
    def move(self):
        self.check_collision()
        if self.DIRECTION == "right" and self.CAN_MOVE_RIGHT:
            self.X += self.SPEED
        elif self.DIRECTION == "left" and self.CAN_MOVE_LEFT:
            self.X -= self.SPEED
        
        if self.X >= self.FINISH_X or self.CAN_MOVE_RIGHT == False:
            self.DIRECTION = "left"
        if self.X <= self.START_X or self.CAN_MOVE_LEFT == False:
            self.DIRECTION = "right"

    def animation(self):
        if self.ENEMY_DEATH:
            self.play_animation(10, 40, self.ENEMY_DEATH_LIST)
            if self.IMAGE_COUNTER == 39:
                map.ENEMY_LIST.remove(self)
        else:
            self.move()
            self.atack()
            self.play_animation(time= 7, max_count= 34, list_image= self.MOVE_LIST, list_image_left= self.MOVE_LIST_LEFT)


    def atack(self):
        if self.DIRECTION == "right":
            enemy_view_rect = pygame.Rect(self.X + self.WIDTH, self.Y, self.WIDTH * 3, self.HEIGTH )
        else:
            enemy_view_rect = pygame.Rect(self.X - self.WIDTH * 3, self.Y, self.WIDTH * 3, self.HEIGTH )
        #pygame.draw.rect(screen, "yellow", enemy_view_rect)
        if hero.RECT_HERO.colliderect(enemy_view_rect) and self.BULLET_DELAY == 0:
            self.BULLET_DELAY = 200
            self.BULLET.X = self.X + self.WIDTH / 2
            self.BULLET.Y = self.Y + self.HEIGTH / 2
            self.BULLET.DIRECTION = self.DIRECTION
        if self.DIRECTION == "right":
            self.BULLET.IMAGE = self.BULLET.img_load("enemy3/bullet.png")
        else:
            self.BULLET.IMAGE = self.BULLET.img_load("enemy3/bullet.png", flip_x = True)
        if self.BULLET_DELAY > 0:
            self.bullet_move()
        if self.BULLET_DELAY < 0:
            self.BULLET_DELAY += 1
    def bullet_move(self):
        # print("bebe")
        if self.BULLET.DIRECTION == "right":
            self.BULLET.X += 8
        else:
            self.BULLET.X -= 8
        self.BULLET.show_image()
        self.BULLET_DELAY -= 1
        self.BULLET_RECT = pygame.Rect(self.BULLET.X, self.BULLET.Y, self.BULLET.WIDTH, self.BULLET.HEIGTH)
        if hero.RECT_HERO.colliderect(self.BULLET_RECT):
            if hero.PROTECT == True:
                hero.PROTECT = False
            else:
                hero.HEART -= 1
            self.BULLET_DELAY = -50
        for block in map.LIST_COLLISION:
            block_rect = pygame.Rect(block.x, block.y, block.width, block.height)
            # pygame.draw.rect(screen,'RED',block_rect)
            if block_rect.colliderect(self.BULLET_RECT):
                self.BULLET_DELAY = -50
                break
enemy1 = Enemy(width= 80, height= 80, x= 900, y= 570, speed= 2, finish_x= 1500)
map.ENEMY_LIST.append(enemy1)