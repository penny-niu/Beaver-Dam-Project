import pygame
from settings import (HEIGHT, RIVER_COLOUR, RIVER_WIDTH, WIDTH, INITIAL_RIVER_DEPTH, TOP_VIEW_SCALE, 
                      MAX_WATER_DEPTH, UPSTREAM_REACH_LENGTH, DOWNSTREAM_REACH_LENGTH, INFLOW_RATE, 
                      DOWNSTREAM_OUTFLOW_RATE, WEIR_COEFFICINT, HYDRAULIC_CONDUCTIVITY)


class River:

    def __init__(self):

        world_width_m = WIDTH / TOP_VIEW_SCALE

        self.width = RIVER_WIDTH

        self.x = (world_width_m - self.width) / 2
    
        self.initial_upstream_depth = INITIAL_RIVER_DEPTH
        self.upstream_depth = INITIAL_RIVER_DEPTH
        self.downstream_depth = INITIAL_RIVER_DEPTH

        self.q_overtop = 0.0
        self.q_leak = 0.0
        self.q_dam = 0.0

        self.dH_upstream_dt = 0.0
        self.dH_downstream_dt = 0.0
        
        self.hydraulic_conductivity = HYDRAULIC_CONDUCTIVITY


    def update_water_level(self, dam, dt):

        # storage areas

        upstream_area = (self.width * UPSTREAM_REACH_LENGTH)

        downstream_area = (self.width * DOWNSTREAM_REACH_LENGTH)


        # overtopping flow
        
            # If downstream water is below the dam crest,
            # the crest controls the overflow.
            # If downstream water rises above the crest,
            # the dam is submerged and the downstream
            # water level reduces the driving head.

        controlling_level = max(dam.height, self.downstream_depth)
        
        overflow_head = max(self.upstream_depth - controlling_level, 0.0)
        
        self.q_overtop = (WEIR_COEFFICINT * dam.width * overflow_head ** 1.5)


        # leakage through dam

        head_difference = max(self.upstream_depth - self.downstream_depth, 0.0)

        submerged_height = min(self.upstream_depth, dam.height)

        wetted_area = (dam.width * submerged_height)

        if dam.thickness > 0.0 and submerged_height > 0.0:
            self.q_leak = (
                self.hydraulic_conductivity
                * wetted_area
                * head_difference
                / dam.thickness
            )
        else:
            self.q_leak = 0.0


        # total flow through / over dam

        self.q_dam = self.q_overtop + self.q_leak


        # upstream water balance

        self.dH_upstream_dt = (INFLOW_RATE - self.q_dam) / upstream_area

        self.upstream_depth += (self.dH_upstream_dt * dt)


        # downstream water balance

        self.dH_downstream_dt = (self.q_dam - DOWNSTREAM_OUTFLOW_RATE) / downstream_area

        self.downstream_depth += (self.dH_downstream_dt * dt)


        # physical limits

        self.upstream_depth = max(0.0,
                                  min(self.upstream_depth, MAX_WATER_DEPTH ))

        self.downstream_depth = max(0.0,
                                    min(self.downstream_depth, MAX_WATER_DEPTH))


    

    def draw(self, screen):

        x_px = self.x * TOP_VIEW_SCALE
        width_px = self.width * TOP_VIEW_SCALE

        pygame.draw.rect(screen, 
                         RIVER_COLOUR, 
                         (int(x_px), 0, int(width_px), HEIGHT))
   