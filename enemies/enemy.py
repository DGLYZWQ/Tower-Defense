import pygame
import math
import os


class Enemy:
    def __init__(self):
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.vel = 3
        self.path = [(-10, 224), (43, 224), (143, 222), (244, 254), (332, 283), (599, 278), (663, 246), (694, 197), (714, 128), (763, 78), (826, 57), (889, 71), (924, 116), (942, 169), (967, 230), (1013, 268), (1078, 282), (1138, 306), (1176, 344), (1168, 398), (1136, 442), (1065, 478), (866, 487), (790, 519), (679, 539), (212, 532), (122, 490), (97, 413), (64, 346), (22, 313), (0, 311), (-40, 314)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = pygame.image.load(os.path.join("game_assets/enemies/1", "1_enemies_1_run_000.png"))
        self.dis = 0
        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        self.imgs = []
        self.flipped = False
        self.max_health = 0
        self.speed_increase = 1.2

    def draw(self, win):
        '''
        用给定的图像画出怪物
        :param win: surface
        :return: None
        '''
        self.img = self.imgs[self.animation_count]

      # 绘制敌人路径
      # for dot in self.path:
            # pygame.draw.circle(win, (255,0,0), dot, 10, 0)

        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2 - 30))
        self.draw_health_bar(win)
        #self.move()

    def draw_health_bar(self, win):
        '''
        绘制怪物头顶的生命值
        :param win: surface
        :return: None
        '''
        length = 50
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)

        pygame.draw.rect(win, (255, 0, 0), (self.x - 30, self.y - 75, length, 10), 0)  # 矩形生命值
        pygame.draw.rect(win, (0, 255, 0), (self.x - 30, self.y - 75, health_bar, 10), 0)

    def collide(self, X, Y):
        '''
        如果当前位置击中怪物则返回True 否则返回False
        :param x: int
        :param y: int
        :return: Bool
        '''
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def move(self):
        '''
        怪物按给定的路径移动
        :return: None
        '''
        # 怪物移动时进行图像切换
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0
        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (-10, 337)
        else:
            x2, y2 = self.path[self.path_pos + 1]
        # 计算两点之间的值 判断是否需要图像翻转
        dirn = ((x2-x1)*2, (y2-y1)*2)
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = (dirn[0]/length, dirn[1]/length)
        # 控制向左或向右时图像翻转
        if dirn[0] < 0 and not(self.flipped):
            self.flipped = True
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
        self.x = move_x
        self.y = move_y
        # 前往下一个点
        if dirn[0] >= 0:   # 向右移动
            if dirn[1] >= 0:  # 向下移动
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else:  # 向左移动
            if dirn[1] >= 0:  # 向下移动
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1

    def hit(self, damage):
        '''
        返回是否有敌人死亡 并且 每次调用都会移除一个生命值
        :return: Bool
        '''
        self.health -= damage
        if self.health <= 0:
            return True
        return False

        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = None
        self.dis = 0
        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        self.imgs = []
        self.flipped = False
        self.max_health = 0

    def draw(self, win):
        '''
        用给定的图像绘制怪物
        :param win: surface
        :return: None
        '''
        self.img = self.imgs[self.animation_count]

        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2 - 30))
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        '''
        在怪物上方绘制血量条
        :param win: surface
        :return: None
        '''
        length = 50
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)

        pygame.draw.rect(win, (255, 0, 0), (self.x - 30, self.y - 75, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x - 30, self.y - 75, health_bar, 10), 0)

    def collide(self, X, Y):
        '''
        如果当前位置击中怪物则返回True 否则返回False
        :param x: int
        :param y: int
        :return: Bool
        '''
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def move(self):
        '''
        怪物按给定的路径移动
        :return:None
        '''
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0

        x1, y1 = self.path[self.path_pos]

        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (-10, 337)
        else:
            x2, y2 = self.path[self.path_pos + 1]

        dirn = ((x2 - x1)*2, (y2 - y1)*2)
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = (dirn[0]/length * self.speed_increase, dirn[1]/length * self.speed_increase)  # 提高移动速度

        if dirn[0] < 0 and not(self.flipped):
            self.flipped = True
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))

        self.x = move_x
        self.y = move_y

        # 去下一个点
        if dirn[0] >= 0:  # 向右移动
            if dirn[1] >= 0:  # 向下移动
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else:  # 向左移动
            if dirn[1] >= 0:  # 向下移动
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1

    def hit(self, damage):
        '''
        返回是否有敌人死亡 并且 每次调用都会移除一个生命值
        :return: Bool
        '''
        self.health -= damage
        if self.health <= 0:
            return True
        return False










