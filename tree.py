import pygame
from settings import (TREE_COLOURS, SPECIES_PROBABILITIES, PREFERRED_SPECIES, 
                      AVOIDED_SPECIES, TREE_MIN_WIDTH, TREE_MAX_WIDTH, TREE_MODE_WIDTH, 
                      TREE_MIN_HEIGHT, TREE_MAX_HEIGHT, TREE_MODE_HEIGHT, TOP_VIEW_SCALE)
import random
import math


class Tree:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.species = random.choices(list(SPECIES_PROBABILITIES.keys()),
                                        weights = list(SPECIES_PROBABILITIES.values()))[0]
        
        self.width = random.triangular(TREE_MIN_WIDTH, TREE_MAX_WIDTH, TREE_MODE_WIDTH)
        self.height = random.triangular(TREE_MIN_HEIGHT, TREE_MAX_HEIGHT, TREE_MODE_HEIGHT)
        self.volume = math.pi * (self.width / 2) ** 2 * self.height

        self.is_preferred = self.species in PREFERRED_SPECIES
   

    def draw(self, screen):

        x_px = self.x * TOP_VIEW_SCALE
        y_px = self.y * TOP_VIEW_SCALE

        width_px = self.width * TOP_VIEW_SCALE
        height_px = self.height * TOP_VIEW_SCALE


        pygame.draw.rect(screen, 
                         TREE_COLOURS[self.species], 
                         (int(x_px), int(y_px), int(width_px), int(height_px)))
