from enum import Enum
import pygame


class ChangeSceneEnum(Enum):
    STARTSCENE = pygame.event.USEREVENT + 1
    HOSTJOINSCENE = pygame.event.USEREVENT + 2
    JOINSCENE = pygame.event.USEREVENT + 3
    HOSTMENUSCENE = pygame.event.USEREVENT + 4
    CREATEGAMEMENU = pygame.event.USEREVENT + 5
    CHARACTERSCENE = pygame.event.USEREVENT + 6
    LOADGAME = pygame.event.USEREVENT + 7
    LOBBYSCENE = pygame.event.USEREVENT + 8
