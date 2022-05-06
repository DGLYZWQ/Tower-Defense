import pygame
import os
pygame.font.init()

star = pygame.transform.scale((pygame.image.load(os.path.join("game_assets","star2.png"))),(32,32))
star2 = pygame.transform.scale((pygame.image.load(os.path.join("game_assets","star2.png"))),(21,21))

class Button:
    '''
    菜单上的按钮
    '''
    def __init__(self, menu, img, name):
        self.name = name
        self.img = img
        self.x = menu.x - 50
        self.y = menu.y - 115
        self.menu = menu
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def click(self, X, Y):
        '''
        如果菜单上的位置被点击，则返回True
        :param X: int
        :param Y: int
        :return: bool
        '''
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def draw(self, win):
        '''
        绘制按钮
        :param win: surface
        :return: None
        '''
        win.blit(self.img, (self.x, self.y))

    def update(self):
        '''
        更新按钮位置
        :return: None
        '''
        self.x = self.menu.x - 50
        self.y = self.menu.y - 115

class PlayPauseButton(Button):
    def __init__(self, play_img, pause_img, x, y):
        self.img = play_img
        self.play = play_img
        self.pause = pause_img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.paused = True

    def draw(self, win):
        if self.paused:
            win.blit(self.play, (self.x, self.y))
        else:
            win.blit(self.pause, (self.x, self.y))

class VerticalButton(Button):
    '''
    菜单上的对象按钮
    '''
    def __init__(self, x, y, img, name, cost):
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.cost = cost

class Menu:
    '''
    游戏界面的菜单
    '''
    def __init__(self, tower, x, y, img, item_cost):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.item_cost = item_cost
        self.buttons = []
        self.items = 0
        self.bg = img
        self.font = pygame.font.SysFont("comicsans", 18)
        self.tower = tower

    def add_btn(self, img, name):
        '''
        向菜单添加按钮
        :param img: surface
        :param name: str
        :return: None
        '''
        self.items += 1
        #btn_x = self.x - self.bg.get_width()/2 + 10
        #btn_y = self.y - 115
        self.buttons.append(Button(self, img, name))

    def get_item_cost(self):
        '''
        获得升级到下一个级别的价格
        :return: int
        '''
        return self.item_cost[self.tower.level - 1]

    def draw(self, win):
        '''
        绘制按钮和菜单背景图
        :param win: surface
        :return: None
        '''
        win.blit(self.bg, (self.x - self.bg.get_width()/2, self.y-120))
        for item in self.buttons:
            item.draw(win)
            win.blit(star, (item.x + item.width + 10, item.y))
            text = self.font.render(str(self.item_cost[self.tower.level -1]), 1, (255,255,255))
            win.blit(text, (item.x + item.width + 5, item.y + star.get_height() - 3))


    def get_clicked(self, X, Y):
        '''
        从菜单中返回点击的项目
        :param X: int
        :param Y: int
        :return: str
        '''
        for btn in self.buttons:
            if btn.click(X,Y):
                return btn.name

        return None

    def update(self):
        '''
        更新菜单和按钮位置
        :return: None
        '''
        for btn in self.buttons:
            btn.update()

class VerticalMenu(Menu):
    '''
    游戏侧边栏的垂直菜单
    '''
    def __init__(self,  x, y, img):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.buttons = []
        self.items = 0
        self.bg = img
        self.font = pygame.font.SysFont("comicsans", 25)

    def add_btn(self, img, name, cost):
        '''
        向菜单添加按钮
        :param img: surface
        :param name: str
        :return: None
        '''
        self.items += 1
        #inc_x = self.width/self.items/2
        btn_x = self.x  - 50
        btn_y = self.y + (self.items-1)*90 - 130
        self.buttons.append(VerticalButton(btn_x, btn_y, img, name, cost))

    def get_item_cost(self, name):
        '''
        获取物品的价格
        :param name: str
        :return: int
        '''
        for btn in self.buttons:
            if btn.name == name:
                return btn.cost
        return -1


    def draw(self, win):
        '''
        绘制按钮和菜单背景图
        :param win: surface
        :return: None
        '''
        win.blit(self.bg, (self.x - self.bg.get_width()/2, self.y - 120))
        for item in self.buttons:
            item.draw(win)
            win.blit(star2, (item.x + 5, item.y + item.height - 33))
            text = self.font.render(str(item.cost), 1, (255, 255, 255))
            win.blit(text, (item.x + item.width/2 - text.get_width()/2 + 5, item.y + item.height - 40 ))
