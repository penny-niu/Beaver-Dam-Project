This file is a record of the research that actually influenced the project, including research I did at the beginning and reality checks I carried out much later.
I don't want this to make the model look more “scientifically calibrated” than it really is. A lot of the project still relies on simplifications and choices I made myself. What the research helped me do was decide which ideas were reasonable, spot assumptions that were not, and understand which parts of the final model I could defend more confidently.


1. Where the project started

The original idea for this project was quite different than the final model.
I first wanted to investigate whether a beaver could deliberately cut a tree in a way that made it fall towards the river, reducing the distance it then had to transport the wood.
That question led me into research on tree cutting, transport and beaver foraging. I eventually decided not to build a detailed tree-fall mechanics model because I could not find enough evidence to justify assumptions about things such as cutting angle, centre of mass, terrain, branch distribution and uncertainty in the direction of fall.
Rather than inventing all of those mechanics, I moved towards something I could support more convincingly: how a beaver chooses between available trees, how material is transported to the dam, and what happens hydraulically as the dam grows.

The original falling-angle question still matters because it explains where the whole project came from, but it is no longer the main question being tested.


2. Foraging

One of the ideas that became important quite early was central-place foraging.
Beavers repeatedly leave the water, collect woody material, and return towards the water or another central location. Research by Haarberg and Rosell found that foraging intensity decreased as distance from the river increased, and that size/species selectivity also changed with distance [1].
That gave me a useful way to think about tree selection:
a tree should not be attractive simply because it is large; the benefit of collecting it has to be balanced against the cost of reaching, cutting and transporting it.

That became the inspiration for the selection score in the simulation.
The score itself is my own simplified rule. It uses:
- a size term;
- a species-preference factor;
- distance;
- a cutting-cost term.

I used width × height as a simple size proxy in this behavioural score. This is deliberately not the physical wood volume. When material actually reaches the dam, I calculate its cylindrical volume separately.
I considered changing the selection score to use cylindrical volume as well, but decided against doing this during the final revision. Using volume would strongly favour thicker pieces because volume scales with diameter squared, while my current cutting-cost term only grows linearly with diameter. Changing one without rebuilding the cost model would not automatically make the behaviour more realistic.
So the current selection rule should be understood as a central-place-foraging-inspired heuristic, rather than a calibrated ecological equation.


3. Tree species preference

Species preference is another feature I wanted the model to represent.
Beaver diets vary between habitats, so there is not one universal ordering of every tree species. However, willow and members of the poplar group are frequently important resources, and North American sources commonly identify willow, cottonwood and aspen as heavily used woody species [2].
I therefore made:
- aspen,
- willow,
- cottonwood
the preferred species in the simulation.
The exact preference weights and the probabilities used to generate each species in my forest are not taken from a field dataset. They are modelling choices used to create a mixed environment in which species preference can influence the beaver's decision.
This distinction matters: the research supports the idea of species-dependent preference, but not my precise numerical probabilities.
4. What do the “trees” in the simulation represent?
This became slightly confusing during development because drawing whole realistic trees created a scale problem.
Most parts of the environment can be represented at a reasonably sensible physical scale, but full trees would be much too large relative to the river and screen.
I therefore treat each tree agent as a tree resource with:
- a species;
- a location;
- an effective usable-wood diameter;
- an effective usable-wood length.
When it is delivered to the dam, its wood volume is calculated as a cylinder:
\[
V_{\text{wood}}
=
\pi
\left(\frac{d}{2}\right)^2
L.
\]So the rectangles shown in the top view should not be interpreted as literal full trees drawn to scale.
There are 80 tree agents in the final baseline simulation. This should also not be interpreted as a claim that a real beaver dam contains only 80 sticks. Each agent is an effective usable-wood unit within the simplified model.
5. River size: a late reality check
I originally chose a small stream with:
- width = 3 m
- initial water depth = 0.36 m
as a reasonable modelling scenario.
Later, while checking the project against real measurements, I found a study by Hartman and Törnlöv [3] that measured 74 Eurasian-beaver dam sites.
They reported:
Measurement	Mean	Observed range
Stream width at dam sites	2.5 m	0.5–6.0 m
Water depth at dam sites	0.36 m	0.10–0.85 m


This was reassuring because my original 3 m × 0.36 m stream sits very close to those reported dam-site conditions.
Importantly, I did not choose my original values from this study. I found it during the final reality-check stage, so I kept my existing stream dimensions rather than changing them retrospectively and pretending they had been calibrated from the beginning.
That became a useful lesson in the project: sometimes research confirmed an assumption I had already made, while in other cases it showed that I needed to change one.
6. How large should the dam be?
Dam dimensions vary a lot between sites, so I do not think it makes sense to talk about one single “normal” beaver dam.
A review of North American beaver dams reports heights commonly in the range of roughly 0.2–2.2 m, with a mean around 1 m across compiled studies [4].
My completed baseline dam has a height of approximately:
\[
H_d = 0.437\text{ m}.
\]This puts it towards the smaller end of observed dams, but still within a realistic range.
I decided not to increase the number of wood units simply to make the dam closer to the reported mean height. The simulated stream is small, and the goal is not to reproduce an “average dam” at all costs.
The final dam should therefore be thought of as a relatively small dam in an idealised small-stream scenario.
7. Dam materials
Another important simplification is that real beaver dams are not made from wood alone.
Beavers use combinations of:
- branches and logs;
- mud;
- vegetation;
- rocks and gravel;
- naturally trapped debris and sediment.
The U.S. National Park Service describes trees and branches being combined with grass, rocks and mud during dam construction [5].
My model tracks only usable wood volume.
This means I currently treat the accumulated wood volume as the volume used to determine the idealised dam envelope. In reality there would be voids and non-wood material as well.
I considered introducing an additional packing or material-composition factor, but I decided not to add another parameter without evidence for what its value should be.
So this remains a known simplification rather than something I tried to hide with another guessed constant.
8. The biggest geometry correction
One of the most important research moments happened very late in the project.
My earlier model assumed a rectangular dam and used a linear rule:
\[
T = T_0 + kH_d.
\]I initially tried:
\[
k = 1.5,
\]then reduced it to:
\[
k = 0.6
\]because the first value made the dam appear to thicken too aggressively.
At that stage, however, both values were still heuristic. I had not calibrated either one against real dam geometry.
While checking the model before writing the final documentation, I found Müller and Watling's work on the engineering of beaver dams [6]. They describe wooden dams as having:
- a roughly triangular cross-section;
- an average width-to-height ratio of about 2.9;
- a shallower upstream face;
- a steeper downstream face.
That immediately showed that my old dam was actually too thin relative to its height.
Instead of trying to find yet another value of \(k\), I removed the linear-thickness model altogether.
The final model uses:
\[
T = 2.9H_d.
\]For a triangular cross-section:
\[
V_{\text{dam}}
=
\frac{1}{2}WTH_d.
\]The full derivation of the resulting height equation is kept in math_notes.md.
After making this change, I reran the construction baseline and both experiments.
This was probably the clearest example in the project of research actually changing the model rather than simply being used to justify something I had already built.
A detail I did not get from the paper
In the side-view drawing I represent the upstream face as shallower than the downstream face using an approximate 70:30 visual split.
The literature supports the general asymmetry, but not that exact 70:30 value.
That part remains schematic.
9. Permeability and leakage
A beaver dam is not an impermeable wall.
Water can move through gaps and porous material inside the dam as well as over its crest.
Müller and Watling performed laboratory tests on wooden beaver-dam structures and found that one tested dam could be approximated as a Darcy-type filter, with a reported filter coefficient of about:
\[
0.67\text{ m/s}.
\][6]
This helped support the idea of including a leakage term in the model.
The simulation uses:
\[
Q_{\text{leak}}
=
K A_{\text{wetted}}
\frac{\Delta H}{T}.
\]However, I do not use \(0.67\text{ m/s}\) as the baseline conductivity.
The baseline:
\[
K = 0.01\text{ m/s}
\]is a modelling scenario rather than a calibrated field value.
Instead, Experiment 2 varies \(K\), and I later extended the experiment to include \(0.67\text{ m/s}\) as a published reference-scale case.
This seemed more defensible than pretending one laboratory measurement represents the permeability of every natural beaver dam.
Real permeability could vary with:
- wood arrangement;
- mud and sediment;
- void structure;
- maintenance;
- dam age;
- local flow conditions.
I therefore treat \(K\) as an effective bulk parameter.
10. Overtopping
Water can also cross the dam by flowing over the crest.
For this part I used the standard weir-style relationship:
\[
Q_{\text{overtop}}
=
CWh^{3/2}.
\]Engineering hydraulic models use the same general form, although the discharge coefficient \(C\) depends on the geometry of the structure [7].
This gave me a simple way to represent the rapid increase in overtopping once water rises above the controlling level.
The coefficient in my model is not a measured “beaver-dam coefficient”. It is another engineering simplification.
The treatment of a fully submerged dam is also simplified and should not be interpreted as a full submerged-weir model.
11. What this research does — and does not — let me claim
After going through the project again, I think this distinction is important.
There are parts of the final model that now have clear support from research:
- beaver foraging is affected by distance;
- tree species and size influence selection;
- small streams are common dam-building sites;
- wooden dams can have triangular, asymmetric cross-sections;
- natural dams are permeable;
- real dams contain more than wood.
There are also still many things that are my modelling assumptions:
- exact species probabilities;
- exact species preference weights;
- the tree-selection equation;
- the cutting-cost coefficient;
- 80 tree agents;
- the initial forest distributions;
- baseline conductivity \(K=0.01\);
- fixed inflow and outflow of \(0.05\text{ m}^3/\text{s}\);
- the simplified river storage geometry;
- the 70:30 visual slope split;
- the overtopping coefficient.
I do not see that as something to disguise.
The point of this project was not to produce a perfectly calibrated ecological simulator. It was to build a model from scratch, question its assumptions, compare them with real evidence, and revise the model when the evidence showed that something no longer made sense.
References
[1] Haarberg, O. & Rosell, F. (2006). Selective foraging on woody plant species by the Eurasian beaver (Castor fiber) in Telemark, Norway. Journal of Zoology, 270, 201–208. DOI: 10.1111/j.1469-7998.2006.00142.x.
[2] U.S. National Park Service. Beaver habitat and feeding information, including use of willow, cottonwood and aspen.
[3] Hartman, G. & Törnlöv, S. (2006). Influence of watercourse depth and width on dam-building behaviour by Eurasian beaver (Castor fiber). Journal of Zoology, 268, 127–131. DOI: 10.1111/j.1469-7998.2005.00025.x.
[4] Ronnquist, A. L. & Westbrook, C. J. (2021). Influence of topographic, geomorphic, and hydrologic variables on beaver dam height and persistence in the intermountain western United States. Hydrobiologia.
[5] U.S. National Park Service. Build a Beaver Dam. Description of wood, branches, grass, rocks and mud used in dam construction.
[6] Müller, G. & Watling, J. The engineering in beaver dams. University of Southampton. Includes wooden-dam cross-sectional geometry and laboratory permeability experiments.
[7] U.S. Army Corps of Engineers, HEC-HMS Technical Reference. Weir-flow relationship \(Q = CLH^{1.5}\).
