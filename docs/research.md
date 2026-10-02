# Research and Reality Checks

This file records the research that actually influenced the project, including research I did near the beginning and reality checks I carried out much later.

I do not want this file to make the model look more scientifically calibrated than it really is. A lot of the project still relies on simplifications and choices I made myself. What the research helped me do was decide which ideas were reasonable, notice assumptions that were weak, and understand which parts of the final model I could defend more confidently.

---

## 1. Where the project started

The original idea for this project was quite different from the final model.

I first wanted to investigate whether a beaver could deliberately cut a tree in a way that made it fall towards the river, reducing the distance it then had to transport the wood.

That question led me towards tree cutting, transport and beaver foraging. I eventually decided not to build a detailed tree-fall mechanics model because I could not find enough evidence to justify assumptions about things such as cutting angle, centre of mass, terrain, branch distribution and uncertainty in the direction of fall.

Rather than inventing all of those mechanics, I moved towards something I could support more convincingly: how a beaver chooses between available trees, how the material is transported to the dam, and what happens hydraulically as the dam grows.

The original tree-fall question still matters because it explains where the project came from, but it is no longer the main question being tested.

---

## 2. Foraging and tree selection

One of the ideas that became important quite early was **central-place foraging**.

Haarberg and Rosell studied Eurasian beaver foraging in Norway and found that foraging intensity declined as distance from the river increased. They also found evidence that size and species selectivity changed with distance [1].

That gave me a useful way to think about tree selection: a tree should not be attractive simply because it is large. The possible benefit of collecting it also has to be balanced against the cost of reaching, cutting and transporting it.

That idea became the inspiration for the selection score in the simulation.

The score itself is my own simplified rule. It includes:

- a size term;
- a species-preference factor;
- distance from the beaver;
- a cutting-cost term.

I use `diameter × length` as a simple size / benefit proxy in this behavioural score. This is deliberately not the same as physical wood volume. Once material reaches the dam, I calculate cylindrical volume separately.

I considered changing the selection score to use cylindrical volume as well, but decided against doing this during the final revision. Volume scales with diameter squared, so it would strongly reward thick pieces, while my current cutting-cost term only grows linearly with diameter. Changing only the benefit side would not automatically make the behaviour more realistic.

The current selection rule should therefore be understood as a **central-place-foraging-inspired heuristic**, not as a calibrated ecological equation.

---

## 3. Tree species preference

Species preference is another feature I wanted the model to represent.

There is no single universal preference order for beavers because diet and available vegetation differ between habitats. Haarberg and Rosell's Eurasian-beaver study, for example, found strong use of willow along with other locally available species [1]. North American National Park Service sources also describe willow, aspen and cottonwood as important or preferred woody foods in several beaver habitats [2].

I therefore made the following species preferred in the simulation:

- aspen;
- willow;
- cottonwood.

Oak, pine and fir are treated as less preferred.

The exact species probabilities and numerical preference weights are **not** taken from a field dataset. They are modelling choices used to create a mixed environment in which species preference can influence the beaver's decision.

So the research supports the idea that species matters, but it does not justify my exact probabilities or the precise factors `1.0` and `0.2` used in the model.

---

## 4. What do the “trees” in the simulation represent?

This became slightly confusing during development because drawing whole realistic trees created a scale problem.

A full tree would be very large relative to the small stream and the simulation window, while a physically realistic trunk diameter could become almost invisible on screen.

I therefore treat each tree agent as an **effective usable-wood resource** with:

- a species;
- a location;
- an effective usable-wood diameter;
- an effective usable-wood length.

When the material is delivered to the dam, its wood volume is approximated as a cylinder:

```math
V_{\mathrm{wood}}
=
\pi\left(\frac{d}{2}\right)^2L
```

The rectangles shown in the top view should therefore not be interpreted as literal full trees drawn to physical scale.

There are 80 tree agents in the final baseline simulation. This is also not a claim that a real beaver dam contains only 80 sticks. Each agent is an effective usable-wood unit inside the simplified model.

---

## 5. River size: a late reality check

I originally chose a small-stream baseline with:

- river width = **3.0 m**;
- initial water depth = **0.36 m**.

These values were chosen as a modelling scenario, not taken from a particular field study.

Later, while checking the project against real measurements, I found a study by Hartman and Törnlöv that measured stream conditions at 74 Eurasian-beaver dam sites [3]. They reported:

| Measurement | Mean | Observed range |
|---|---:|---:|
| Stream width at dam sites | 2.5 m | 0.5–6.0 m |
| Water depth at dam sites | 0.36 m | 0.10–0.85 m |

This was reassuring because my original `3.0 m × 0.36 m` stream lies close to the conditions reported for those dam sites.

Importantly, I did **not** choose my original values from this study. I found the paper during the later reality-check stage, so I kept my existing stream dimensions rather than changing them retrospectively and pretending they had been calibrated from the beginning.

This became a useful distinction in the project: sometimes later research confirmed an assumption I had already made; in other cases it showed that I needed to change one.

---

## 6. How large should the dam be?

Dam dimensions vary a lot between locations, so I do not think it makes sense to describe one single “normal” beaver dam.

Hafen et al. summarise earlier North American studies as giving dam heights generally around **0.2–2.2 m**, with a mean of roughly **1.0 m** across the compiled literature [4].

My completed baseline dam has a height of approximately:

```math
H_d = 0.437\ \mathrm{m}
```

This places the simulated dam towards the smaller end of that broad reported range.

I decided not to increase the number of wood units simply to force the final dam closer to the reported mean. The simulated stream is small, and the aim is not to reproduce an “average dam” at all costs.

The completed baseline should therefore be interpreted as a relatively small dam in an idealised small-stream scenario.

---

## 7. Dam materials

Another important simplification is that real beaver dams are not made from wood alone.

The U.S. National Park Service describes beavers using combinations of trees and branches with materials such as grass, rocks and mud during dam construction [5]. Real structures can also trap sediment and other debris over time.

My model tracks only usable wood volume.

This means the accumulated wood volume is currently mapped directly into the idealised dam envelope. In reality, the structure would contain voids as well as non-wood material.

I considered introducing another packing or material-composition factor, but I decided not to add an extra parameter without evidence for what its value should be.

So this remains a known simplification rather than something I tried to hide by introducing another guessed constant.

---

## 8. The biggest geometry correction

One of the most important research moments happened very late in the project.

My earlier model assumed a rectangular cross-section and used a linear thickness rule:

```math
T = T_0 + kH_d
```

I initially tried:

```math
k = 1.5
```

and later reduced it to:

```math
k = 0.6
```

because the first value made the dam thicken too aggressively.

At that stage, however, both values were still heuristic. I had not calibrated either one against measured beaver-dam geometry.

During the final reality check I found Müller and Watling's work on the engineering of beaver dams [6]. Their paper reports that wooden dams have:

- a roughly triangular cross-section;
- an average cross-sectional width-to-height ratio of about **2.9**;
- a shallower upstream face;
- a steeper downstream face.

This showed that my earlier model was actually too thin relative to its height.

Instead of trying to find another value of `k`, I removed the linear-thickness rule altogether.

In the final model, the streamwise dam thickness is represented by:

```math
T = 2.9H_d
```

For a triangular cross-section,

```math
V_{\mathrm{dam}}
=
\frac{1}{2}WTH_d
```

The resulting height equation is derived in `math_notes.md`.

After making this change, I reran the construction baseline and both experiments. This was probably the clearest example in the project of research **changing** the model rather than simply being used to justify something I had already built.

### A detail I did not get from the paper

In the side-view drawing I represent the upstream face as shallower than the downstream face using an approximate **70:30 visual split**.

The literature supports the general asymmetry, but not that exact 70:30 value. That part of the diagram is schematic.

---

## 9. Permeability and leakage

A beaver dam is not an impermeable wall. Water can move through gaps and porous material inside the structure as well as over its crest.

Müller and Watling report laboratory tests on wooden dam structures in which one tested dam was described approximately as a linear / Darcy filter, with a filter coefficient of about:

```math
k_f = 0.67\ \mathrm{m/s}
```

[6]

This helped support the decision to include a Darcy-style leakage term in the model.

The simulation uses:

```math
Q_{\mathrm{leak}}
=
K A_{\mathrm{wetted}}
\frac{\Delta H}{T}
```

I do **not** treat the published `0.67 m/s` value as a universal hydraulic conductivity for natural beaver dams. It came from one laboratory structure with its own geometry and construction.

The baseline value in my simulation is:

```math
K = 0.01\ \mathrm{m/s}
```

and this is a modelling scenario rather than a calibrated field value.

Experiment 2 varies `K` over a wide range, and I later included `0.67 m/s` as a published reference-scale case rather than as the baseline.

Real effective permeability could depend on many things, including:

- wood arrangement;
- mud and sediment;
- void structure;
- maintenance;
- dam age;
- local flow conditions.

I therefore treat `K` as a single **effective bulk parameter** for the simplified dam.

---

## 10. Overtopping

Water can also cross the dam by flowing over the controlling level.

For this part I use a standard weir-style relationship:

```math
Q_{\mathrm{overtop}}
=
CWh^{3/2}
```

The U.S. Army Corps of Engineers uses the same general form for weir flow, written as `Q = CLH^{1.5}`, where the discharge coefficient depends on the configuration of the weir [7].

This gave me a simple way to represent the rapid increase in overtopping as the water level rises above the controlling level.

The coefficient `C` in my model is **not** a measured “beaver-dam coefficient”. It is another engineering simplification.

The treatment of a fully submerged dam is also simplified and should not be interpreted as a complete submerged-weir formulation.

---

## 11. What this research does — and does not — let me claim

After going through the project again, I think this distinction is important.

Research gives me reasonable support for the following general ideas:

- beaver foraging is affected by distance from water;
- tree size and species can influence selection;
- small streams are common dam-building environments;
- wooden beaver dams can have triangular, asymmetric cross-sections;
- beaver dams are permeable rather than perfectly solid barriers;
- real dams contain more than wood alone.

There are still many things that remain my own modelling assumptions:

- exact species-generation probabilities;
- exact species-preference weights;
- the tree-selection equation;
- the cutting-cost coefficient;
- the choice of 80 tree agents;
- the triangular distributions used for usable wood dimensions;
- baseline conductivity `K = 0.01 m/s`;
- fixed inflow and outflow of `0.05 m³/s`;
- the simplified two-storage river geometry;
- the 70:30 visual slope split;
- the overtopping coefficient.

I do not see that as something to disguise.

The point of the project was not to produce a perfectly calibrated ecological or hydraulic simulator. It was to build a model from scratch, question its assumptions, compare them with real evidence, and revise the model when the evidence showed that something no longer made sense.

---

## References

[1] Haarberg, O. & Rosell, F. (2006). *Selective foraging on woody plant species by the Eurasian beaver (Castor fiber) in Telemark, Norway*. **Journal of Zoology, 270**, 201–208. DOI: [10.1111/j.1469-7998.2006.00142.x](https://doi.org/10.1111/j.1469-7998.2006.00142.x)

[2] U.S. National Park Service. *Beaver — Yellowstone National Park*. Describes willow, aspen and cottonwood as preferred foods in Yellowstone. https://www.nps.gov/yell/learn/nature/beaver.htm

[3] Hartman, G. & Törnlöv, S. (2006). *Influence of watercourse depth and width on dam-building behaviour by Eurasian beaver (Castor fiber)*. **Journal of Zoology, 268**, 127–131. DOI: [10.1111/j.1469-7998.2005.00025.x](https://doi.org/10.1111/j.1469-7998.2005.00025.x)

[4] Hafen, K. C., Wheaton, J. M., Roper, B. B., Bailey, P. & Bouwes, N. (2020). *Influence of topographic, geomorphic, and hydrologic variables on beaver dam height and persistence in the intermountain western United States*. **Earth Surface Processes and Landforms, 45(11)**, 2664–2674. DOI: [10.1002/esp.4921](https://doi.org/10.1002/esp.4921)

[5] U.S. National Park Service. *Build a Beaver Dam*. Describes trees and branches being combined with grass, rocks and mud during dam construction. https://www.nps.gov/articles/buildabeaverdam.htm

[6] Müller, G. & Watling, J. (2016). *The engineering in beaver dams*. **River Flow 2016: Eighth International Conference on Fluvial Hydraulics**. University of Southampton ePrints: https://eprints.soton.ac.uk/400282/

[7] U.S. Army Corps of Engineers, HEC-HMS Technical Reference. *Diversion Modeling Concepts and Equations*. Includes the weir-flow relationship `Q = CLH^1.5`. https://www.hec.usace.army.mil/confluence/hmsdocs/hmstrm/diversion-modeling/diversion-modeling-concepts-and-equations
