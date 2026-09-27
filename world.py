import pygame
from river import River
from tree import Tree
from beaver import Beaver
from dam import Dam
import random
from settings import (TREE_MODE_HEIGHT, TREE_MODE_WIDTH, WIDTH, HEIGHT, TREE_RIVER_GAP, 
                      TREE_MAX_WIDTH, TREE_MAX_HEIGHT, TOP_VIEW_SCALE, INFLOW_RATE, 
                      DOWNSTREAM_OUTFLOW_RATE, EQUILIBRIUM_FLOW_TOLERANCE, EQUILIBRIUM_HOLD_TIME)


class World:

    def __init__(self):

        random.seed(42)

        self.world_width = WIDTH / TOP_VIEW_SCALE
        self.world_height = HEIGHT / TOP_VIEW_SCALE

        self.river = River()

        self.trees = []

        self.beaver = Beaver(4.2, 4.0)

        self.dam = Dam(self.river.x, self.world_height / 2)

        self.phase = "construction"

        self.settling_time = 0.0
        self.equilibrium_hold_time = 0.0

        self.equilibrium_reached = False
        self.equilibrium_result = None

        river_left = self.river.x
        river_right = self.river.x + self.river.width

        for i in range(80):

            attempts = 0
            while True:

                if random.random() < 0.5:
                    x = random.uniform(0, river_left - TREE_RIVER_GAP - TREE_MAX_WIDTH)

                else:
                    x = random.uniform(river_right + TREE_RIVER_GAP,
                                        self.world_width - TREE_MAX_WIDTH)

                y = random.uniform(0, self.world_height - TREE_MAX_HEIGHT)

                if self.is_position_valid(x, y):
                    break

                attempts += 1

                if attempts > 100:
                    break

            tree = Tree(x, y)
            self.trees.append(tree)
        


    def is_position_valid(self, x, y):

        for existing_tree in self.trees:

            dx = abs(existing_tree.x - x)
            dy = abs(existing_tree.y - y)

            if dx < (TREE_MODE_WIDTH + 0.05) and dy < (TREE_MODE_HEIGHT + 0.05):
                return False
   
        return True


    def draw(self, screen):

        self.river.draw(screen)

        for tree in self.trees:
            tree.draw(screen)

        self.beaver.draw(screen)
        self.dam.draw(screen)

        font = pygame.font.Font(None, 30)

        text = font.render(f"Dam height: {self.dam.height:.3f}m", 
                           True, 
                           (0, 0, 0))
        
        screen.blit(text, (10, 10))



    def update(self, dt):

    # =====================================
    # PHASE 1: Beaver builds the dam
    # =====================================

        if self.phase == "construction":

            self.beaver.update(dt,
                               self.trees,
                               self.dam)

            self.river.update_water_level(self.dam,
                                          dt)

        # All trees have been used and the beaver
        # has finished its final delivery
            if len(self.trees) == 0 and self.beaver.state == "idle":

                self.phase = "settling"

                print("\nConstruction finished.")
                print("Hydrology is now settling...")
                print(f"Final dam height: {self.dam.height:.3f} m")
                print(f"Final dam thickness: {self.dam.thickness:.3f} m")
                print(f"Total delivered wood volume: "f"{self.dam.material_volume:.6f} m^3")


    # =====================================
    # PHASE 2: Dam frozen, water keeps moving
    # =====================================

        elif self.phase == "settling":

            self.settling_time += dt

        # IMPORTANT:
        # Beaver is no longer updated.
        # Dam geometry therefore remains fixed.

            self.river.update_water_level(self.dam,
                                          dt)

            upstream_balanced = (abs(INFLOW_RATE - self.river.q_dam)
                                 < EQUILIBRIUM_FLOW_TOLERANCE)

            downstream_balanced = (abs(self.river.q_dam
                                       - DOWNSTREAM_OUTFLOW_RATE)
                                   < EQUILIBRIUM_FLOW_TOLERANCE)

            if upstream_balanced and downstream_balanced:

                self.equilibrium_hold_time += dt

            else:

                self.equilibrium_hold_time = 0.0

        # Conditions have remained stable long enough
            if (self.equilibrium_hold_time >= EQUILIBRIUM_HOLD_TIME):

                self.phase = "equilibrium"
                self.equilibrium_reached = True

                self.equilibrium_result = {"dam_height": self.dam.height,
                                           "dam_thickness": self.dam.thickness,
                                           "upstream_depth": self.river.upstream_depth,
                                           "downstream_depth":self.river.downstream_depth,
                                           "head_difference": self.river.upstream_depth - self.river.downstream_depth,
                                           "q_leak":self.river.q_leak,
                                           "q_overtop":self.river.q_overtop,
                                           "q_dam": self.river.q_dam,
                                           "settling_time":self.settling_time}

                print("\n============================")
                print("EQUILIBRIUM REACHED")
                print("============================")

                print(f"Upstream depth: "
                      f"{self.river.upstream_depth:.3f} m")

                print(f"Downstream depth: "
                      f"{self.river.downstream_depth:.3f} m")
                print(f"Head difference: "
                      f"{self.equilibrium_result['head_difference']:.3f} m")

                print(f"Dam flow: "
                      f"{self.river.q_dam:.5f} m^3/s")

                print(f"Leakage: "
                      f"{self.river.q_leak:.5f} m^3/s")

                print(f"Overtopping: "
                      f"{self.river.q_overtop:.5f} m^3/s")

                print(f"Settling time: "
                      f"{self.settling_time:.1f} s")