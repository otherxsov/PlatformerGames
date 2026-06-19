from .character import Character
from ..map import map



class FriendlyBot(Character):
    def __init__(self, width, height, x, y):
        Character.__init__(self, width, height, "friendly_bot/breath/0.png", x, y, 0)
        self.ANIMATION_BREATH = self.create_animation_list(folder_name = "friendly_bot/breath", count_image= 2)

        self.ANIMATION_DEATH = self.create_animation_list(folder_name = "friendly_bot/death", count_image=4)


    def animation(self):
        if self.ENEMY_DEATH:
            self.play_animation(10, 40, self.ANIMATION_DEATH)
            if self.IMAGE_COUNTER == 39:
                map.ENEMY_LIST.remove(self)
        else:
            self.play_animation(20, 39, self.ANIMATION_BREATH)


friendly_bot = FriendlyBot(80, 80, 1125, 370)
map.ENEMY_LIST.append(friendly_bot)
