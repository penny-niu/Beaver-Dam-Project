WIDTH = 1200
HEIGHT = 800
TITLE = "Beaver Simulation"
FPS = 60



# COLOURS

BACKGROUND_COLOUR = (120, 130, 82) #Green
RIVER_COLOUR = (150, 200, 210) #Blue

TREE_COLOURS = {'aspen': (255, 215, 0), #Gold
                 'willow': (154, 205, 50),  #Yellow Green
                 'cottonwood': (173, 255, 47), #Green Yellow
                 'oak': (139, 69, 19), #Saddle Brown
                 'pine': (0, 100, 0), #Dark Green
                 'fir': (0,80, 0)} #Darker Green

BEAVER_COLOUR = (101, 67,33)
DAM_COLOUR = (139, 69, 19) #Saddle Brown



# SCALES (pixels per metre)

TOP_VIEW_SCALE = 100
SIDE_VIEW_SCALE = 350



# RIVER - PHYSICAL UNITS (metres)

RIVER_WIDTH = 3.0  
INITIAL_RIVER_DEPTH = 0.36
MAX_WATER_DEPTH = 1.5



# TREES - PHYSICAL UNITS （metres）
TREE_RIVER_GAP = 0.5

SPECIES_PROBABILITIES = {"aspen": 0.25, 
                         'willow': 0.25, 
                         'cottonwood': 0.15, 
                         'oak': 0.15,
                         'pine': 0.10, 
                         'fir': 0.10}

PREFERRED_SPECIES = ['aspen', 'willow', 'cottonwood']
AVOIDED_SPECIES = ['oak', 'pine', 'fir']

# effective usable wood diameter & length
TREE_MIN_WIDTH = 0.05
TREE_MAX_WIDTH = 0.30
TREE_MODE_WIDTH = 0.15

TREE_MIN_HEIGHT = 0.20
TREE_MAX_HEIGHT = 0.80
TREE_MODE_HEIGHT = 0.40



# BEAVER - PHYSICAL UNITS (metres)

BEAVER_RADIUS = 0.12

BEAVER_SPEED = 10.0 # metre per second

PREFFERED_FACTOR = 1.0
AVOIDED_FACTOR = 0.2

CUTTING_COST_PER_WIDTH = 0.5



# DAM - PHYSICAL UNITS (metres)

DAM_WIDTH = RIVER_WIDTH

DAM_INITIAL_HEIGHT = 0.0

# Wooden beaver dams are approximated with a triangular cross-section.
# Muller & Watling, in "The engineering in beaver dams", report an average
# cross-sectional width-to-height ratio of 2.9 for wooden dams. Here the
# cross-sectional width is represented
# by the streamwise dam thickness.
DAM_WIDTH_HEIGHT_RATIO = 2.9



# WATER FLOW

UPSTREAM_REACH_LENGTH = 4.0    # metres
DOWNSTREAM_REACH_LENGTH = 4.0 

INFLOW_RATE = 0.05             # m^3/s
DOWNSTREAM_OUTFLOW_RATE = 0.05

WEIR_COEFFICINT = 1.7

HYDRAULIC_CONDUCTIVITY = 0.01   # m/s, assumed provisional value

EQUILIBRIUM_FLOW_TOLERANCE = 0.0001
EQUILIBRIUM_HOLD_TIME = 5.0