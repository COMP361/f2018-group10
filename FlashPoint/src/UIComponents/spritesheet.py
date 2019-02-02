from typing import List, Tuple

import pygame
from src.UIComponents.FileImporter import FileImporter


class Spritesheet(object):
    """Loader for sprite sheets. Provides an interface for dealing with visual sprites."""

    def __init__(self, filename: str, cols: int, rows: int):
        try:
            self._sheet = FileImporter.import_image(filename)
        except pygame.error as e:
            print("Unable to load spritesheet image:", filename)
            raise e

        self._num_cols = cols
        self._num_rows = rows
        self._total_cells = cols*rows

        self.rect = self._sheet.get_rect()
        width = self._cell_width = int(self.rect.width/cols)
        height = self._cell_height = int(self.rect.height/rows)

        # Index to loop through the animation
        self._index = 0.0

        # Create a list of rects
        self._cell_rects = [[(i*width, j*height, width, height) for i in range(cols)] for j in range(rows)]
        self.cell_images = self._load_images(self._cell_rects)

    def _image_at(self, rect):
        """Return a surface image for a specific Rect area."""
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self._sheet, (0, 0), rect)
        return image

    def _load_images(self, cells: List[List[Tuple]]):
        """Load a list of images"""
        return [[self._image_at(rect) for rect in l] for l in cells]


class SpriteAnimation(object):

    def __init__(self, sprite_sheet: Spritesheet, frame_rate: int=12, loop: bool=True, reverse: bool=False):
        self._frame_rate = frame_rate
        self._sheet = sprite_sheet
        self._loop = loop
        self._reverse = reverse

        self._frame_buffer = frame_rate
        self._index = 0

    def __iter__(self):
        self.i = 0
        self._frame_buffer = self._frame_rate
        return self

    def __next__(self):
        if self._index >= len(self._sheet.cell_images):
            if not self._loop:
                raise StopIteration
            else:
                self._index = 0
        image = self._sheet.cell_images[self._index]

        self._frame_buffer -= 1
        if self._frame_buffer == 0:
            self._index += 1
            self._frame_buffer = self._frame_rate
        return image
