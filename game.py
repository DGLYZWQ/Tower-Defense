import pygame
import os
from enemies.scorpion import Scorpion
from enemies.club import Club
from enemies.wizard import Wizard
from enemies.sword import Sword
from towers.archerTower import ArcherTowerLong, ArcherTowerShort
from towers.supportTower import RangeTower, DamageTower
from menu.menu import VerticalMenu, PlayPauseButton
import time
import random
pygame.font.init() # 字体初始化
pygame.init() # 初始化
pygame.display.set_caption("Tower Defense") # 窗体上显示的游戏名字
icon = pygame.image.load(os.path.join("game_assets", "icon.png"))
pygame.display.set_icon(icon) # 窗体上显示的游戏图标
# 怪物移动路径
path = [(-10, 224), (43, 224), (143, 222), (244, 254), (332, 283), (599, 278), (663, 246), (694, 197), (714, 128), (763, 78), (826, 57), (889, 71), (924, 116), (942, 169), (967, 230), (1013, 268), (1078, 282), (1138, 306), (1176, 344), (1168, 398), (1136, 442), (1065, 478), (866, 487), (790, 519), (679, 539), (212, 532), (122, 490), (97, 413), (64, 346), (22, 313), (0, 311), (-40, 314)]
# 加载生命值 金币 侧边栏背景图
lives_img = pygame.image.load(os.path.join("game_assets", "heart1.png"))
star_img = pygame.image.load(os.path.join("game_assets", "star2.png"))
side_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "side5.png")), (100, 400))
# 加载侧边栏中购买炮塔的图标
buy_archer = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_archer.png")), (100, 100))
buy_archer_2 = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_archer_2.png")), (100, 100))
buy_damage = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_damage.png")), (100, 100))
buy_range = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_range.png")), (100, 100))
# 开始/暂停 图标
play_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "button_start.png")), (75, 75))
pause_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "button_pause.png")), (75, 75))
# 播放/静音 图标
sound_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "button_sound.png")), (75, 75))
sound_off_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "button_sound_off.png")), (75, 75))
# 左上角显示怪物的当前波数
wave_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "wave.png")), (150, 65))
# 攻击型炮塔和辅助型炮塔的名字
attack_tower_names = ["archer", "archer2"]
support_tower_names = ["range", "damage"]

# 加载游戏背景音乐
pygame.mixer.music.load(os.path.join("game_assets", "moonlight.wav"))

# 每一波怪物的种类和数量
# (# scorpions, # wizards, # clubs, # swords)
waves = [
    [20, 0, 0],
    [10, 20, 0],
    [10, 10, 10],
    [30, 20, 10],
    [20, 20, 10, 1],
    [10, 10, 20, 2],
    [20, 20, 30, 3],
    [0, 30, 30, 4],
    [0, 0, 50, 5],
    [10, 20, 30, 6],
    [30, 40, 50, 8],
    [100, 100, 100, 10],
]


class Game:
    def __init__(self, win):
        self.width = 1350
        self.height = 700
        self.win = win # 窗体
        self.enemys = []
        self.attack_towers = []
        self.support_towers = []
        self.lives = 10
        self.money = 3000
        self.bg = pygame.image.load(os.path.join("game_assets", "bg2.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("comicsans", 50)
        self.selected_tower = None
        self.menu = VerticalMenu(self.width - side_img.get_width() + 60, 260, side_img)
        self.menu.add_btn(buy_archer, "buy_archer", 500)
        self.menu.add_btn(buy_archer_2, "buy_archer_2", 750)
        self.menu.add_btn(buy_damage, "buy_damage", 1000)
        self.menu.add_btn(buy_range, "buy_range", 1000)
        self.moving_object = None
        self.wave = 0
        self.current_wave = waves[self.wave][:]
        self.pause = True
        self.music_on = True
        self.playPauseButton = PlayPauseButton(play_btn, pause_btn, 10, self.height - 85)
        self.soundButton = PlayPauseButton(sound_btn, sound_off_btn, 95, self.height - 85)
        self.wave_font = pygame.font.SysFont("comicsans", 30)

    def gen_enemies(self):
        '''
        生成下一个或多个要显示的敌人
        :return:enemy
        '''
        if sum(self.current_wave) == 0:
            if len(self.enemys) == 0:
                self.wave += 1
                self.current_wave = waves[self.wave]
                self.pause = True
                self.playPauseButton.paused = self.pause
        else:
            wave_enemies = [Scorpion(), Wizard(), Club(), Sword()]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] != 0:
                    self.enemys.append(wave_enemies[x])
                    self.current_wave[x] = self.current_wave[x] - 1
                    break

    def run(self):
        pygame.mixer.music.play(loops=-1)
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(300)   # 更改游戏速率
            # pygame.time.delay(500)
            if self.pause == False:
                # 生成怪物
                if time.time() - self.timer >= random.randrange(1, 5) / 3:   # 怪物生成的时间间隔
                    self.timer = time.time()
                    # self.enemys.append(random.choice([Club(), Scorpion(), Wizard()]))
                    self.gen_enemies()

            pos = pygame.mouse.get_pos()   # 获取鼠标点击的坐标值

            # 检查移动物体
            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])
                tower_list = self.attack_towers[:] + self.support_towers[:]
                collide = False
                for tower in tower_list:
                    if tower.collide(self.moving_object):
                        collide = True
                        tower.place_color = (255, 0, 0, 100)
                        self.moving_object.place_color = (255, 0, 0, 100)
                    else:
                        tower.place_color = (0, 0, 255, 100)
                        if not collide:
                            self.moving_object.place_color = (0, 0, 255, 100)

            # 主事件循环
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:  # 检测到鼠标按键释放时
                    # 如果点击选中正在移动的对象
                    if self.moving_object:
                        not_allowed = False
                        tower_list = self.attack_towers[:] + self.support_towers[:]
                        for tower in tower_list:
                            if tower.collide(self.moving_object):
                                not_allowed = True

                    # 绘制怪物路径并粘贴打印点的值 放入路径中
                    #self.path.append(pos)
                    #print(pos)
                        # 如果选中炮塔并且可以放置
                        if not not_allowed and self.point_to_line(self.moving_object):
                            if self.moving_object.name in attack_tower_names:
                                self.attack_towers.append(self.moving_object)
                            elif self.moving_object.name in support_tower_names:
                                self.support_towers.append(self.moving_object)

                            self.moving_object.moving = False
                            self.moving_object = None

                    else:
                        # 检测暂停键是否被点击
                        if self.playPauseButton.click(pos[0], pos[1]):
                            self.pause = not (self.pause)
                            self.playPauseButton.paused = self.pause
                            #self.playPauseButton.change_img()
                        # 检测音乐键是否被点击
                        if self.soundButton.click(pos[0], pos[1]):
                            self.music_on = not(self.music_on)
                            self.soundButton.paused = self.music_on
                            if self.music_on:
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()

                        # 检查是否点击侧边菜单栏
                        side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.money >= cost:
                                self.money -= cost
                                self.add_tower(side_menu_button)
                            #print(side_menu_button)

                        # 检测是否点击了攻击塔或者辅助塔
                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                            if btn_clicked:
                                if btn_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    if self.money >= cost:
                                        self.money -= cost
                                        self.selected_tower.upgrade()

                        if not(btn_clicked):
                            for tw in self.attack_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False

                            # 检查是否点击了辅助塔
                            for tw in self.support_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False

            # 循环敌人移动
            if not self.pause:
                to_del = []
                for en in self.enemys:
                    en.move()
                    if en.x < -15:
                        to_del.append(en)

                # 删除屏幕范围外的所有敌人
                for d in to_del:
                    self.lives -= 1
                    self.enemys.remove(d)

                # 循环攻击塔攻击
                for tw in self.attack_towers:
                    self.money += tw.attack(self.enemys)

                # 循环辅助塔辅助攻击塔
                for tw in self.support_towers:
                    tw.support(self.attack_towers)

                # 生命值小于等于0
                if self.lives <= 0:
                    print("You Lose")
                    run = False

            self.draw()

    def point_to_line(self, tower):
        """
        检测是否可以根据与路径的距离放置塔
        :param tower: Tower
        :return: Bool
        """
        # 找到两个最近的点
        return True

    def draw(self):
        self.win.blit(self.bg, (0, 0))  # blit将游戏背景图渲染到surface上

        # 绘制路径
        #for pos in self.path:
            #pygame.draw.circle(self.win, (255, 0, 0), pos, 5, 0)

        # 绘制炮塔放置时出现的范围环
        if self.moving_object:
            for tower in self.attack_towers:
                tower.draw_placement(self.win)

            for tower in self.support_towers:
                tower.draw_placement(self.win)

            self.moving_object.draw_placement(self.win)

        # 绘制攻击型炮塔
        for tw in self.attack_towers:
            tw.draw(self.win)

        # 绘制辅助型炮塔
        for tw in self.support_towers:
            tw.draw(self.win)

        # 绘制怪物
        for en in self.enemys:
            en.draw(self.win)

        # 重绘选中的塔
        if self.selected_tower:
            self.selected_tower.draw(self.win)

        # 绘制移动物体
        if self.moving_object:
            self.moving_object.draw(self.win)

        # 绘制菜单
        self.menu.draw(self.win)

        # 绘制暂停键
        self.playPauseButton.draw(self.win)

        # 绘制静音键
        self.soundButton.draw(self.win)

        # 绘制生命值
        text = self.life_font.render(str(self.lives), 1, (255, 255, 255))   # text的绘制需要用render
        life = pygame.transform.scale(lives_img, (90, 90))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() + 10, 15))
        self.win.blit(life, (start_x, 5))

        # 绘制金币
        text = self.life_font.render(str(self.money), 1, (255, 255, 255))
        money = pygame.transform.scale(star_img, (50, 50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() + 10, 75))
        self.win.blit(money, (start_x + 20, 85))

        # 绘制当前怪物的波数
        self.win.blit(wave_bg, (10, 10))
        text = self.wave_font.render("Wave #" + str(self.wave), 1, (255, 255, 255))
        self.win.blit(text, (10 + wave_bg.get_width()/2 - text.get_width()/2, 20))

        pygame.display.update()

    def add_tower(self, name):
        '''
        增加炮塔
        :param name: str
        :return: None
        '''
        x, y = pygame.mouse.get_pos()
        name_list = ["buy_archer", "buy_archer_2", "buy_damage", "buy_range"]
        object_list = [ArcherTowerLong(x, y), ArcherTowerShort(x, y), DamageTower(x, y), RangeTower(x, y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        # name不在name_list中的炮塔将会抛出异常
        except Exception as e:
            print(str(e) + "NOT VALID NAME")
