import pandas as pd
from scipy.optimize import root_scalar

from settings import (RIVER_WIDTH,INITIAL_RIVER_DEPTH,
                      UPSTREAM_REACH_LENGTH,DOWNSTREAM_REACH_LENGTH,
                      INFLOW_RATE,WEIR_COEFFICINT)


# LOAD SIMULATION RESULTS

results = pd.read_csv("results/data/permeability_experiment.csv")


# WATER STORAGE

upstream_area = ( RIVER_WIDTH * UPSTREAM_REACH_LENGTH)

downstream_area = (RIVER_WIDTH * DOWNSTREAM_REACH_LENGTH)

total_water_volume = (upstream_area + downstream_area) * INITIAL_RIVER_DEPTH


# EQUILIBRIUM EQUATION

def flow_residual(delta_h, hydraulic_conductivity, dam_height, dam_thickness):

    downstream_depth = ((total_water_volume - upstream_area * delta_h) / 
                        (upstream_area + downstream_area))

    upstream_depth = (downstream_depth + delta_h)


    # Overtopping

    controlling_level = max(dam_height, downstream_depth)

    overflow_head = max(upstream_depth - controlling_level, 0.0)

    q_overtop = (WEIR_COEFFICINT * RIVER_WIDTH * overflow_head ** 1.5)


    # Leakage

    submerged_height = min(upstream_depth, dam_height)

    wetted_area = (RIVER_WIDTH * submerged_height)

    q_leak = (hydraulic_conductivity * wetted_area * delta_h / dam_thickness)

    q_dam = q_overtop + q_leak

    return INFLOW_RATE - q_dam


# SCIPY ROOT FINDING

scipy_head_differences = []
absolute_errors = []


for _, row in results.iterrows():

    solution = root_scalar(flow_residual,
                           args=(row["hydraulic_conductivity"],
                                 row["dam_height"],
                                 row["dam_thickness"]),
                           bracket=[0.0, 0.72],
                           method="brentq")

    scipy_delta_h = solution.root

    scipy_head_differences.append(scipy_delta_h)

    absolute_errors.append(abs(scipy_delta_h - row["head_difference"]))


# COMPARE WITH TIME-STEPPING SIMULATION

results["scipy_head_difference"] = (scipy_head_differences)

results["absolute_error"] = (absolute_errors)


print(results[["hydraulic_conductivity",
               "head_difference",
               "scipy_head_difference",
               "absolute_error"]])

print("\nMaximum absolute error:", results["absolute_error"].max())