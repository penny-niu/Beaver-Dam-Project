import pygame
import math
from settings import (BEAVER_COLOUR, BEAVER_RADIUS, BEAVER_SPEED, 
                      PREFFERED_FACTOR, AVOIDED_FACTOR, CUTTING_COST_PER_WIDTH,TOP_VIEW_SCALE)


class Beaver:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.speed = BEAVER_SPEED

        self.target_tree = None
        self.carried_tree = None

        self.state = "idle"  # Possible states: "idle", "moving", "cutting"



    def select_tree(self, trees):
        """Choose the best tree based on Central Foragind Theory score."""
        if not trees:
            return None

        best_tree = None
        best_score = -1.0

        for tree in trees:

            if tree.is_preferred:
                preference = PREFFERED_FACTOR
            else:
                preference = AVOIDED_FACTOR

            value = tree.width * tree.height * preference

            dx = tree.x - self.x
            dy = tree.y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            cutting_cost = tree.width * CUTTING_COST_PER_WIDTH

            score = value / (distance + cutting_cost + 1)  # +1 to avoid division by zero

            if score > best_score:
                best_score = score
                best_tree = tree

        return best_tree



    def update(self, dt, trees, dam):

        if self.state == 'idle'and self.target_tree is None:

            self.target_tree = self.select_tree(trees)

            if self.target_tree is not None:
                self.state = "moving"
            else:
                self.state = "idle"

        if self.state == "moving":

            target = self.target_tree
            
            dx = target.x - self.x
            dy = target.y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            step = self.speed * dt   # How far the Beaver can travel in this single update

            if distance <= step:

                self.x = target.x
                self.y = target.y
                self.state = "cutting"

            else:
            
                self.x += (dx / distance) * step
                self.y += (dy / distance) * step


        if self.state == "cutting":
            if self.target_tree in trees:
                trees.remove(self.target_tree)

            self.carried_tree = self.target_tree
            self.target_tree = None
            self.state = "carrying_to_dam"


        if self.state == "carrying_to_dam":

            target_x = dam.x + dam.width / 2
            target_y = dam.y + dam.thickness / 2

            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)


            step = self.speed * dt

            if distance <= step:

                self.x = target_x
                self.y = target_y

                dam.add_material(self.carried_tree.volume)

                self.state = "idle"
                self.carried_tree = None

            else:

                self.x += (dx / distance) * step
                self.y += (dy / distance) * step



    def draw(self, screen):

        x_px = self.x * TOP_VIEW_SCALE
        y_px = self.y * TOP_VIEW_SCALE
        radius_px = BEAVER_RADIUS * TOP_VIEW_SCALE

        pygame.draw.circle(screen, 
                           BEAVER_COLOUR, 
                           (int(x_px), int(y_px)), 
                           int(radius_px))
        
        font = pygame.font.Font(None, 24)

        text = font.render(self.state,
                            True, 
                            (0, 0, 0))
        
        screen.blit(text, (int(x_px + 20), int(y_px - 20)))






        