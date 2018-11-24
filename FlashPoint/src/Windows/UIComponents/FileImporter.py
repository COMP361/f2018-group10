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
    def import_audio(file_path: str):
        if FileImporter.file_exists(file_path):
            return pygame.mixer.music.load(os.path.abspath(file_path))
        else:
            raise Exception("Path not found!")
