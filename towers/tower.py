import pygame
from menu.menu import Menu
import os
import math

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "menu.png")), (120, 60))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "upgrade.png")), (50, 50))


class Tower:
    '''
    炮塔的抽象类
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.sell_price = [0, 0, 0]
        self.price = [0, 0, 0]
        self.level = 1
        self.selected = False
        # 定义升级炮塔时弹出的菜单和按钮
        self.menu = Menu(self, self.x, self.y, menu_bg, [2000, "MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.range = 150

        self.tower_imgs = []
        self.damage = 1

        self.place_color = (0, 0, 255, 100)  # 放置炮塔时出现的颜色

    def draw(self, win):
        '''
        绘制炮塔
        :param win: surface
        :return: None
        '''
        img = self.tower_imgs[self.level - 1]
        win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2))

        # 绘制菜单
        if self.selected:
            self.menu.draw(win)

    def draw_radius(self, win):
        if self.selected:
            # 绘制选中炮塔时显示的范围圈
            surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)  # SRCALPHA 表示透明化
            pygame.draw.circle(surface, (128, 128, 128, 100), (self.range, self.range), self.range, 0)

            win.blit(surface, (self.x - self.range, self.y - self.range))

    def draw_placement(self, win):
        # 绘制炮塔放置时的范围圈
        surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, self.place_color, (50, 50), 50, 0)

        win.blit(surface, (self.x - 50, self.y - 50))

    def click(self, X, Y):
        '''
         点击炮塔并选中
        :param X:int
        :param Y:int
        :return:bool
        '''
        img = self.tower_imgs[self.level - 1]
        if X  <= self.x - img.get_width()//2 + self.width and X >= self.x - img.get_width()//2:
            if Y  <= self.y  + self.height - img.get_height()//2 and Y >= self.y - img.get_height()//2:
                return True
        return False

    def sell(self):
        '''
        卖掉炮塔
        :return: int
        '''
        return self.sell_price[self.level-1]

    def upgrade(self):
        '''
        以给定的价格升级炮塔
        :return: None
        '''
        if self.level < len(self.tower_imgs):
            self.level += 1
            self.damage += 1

    def get_upgrade_cost(self):
        '''
        现有的钱减去升级炮塔所需的钱，如果小于0则不能升级
        :return: int
        '''
        return self.price[self.level-1]

    def move(self, x, y):
        '''
        将塔移动到给定的 x 和 y
        :param x: int
        :param y: int
        :return: None
        '''
        self.x = x
        self.y = y
        self.menu.x = x
        self.menu.y = y
        self.menu.update()

    def collide(self, otherTower):
        '''
        检测与已放置炮塔的距离，太近则无法放置
        :param otherTower: 其他炮塔
        :return: Bool
        '''
        x2 = otherTower.x
        y2 = otherTower.y

        dis = math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)
        if dis >= 100:
            return False
        else:
            return True
