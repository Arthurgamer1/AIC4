import pygame
import sys
import os
import subprocess
from button import Button

pygame.init()

# Constant Variables
WIDTH = 1280
HEIGHT = 720
CURR_DIR = os.path.dirname(__file__)

# Get Paths
BG_PATH = os.path.join(CURR_DIR, "assets", "BG1.png")
FONT_PATH = os.path.join(CURR_DIR, "assets", "erasfont.ttf")
PLAY_PATH = os.path.join(CURR_DIR, "assets", "PlayB.png")
OPT_PATH = os.path.join(CURR_DIR, "assets", "OptionsB.png")
QUIT_PATH = os.path.join(CURR_DIR, "assets", "QuitB.png")

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")


def get_font(size):
    return pygame.font.Font(FONT_PATH, size)


def scale_image(image, target_width, target_height):
    img_width, img_height = image.get_size()
    scale = min(target_width / img_width, target_height / img_height)
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
    return pygame.transform.scale(image, (new_width, new_height))


def load_and_scale_button(path, target_width, target_height):
    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (target_width, target_height))
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        return None


# Load a background image
BG = pygame.image.load(BG_PATH)
BG = scale_image(BG, WIDTH, HEIGHT)


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(650, 100))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        AI_V_HUMAN = Button(
            image=None,
            pos=(650, 200),
            text_input="HUMAN VS AI",
            font=get_font(75),
            base_color="White",
            hovering_color="Green",
        )

        AI_V_AI = Button(
            image=None,
            pos=(650, 350),
            text_input="AI VS AI",
            font=get_font(75),
            base_color="White",
            hovering_color="Green",
        )

        PLAY_BACK = Button(
            image=None,
            pos=(650, 500),
            text_input="BACK",
            font=get_font(75),
            base_color="White",
            hovering_color="Green",
        )

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        AI_V_HUMAN.changeColor(PLAY_MOUSE_POS)
        AI_V_HUMAN.update(SCREEN)

        AI_V_AI.changeColor(PLAY_MOUSE_POS)
        AI_V_AI.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if AI_V_HUMAN.checkForInput(PLAY_MOUSE_POS):
                    humanAI()
                if AI_V_AI.checkForInput(PLAY_MOUSE_POS):
                    subprocess.Popen(
                        ["python", os.path.join(CURR_DIR, "Visual_MC_Minimax.py")]
                    )

        pygame.display.update()


def humanAI():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("Choose an AI to go against!", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(650, 100))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        MTCS = Button(
            image=None,
            pos=(650, 200),
            text_input="Human VS MTCS Algorithm",
            font=get_font(75),
            base_color="White",
            hovering_color="Green",
        )

        MINIMAX = Button(
            image=None,
            pos=(650, 350),
            text_input="Human vs Minimax Algorithm",
            font=get_font(75),
            base_color="White",
            hovering_color="Green",
        )

        PLAY_BACK = Button(
            image=None,
            pos=(650, 500),
            text_input="BACK",
            font=get_font(75),
            base_color="White",
            hovering_color="Green",
        )

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        MTCS.changeColor(PLAY_MOUSE_POS)
        MTCS.update(SCREEN)

        MINIMAX.changeColor(PLAY_MOUSE_POS)
        MINIMAX.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    play()
                if MTCS.checkForInput(PLAY_MOUSE_POS):
                    subprocess.Popen(
                        [
                            "python",
                            os.path.join(CURR_DIR, "monte_carlo_connect_four.py"),
                        ]
                    )
                if MINIMAX.checkForInput(PLAY_MOUSE_POS):
                    subprocess.Popen(
                        ["python", os.path.join(CURR_DIR, "connect_four.py")]
                    )

        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(
            image=None,
            pos=(640, 460),
            text_input="BACK",
            font=get_font(75),
            base_color="Black",
            hovering_color="Green",
        )

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)

        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    pygame.display.set_caption("Menu")

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_GET_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("CONNECT 4 MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Adjustable Width and Height for Buttons
        button_width = 150
        button_height = 150

        # Menu Buttons
        PLAY_BUTTON = Button(
            image=load_and_scale_button(PLAY_PATH, button_width, button_height),
            pos=(500, 350),
            text_input="",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )
        OPTIONS_BUTTON = Button(
            image=load_and_scale_button(OPT_PATH, button_width, button_height),
            pos=(800, 350),
            text_input="",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )
        QUIT_BUTTON = Button(
            image=load_and_scale_button(QUIT_PATH, button_width, button_height),
            pos=(650, 500),
            text_input="",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        PLAY_BUTTON.update(SCREEN)
        OPTIONS_BUTTON.update(SCREEN)
        QUIT_BUTTON.update(SCREEN)

        # Event Listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_GET_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_GET_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_GET_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
