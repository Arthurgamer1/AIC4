import pygame
import sys
from button import Button

pygame.init()

# Constant Variables
WIDTH = 1920
HEIGHT = 1080

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

# load a bg image
BG = pygame.image.load("assets/BG1.png")


def get_font(size):
    pass


def play():
    pass


def main_menu():
    pygame.display.set_caption("Menu")

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_GET_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("CONNECT 4 MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
