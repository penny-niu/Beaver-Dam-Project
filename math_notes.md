# Mathematical Notes

This file contains the main mathematics behind the simulation and the two final experiments.

The project did not begin with all of these equations already worked out. Some of the most useful mathematics came later, when I tried to understand why the simulation was producing particular patterns. I have kept those derivations here because they explain the model much better than the plots alone.

The model is deliberately simplified. The aim is not to reproduce every detail of a real river or beaver dam, but to make the assumptions explicit enough that I can understand what drives the results.

---

## 1. Main notation and baseline parameters

| Symbol | Meaning |
|---|---|
| `H_d` | dam height |
| `T` | streamwise dam thickness |
| `W` | river / dam width |
| `H_u` | upstream water depth |
| `H_down` | downstream water depth |
| `ΔH` | head difference, `H_u - H_down` |
| `K` | effective hydraulic conductivity |
| `A_wetted` | wetted cross-sectional area of the dam |
| `Q_leak` | leakage through the dam |
| `Q_overtop` | flow over / across the crest |
| `Q_dam` | total flow across the dam |
| `Q_in` | external upstream inflow |
| `Q_out` | external downstream outflow |
| `C` | overtopping coefficient |
| `r` | dam thickness-to-height ratio |

The baseline stream has width **3.0 m**. The initial upstream and downstream depths are both **0.36 m**.

```math
W = 3.0
```

```math
H_u(0) = H_{\mathrm{down}}(0) = 0.36
```

The modelled upstream and downstream reaches are both 4 m long, so their horizontal storage areas are

```math
A_u = A_{\mathrm{down}} = 3 \times 4 = 12\ \mathrm{m^2}
```

The external inflow and outflow are both fixed at **0.05 m³/s**:

```math
Q_{\mathrm{in}} = Q_{\mathrm{out}} = 0.05
```

These equal external rates are imposed so that the system can reach a steady state without continuously gaining or losing total water. The value 0.05 m³/s is a baseline scenario assumption rather than a field-calibrated discharge.

---

## 2. Stochastic forest generation

The final baseline contains 80 tree agents.

A fixed random seed is used:

```python
random.seed(42)
```

This means that the same pseudo-random forest can be reproduced each time the simulation starts.

### 2.1 Species distribution

Species are generated from the following categorical probabilities:

```math
P(\mathrm{aspen}) = 0.25,\qquad
P(\mathrm{willow}) = 0.25,\qquad
P(\mathrm{cottonwood}) = 0.15
```

```math
P(\mathrm{oak}) = 0.15,\qquad
P(\mathrm{pine}) = 0.10,\qquad
P(\mathrm{fir}) = 0.10
```

Aspen, willow and cottonwood are classed as preferred species with preference factor 1.0. Oak, pine and fir use preference factor 0.2.

These exact probabilities and weights are modelling assumptions, not fitted ecological parameters.

### 2.2 Effective wood dimensions

Each tree agent represents a usable wood unit rather than a whole tree drawn to physical scale.

Effective diameter is generated using a triangular distribution:

```math
d \sim \operatorname{Triangular}(0.05,\ 0.15,\ 0.30)
```

where the minimum is 0.05 m, the mode is 0.15 m, and the maximum is 0.30 m.

Effective usable length is generated similarly:

```math
L \sim \operatorname{Triangular}(0.20,\ 0.40,\ 0.80)
```

where the minimum is 0.20 m, the mode is 0.40 m, and the maximum is 0.80 m.

I used triangular rather than uniform distributions so that intermediate values near the chosen mode occur more frequently, while smaller and larger pieces remain possible.

For a triangular distribution with minimum `a`, maximum `b`, and mode `c`, the probability density is

```math
f(x)=
\begin{cases}
\dfrac{2(x-a)}{(b-a)(c-a)}, & a\le x\le c,\\[6pt]
\dfrac{2(b-x)}{(b-a)(b-c)}, & c<x\le b,\\[6pt]
0, & \text{otherwise}.
\end{cases}
```

The tree positions are also randomly generated on either side of the river, with rejection checks used to reduce excessive overlap.

---

## 3. Beaver tree-selection model

The behavioural part of the model uses a simplified central-place-foraging-inspired score.

For each available tree agent `i`,

```math
S_i = \frac{d_iL_iP_i}{D_i + c d_i + 1}
```

where:

- `d_i` is effective wood diameter;
- `L_i` is effective wood length;
- `P_i` is the species preference factor;
- `D_i` is the distance from the beaver;
- `c` is the cutting-cost coefficient.

The model uses `c = 0.5`.

The numerator `d_i L_i` is a simple size / benefit proxy. The cutting-cost term `c d_i` makes thicker wood more expensive to cut. The `+1` prevents division by zero.

The beaver chooses the tree with the largest score.

### Why does the score not use actual wood volume?

Actual cylindrical volume scales with `d²L`, whereas the selection score currently uses only `dL`.

I considered replacing the numerator with true wood volume, but doing so would strongly increase the reward for thick pieces while the cutting-cost term still grows only linearly with diameter. Changing only the benefit side would therefore not automatically make the behavioural model more realistic.

For this version I keep `dL` as a simple profitability proxy, while using true cylindrical volume only once material is delivered to the dam. A more detailed future behavioural model could use energetic gain together with nonlinear cutting and transport costs.

---

## 4. Wood volume delivered to the dam

Once a wood unit reaches the dam, it is treated as a cylinder.

```math
V_i = \pi\left(\frac{d_i}{2}\right)^2L_i
```

Total delivered material is

```math
V_{\mathrm{wood}} = \sum_{i=1}^{80}V_i
```

For the fixed seed-42 forest, the final construction run gives **0.832561 m³** of delivered wood.

```math
V_{\mathrm{wood}} = 0.832561
```

All 80 agents are eventually delivered in the current model. This means the foraging score changes the **order of harvesting**, rather than the final subset of material included in the dam.

---

## 5. Dam geometry

The final model approximates the dam as having a triangular cross-section.

The literature-informed thickness-to-height relation is

```math
T = rH_d,\qquad r=2.9
```

For a triangular cross-section,

```math
V_{\mathrm{dam}} = \frac{1}{2}WTH_d
```

Substituting `T = rH_d` gives

```math
V_{\mathrm{dam}}
= \frac{1}{2}WrH_d^2
```

so

```math
H_d^2 = \frac{2V_{\mathrm{dam}}}{Wr}
```

and therefore

```math
\boxed{H_d = \sqrt{\frac{2V_{\mathrm{dam}}}{Wr}}}
```

with

```math
\boxed{T = rH_d}
```

Using the final delivered volume, `W = 3 m`, and `r = 2.9` gives approximately

```math
H_d \approx 0.4375,\qquad T \approx 1.269
```

which agrees with the completed construction simulation.

The model currently treats delivered effective wood volume as the volume of the idealised triangular dam envelope. It does not separately represent voids, mud, stone or trapped sediment.

---

## 6. Water-storage model

The river is represented as two simplified rectangular storage regions: one upstream and one downstream.

### 6.1 Upstream balance

The upstream water volume is

```math
V_u = A_uH_u
```

The rate of change of upstream volume is the difference between external inflow and flow crossing the dam:

```math
\frac{dV_u}{dt} = Q_{\mathrm{in}} - Q_{\mathrm{dam}}
```

Because `A_u` is constant,

```math
\frac{dV_u}{dt} = A_u\frac{dH_u}{dt}
```

Therefore,

```math
A_u\frac{dH_u}{dt} = Q_{\mathrm{in}} - Q_{\mathrm{dam}}
```

and hence

```math
\boxed{
\frac{dH_u}{dt}
=
\frac{Q_{\mathrm{in}}-Q_{\mathrm{dam}}}{A_u}
}
```

### 6.2 Downstream balance

Similarly,

```math
V_{\mathrm{down}} = A_{\mathrm{down}}H_{\mathrm{down}}
```

and

```math
\frac{dV_{\mathrm{down}}}{dt}
=
Q_{\mathrm{dam}}-Q_{\mathrm{out}}
```

so

```math
\boxed{
\frac{dH_{\mathrm{down}}}{dt}
=
\frac{Q_{\mathrm{dam}}-Q_{\mathrm{out}}}{A_{\mathrm{down}}}
}
```

---

## 7. Conservation of total stored water

Because the two storage areas are equal and `Q_in = Q_out`, adding the two depth equations gives

```math
\frac{dH_u}{dt} + \frac{dH_{\mathrm{down}}}{dt} = 0
```

Therefore,

```math
H_u + H_{\mathrm{down}} = \text{constant}
```

Initially both depths are 0.36 m, so

```math
\boxed{H_u + H_{\mathrm{down}} = 0.72}
```

Let

```math
S = 0.72
```

and define the head difference as

```math
\Delta H = H_u - H_{\mathrm{down}}
```

We now have

```math
H_u + H_{\mathrm{down}} = S,
\qquad
H_u - H_{\mathrm{down}} = \Delta H
```

Solving these simultaneously gives

```math
\boxed{H_u = \frac{S+\Delta H}{2}}
```

and

```math
\boxed{H_{\mathrm{down}} = \frac{S-\Delta H}{2}}
```

### Why rewrite the system using `ΔH`?

The simulation itself does not need this transformation. The code still updates `H_u` and `H_down` separately.

It is useful for mathematical analysis. Because total stored depth `S` is fixed, once `ΔH` is known, both individual water depths are automatically determined. The hydraulic state can therefore be reduced from two variables to one.

This later makes it possible to explain the plateau in Experiment 1, derive the critical conductivity in Experiment 2, and analyse how changing river discharge would affect equilibrium.

---

## 8. Leakage through the dam

### 8.1 Starting from Darcy's law

A standard form of Darcy's law for volumetric flow through a porous medium is

```math
Q = KA\frac{\Delta h}{L}
```

where `K` is hydraulic conductivity, `A` is flow area, `Δh` is hydraulic-head difference, and `L` is flow-path length.

In this simplified dam model,

```math
A \rightarrow A_{\mathrm{wetted}},\qquad
\Delta h \rightarrow \Delta H,\qquad
L \rightarrow T
```

so I use

```math
\boxed{
Q_{\mathrm{leak}}
=
K A_{\mathrm{wetted}}\frac{\Delta H}{T}
}
```

A real beaver dam is highly heterogeneous, so this should be interpreted as an effective Darcy-style relation rather than a detailed porous-media model. The single parameter `K` represents the combined permeability of the simplified dam.

### 8.2 Dimensional check

Hydraulic conductivity has units of m/s, wetted area has units of m², and `ΔH/T` is dimensionless. Therefore

```math
[Q_{\mathrm{leak}}]
=
\frac{\mathrm m}{\mathrm s}\times\mathrm m^2
=
\mathrm{m^3/s}
```

which is the correct unit for volumetric discharge.

### 8.3 Wetted area

The submerged height of the dam is

```math
H_{\mathrm{wet}} = \min(H_u,H_d)
```

so

```math
\boxed{
A_{\mathrm{wetted}} = W\min(H_u,H_d)
}
```

The full leakage equation is therefore

```math
Q_{\mathrm{leak}}
=
KW\min(H_u,H_d)\frac{\Delta H}{T}
```

Since `T = rH_d`, two cases are especially useful.

#### Case A: upstream water reaches or exceeds the crest

If `H_u ≥ H_d`, then `A_wetted = WH_d`, so

```math
Q_{\mathrm{leak}}
=
KWH_d\frac{\Delta H}{rH_d}
=
\boxed{\frac{KW}{r}\Delta H}
```

The dam height cancels.

#### Case B: upstream water is below the crest

If `H_u < H_d`, then `A_wetted = WH_u`, giving

```math
\boxed{
Q_{\mathrm{leak}}
=
\frac{KWH_u\Delta H}{rH_d}
}
```

---

## 9. Overtopping

The model uses a simplified weir-style relationship

```math
Q_{\mathrm{overtop}} = CW h^{3/2}
```

The controlling level is defined as

```math
H_{\mathrm{control}} = \max(H_d,H_{\mathrm{down}})
```

so the overflow head is

```math
\boxed{
h = \max\left[H_u-\max(H_d,H_{\mathrm{down}}),0\right]
}
```

and therefore

```math
\boxed{
Q_{\mathrm{overtop}}
=
CW\left[\max\left(H_u-\max(H_d,H_{\mathrm{down}}),0\right)\right]^{3/2}
}
```

### 9.1 Free overtopping

If

```math
H_{\mathrm{down}} < H_d < H_u
```

the crest controls the overflow, so

```math
h = H_u-H_d
```

### 9.2 Submerged dam

If

```math
H_d < H_{\mathrm{down}} < H_u
```

the downstream water level is above the crest. The model then uses

```math
h = H_u-H_{\mathrm{down}} = \Delta H
```

This is a simplified representation of submerged-dam flow rather than a complete submerged-weir formulation.

---

## 10. Total dam flow and the meaning of 0.05 m³/s

Total discharge across the dam is

```math
\boxed{
Q_{\mathrm{dam}} = Q_{\mathrm{leak}} + Q_{\mathrm{overtop}}
}
```

An important distinction is that `Q_dam` is **not prescribed** to be 0.05 m³/s.

The prescribed quantities are the external boundary flows:

```math
Q_{\mathrm{in}} = Q_{\mathrm{out}} = 0.05
```

At the start of a controlled experiment,

```math
H_u = H_{\mathrm{down}} = 0.36
```

so

```math
\Delta H = 0
```

Depending on dam height, the initial dam discharge can be much smaller than 0.05 m³/s and may initially be zero.

If `Q_dam < Q_in`, upstream depth rises. At the same time, if `Q_dam < Q_out`, downstream depth falls. This creates a growing head difference, which increases leakage and/or overtopping and therefore raises `Q_dam`.

At equilibrium, mass balance requires

```math
\boxed{
Q_{\mathrm{in}} = Q_{\mathrm{dam}} = Q_{\mathrm{out}} = 0.05
}
```

Numerically, equilibrium is declared when both flow residuals are smaller than `10⁻⁴ m³/s` for at least five simulated seconds.

---

## 11. Final construction baseline

The seed-42 construction simulation delivers all 80 wood units.

Final construction state:

- delivered wood volume: **0.832561 m³**;
- dam height: **0.437 m**;
- dam thickness: **1.269 m**.

After construction stops, dam geometry is frozen while the hydrology continues to settle.

Final equilibrium state:

- upstream depth: **0.482 m**;
- downstream depth: **0.238 m**;
- head difference: **0.243 m**;
- leakage: **0.00252 m³/s**;
- overtopping: **0.04743 m³/s**;
- total dam flow: **0.04995 m³/s**;
- post-construction settling time: **48.6 s**.

---

## 12. Experiment 1 — varying dam height

Experiment 1 investigates how equilibrium head difference changes with overall dam size.

Hydraulic conductivity is fixed at `K = 0.01 m/s`. Because `T = 2.9H_d`, changing dam height also changes thickness. The experiment therefore varies overall dam geometry while preserving the chosen thickness-to-height ratio.

### 12.1 The low-height plateau

For the smallest dam heights,

```math
H_d < H_{\mathrm{down}} < H_u
```

so the dam is submerged.

Because the upstream water reaches above the crest, the leakage equation reduces to

```math
Q_{\mathrm{leak}}
=
\frac{KW}{r}\Delta H
```

and because downstream water is also above the crest, the simplified submerged overflow term is

```math
Q_{\mathrm{overtop}}
=
CW(\Delta H)^{3/2}
```

Therefore,

```math
\boxed{
Q_{\mathrm{dam}}
=
\frac{KW}{r}\Delta H + CW(\Delta H)^{3/2}
}
```

The important point is that `H_d` has disappeared from the equation.

At equilibrium, `Q_dam = Q_in = 0.05 m³/s`, so while the dam remains submerged the equilibrium head difference is controlled by the flow parameters rather than by dam height.

The numerical experiment gives

```math
\Delta H^* = 0.045504
```

for `H_d = 0.20 m`, `0.30 m`, and `0.32 m`.

The plateau is therefore a consequence of the equations rather than a numerical coincidence.

### 12.2 Why the transition occurs between 0.32 m and 0.34 m

Within the submerged plateau,

```math
H_{\mathrm{down}}^* \approx 0.33725
```

As long as `H_d < H_down*`, the downstream water surface remains above the dam crest. Once `H_d > H_down*`, the crest itself becomes the controlling level for overtopping.

The experiment sampled 0.32 m and 0.34 m, so the transition is bracketed by

```math
\boxed{H_d = 0.32\text{--}0.34\ \mathrm{m}}
```

### 12.3 Why increasing dam height increases equilibrium head difference

After the transition,

```math
H_{\mathrm{down}} < H_d < H_u
```

so the model is in the free-overtopping regime.

Leakage remains

```math
Q_{\mathrm{leak}} = \frac{KW}{r}\Delta H
```

while overtopping depth becomes

```math
h = H_u-H_d
```

Using

```math
H_u = \frac{S+\Delta H}{2}
```

we obtain the equilibrium equation

```math
Q
=
\frac{KW}{r}\Delta H
+
CW\left(\frac{S+\Delta H}{2}-H_d\right)^{3/2}
```

Here `Q` is fixed. If `H_d` increases, the overtopping depth becomes smaller. The system therefore needs a larger `ΔH` to continue carrying the same discharge.

We can make that argument precise using implicit differentiation.

Define

```math
F(\Delta H,H_d)
=
\frac{KW}{r}\Delta H
+
CW\left(\frac{S+\Delta H}{2}-H_d\right)^{3/2}
-Q
```

Equilibrium corresponds to

```math
F(\Delta H,H_d)=0
```

Because `ΔH` changes with `H_d`, differentiate with respect to `H_d`:

```math
\frac{\partial F}{\partial \Delta H}\frac{d\Delta H}{dH_d}
+
\frac{\partial F}{\partial H_d}
=0
```

so

```math
\boxed{
\frac{d\Delta H}{dH_d}
=
-\frac{\partial F/\partial H_d}{\partial F/\partial \Delta H}
}
```

Let

```math
g = \frac{S+\Delta H}{2}-H_d
```

In the free-overtopping regime, `g > 0`. Then

```math
\frac{\partial F}{\partial H_d}
=
-\frac{3}{2}CW\sqrt{g}
<0
```

while

```math
\frac{\partial F}{\partial \Delta H}
=
\frac{KW}{r}
+
\frac{3}{4}CW\sqrt{g}
>0
```

Therefore,

```math
\boxed{
\frac{d\Delta H^*}{dH_d}>0
}
```

So, within the free-overtopping regime of this model, increasing dam height must increase equilibrium head difference.

---

## 13. Experiment 2 — varying hydraulic conductivity

Experiment 2 fixes the dam close to the completed construction baseline at approximately `H_d = 0.4375 m`, giving `T ≈ 1.26875 m`.

The tested conductivity values range from `K = 0.002 m/s` to `K = 0.67 m/s`.

The main numerical result is that increasing `K` reduces equilibrium head difference.

### 13.1 Why increasing `K` reduces `ΔH*`

In the mixed leakage/overtopping regime,

```math
Q
=
\frac{KW}{r}\Delta H
+
CW\left(\frac{S+\Delta H}{2}-H_d\right)^{3/2}
```

Increasing `K` means that more leakage can pass through the dam for the same head difference. Since the required total equilibrium flow remains fixed at 0.05 m³/s, the system no longer requires as large a `ΔH`.

Implicit differentiation gives

```math
\frac{\partial F}{\partial K}
=
\frac{W}{r}\Delta H
>0
```

while

```math
\frac{\partial F}{\partial \Delta H}>0
```

so

```math
\boxed{
\frac{d\Delta H^*}{dK}<0
}
```

This matches the numerical experiment.

### 13.2 Transition to leakage-only flow

As `K` increases, leakage carries an increasing proportion of the required total discharge.

The transition to leakage-only flow occurs when the upstream water surface has just fallen to the dam crest:

```math
H_u = H_d
```

For Experiment 2,

```math
H_d = 0.4375
```

Since

```math
H_u+H_{\mathrm{down}} = 0.72
```

we get

```math
H_{\mathrm{down}} = 0.72-0.4375 = 0.2825
```

and therefore

```math
\Delta H_{\mathrm{crit}} = 0.4375-0.2825 = 0.155
```

At the threshold there is no overtopping, so all equilibrium flow passes through the dam:

```math
Q = Q_{\mathrm{leak}}
```

Since the wetted height reaches the full dam height,

```math
Q = \frac{KW}{r}\Delta H_{\mathrm{crit}}
```

Solving for `K` gives

```math
\boxed{
K_{\mathrm{crit}}
=
\frac{rQ}{W\Delta H_{\mathrm{crit}}}
}
```

Substituting `r = 2.9`, `Q = 0.05`, `W = 3`, and `ΔH_crit = 0.155` gives

```math
K_{\mathrm{crit}} \approx 0.3118\ \mathrm{m/s}
```

The numerical experiment gives a very similar result. At `K = 0.31 m/s`, there is still a tiny overtopping flow of about `2.69 × 10⁻⁵ m³/s`. At `K = 0.32 m/s`, overtopping is zero.

Therefore the numerical transition is bracketed by

```math
\boxed{K \approx 0.31\text{--}0.32\ \mathrm{m/s}}
```

in close agreement with the analytical prediction.

### 13.3 Analytical solution in the leakage-only regime

Once

```math
H_u < H_d
```

there is no overtopping.

The wetted height is now `H_u`, so

```math
Q
=
\frac{KWH_u\Delta H}{rH_d}
```

Using

```math
H_u = \frac{S+\Delta H}{2}
```

gives

```math
Q
=
\frac{KW}{2rH_d}\left(S\Delta H+\Delta H^2\right)
```

Rearranging,

```math
\Delta H^2
+
S\Delta H
-
\frac{2rH_dQ}{KW}
=0
```

The physically relevant positive root is

```math
\boxed{
\Delta H
=
\frac{-S+\sqrt{S^2+\frac{8rH_dQ}{KW}}}{2}
}
```

This expression directly shows how the leakage-only equilibrium depends on conductivity.

At `K = 0.67 m/s`, the numerical experiment gives

```math
\Delta H^* = 0.078922\ \mathrm{m}
```

---

## 14. Analytical extension — what if discharge were varied?

I did not run this as a third experiment, but I explored what the current equations predict if

```math
Q_{\mathrm{in}} = Q_{\mathrm{out}} = Q
```

is varied while dam geometry and `K` remain fixed.

The model predicts

```math
\boxed{Q\uparrow\quad\Longrightarrow\quad\Delta H^*\uparrow}
```

### 14.1 Submerged regime

```math
Q
=
\frac{KW}{r}\Delta H
+
CW(\Delta H)^{3/2}
```

so

```math
\frac{dQ}{d\Delta H}
=
\frac{KW}{r}
+
\frac{3}{2}CW\sqrt{\Delta H}
>0
```

### 14.2 Free-overtopping regime

```math
Q
=
\frac{KW}{r}\Delta H
+
CW\left(\frac{S+\Delta H}{2}-H_d\right)^{3/2}
```

so

```math
\frac{dQ}{d\Delta H}
=
\frac{KW}{r}
+
\frac{3CW}{4}\sqrt{\frac{S+\Delta H}{2}-H_d}
>0
```

### 14.3 Leakage-only regime

```math
Q
=
\frac{KW}{2rH_d}\left(S\Delta H+\Delta H^2\right)
```

so

```math
\frac{dQ}{d\Delta H}
=
\frac{KW}{2rH_d}(S+2\Delta H)
>0
```

Therefore, within all three regimes of this simplified model, higher discharge requires a larger equilibrium head difference.

This also shows why the conductivity transition found in Experiment 2 is scenario-dependent. At the leakage-only threshold,

```math
K_{\mathrm{crit}}
=
\frac{rQ}{W\Delta H_{\mathrm{crit}}}
```

so, for fixed geometry and stored water,

```math
\boxed{K_{\mathrm{crit}}\propto Q}
```

The numerical value `K_crit ≈ 0.312 m/s` is therefore not a universal property of beaver dams. It is the threshold predicted by this model for the baseline discharge of 0.05 m³/s.

Varying discharge would be a useful future sensitivity experiment.

---

## 15. Numerical implementation and timescales

The interactive construction simulation and the controlled experiments use slightly different timing approaches.

### 15.1 Interactive simulation

`main.py` runs at a target of 60 frames per second. The update time step is calculated from actual elapsed frame time:

```python
dt = clock.tick(FPS) / 1000.0
```

During construction, beaver movement, dam growth and river hydrology all evolve together.

After all 80 tree agents have been delivered, the model enters a separate settling phase. At this point the dam geometry is frozen and only the hydrology continues to evolve.

For the final baseline run, the post-construction settling time was **48.6 s**.

### 15.2 Controlled experiments

`experiment.py` uses a fixed numerical time step of **0.1 s**.

Every experiment begins immediately with a completed dam and with both water depths reset to 0.36 m. A run ends when the equilibrium conditions remain satisfied for five seconds. A safety limit of 5000 simulated seconds prevents a failed run from continuing indefinitely.

Because the experiments and the interactive construction run start from different hydraulic states, their settling times should not be compared directly.

### 15.3 Development timeframe

The project was originally planned as a ten-day personal mathematical-modelling project.

In practice, development was spread intermittently from late July to late September 2026. The later stages included experimental analysis, code verification, literature reality checks, replacement of the original rectangular dam geometry, rerunning the experiments, and final documentation.

A fuller chronology is recorded separately in the project journal.

---

## 16. Mathematical limitations

The equations above explain the behaviour of the simulation, but they are not a complete physical model of a natural river or beaver dam.

Important simplifications include:

- upstream and downstream water are each represented by one uniform depth;
- the storage geometry is rectangular;
- velocity fields and momentum equations are not modelled;
- spatial backwater effects are ignored;
- external inflow and downstream outflow are fixed;
- dam permeability is represented by one effective hydraulic conductivity `K`;
- the leakage relation treats the dam as a simplified porous medium;
- overtopping uses an idealised weir-style law;
- submerged-dam flow is simplified rather than using a full submerged-weir correction;
- the dam is forced to maintain the fixed relation `T/H_d = 2.9`;
- the triangular dam envelope does not separately represent voids, mud, stones or sediment;
- the tree-selection rule is a heuristic rather than a full energetic optimisation model;
- all 80 tree agents are eventually harvested, so the foraging rule affects harvesting order rather than the final amount of material.

These limitations mean that numerical values such as `K_crit ≈ 0.312 m/s` belong to the particular scenario used in this project.

The more general results are the mechanisms revealed by the equations:

1. A sufficiently low submerged dam produces a plateau in equilibrium head difference because dam height cancels from the governing flow equation.
2. Once the crest becomes the controlling level, increasing dam height increases equilibrium head difference.
3. Increasing hydraulic conductivity reduces the head difference needed to carry the imposed discharge.
4. At sufficiently high conductivity, leakage alone can carry the required flow and overtopping disappears.
5. For a fixed dam and conductivity, increasing river discharge requires a larger equilibrium head difference.

These mathematical explanations became an important part of the project because they allowed the numerical results to be understood rather than only observed.
