import os

import pygame


class FileImporter:
    @staticmethod
    def file_exists(file_path: str):
        return os.path.exists(os.path.abspath(file_path))

    @staticmethod
    def import_image(file_path: str):
        if FileImporter.file_exists(file_path):
            return pygame.image.load(os.path.abspath(file_path))
        else:
            raise Exception("Path not found!")

    @staticmethod
    def play_music(file_path: str, loops=0, start=0.0):
        if FileImporter.file_exists(file_path):
            pygame.mixer.music.load(os.path.abspath(file_path))
            return pygame.mixer.music.play(loops, start)
        else:
            raise Exception("Path not found!")

    @staticmethod
    def play_audio(file_path: str, loops=0, maxtime=0, fade_ms=0):
        if FileImporter.file_exists(file_path):
            audio = pygame.mixer.Sound(os.path.abspath(file_path))
            return pygame.mixer.Sound.play(audio, loops, maxtime, fade_ms)
        else:
            raise Exception("Path not found!")
