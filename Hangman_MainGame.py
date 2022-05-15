import pygame
from pygame import mixer
import math
import random
import json  # Import Wordlist
import os

# word data loading ...
data = json.load(open('Word_list.json'))
Wordlist = data['data']  # parse data

# song data loading
mixer.pre_init(44100, 16, 1, 512)
mixer.init()
BASE_DIR = os.getcwd()
SOUND_EFFECTS = {
    "wrong": mixer.Sound(os.path.join(BASE_DIR, "musics/wrong.wav")),
    "correct": mixer.Sound(os.path.join(BASE_DIR, "musics/correct.wav")),
    "won": mixer.Sound(os.path.join(BASE_DIR, "musics/won.wav")),
    "background": mixer.Sound(os.path.join(BASE_DIR, "musics/background.wav")),
    "background2": mixer.Sound(os.path.join(BASE_DIR, "musics/background2.mp3")),
    "lost": mixer.Sound(os.path.join(BASE_DIR, "musics/lost.mp3")),
    "menu": mixer.Sound(os.path.join(BASE_DIR, "musics/menu.wav")),
}

# Initialize the game
pygame.init()
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hangman Game")
LOGO = "hang_icon.png"
pygame.display.set_icon(pygame.image.load(LOGO))

# font
Menu_Font = pygame.font.SysFont('timesnewroman', 45)
Letter_Font = pygame.font.SysFont('timesnewroman', 30)
Guessed_Font = pygame.font.SysFont('timesnewroman', 40)
Message_Font = pygame.font.SysFont('timesnewroman', 50)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (255, 0, 0)

# Load Images
Images = []
for i in range(7):
    Image = pygame.image.load("hangman" + str(i) + ".png")
    Images.append(Image)

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((width - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65


def Letter():
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (RADIUS * 2 + GAP))
        letters.append([x, y, chr(A + i), True])
    return letters


# Word
# Choose randomly a word from the Wordlist
def get_valid_word(Wordlist):
    word = random.choice(Wordlist)  # randomly chooses something from the list
    while '-' in word or ' ' in word:
        word = random.choice(Wordlist)

    return word.upper()


# draw
def draw():
    win.fill(WHITE)

    # SOUND_EFFECTS.get("background").play()

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = Guessed_Font.render(display_word, True, GREEN)
    win.blit(text, [330, 200])

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, [x, y], RADIUS, 2)
            text = Letter_Font.render(ltr, True, BLACK)
            win.blit(text, [x - text.get_width() / 2, y - text.get_height() / 2])

    win.blit(Images[hangman_status], [70, 50])
    pygame.display.update()


def display_window(Result):
    if Result:
        message = "YOU WON!"
        win.fill(WHITE)
        text = Message_Font.render(message, True, GREEN)
        win.blit(text, [(width - text.get_width()) / 2, (height - text.get_height()) / 2])
        pygame.display.update()
        pygame.time.delay(5000)
    else:
        message = "YOU LOST!"
        win.fill(BLACK)
        text = Message_Font.render(message, True, RED)
        win.blit(text, [(width - text.get_width()) / 2, (height - text.get_height()) / 2])
        pygame.display.update()
        pygame.time.delay(5000)


def reset_game():
    global word, guessed, letters
    word = get_valid_word(Wordlist)
    guessed = []
    letters = Letter()


# Main Loop
def main_loop():
    # Game Status
    global hangman_status
    hangman_status = 0

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis <= RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr in word:
                                SOUND_EFFECTS.get("correct").play(maxtime=300)
                            if ltr not in word:
                                SOUND_EFFECTS.get("wrong").play(maxtime=400)
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False

        if won:
            pygame.time.delay(500)
            SOUND_EFFECTS.get("won").play(maxtime=5000)
            pygame.time.delay(1000)
            Result = True
            display_window(Result)
            break

        if hangman_status >= 6:
            pygame.time.delay(300)
            SOUND_EFFECTS.get("lost").play(maxtime=3500)
            pygame.time.delay(1000)
            Result = False
            display_window(Result)
            break


def main_menu():
    FPS = 60
    clock = pygame.time.Clock()

    menu = True
    while menu:
        clock.tick(FPS)

        win.fill(BLACK)
        menu_text = Menu_Font.render('Please Enter Any Key to Start Game', True, GREEN)
        win.blit(menu_text, ((width - menu_text.get_width()) / 2, (height - menu_text.get_height()) / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
                reset_game()
                main_loop()

        menu = True


main_menu()
