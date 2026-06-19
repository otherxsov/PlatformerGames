import pygame 
from .character import Character
from ..image import Sprite
from ..settings import screen
from ..map import map



class Hero(Character):
    def __init__(self, width, height, image_name, x, y, speed):
        Character.__init__(self, width, height, image_name, x, y, speed)
        self.LIST_RUN = self.create_animation_list("hero/run", 6)
        self.LIST_RUN_LEFT = self.create_animation_list("hero/run", 6, flip_x= True)
        
        self.LIST_JUMP = self.create_animation_list("hero/jump", 2)
        self.LIST_JUMP_LEFT = self.create_animation_list("hero/jump", 2, flip_x= True)
        
        self.LIST_BREATH = self.create_animation_list("hero/breath", 11)
        
        self.CRAWL_IMAGE = self.create_animation_list("hero/crawl", 5)
        self.LEFT_CRAWL_IMAGE = self.create_animation_list("hero/crawl", 5, True)
        
        
        self.IS_HOLD_BLASTER = False
        self.SHOOTING_RUN = self.create_animation_list("hero/shooting_run", 6)
        self.SHOOTING_RUN_LEFT = self.create_animation_list("hero/shooting_run", 6, flip_x= True)
        
        
        self.HEART = 3 
        self.HEART_IMG = Sprite(width=50,height=50,image_name="heart.png",x=0,y=25)
        self.EMTY_HEART_IMAGE = Sprite(width=50,height=50,image_name="empty_heart.png",x=0,y=25)

        self.BULLET_DELAY = 0
        self.BULLET = Sprite(width=20, height=20, image_name= "hero/bullet.png", x=0, y=0)
        
        self.BATTERY_COUNT = 5
        self.BATTERY_IMG = Sprite(width = 40, height = 40, image_name = "battery/5.png", x = 25, y = 30)
        self.BATTERY_IMG.ANIMATION_BATTERY = self.BATTERY_IMG.create_animation_list(folder_name= "battery", count_image=6 )
        
        self.LADDER_UP = False
        self.LADDER_UP_ANIMATION = self.create_animation_list("hero/climb", 2)
        self.HAS_KEY = False

        self.PROTECT = False
        self.PROTECT_IMAGE = Sprite(width=40, height=40, image_name= "protect.png", x= 25 , y = 80)
    def move(self):
        self.check_collision()
        self.LIST_KEYS = pygame.key.get_pressed()
        self.atack()
        if self.LIST_KEYS[pygame.K_LSHIFT]:
            self.CRAWL_COLLISION = True
        elif self.CAN_STAND_UP:
            self.CRAWL_COLLISION = False
        if self.LIST_KEYS[pygame.K_d] and self.CAN_MOVE_RIGHT:
            self.DIRECTION = "right"
            if self.CRAWL_COLLISION == True:
                self.X += self.SPEED / 2
                self.play_animation(time = 15, max_count = 74, list_image= self.CRAWL_IMAGE)
            else:
                self.X += self.SPEED
                if self.IS_HOLD_BLASTER == True:
                    self.play_animation(time = 5, max_count = 29, list_image= self.SHOOTING_RUN, list_image_left = self.SHOOTING_RUN_LEFT)
                else:
                    self.play_animation(time = 5, max_count = 29, list_image= self.LIST_RUN, list_image_left = self.LIST_RUN_LEFT)
        elif self.LIST_KEYS[pygame.K_a] and self.CAN_MOVE_LEFT:
            self.DIRECTION = "left"
            if self.CRAWL_COLLISION == True:
                self.X -= self.SPEED / 2
                self.play_animation(time = 15, max_count = 74, list_image= self.CRAWL_IMAGE, list_image_left = self.LEFT_CRAWL_IMAGE )
            else:
                self.X -= self.SPEED
                if self.IS_HOLD_BLASTER == True:
                    self.play_animation(time = 5, max_count = 29, list_image= self.SHOOTING_RUN, list_image_left = self.SHOOTING_RUN_LEFT)
                else:
                    self.play_animation(time = 5, max_count = 29, list_image= self.LIST_RUN, list_image_left = self.LIST_RUN_LEFT)
        elif self.JUMP_COUNTER == 0 and self.CAN_MOVE_DOWN == False:
            if self.CRAWL_COLLISION == True:
                if self.DIRECTION == "right":
                    self.IMAGE = self.CRAWL_IMAGE[0]
                else: 
                    self.IMAGE = self.CRAWL_IMAGE[0]
            else:
                
                self.play_animation(time= 15, max_count= 164, list_image= self.LIST_BREATH)
        if self.CAN_MOVE_DOWN and self.LADDER_UP == False and self.JUMP_COUNTER == 0:
            self.Y += self.SPEED
            if self.DIRECTION == "right":
                self.IMAGE = self.LIST_JUMP[1]
            else:
                self.IMAGE = self.LIST_JUMP_LEFT[1]
        self.jump()
        self.climb()
    def jump(self):
        if self.LIST_KEYS[pygame.K_SPACE] and self.CAN_MOVE_DOWN == False and self.CAN_STAND_UP:
            self.JUMP_COUNTER = 23
        if self.JUMP_COUNTER > 0:
            self.JUMP_COUNTER -= 1
            self.Y -= 7
            if self.DIRECTION == "right":
                self.IMAGE = self.LIST_JUMP[1]
            else:
                self.IMAGE = self.LIST_JUMP_LEFT[1]
    
    def show_states(self):
        if self.PROTECT == True :
            self.PROTECT_IMAGE.show_image()
        for count_heart in range(3):
            if count_heart < self.HEART:
                screen.blit(self.HEART_IMG.IMAGE, (50 * (count_heart + 2), 25))
            else:
                screen.blit(self.EMTY_HEART_IMAGE.IMAGE,(50 * (count_heart + 2), 25))
        self.BATTERY_IMG.show_image()

    
    def atack(self):
        if self.LIST_KEYS[pygame.K_e] and self.IS_HOLD_BLASTER == True and self.BULLET_DELAY == 0 and self.BATTERY_COUNT > 0 :
            self.BATTERY_COUNT -= 1
            self.BATTERY_IMG.IMAGE = self.BATTERY_IMG.ANIMATION_BATTERY[self.BATTERY_COUNT]
            self.BULLET_DELAY = 200
            self.BULLET.X = self.X + self.WIDTH / 2
            self.BULLET.Y = self.Y + self.HEIGTH / 2
            self.BULLET.DIRECTION = self.DIRECTION
            # табуляция
            if self.BULLET.DIRECTION == "right":
                self.BULLET.IMAGE = self.BULLET.img_load("hero/bullet.png")
            else:
                self.BULLET.IMAGE = self.BULLET.img_load("hero/bullet.png", flip_x = True)
        if self.BULLET_DELAY > 0:
            self.bullet_move()
        if self.BULLET_DELAY < 0:
            self.BULLET_DELAY += 1
    def bullet_move(self):
        if self.BULLET.DIRECTION == "right":
            self.BULLET.X += 8
        else:
            self.BULLET.X -= 8
        self.BULLET.show_image()
        self.BULLET_DELAY -= 1
        self.BULLET_RECT = pygame.Rect(self.BULLET.X, self.BULLET.Y, self.BULLET.WIDTH, self.BULLET.HEIGTH)
        for block in map.LIST_COLLISION:
            block_rect = pygame.Rect(block.x, block.y, block.width, block.height)
            # pygame.draw.rect(screen,'RED',block_rect)
            if block_rect.colliderect(self.BULLET_RECT):
                self.BULLET_DELAY = -50
                break
        for enemy in map.ENEMY_LIST:
            enemy_rect = pygame.Rect(enemy.X, enemy.Y, enemy.WIDTH, enemy.HEIGTH)
            if self.BULLET_RECT.colliderect(enemy_rect):
                # map.ENEMY_LIST.remove(enemy)
                enemy.ENEMY_DEATH = True
                enemy.IMAGE_COUNTER = 0
                self.BULLET_DELAY = -50
    def climb(self):
        self.LADDER_UP = False
        for ladder in map.LIST_LADDER_COLLISION:
            if hero.RECT_HERO.colliderect(ladder):
                self.LADDER_UP = True
                break
        if self.LADDER_UP:
            if self.LIST_KEYS[pygame.K_w] and self.CAN_STAND_UP:
                self.Y -= 2
                self.play_animation(10,19, self.LADDER_UP_ANIMATION)
            elif self.LIST_KEYS[pygame.K_s]:
                self.Y += 2
                self.play_animation(10,19, self.LADDER_UP_ANIMATION)
                
           
            


           

hero = Hero(width=80, height=80, image_name="hero.png", x= 100, y= 100, speed= 4)
