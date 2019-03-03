import pygame


class ChangeSceneEnum(object):
    STARTSCENE = pygame.USEREVENT + 1
    HOSTJOINSCENE = pygame.USEREVENT + 2
    JOINSCENE = pygame.USEREVENT + 3
    HOSTMENUSCENE = pygame.USEREVENT + 4
    CREATEGAMEMENU = pygame.USEREVENT + 5
    CHARACTERSCENE = pygame.USEREVENT + 6
    LOADGAME = pygame.USEREVENT + 7
    LOBBYSCENE = pygame.USEREVENT + 8
    GAMEBOARDSCENE = pygame.USEREVENT + 9
    REGISTER = pygame.USEREVENT + 10
