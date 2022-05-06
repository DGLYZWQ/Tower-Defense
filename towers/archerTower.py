import pygame
from .tower import Tower
from menu.menu import Menu
import os
import math


menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "menu.png")), (120, 60))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "upgrade.png")), (50, 50))

tower_imgs1 = []
archer_imgs1 = []
# 加载长距离攻击炮塔图片
for x in range(7, 10):
    tower_imgs1.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/archer_towers/archer_1", str(x) + ".png")),
        (90, 90)))

# 加载长距离攻击炮塔上的武器图片
for x in range(37, 42):
    archer_imgs1.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/archer_towers/archer_top", str(x) + ".png")),
        (45, 45)))

class ArcherTowerLong(Tower):
    '''
    定义长距离攻击炮塔的属性
    '''
    def __init__(self, x, y):
        super().__init__(x, y)
        self.tower_imgs = tower_imgs1[:]
        self.archer_imgs = archer_imgs1[:]
        self.archer_count = 0  # 武器动画计数值
        self.range = 200  # 攻击范围
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.damage = 1
        self.original_damage = self.damage
        self.width = self.height = 90
        self.moving = False
        self.name = "archer"

        self.menu = Menu(self, self.x, self.y, menu_bg, [2000, 5000, "MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")

    def get_upgrade_cost(self):
        '''
        获取升级费用值
        :return: int
        '''
        return self.menu.get_item_cost()

    def draw(self, win):
        '''
        绘制炮塔和武器动画
        :param win: surface
        :return: int
        '''
        super().draw_radius(win)
        super().draw(win)

        if self.inRange and not self.moving:
            self.archer_count += 1
            if self.archer_count >= len(self.archer_imgs) * 10:
                self.archer_count = 0
        else:
            self.archer_count = 0

        archer = self.archer_imgs[self.archer_count // 10]
        if self.left == True:
            add = -25
        else:
            add = -24
        win.blit(archer, ((self.x  + add), (self.y - archer.get_height() + add)))

    def change_range(self, r):
        '''
        范围炮塔改变范围
        :param r:int
        :return:None
        '''
        self.range = r

    def attack(self, enemies):
        '''
        攻击怪物列表中的怪物，修改列表
        :param enemies: list of enemies
        :return: None
        '''
        money = 0
        self.inRange = False
        enemy_closest = []
        for enemy in enemies:
            x = enemy.x
            y = enemy.y
            # 计算怪物与塔之间的距离 判断是否攻击怪物
            dis = math.sqrt((self.x - enemy.img.get_width()/2 - x)**2 + (self.y - enemy.img.get_height()/2 - y)**2)
            if dis < self.range:
                self.inRange = True
                enemy_closest.append(enemy)
        # 攻击与炮塔距离最近的怪物
        enemy_closest.sort(key=lambda x: x.path_pos)
        enemy_closest = enemy_closest[::-1]
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if self.archer_count == 5:
                if first_enemy.hit(self.damage) == True:
                    money = first_enemy.money * 2    # 第一个击杀的怪物将获得双倍金币
                    enemies.remove(first_enemy)
            # 炮塔的武器向左还是向右投掷
            if first_enemy.x < self.x and not (self.left):
                self.left = True
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)
            elif self.left and first_enemy.x < self.x:
                self.left = False
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)
        return money

tower_imgs = []
archer_imgs = []
#  加载短距离攻击炮塔图片
for x in range(10, 13):
    tower_imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/archer_towers/archer_2", str(x) + ".png")),
        (90, 90)))

#  加载短距离攻击炮塔图片上的武器图片
for x in range(43, 48):
    archer_imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/archer_towers/archer_top_2", str(x) + ".png")),
        (45, 45)))


class ArcherTowerShort(ArcherTowerLong):
    '''
    定义短距离攻击炮塔的属性
    '''
    def __init__(self, x, y):
        super().__init__(x, y)
        self.tower_imgs = tower_imgs[:]
        self.archer_imgs = archer_imgs[:]
        self.archer_count = 0
        self.range = 150
        self.original_range = self.range  # 初始范围
        self.inRange = False
        self.left = True
        self.damage = 2
        self.original_damage = self.damage

        self.menu = Menu(self, self.x, self.y, menu_bg, [2500, 5500, "MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.name = "archer2"
