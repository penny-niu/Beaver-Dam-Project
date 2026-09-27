import csv
import os
import matplotlib.pyplot as plt


# ============================================================
# SETUP
# ============================================================

os.makedirs("results", exist_ok=True)


def read_csv(filename):
    """
    Read an experiment CSV and convert numerical values
    from strings into floats.
    """

    rows = []

    with open(filename, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            converted_row = {}

            for key, value in row.items():
                converted_row[key] = float(value)

            rows.append(converted_row)

    return rows


# ============================================================
# LOAD EXPERIMENT DATA
# ============================================================

height_results = read_csv(
    "results/data/dam_height_experiment.csv"
)

permeability_results = read_csv(
    "results/data/permeability_experiment.csv"
)


# Sort results so the lines are always plotted in order

height_results.sort(
    key=lambda row: row["dam_height"]
)

permeability_results.sort(
    key=lambda row: row["hydraulic_conductivity"]
)


# ============================================================
# EXPERIMENT 1
# DAM HEIGHT
# ============================================================

dam_heights = [
    row["dam_height"]
    for row in height_results
]

head_differences_height = [
    row["head_difference"]
    for row in height_results
]


fig = plt.figure(figsize=(11, 6))

grid = fig.add_gridspec(
    1,
    2,
    width_ratios=[3, 1]
)

ax = fig.add_subplot(grid[0, 0])
table_ax = fig.add_subplot(grid[0, 1])


# -------------------------
# Main graph
# -------------------------

ax.plot(
    dam_heights,
    head_differences_height,
    marker="o"
)


# Approximate hydraulic regime transition

ax.axvspan(
    0.32,
    0.34,
    alpha=0.15,
    label="Submerged → free-overtopping transition"
)


ax.set_xlabel(
    "Dam height, $H_d$ (m)"
)

ax.set_ylabel(
    "Equilibrium head difference, "
    "$\\Delta H^*$ (m)"
)

ax.set_title(
    "Effect of Dam Height on "
    "Equilibrium Head Difference"
)

ax.set_ylim(
    0,
    0.60
)

ax.grid(
    True,
    alpha=0.3
)

ax.legend()


# -------------------------
# Transition table
# -------------------------

transition_heights = [
    0.30,
    0.32,
    0.34,
    0.36
]

transition_height_data = []

for row in height_results:

    if row["dam_height"] in transition_heights:

        transition_height_data.append([
            f"{row['dam_height']:.2f}",
            f"{row['downstream_depth']:.3f}"
        ])


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


# ============================================================
# EXPERIMENT 2
# HYDRAULIC CONDUCTIVITY
# ============================================================

conductivities = [
    row["hydraulic_conductivity"]
    for row in permeability_results
]

head_differences_conductivity = [
    row["head_difference"]
    for row in permeability_results
]


fig = plt.figure(figsize=(11, 6))

grid = fig.add_gridspec(
    1,
    2,
    width_ratios=[3, 1]
)

ax = fig.add_subplot(grid[0, 0])
table_ax = fig.add_subplot(grid[0, 1])


# -------------------------
# Main graph
# -------------------------

ax.plot(
    conductivities,
    head_differences_conductivity,
    marker="o"
)


# Transition from mixed flow to leakage-only

ax.axvspan(
    0.31,
    0.32,
    alpha=0.15,
    label="Mixed flow → leakage-only transition"
)


ax.set_xlabel(
    "Hydraulic conductivity, $K$ (m/s)"
)

ax.set_ylabel(
    "Equilibrium head difference, "
    "$\\Delta H^*$ (m)"
)

ax.set_title(
    "Effect of Hydraulic Conductivity on "
    "Equilibrium Head Difference"
)

ax.set_xlim(0.0, 0.70)


ax.grid(
    True,
    alpha=0.3
)

ax.legend()


# -------------------------
# Transition table
# -------------------------

transition_conductivities = [
    0.300,
    0.310,
    0.320,
    0.330
]

transition_conductivity_data = []

for row in permeability_results:

    if row["hydraulic_conductivity"] in transition_conductivities:

        transition_conductivity_data.append([
            f"{row['hydraulic_conductivity']:.3f}",
            f"{row['upstream_depth']:.3f}",
            f"{row['q_overtop']:.5f}"
        ])


table_ax.axis("off")

table_ax.set_title(
    "Transition check\n"
    "$H_u^*$ and overtopping",
    pad=20
)

table = table_ax.table(
    cellText=transition_conductivity_data,
    colLabels=[
        "$K$(m/s)",
        "$H_u^*$",
        "$Q_{overtop}$($m^3$/s)"
    ],
    cellLoc="center",
    loc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.1, 1.6)


plt.tight_layout()

plt.savefig(
    "results/permeability_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("Analysis complete.")
print("Saved:")
print("results/dam_height_analysis.png")
print("results/permeability_analysis.png")

