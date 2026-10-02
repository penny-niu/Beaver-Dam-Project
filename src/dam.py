import pygame
import math
from settings import (DAM_COLOUR, DAM_WIDTH, DAM_INITIAL_HEIGHT,
                      DAM_WIDTH_HEIGHT_RATIO, TOP_VIEW_SCALE)


class Dam:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.width = DAM_WIDTH
        self.height = DAM_INITIAL_HEIGHT
        self.thickness = DAM_WIDTH_HEIGHT_RATIO * self.height

        # Triangular cross-section: V = 1/2 * W * T * H
        self.initial_volume = (
            0.5 * self.width * self.thickness * self.height
        )

        self.material_volume = 0.0  # Total usable wood volume delivered to the dam


    def add_material(self, volume):

        self.material_volume += volume
        self.update_geometry()


    def set_height(self, height):
        """Set a completed-dam height and apply the geometric ratio."""

        self.height = max(0.0, height)
        self.thickness = DAM_WIDTH_HEIGHT_RATIO * self.height
        self.initial_volume = (
            0.5 * self.width * self.thickness * self.height
        )
        self.material_volume = 0.0


    def update_geometry(self):

        ratio = DAM_WIDTH_HEIGHT_RATIO
        total_volume = self.initial_volume + self.material_volume

        # Triangular cross-section:
        # V = 1/2 * W * T * H
        # T = ratio * H
        #
        # Therefore:
        # V = 1/2 * W * ratio * H^2
        # H = sqrt(2V / (W * ratio))

        if total_volume <= 0.0:
            self.height = 0.0
            self.thickness = 0.0
            return

        self.height = math.sqrt(
            2.0 * total_volume / (self.width * ratio)
        )
        self.thickness = ratio * self.height


    def draw(self, screen):

        x_px = self.x * TOP_VIEW_SCALE
        y_px = self.y * TOP_VIEW_SCALE
        width_px = self.width * TOP_VIEW_SCALE
        thickness_px = self.thickness * TOP_VIEW_SCALE

        pygame.draw.rect(
            screen,
            DAM_COLOUR,
            (int(x_px), int(y_px), int(width_px), int(thickness_px))
        )
