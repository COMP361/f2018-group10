import os

import pygame


class FileImporter:
    @staticmethod
    def file_exists(file_path: str):
        return os.path.exists(file_path)

    @staticmethod
    def import_image(file_path: str):
        if FileImporter.file_exists(file_path):
            image = pygame.image.load(os.path.abspath(file_path))
            return image
        else:
            raise Exception("Path not found!")
