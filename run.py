import pygame

if __name__ == "__main__":
    pygame.init()  # 初始化
    win = pygame.display.set_mode((1350, 700))  # 游戏窗口大小
    from main_menu.main_menu import MainMenu
    mainMenu = MainMenu(win)
    mainMenu.run()
