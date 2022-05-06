from game import Game
import pygame
import os

start_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "fight.png")), (150, 150))
logo = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "logo2.png")), (500, 500))


class MainMenu:
    '''
    进入游戏时加载的开始菜单
    '''
    def __init__(self, win):
        self.width = 1350
        self.height = 700
        self.bg = pygame.image.load(os.path.join("game_assets", "bg2.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.win = win
        self.btn = (self.width/2 - start_btn.get_width()/2, 350, start_btn.get_width(), start_btn.get_height())

    def run(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:
                    # 检测是否点击开始按钮
                    x, y = pygame.mouse.get_pos()

                    if self.btn[0] <= x <= self.btn[0] + self.btn[2]:
                        if self.btn[1] <= y <= self.btn[1] + self.btn[3]:
                            game = Game(self.win)
                            game.run()
                            del game
            self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0, 0))
        self.win.blit(logo, (self.width/2 - logo.get_width()/2, -80))
        self.win.blit(start_btn, (self.btn[0], self.btn[1]))
        pygame.display.update()
