import pygame
from settings import(WIDTH, HEIGHT, SIDE_VIEW_SCALE)


class SideView:

    def __init__(self):

        self.view_left = 150
        self.view_right = WIDTH - 150
        
        self.riverbed_y = HEIGHT - 140
        self.dam_x = WIDTH // 2
    
        self.riverbed_depth = 140
    


    def draw(self, screen, river, dam):

        screen.fill((240, 240, 240))

        upstream_water_height_px = river.upstream_depth * SIDE_VIEW_SCALE
        downstream_water_height_px = (river.downstream_depth * SIDE_VIEW_SCALE)

        dam_height_px = dam.height * SIDE_VIEW_SCALE
        dam_thickness_px = dam.thickness * SIDE_VIEW_SCALE

        upstream_surface_y = self.riverbed_y - upstream_water_height_px
        downstream_surface_y = self.riverbed_y - downstream_water_height_px

  
#riverbed        
        pygame.draw.rect(screen, 
                         (190, 160, 105), 
                         (self.view_left, self.riverbed_y, self.view_right - self.view_left,self.riverbed_depth))



# ============================================================
# Dam geometry in the side view
# ============================================================

# Total base width = dam thickness.
# The upstream face is intentionally shallower than the downstream face.
        upstream_base_x = self.dam_x - 0.70 * dam_thickness_px
        downstream_base_x = self.dam_x + 0.30 * dam_thickness_px
        crest_x = self.dam_x
        dam_top_y = self.riverbed_y - dam_height_px


# ============================================================
# Water meeting the triangular dam
# ============================================================

        if dam_height_px > 0:

    # ----- Upstream intersection -----
    # Fraction of dam height reached by the upstream water.
            upstream_fraction = min(
                max(upstream_water_height_px / dam_height_px, 0.0),
                1.0)

    # Move along the upstream slope from base to crest.
            upstream_intersection_x = (
                upstream_base_x
                + upstream_fraction * (crest_x - upstream_base_x) )

    # ----- Downstream intersection -----
            downstream_fraction = min(
                max(downstream_water_height_px / dam_height_px, 0.0),
                1.0)

    # Move along the downstream slope from base to crest.
            downstream_intersection_x = (
                downstream_base_x
                + downstream_fraction * (crest_x - downstream_base_x))

        else:
    # Safe fallback before any dam has been built.
            upstream_intersection_x = self.dam_x
            downstream_intersection_x = self.dam_x


# ============================================================
# Upstream water
# ============================================================
        if upstream_water_height_px < dam_height_px:
            # water surface intersects the upstream face of the dam
            upstream_fraction = upstream_water_height_px / dam_height_px
            
            upstream_intersection_x = (upstream_base_x + 
                                       upstream_fraction * (crest_x - upstream_base_x))
            
            upstream_water_points = [(int(self.view_left),int(upstream_surface_y)),
                                     (int(upstream_intersection_x), int(upstream_surface_y)),
                                     (int(upstream_base_x), int(self.riverbed_y)),
                                     (int(self.view_left), int(self.riverbed_y))]
            
        else:
            # water has reached or passed the dam crest
            upstream_water_points = [(int(self.view_left), int(upstream_surface_y)),
                                      (int(crest_x), int(upstream_surface_y)),
                                      (int(crest_x), int(self.riverbed_y)),
                                      (int(self.view_left), int(self.riverbed_y))]
            
                                     
                                      
        pygame.draw.polygon(screen,
                            (100, 170, 230),
                            upstream_water_points)
    
        


# ============================================================
# Downstream water
# ============================================================

        if downstream_water_height_px < dam_height_px:
            #water surface inrersects the downstream face
            downstream_fraction = downstream_water_height_px / dam_height_px
            
            downstream_intersection_x = (downstream_base_x +
                                         downstream_fraction * (crest_x - downstream_base_x))
            
            downstream_water_points = [
                (int(downstream_intersection_x), int(downstream_surface_y)),
                (int(self.view_right), int(downstream_surface_y)),
                (int(self.view_right), int(self.riverbed_y)),
                (int(downstream_base_x), int(self.riverbed_y))]

        else:
            # Downstream water has reached or passed the crest
            downstream_water_points = [
                (int(crest_x), int(downstream_surface_y)),
                (int(self.view_right), int(downstream_surface_y)),
                (int(self.view_right), int(self.riverbed_y)),
                (int(crest_x), int(self.riverbed_y))]

        
        pygame.draw.polygon(screen,
                            (100, 170, 230),
                            downstream_water_points)



# ============================================================
# Dam drawn last, so it sits in front of the water
# ============================================================

        pygame.draw.polygon(screen,
                            (110, 75, 45),
                            [(int(upstream_base_x), int(self.riverbed_y)),
                            (int(crest_x), int(dam_top_y)),
                            (int(downstream_base_x), int(self.riverbed_y))])



#labels            
        font = pygame.font.Font(None, 28)

        hu_text = font.render( f"H_u = {river.upstream_depth:.2f}m", 
                                 True, 
                                 (0, 0, 0))

        hd_text = font.render( f"H_d = {dam.height:.2f}m", 
                               True, 
                               (0, 0, 0))

        hdown_text = font.render(f"H_down = {river.downstream_depth:.2f}m",
                                 True,
                                 (0,0,0))

        thickness_text = font.render( f"T_d = {dam.thickness:.2f}m",
                                     True,
                                     (0, 0, 0))
                                     

        upstream_text = font.render("Upstream",
                                    True, 
                                    (0, 0, 0))

        downstream_text = font.render("Downstream",
                                      True,
                                      (0, 0, 0))
        

        screen.blit(hu_text, (20, 20))
        screen.blit(hd_text, (20, 50))
        screen.blit(thickness_text, (20, 80))
        screen.blit(hdown_text, (20,110))

        screen.blit(upstream_text, 
                    (WIDTH // 4 - 40,
                      self.riverbed_y + 20))
        
        screen.blit(downstream_text,
                    (3 * WIDTH // 4 - 50,
                     self.riverbed_y + 20))