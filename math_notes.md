# Mathematical Notes

This file contains the main mathematics behind the simulation and the two final experiments.

The project did not begin with all of these equations already worked out. Some of the most useful mathematics came later, when I tried to understand why the simulation was producing particular patterns. I have kept those derivations here because they explain the model much better than the plots alone.

The model is deliberately simplified. The aim is not to reproduce every detail of a real river or beaver dam, but to make the assumptions explicit enough that I can understand what drives the results.

---

# 1. Main notation and baseline parameters

| Symbol | Meaning |
|---|---|
| $H_d$ | dam height |
| $T$ | streamwise dam thickness |
| $W$ | river / dam width |
| $H_u$ | upstream water depth |
| $H_{\mathrm{down}}$ | downstream water depth |
| $\Delta H$ | head difference, $H_u-H_{\mathrm{down}}$ |
| $K$ | effective hydraulic conductivity |
| $A_{\mathrm{wetted}}$ | wetted cross-sectional area of the dam |
| $Q_{\mathrm{leak}}$ | leakage through the dam |
| $Q_{\mathrm{overtop}}$ | flow over / across the crest |
| $Q_{\mathrm{dam}}$ | total flow across the dam |
| $Q_{\mathrm{in}}$ | external upstream inflow |
| $Q_{\mathrm{out}}$ | external downstream outflow |
| $C$ | overtopping coefficient |
| $r$ | dam thickness-to-height ratio |

The baseline stream uses

$$
W=3.0\ \mathrm{m},
$$

with initial water depths

$$
H_u(0)=H_{\mathrm{down}}(0)=0.36\ \mathrm{m}.
$$

The modelled upstream and downstream reaches are both 4 m long, so their horizontal storage areas are

$$
A_u=A_{\mathrm{down}}
=
3\times4
=
12\ \mathrm{m^2}.
$$

The external flow rates are fixed at

$$
Q_{\mathrm{in}}
=
Q_{\mathrm{out}}
=
0.05\ \mathrm{m^3/s}.
$$

These equal external rates are imposed so that the system can reach a steady state without continuously gaining or losing total water.

The value $0.05\ \mathrm{m^3/s}$ is a baseline scenario assumption rather than a field-calibrated discharge.

---

# 2. Stochastic forest generation

The final baseline contains 80 tree agents.

A fixed random seed,

```python
random.seed(42)
```

is used so that the same pseudo-random forest can be reproduced each time the simulation starts.

## 2.1 Species distribution

Species are generated from the categorical probabilities

$$
P(\mathrm{aspen})=0.25,
$$

$$
P(\mathrm{willow})=0.25,
$$

$$
P(\mathrm{cottonwood})=0.15,
$$

$$
P(\mathrm{oak})=0.15,
$$

$$
P(\mathrm{pine})=0.10,
$$

and

$$
P(\mathrm{fir})=0.10.
$$

Aspen, willow and cottonwood are classed as preferred species.

Their preference factor is

$$
P_i=1.0,
$$

while oak, pine and fir use

$$
P_i=0.2.
$$

These exact probabilities and weights are modelling assumptions, not fitted ecological parameters.

## 2.2 Effective wood dimensions

Each tree agent represents a usable wood unit rather than a whole tree drawn to physical scale.

Effective diameter is generated using a triangular distribution:

$$
d
\sim
\operatorname{Triangular}
(0.05,\ 0.15,\ 0.30),
$$

where

- minimum diameter = 0.05 m,
- mode = 0.15 m,
- maximum diameter = 0.30 m.

Effective usable length is generated similarly:

$$
L
\sim
\operatorname{Triangular}
(0.20,\ 0.40,\ 0.80).
$$

Here,

- minimum length = 0.20 m,
- mode = 0.40 m,
- maximum length = 0.80 m.

I used triangular rather than uniform distributions so that intermediate values near the chosen mode occur more frequently, while smaller and larger pieces remain possible.

For a triangular distribution with minimum $a$, maximum $b$, and mode $c$, the probability density is

$$
f(x)
=
\begin{cases}
\dfrac{2(x-a)}{(b-a)(c-a)},
& a\le x\le c, \\[8pt]
\dfrac{2(b-x)}{(b-a)(b-c)},
& c<x\le b, \\[8pt]
0,
& \text{otherwise}.
\end{cases}
$$

The tree positions are also randomly generated on either side of the river, with rejection checks used to reduce excessive overlap.

---

# 3. Beaver tree-selection model

The behavioural part of the model uses a simplified central-place-foraging-inspired score.

For each available tree agent $i$,

$$
S_i
=
\frac{
d_iL_iP_i
}{
D_i+c\,d_i+1
}.
$$

Here,

- $d_i$ = effective wood diameter,
- $L_i$ = effective wood length,
- $P_i$ = species preference factor,
- $D_i$ = distance from the beaver,
- $c$ = cutting-cost coefficient.

The model uses

$$
c=0.5.
$$

The term

$$
d_iL_i
$$

is a simple size / benefit proxy.

The cutting-cost term is

$$
c\,d_i,
$$

so thicker wood is more expensive to cut.

The `+1` in the denominator prevents division by zero.

The beaver chooses the tree with the largest score.

## Why does the score not use actual wood volume?

Actual cylindrical volume scales with $d^2L$, whereas the selection score currently uses only $dL$.

I considered replacing the numerator with true wood volume, but doing so would strongly increase the reward for thick pieces while the cutting-cost term still grows only linearly with diameter.

Changing only the benefit side would therefore not automatically make the behavioural model more realistic.

For this version I keep

$$
dL
$$

as a simple profitability proxy, while using true cylindrical volume only once material is delivered to the dam.

A more detailed future behavioural model could use energetic gain together with nonlinear cutting and transport costs.

---

# 4. Wood volume delivered to the dam

Once a wood unit reaches the dam, it is treated as a cylinder.

Its volume is

$$
V_i
=
\pi
\left(
\frac{d_i}{2}
\right)^2
L_i.
$$

Total delivered material is

$$
V_{\mathrm{wood}}
=
\sum_{i=1}^{80}V_i.
$$

For the fixed seed-42 forest, the final construction run gives

$$
V_{\mathrm{wood}}
=
0.832561\ \mathrm{m^3}.
$$

All 80 agents are eventually delivered in the current model.

This means the foraging score changes the **order of harvesting**, rather than the final subset of material included in the dam.

---

# 5. Dam geometry

The final model approximates the dam as having a triangular cross-section.

The literature-informed thickness-to-height relation is

$$
T=rH_d,
$$

with

$$
r=2.9.
$$

For a triangular cross-section,

$$
V_{\mathrm{dam}}
=
\frac12 WTH_d.
$$

Substituting

$$
T=rH_d
$$

gives

$$
V_{\mathrm{dam}}
=
\frac12 WrH_d^2.
$$

Therefore,

$$
H_d^2
=
\frac{2V_{\mathrm{dam}}}{Wr},
$$

so

$$
\boxed{
H_d
=
\sqrt{
\frac{2V_{\mathrm{dam}}}{Wr}
}
}
$$

and

$$
\boxed{
T=rH_d.
}
$$

Using the final delivered volume,

$$
V_{\mathrm{dam}}
=
0.832561\ \mathrm{m^3},
$$

with

$$
W=3\ \mathrm{m}
$$

and

$$
r=2.9,
$$

gives approximately

$$
H_d
\approx
0.4375\ \mathrm{m},
$$

and therefore

$$
T
\approx
1.269\ \mathrm{m}.
$$

These agree with the completed construction simulation.

The model currently treats delivered effective wood volume as the volume of the idealised triangular dam envelope. It does not separately represent voids, mud, stone or trapped sediment.

---

# 6. Water-storage model

The river is represented as two simplified rectangular storage regions: one upstream and one downstream.

## 6.1 Upstream balance

The upstream water volume is

$$
V_u=A_uH_u.
$$

The rate of change of upstream volume is the difference between external inflow and flow crossing the dam:

$$
\frac{dV_u}{dt}
=
Q_{\mathrm{in}}
-
Q_{\mathrm{dam}}.
$$

Because $A_u$ is constant,

$$
\frac{dV_u}{dt}
=
A_u\frac{dH_u}{dt}.
$$

Therefore,

$$
A_u\frac{dH_u}{dt}
=
Q_{\mathrm{in}}
-
Q_{\mathrm{dam}},
$$

and hence

$$
\boxed{
\frac{dH_u}{dt}
=
\frac{
Q_{\mathrm{in}}
-
Q_{\mathrm{dam}}
}{
A_u
}.
}
$$

## 6.2 Downstream balance

Similarly,

$$
V_{\mathrm{down}}
=
A_{\mathrm{down}}H_{\mathrm{down}}.
$$

The downstream volume changes according to

$$
\frac{dV_{\mathrm{down}}}{dt}
=
Q_{\mathrm{dam}}
-
Q_{\mathrm{out}}.
$$

Since the downstream storage area is constant,

$$
A_{\mathrm{down}}
\frac{dH_{\mathrm{down}}}{dt}
=
Q_{\mathrm{dam}}
-
Q_{\mathrm{out}},
$$

so

$$
\boxed{
\frac{dH_{\mathrm{down}}}{dt}
=
\frac{
Q_{\mathrm{dam}}
-
Q_{\mathrm{out}}
}{
A_{\mathrm{down}}
}.
}
$$

---

# 7. Conservation of total stored water

Because

$$
A_u=A_{\mathrm{down}}=A
$$

and

$$
Q_{\mathrm{in}}=Q_{\mathrm{out}},
$$

adding the two depth equations gives

$$
\frac{dH_u}{dt}
+
\frac{dH_{\mathrm{down}}}{dt}
=
0.
$$

Therefore,

$$
H_u+H_{\mathrm{down}}
=
\text{constant}.
$$

Initially,

$$
H_u(0)
=
H_{\mathrm{down}}(0)
=
0.36,
$$

so

$$
\boxed{
H_u+H_{\mathrm{down}}
=
0.72\ \mathrm{m}.
}
$$

Let

$$
S=0.72\ \mathrm{m}.
$$

We also define the head difference

$$
\Delta H
=
H_u-H_{\mathrm{down}}.
$$

We therefore have two equations:

$$
H_u+H_{\mathrm{down}}=S
$$

and

$$
H_u-H_{\mathrm{down}}=\Delta H.
$$

Solving them gives

$$
\boxed{
H_u
=
\frac{S+\Delta H}{2}
}
$$

and

$$
\boxed{
H_{\mathrm{down}}
=
\frac{S-\Delta H}{2}.
}
$$

## Why rewrite the system using $\Delta H$?

The simulation itself does not need this transformation. The code still updates $H_u$ and $H_{\mathrm{down}}$ separately.

It is useful for mathematical analysis.

Because total stored depth $S$ is fixed, once $\Delta H$ is known, both individual water depths are automatically determined.

The hydraulic state can therefore be reduced from two variables,

$$
(H_u,H_{\mathrm{down}}),
$$

to one variable,

$$
\Delta H.
$$

This later makes it possible to:

- explain the plateau in Experiment 1;
- prove how equilibrium head difference changes with dam height;
- derive the critical conductivity in Experiment 2;
- derive an analytical leakage-only solution;
- analyse how changing river discharge would affect equilibrium.

---

# 8. Leakage through the dam

## 8.1 Starting from Darcy's law

A standard form of Darcy's law for volumetric flow through a porous medium is

$$
Q
=
KA
\frac{\Delta h}{L}.
$$

Here,

- $K$ is hydraulic conductivity,
- $A$ is the flow area,
- $\Delta h$ is the hydraulic-head difference,
- $L$ is the flow-path length.

In this simplified dam model, these become

$$
A
\rightarrow
A_{\mathrm{wetted}},
$$

$$
\Delta h
\rightarrow
\Delta H,
$$

and

$$
L
\rightarrow
T.
$$

Therefore I use

$$
\boxed{
Q_{\mathrm{leak}}
=
K A_{\mathrm{wetted}}
\frac{\Delta H}{T}.
}
$$

A real beaver dam is highly heterogeneous, so this should be interpreted as an effective Darcy-style relation rather than a detailed porous-media model.

The single parameter $K$ represents the combined permeability of the simplified dam.

## 8.2 Dimensional check

Hydraulic conductivity has units

$$
[K]
=
\mathrm{m/s}.
$$

Area has units

$$
[A_{\mathrm{wetted}}]
=
\mathrm{m^2}.
$$

The hydraulic gradient

$$
\frac{\Delta H}{T}
$$

is dimensionless.

Therefore,

$$
[Q_{\mathrm{leak}}]
=
\frac{\mathrm m}{\mathrm s}
\times
\mathrm m^2
=
\mathrm{m^3/s},
$$

which is the correct unit for volumetric discharge.

## 8.3 Wetted area

The submerged height of the dam is

$$
H_{\mathrm{wet}}
=
\min(H_u,H_d).
$$

Therefore,

$$
\boxed{
A_{\mathrm{wetted}}
=
W\min(H_u,H_d).
}
$$

The full leakage equation is therefore

$$
Q_{\mathrm{leak}}
=
KW
\min(H_u,H_d)
\frac{\Delta H}{T}.
$$

Since

$$
T=rH_d,
$$

there are two important cases.

### Case A: upstream water reaches or exceeds the crest

If

$$
H_u\ge H_d,
$$

then

$$
A_{\mathrm{wetted}}
=
WH_d.
$$

So

$$
Q_{\mathrm{leak}}
=
KWH_d
\frac{\Delta H}{rH_d}.
$$

The $H_d$ terms cancel:

$$
\boxed{
Q_{\mathrm{leak}}
=
\frac{KW}{r}\Delta H.
}
$$

### Case B: upstream water is below the crest

If

$$
H_u<H_d,
$$

then

$$
A_{\mathrm{wetted}}
=
WH_u.
$$

Therefore,

$$
\boxed{
Q_{\mathrm{leak}}
=
\frac{
KWH_u\Delta H
}{
rH_d
}.
}
$$

---

# 9. Overtopping

The model uses a simplified weir-style relationship

$$
Q_{\mathrm{overtop}}
=
CW h^{3/2}.
$$

The controlling level is defined as

$$
H_{\mathrm{control}}
=
\max(H_d,H_{\mathrm{down}}).
$$

Therefore the overflow head is

$$
\boxed{
h
=
\max
\left[
H_u-\max(H_d,H_{\mathrm{down}}),
0
\right].
}
$$

Hence,

$$
\boxed{
Q_{\mathrm{overtop}}
=
CW
\left[
\max
\left(
H_u-\max(H_d,H_{\mathrm{down}}),
0
\right)
\right]^{3/2}.
}
$$

There are two main situations.

## 9.1 Free overtopping

If

$$
H_{\mathrm{down}}<H_d<H_u,
$$

the crest controls the overflow.

Then

$$
h=H_u-H_d.
$$

## 9.2 Submerged dam

If

$$
H_d<H_{\mathrm{down}}<H_u,
$$

the downstream water level is above the crest.

The model then uses

$$
h
=
H_u-H_{\mathrm{down}}
=
\Delta H.
$$

This is a simplified representation of submerged-dam flow rather than a complete submerged-weir formulation.

---

# 10. Total dam flow and the meaning of $0.05\ \mathrm{m^3/s}$

Total discharge across the dam is

$$
\boxed{
Q_{\mathrm{dam}}
=
Q_{\mathrm{leak}}
+
Q_{\mathrm{overtop}}.
}
$$

An important distinction is that

$$
Q_{\mathrm{dam}}
$$

is **not prescribed** to be $0.05\ \mathrm{m^3/s}$.

The prescribed quantities are the external boundary flows:

$$
Q_{\mathrm{in}}
=
Q_{\mathrm{out}}
=
0.05\ \mathrm{m^3/s}.
$$

At the start of a controlled experiment,

$$
H_u
=
H_{\mathrm{down}}
=
0.36\ \mathrm{m}.
$$

Therefore,

$$
\Delta H=0.
$$

Depending on dam height, the initial dam discharge can be much smaller than $0.05\ \mathrm{m^3/s}$ and may initially be zero.

If

$$
Q_{\mathrm{dam}}
<
Q_{\mathrm{in}},
$$

then

$$
\frac{dH_u}{dt}>0,
$$

so upstream depth rises.

At the same time, if

$$
Q_{\mathrm{dam}}
<
Q_{\mathrm{out}},
$$

then

$$
\frac{dH_{\mathrm{down}}}{dt}<0,
$$

so downstream depth falls.

This creates a growing head difference.

A larger $\Delta H$ increases leakage and/or overtopping, so $Q_{\mathrm{dam}}$ rises.

At equilibrium, mass balance requires

$$
\boxed{
Q_{\mathrm{in}}
=
Q_{\mathrm{dam}}
=
Q_{\mathrm{out}}
=
0.05\ \mathrm{m^3/s}.
}
$$

Numerically, equilibrium is declared when both

$$
\left|
Q_{\mathrm{in}}
-
Q_{\mathrm{dam}}
\right|
<
10^{-4}\ \mathrm{m^3/s}
$$

and

$$
\left|
Q_{\mathrm{dam}}
-
Q_{\mathrm{out}}
\right|
<
10^{-4}\ \mathrm{m^3/s}
$$

remain satisfied for at least five simulated seconds.

---

# 11. Final construction baseline

The seed-42 construction simulation delivers all 80 wood units.

The final dam has

$$
V_{\mathrm{wood}}
=
0.832561\ \mathrm{m^3},
$$

$$
H_d
\approx
0.437\ \mathrm{m},
$$

and

$$
T
\approx
1.269\ \mathrm{m}.
$$

After construction stops, dam geometry is frozen while the hydrology continues to settle.

The final equilibrium state is approximately

$$
H_u
=
0.482\ \mathrm{m},
$$

$$
H_{\mathrm{down}}
=
0.238\ \mathrm{m},
$$

so

$$
\boxed{
\Delta H
=
0.243\ \mathrm{m}.
}
$$

The equilibrium flow components are approximately

$$
Q_{\mathrm{leak}}
=
0.00252\ \mathrm{m^3/s},
$$

$$
Q_{\mathrm{overtop}}
=
0.04743\ \mathrm{m^3/s},
$$

and

$$
Q_{\mathrm{dam}}
=
0.04995\ \mathrm{m^3/s}.
$$

The post-construction settling time in this interactive run was

$$
48.6\ \mathrm{s}.
$$

---

# 12. Experiment 1 — varying dam height

Experiment 1 investigates how equilibrium head difference changes with overall dam size.

Hydraulic conductivity is fixed at

$$
K=0.01\ \mathrm{m/s}.
$$

The tested dam heights are

$$
0.20,\ 0.30,\ 0.32,\ 0.34,\ 0.36,\ 0.38,\ 0.40,\ 0.50,\ 0.60\ \mathrm{m}.
$$

Because

$$
T=2.9H_d,
$$

changing $H_d$ also changes thickness.

The experiment therefore varies overall dam geometry while preserving the chosen thickness-to-height ratio.

---

## 12.1 The low-height plateau

For the smallest dam heights,

$$
H_d
<
H_{\mathrm{down}}
<
H_u.
$$

The dam is submerged.

Since

$$
H_u>H_d,
$$

the leakage relation is

$$
Q_{\mathrm{leak}}
=
\frac{KW}{r}\Delta H.
$$

Because downstream water is also above the crest, the simplified submerged overflow term becomes

$$
Q_{\mathrm{overtop}}
=
CW(\Delta H)^{3/2}.
$$

Therefore,

$$
\boxed{
Q_{\mathrm{dam}}
=
\frac{KW}{r}\Delta H
+
CW(\Delta H)^{3/2}.
}
$$

The important feature is that $H_d$ has disappeared from the equation.

At equilibrium,

$$
Q_{\mathrm{dam}}
=
Q_{\mathrm{in}}
=
0.05\ \mathrm{m^3/s}.
$$

So while the dam remains submerged, the equilibrium head difference is controlled by the flow parameters rather than dam height.

The numerical experiment gives

$$
\Delta H^*
=
0.045504\ \mathrm{m}
$$

for all three of

$$
H_d=0.20,\quad0.30,\quad0.32\ \mathrm{m}.
$$

The plateau is therefore a consequence of the equations rather than a numerical coincidence.

---

## 12.2 Why the transition occurs between 0.32 m and 0.34 m

Within the submerged plateau,

$$
H_{\mathrm{down}}^*
\approx
0.33725\ \mathrm{m}.
$$

As long as

$$
H_d
<
H_{\mathrm{down}}^*,
$$

the downstream water surface remains above the dam crest.

Once

$$
H_d
>
H_{\mathrm{down}}^*,
$$

the crest itself becomes the controlling level for overtopping.

The experiment sampled

$$
H_d=0.32\ \mathrm{m}
$$

and

$$
H_d=0.34\ \mathrm{m},
$$

so the transition is bracketed by

$$
\boxed{
H_d
=
0.32\text{--}0.34\ \mathrm{m}.
}
$$

---

## 12.3 Why increasing dam height increases equilibrium head difference

After the transition,

$$
H_{\mathrm{down}}
<
H_d
<
H_u.
$$

This is the free-overtopping regime.

Leakage remains

$$
Q_{\mathrm{leak}}
=
\frac{KW}{r}\Delta H,
$$

while the overtopping depth is

$$
h
=
H_u-H_d.
$$

Using

$$
H_u
=
\frac{S+\Delta H}{2},
$$

the equilibrium condition becomes

$$
Q
=
\frac{KW}{r}\Delta H
+
CW
\left(
\frac{S+\Delta H}{2}
-
H_d
\right)^{3/2}.
$$

Here $Q$ is fixed.

If $H_d$ increases, overtopping depth becomes smaller.

For the system to continue carrying the same imposed discharge, $\Delta H$ must therefore adjust.

We can prove the direction of this adjustment using implicit differentiation.

Define

$$
F(\Delta H,H_d)
=
\frac{KW}{r}\Delta H
+
CW
\left(
\frac{S+\Delta H}{2}
-
H_d
\right)^{3/2}
-Q.
$$

Equilibrium corresponds to

$$
F(\Delta H,H_d)=0.
$$

Since $\Delta H$ depends on $H_d$, differentiate both sides with respect to $H_d$:

$$
\frac{d}{dH_d}
F(\Delta H,H_d)
=
0.
$$

Using the chain rule,

$$
\frac{\partial F}{\partial\Delta H}
\frac{d\Delta H}{dH_d}
+
\frac{\partial F}{\partial H_d}
=
0.
$$

Therefore,

$$
\boxed{
\frac{d\Delta H}{dH_d}
=
-
\frac{
\partial F/\partial H_d
}{
\partial F/\partial\Delta H
}.
}
$$

Let

$$
g
=
\frac{S+\Delta H}{2}
-
H_d.
$$

In the free-overtopping regime,

$$
g>0.
$$

Then

$$
\frac{\partial F}{\partial H_d}
=
-\frac32 CW\sqrt{g}
<
0,
$$

while

$$
\frac{\partial F}{\partial\Delta H}
=
\frac{KW}{r}
+
\frac34CW\sqrt{g}
>
0.
$$

Therefore,

$$
\frac{d\Delta H}{dH_d}
=
\frac{
\frac32CW\sqrt{g}
}{
\frac{KW}{r}
+
\frac34CW\sqrt{g}
}.
$$

Every term is positive, so

$$
\boxed{
\frac{d\Delta H^*}{dH_d}
>
0.
}
$$

Therefore, within the free-overtopping regime of this model, increasing dam height must increase equilibrium head difference.

This mathematical result explains the rising part of the Experiment 1 curve.

---

# 13. Experiment 2 — varying hydraulic conductivity

Experiment 2 fixes the dam near the completed construction baseline:

$$
H_d
=
0.4375\ \mathrm{m}.
$$

Therefore,

$$
T
=
2.9(0.4375)
=
1.26875\ \mathrm{m}.
$$

The tested conductivity values range from

$$
K=0.002
$$

to

$$
K=0.67\ \mathrm{m/s}.
$$

The main numerical result is that increasing $K$ reduces the equilibrium head difference.

---

## 13.1 Why increasing $K$ reduces $\Delta H^*$

In the mixed leakage/overtopping regime,

$$
Q
=
\frac{KW}{r}\Delta H
+
CW
\left(
\frac{S+\Delta H}{2}
-
H_d
\right)^{3/2}.
$$

Increasing $K$ means that more leakage can pass through the dam for the same head difference.

Since the required total equilibrium flow remains fixed,

$$
Q=0.05\ \mathrm{m^3/s},
$$

the system no longer requires as large a $\Delta H$.

Again define

$$
F(\Delta H,K)=0.
$$

Then

$$
\frac{\partial F}{\partial K}
=
\frac{W}{r}\Delta H
>
0,
$$

while

$$
\frac{\partial F}{\partial\Delta H}
>
0.
$$

Implicit differentiation therefore gives

$$
\frac{d\Delta H}{dK}
=
-
\frac{
\partial F/\partial K
}{
\partial F/\partial\Delta H
}
<
0.
$$

Hence,

$$
\boxed{
\frac{d\Delta H^*}{dK}
<
0.
}
$$

This matches the numerical experiment.

---

## 13.2 Transition to leakage-only flow

As $K$ increases, leakage carries an increasing proportion of the required total discharge.

The transition to leakage-only flow occurs when the upstream water surface has just fallen to the dam crest:

$$
H_u
=
H_d.
$$

For Experiment 2,

$$
H_d
=
0.4375\ \mathrm{m}.
$$

Since

$$
H_u+H_{\mathrm{down}}
=
0.72,
$$

the downstream depth at the transition must be

$$
H_{\mathrm{down}}
=
0.72-0.4375
=
0.2825\ \mathrm{m}.
$$

Therefore,

$$
\Delta H_{\mathrm{crit}}
=
0.4375-0.2825
=
0.155\ \mathrm{m}.
$$

At the threshold,

$$
Q_{\mathrm{overtop}}
=
0,
$$

so all equilibrium flow must pass through the dam:

$$
Q
=
Q_{\mathrm{leak}}.
$$

Since the water reaches the full dam height,

$$
Q
=
\frac{KW}{r}
\Delta H_{\mathrm{crit}}.
$$

Solving for $K$,

$$
\boxed{
K_{\mathrm{crit}}
=
\frac{
rQ
}{
W\Delta H_{\mathrm{crit}}
}.
}
$$

Substituting

$$
r=2.9,
$$

$$
Q=0.05,
$$

$$
W=3,
$$

and

$$
\Delta H_{\mathrm{crit}}=0.155
$$

gives

$$
K_{\mathrm{crit}}
\approx
0.3118\ \mathrm{m/s}.
$$

The numerical experiment gives a very similar result.

At

$$
K=0.31\ \mathrm{m/s},
$$

there is still a very small overtopping flow:

$$
Q_{\mathrm{overtop}}
\approx
2.69\times10^{-5}\ \mathrm{m^3/s}.
$$

At

$$
K=0.32\ \mathrm{m/s},
$$

the model gives

$$
Q_{\mathrm{overtop}}
=
0.
$$

Therefore the numerical transition is bracketed by

$$
\boxed{
K
\approx
0.31\text{--}0.32\ \mathrm{m/s},
}
$$

in close agreement with the analytical prediction.

---

## 13.3 Analytical solution in the leakage-only regime

Once

$$
H_u<H_d,
$$

there is no overtopping.

The wetted height is now $H_u$, so

$$
Q
=
\frac{
KWH_u\Delta H
}{
rH_d
}.
$$

Using

$$
H_u
=
\frac{S+\Delta H}{2},
$$

gives

$$
Q
=
\frac{KW}{2rH_d}
\left(
S\Delta H+\Delta H^2
\right).
$$

Rearranging,

$$
\Delta H^2
+
S\Delta H
-
\frac{
2rH_dQ
}{
KW
}
=
0.
$$

The physically relevant positive root is

$$
\boxed{
\Delta H
=
\frac{
-S+
\sqrt{
S^2+
\frac{
8rH_dQ
}{
KW
}
}
}{2}.
}
$$

This expression directly shows how the leakage-only equilibrium depends on conductivity.

For example, at

$$
K=0.67\ \mathrm{m/s},
$$

the numerical experiment gives

$$
\Delta H^*
=
0.078922\ \mathrm{m}.
$$

---

# 14. Analytical extension — what if discharge were varied?

I did not run this as a third experiment, but I explored what the current equations predict if

$$
Q_{\mathrm{in}}
=
Q_{\mathrm{out}}
=
Q
$$

is varied while dam geometry and $K$ remain fixed.

The model predicts

$$
\boxed{
Q\uparrow
\quad\Longrightarrow\quad
\Delta H^*\uparrow.
}
$$

This can be shown mathematically in each flow regime.

## 14.1 Submerged regime

Here,

$$
Q
=
\frac{KW}{r}\Delta H
+
CW(\Delta H)^{3/2}.
$$

Therefore,

$$
\frac{dQ}{d\Delta H}
=
\frac{KW}{r}
+
\frac32CW\sqrt{\Delta H}.
$$

Every term is positive, so

$$
\boxed{
\frac{dQ}{d\Delta H}
>
0.
}
$$

## 14.2 Free-overtopping regime

Here,

$$
Q
=
\frac{KW}{r}\Delta H
+
CW
\left(
\frac{S+\Delta H}{2}
-H_d
\right)^{3/2}.
$$

Therefore,

$$
\frac{dQ}{d\Delta H}
=
\frac{KW}{r}
+
\frac{3CW}{4}
\sqrt{
\frac{S+\Delta H}{2}
-H_d
}.
$$

Again,

$$
\boxed{
\frac{dQ}{d\Delta H}
>
0.
}
$$

## 14.3 Leakage-only regime

Here,

$$
Q
=
\frac{KW}{2rH_d}
\left(
S\Delta H+\Delta H^2
\right).
$$

Therefore,

$$
\frac{dQ}{d\Delta H}
=
\frac{KW}{2rH_d}
\left(
S+2\Delta H
\right)
>
0.
$$

So, within all three regimes of this simplified model,

$$
\boxed{
Q\uparrow
\Longrightarrow
\Delta H^*\uparrow.
}
$$

This also shows why the conductivity transition found in Experiment 2 is scenario-dependent.

At the leakage-only threshold,

$$
K_{\mathrm{crit}}
=
\frac{
rQ
}{
W\Delta H_{\mathrm{crit}}
}.
$$

For fixed geometry and stored water,

$$
\boxed{
K_{\mathrm{crit}}
\propto Q.
}
$$

So the numerical result

$$
K_{\mathrm{crit}}
\approx
0.312\ \mathrm{m/s}
$$

is not a universal property of beaver dams.

It is the critical conductivity predicted by this model for the particular baseline discharge

$$
Q
=
0.05\ \mathrm{m^3/s}.
$$

Varying discharge would therefore be a useful future sensitivity experiment.

---

# 15. Numerical implementation and timescales

The interactive construction simulation and the controlled experiments use slightly different timing approaches.

## 15.1 Interactive simulation

`main.py` runs at a target of 60 frames per second.

The update time step is calculated from actual elapsed frame time:

```python
dt = clock.tick(FPS) / 1000.0
```

During the construction phase,

- the beaver moves and delivers material,
- dam geometry changes,
- river hydrology evolves at the same time.

After all 80 tree agents have been delivered, the model enters a separate settling phase.

At this point,

- beaver motion stops,
- dam geometry is frozen,
- water levels continue evolving until equilibrium.

For the final baseline run, the post-construction settling time was

$$
48.6\ \mathrm{s}.
$$

## 15.2 Controlled experiments

`experiment.py` uses a fixed numerical time step

$$
dt=0.1\ \mathrm{s}.
$$

Every experiment begins immediately with a completed dam and with both water depths reset to

$$
0.36\ \mathrm{m}.
$$

A run ends when the equilibrium flow conditions remain satisfied for five seconds.

A safety limit of

$$
5000\ \mathrm{s}
$$

prevents a failed run from continuing indefinitely.

Because the experiments and the interactive construction run start from different hydraulic states, their equilibrium times should not be compared directly.

For example, the Experiment 2 baseline case near the completed dam height takes about

$$
74.6\ \mathrm{s},
$$

whereas the interactive model reports only the **post-construction** settling period of

$$
48.6\ \mathrm{s}.
$$

The upstream and downstream water depths have already been evolving during construction before that 48.6 s settling phase begins.

## 15.3 Development timeframe

The project was originally planned as a ten-day personal mathematical-modelling project.

In practice, development was spread intermittently from late July to late September 2026.

The later stages included:

- experimental analysis,
- code verification,
- literature reality checks,
- replacement of the original rectangular dam geometry,
- rerunning the experiments,
- and final documentation.

A fuller chronology is recorded separately in the project journal.

---

# 16. Mathematical limitations

The equations above explain the behaviour of the simulation, but they are not a complete physical model of a natural river or beaver dam.

Important simplifications include:

- upstream and downstream water are each represented by one uniform depth;
- the storage geometry is rectangular;
- velocity fields and momentum equations are not modelled;
- spatial backwater effects are ignored;
- external inflow and downstream outflow are fixed;
- dam permeability is represented by one effective hydraulic conductivity $K$;
- the leakage relation treats the dam as a simplified porous medium;
- overtopping uses an idealised weir-style law;
- submerged-dam flow is simplified rather than using a full submerged-weir correction;
- the dam is forced to maintain the fixed relation $T/H_d=2.9$;
- the triangular dam envelope does not separately represent voids, mud, stones or sediment;
- the tree-selection rule is a heuristic rather than a full energetic optimisation model;
- all 80 tree agents are eventually harvested, so the foraging rule affects harvesting order rather than the final amount of material.

These limitations mean that numerical values such as

$$
K_{\mathrm{crit}}
\approx
0.312\ \mathrm{m/s}
$$

belong to the particular scenario used in this project.

The more general results are the mechanisms revealed by the equations:

1. A sufficiently low submerged dam produces a plateau in equilibrium head difference because dam height cancels from the governing flow equation.

2. Once the crest becomes the controlling level, increasing dam height increases equilibrium head difference.

3. Increasing hydraulic conductivity reduces the head difference needed to carry the imposed discharge.

4. At sufficiently high conductivity, leakage alone can carry the required flow and overtopping disappears.

5. For a fixed dam and conductivity, increasing river discharge requires a larger equilibrium head difference.

These mathematical explanations became an important part of the project because they allowed the numerical results to be understood rather than only observed.
