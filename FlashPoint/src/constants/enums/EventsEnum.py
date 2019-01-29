import pygame
from enum import Enum


class EventsEnum(Enum):
    JOIN = pygame.USEREVENT+1               # called when joining a host
    CLIENT_CONNECTED = pygame.USEREVENT+2   # called when a client is connected to local machine

