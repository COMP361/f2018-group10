import pygame

from src.UIComponents.FileImporter import FileImporter


class Spritesheet(object):
    def __init__(self, filename: str, cols: int, rows: int):
        self._sheet = FileImporter.import_image(filename)

        self.cols = cols
        self.rows = rows
        self.total_cell_count = cols*rows

        self.rect = self.sheet.get_rect()
        w = self.cell_width = self.rect.width/cols
        h = self.cell_height = self.rect.height/rows
        hw, hh = self.cell_center = (self.cell_width/2, self.cell_height/2)

        self.cells = [(index % cols * w, index / cols*h, w, h) for index in range(self.total_cell_count)]
        self.handle = [
            (0, 0), (-hw, 0), (-w, 0),
            (0, -hh), (-hw, -hh), (-w, -hh),
            (0, -h), (-hw, -h), (-w, -h), ]

    def draw(self, surface, cell_index, x, y, handle=0):
        surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[cell_index])
