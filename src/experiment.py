import csv
import os

from river import River
from dam import Dam

from settings import (HEIGHT, TOP_VIEW_SCALE, INFLOW_RATE, DOWNSTREAM_OUTFLOW_RATE,
                      EQUILIBRIUM_FLOW_TOLERANCE, EQUILIBRIUM_HOLD_TIME)


def run_equilibrium_experiment(dam_height, hydraulic_conductivity):

    # Create river

    river = River()
    river.hydraulic_conductivity = hydraulic_conductivity

    world_height = HEIGHT / TOP_VIEW_SCALE
 
 
    # Create finished dam

    dam = Dam(river.x, world_height / 2)

  
    dam.set_height(dam_height)

    
    # Numerical simulation

    dt = 0.1

    time = 0.0
    equilibrium_hold_time = 0.0

    # Safety limit so a failed experiment cannot run forever
    max_time = 5000.0

    while time < max_time:

        river.update_water_level(dam, dt)

        time += dt

        upstream_balanced = (abs(INFLOW_RATE - river.q_dam) 
                             < EQUILIBRIUM_FLOW_TOLERANCE)

        downstream_balanced = (abs(river.q_dam - DOWNSTREAM_OUTFLOW_RATE)
                               < EQUILIBRIUM_FLOW_TOLERANCE)

        if upstream_balanced and downstream_balanced:

            equilibrium_hold_time += dt

        else:

            equilibrium_hold_time = 0.0

        if equilibrium_hold_time >= EQUILIBRIUM_HOLD_TIME:

            return {"dam_height": dam.height,
                    "dam_thickness": dam.thickness, 
                    "upstream_depth": river.upstream_depth, 
                    "downstream_depth": river.downstream_depth,
                    "head_difference": river.upstream_depth - river.downstream_depth,
                    "q_leak": river.q_leak,
                    "q_overtop": river.q_overtop,
                    "q_dam": river.q_dam,
                    "equilibrium_time":time}

    return None




# SAVE EXPERIMENT RESULTS

os.makedirs("results/data", exist_ok=True)


def save_results(filename, results, independent_variable):

    fieldnames = [independent_variable,
                  "dam_height",
                  "dam_thickness",
                  "upstream_depth",
                  "downstream_depth",
                  "head_difference",
                  "q_leak",
                  "q_overtop",
                  "q_dam",
                  "equilibrium_time"]

    with open(filename, "w", newline="") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for result in results:
            writer.writerow(result)



# EXPERIMENT 1


dam_heights = [0.20,
               0.30,
               0.32,
               0.34,
               0.36,
               0.38,
               0.40,
               0.50,
               0.60]

height_results = []

for height in dam_heights:

    result = run_equilibrium_experiment(dam_height=height, hydraulic_conductivity=0.01)

    if result is not None:

        result["hydraulic_conductivity"] = 0.01

        height_results.append(result)


save_results("results/data/dam_height_experiment.csv",
             height_results,
             "hydraulic_conductivity")



# EXPERIMENT 2


conductivities = [0.002,
                  0.005,
                  0.010,
                  0.020,
                  0.050,
                  0.100,
                  0.200,
                  0.250,
                  0.280,
                  0.300,
                  0.310,
                  0.320,
                  0.330,
                  0.350,
                  0.500,
                  0.670]

conductivity_results = []

for conductivity in conductivities:

    result = run_equilibrium_experiment(dam_height=0.4375,
                                        hydraulic_conductivity=conductivity)

    if result is not None:

        result["hydraulic_conductivity"] = conductivity

        conductivity_results.append(result)


save_results("results/data/permeability_experiment.csv",
             conductivity_results,
             "hydraulic_conductivity")


print("\nExperiments complete.")
print("Saved:")
print("results/data/dam_height_experiment.csv")
print("results/data/permeability_experiment.csv")
