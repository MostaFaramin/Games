import pygame

pygame.init()
width, height = 800, 600
win = pygame.display.set_mode((width, height))
Menu_Font = pygame.font.SysFont('timesnewroman', 60)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
RED = (255, 0, 0)


def MainMenu():
    menu = True
    while menu:
        win.fill(RED)
        menu_text = Menu_Font.render('Menu', True, GREEN)
        win.blit(menu_text, ((width - menu_text.get_width()) / 2, (height - menu_text.get_height()) / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                menu = False
                win.fill(WHITE)
                pygame.display.update()


MainMenu()
# pygame.quit()
