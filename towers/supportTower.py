import pygame
from .tower import Tower
import os
import math

range_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers", "4.png")), (90, 90)),
              pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers", "5.png")), (90, 90))]

class RangeTower(Tower):
    '''
    为周围的每个炮塔扩大额外的射程范围
    '''
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 100
        self.effect = [0.2, 0.4] # 影响范围
        self.tower_imgs = range_imgs[:] # [:]图像翻转
        self.width = self.height = 90
        self.name = "range"
        self.price = [2000]

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)

    def support(self, towers):
        '''
        将根据不同炮塔的叠加属性修改原有炮塔的范围属性
        :param towers: list
        :return: None
        '''
        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y

            dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
            if dis <= self.range + tower.width/2:
                effected.append(tower)

        # 辅助塔范围内的攻击型炮塔伤害范围扩大
        for tower in effected:
            tower.range = tower.original_range + round(tower.range * self.effect[self.level - 1])

damage_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers", "8.png")), (90, 90)),
              pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers", "9.png")), (90, 90))]

class DamageTower(RangeTower):
    '''
    增加周围炮塔的伤害值
    '''
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 100
        self.tower_imgs = damage_imgs[:]
        self.effect = [0.5, 1]  # 给攻击型炮塔增加的伤害值域
        self.name = "damage"
        self.price = [2000]

    def support(self, towers):
        '''
        将根据不同炮塔的叠加属性修改原有炮塔的范围属性
        :param towers: list
        :return: None
        '''
        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y

            dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

            if dis <= self.range + tower.width/2:
                effected.append(tower)
        # 辅助塔范围内的攻击型炮塔伤害值增加
        for tower in effected:
            tower.damage = tower.original_damage + round(tower.original_damage * self.effect[self.level - 1])
