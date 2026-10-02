import os
import pandas as pd
import matplotlib.pyplot as plt


# SETUP

os.makedirs("results", exist_ok=True)



# LOAD EXPERIMENT DATA

height_results = pd.read_csv("results/data/dam_height_experiment.csv" )

permeability_results = pd.read_csv ("results/data/permeability_experiment.csv")


height_results = height_results.sort_values("dam_height")

permeability_results = permeability_results.sort_values("hydraulic_conductivity")



# EXPERIMENT 1

dam_heights = height_results["dam_height"]

head_differences_height = height_results["head_difference"]


fig = plt.figure(figsize=(11, 6))

grid = fig.add_gridspec(
    1,
    2,
    width_ratios=[3, 1]
)

ax = fig.add_subplot(grid[0, 0])
table_ax = fig.add_subplot(grid[0, 1])



# Main graph

ax.plot(dam_heights,
        head_differences_height,
        marker="o")


 #approximate hydraulic regime transition

ax.axvspan(0.32,
           0.34,
           alpha=0.15,
           label="Submerged → free-overtopping transition")


ax.set_xlabel("Dam height, $H_d$ (m)")

ax.set_ylabel("Equilibrium head difference, " 
              "$\\Delta H^*$ (m)")

ax.set_title("Effect of Dam Height on "
             "Equilibrium Head Difference")

ax.set_ylim(0, 0.60)

ax.grid(True, alpha=0.3)

ax.legend()



# Transition table

transition_heights = [0.30,
                      0.32,
                      0.34,
                      0.36]

transition_height_rows = height_results[
    height_results["dam_height"].isin(transition_heights)]


transition_height_data = []

for _, row in transition_height_rows.iterrows():

    transition_height_data.append([f"{row['dam_height']:.2f}",
                                   f"{row['downstream_depth']:.3f}"])


table_ax.axis("off")

table_ax.set_title(
    "Transition check\n"
    "$H_d$ vs $H_{down}^*$",
    pad=20
)

table = table_ax.table(
    cellText=transition_height_data,
    colLabels=[
        "$H_d$ (m)",
        "$H_{down}^*$ (m)"
    ],
    cellLoc="center",
    loc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.1, 1.6)


plt.tight_layout()

plt.savefig(
    "results/dam_height_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()



# EXPERIMENT 2


conductivities = permeability_results["hydraulic_conductivity"]

head_differences_conductivity = permeability_results["head_difference"]


fig = plt.figure(figsize=(11, 6))

grid = fig.add_gridspec( 1, 2, width_ratios=[3, 1])

ax = fig.add_subplot(grid[0, 0])
table_ax = fig.add_subplot(grid[0, 1])



# Main graph


ax.plot(conductivities,
        head_differences_conductivity,
        marker="o")


 #transition from mixed flow to leakage-only

ax.axvspan(0.31,
           0.32,
           alpha=0.15,
           label="Mixed flow → leakage-only transition")


ax.set_xlabel("Hydraulic conductivity, $K$ (m/s)")

ax.set_ylabel("Equilibrium head difference, "
              "$\\Delta H^*$ (m)")

ax.set_title("Effect of Hydraulic Conductivity on "
             "Equilibrium Head Difference")

ax.set_xlim(0.0, 0.70)


ax.grid(True,
        alpha=0.3)

ax.legend()



# Transition table

transition_conductivities = [0.300,
                             0.310,
                             0.320,
                             0.330]


transition_conductivity_rows = permeability_results[
    permeability_results["hydraulic_conductivity"].isin(transition_conductivities)]


transition_conductivity_data = []

for _, row in transition_conductivity_rows.iterrows():

    transition_conductivity_data.append([f"{row['hydraulic_conductivity']:.3f}",
                                         f"{row['upstream_depth']:.3f}",
                                         f"{row['q_overtop']:.5f}"])


table_ax.axis("off")

table_ax.set_title("Transition check\n"
                   "$H_u^*$ and overtopping",
                   pad=20)

table = table_ax.table(cellText=transition_conductivity_data,
                       colLabels=["$K$(m/s)",
                                  "$H_u^*$",
                                  "$Q_{overtop}$($m^3$/s)"],
                       cellLoc="center",
                       loc="center")

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.1, 1.6)


plt.tight_layout()

plt.savefig("results/permeability_analysis.png",
            dpi=300,
            bbox_inches="tight")

plt.close()



print(permeability_results[["hydraulic_conductivity", "head_difference"]].describe())

print("Analysis complete.")
print("Saved:")
print("results/dam_height_analysis.png")
print("results/permeability_analysis.png")

