# Project Journal

A rough journal of how the project developed. Some entries were reconstructed later from my code and notes, so a few dates are approximate, but I wanted to keep a record of how the model changed rather than only showing the final version.

---

## 28 July 2026

I was wondering whether a beaver could make things easier for itself by cutting a tree so that it falls towards the river when building the dam.

Did some research on beavers, mostly tree choice, how they build dams, what kinds of trees they seem to prefer, etc.

Not really sure how I would model that yet. I was thinking maybe cutting angle? centre of mass? direction of fall? 

---

## 29 July 2026

Installed VS Code and got Pygame working.

Mostly just setup today.

---

## 30 July 2026

Made the screen and the river.

Very basic at the moment but at least there is something visible now.

---

## 10 August 2026

Started adding trees.

Used Python's `random` module to generate positions and stopped them from appearing inside the river.

The first version was a bit chaotic because trees could end up too close together or right against the river edge. Added a gap and some simple overlap checks. 

---

## 12 August 2026

Learnt object-oriented programming and so turned the trees into proper objects instead of just drawing random rectangles directly onto the screen.

This made it much easier to give every tree its own position, dimensions and species later.

---

## 13 August 2026

The view is bothering me. The river is basically top-down, but the trees look more like little rectangles from the side. Should everything be in one perspective?

Also thought about using different colours for species because beavers have preferences for different species of trees.

Then if I choose realistic species, should I also define a particular geographical location and climate for the whole model?

---

## 14 August 2026

Added different tree species and colours.

Also added random width and height instead of making every tree identical. I used triangular distributions to make my forest less artificial. 

---

## 15 August 2026

Spent quite a while thinking about scale. 

If I use actual real-life proportions, tree trunks become tiny compared with the river and are basically invisible.

So I think I need to stop treating the drawing scale and the mathematical scale as the same thing.

The visualization can exaggerate things slightly if it makes the simulation readable?

Also cleaned up tree generation a bit more.

I kept changing the ranges because some forests looked too uniform while others had a few ridiculous trees dominating everything visually.


---

## 17 August 2026

Started thinking properly about how the beaver should choose trees.

From the research I've done, central-place foraging seems useful here: distance matters, but so do the size and species of the tree.

Built the first still beaver. It doesn't move yet.

Also thought about what the beaver should actually *do*. It should follow something like: choose a tree → move to it → cut it → take the material to the dam → choose another tree.

---

## 18 August 2026

Made a first tree-selection score and got the beaver moving towards the selected tree.

Added rough states for moving and cutting.

The cutting part is extremely simplified. The beaver basically reaches the tree and then the model waits briefly before switching state — I'm not modelling an actual cutting process.

The first version had a fairly stupid problem: after cutting a tree, the beaver would just go on to choosing another tree. I had implemented the selection part before properly implementing the "take it to the dam" part.

So at this point it could forage, but it wasn't really building anything.

The project seems to be turning more into a probability / decision-making problem with a dam-building model attached. But what can I actually do with this mathematically???

---

## 25 August 2026

Tried to fix the missing transport step.

Added a `carrying_to_dam` state so the beaver should move to the dam after cutting a tree instead of immediately selecting another one.

It still didn't behave properly at first. Sometimes it looked like it had stopped and I couldn't really tell whether it was moving to the dam or had already switched to something else.

So I added the current state as text above the beaver's head: `idle`, `moving`, `cutting`, `carrying_to_dam`, which made it much easier to see what state it was actually in.

After a few fixes the whole loop finally worked.


---

## 26 August 2026

Connected delivered tree material to the dam.

When a tree reaches the dam I calculate its cylindrical volume and add that material to the dam.

Made a first version of the dam. At the moment it is basically rectangular. 

At this point, I realised I had just kept adding more and more things to the screen, but I had kind of lost sight of what I was actually trying to achieve with all of this.  

I started thinking about directions that would give the model something more measurable to investigate, and decided to focus on the hydraulic effect of the dam — how it changes upstream and downstream water levels and flow. That gave the project a much clearer mathematical direction.

---

## 27 August 2026

Worked on dam growth.

At first I was basically just increasing the dam height as more material arrived, but then I realized that thickness should increase as well.

But what relationship should height and thickness have? Should I make them both proportional to the volume of the tree or what? 

---

## 28 August 2026

Came back to the randomness problem.

I originally thought generating a completely new forest every time was a good thing because it made the model less biased towards one arrangement.

But if I want to run experiments, that is actually annoying because changing one parameter also changes the whole forest.

Found out about random seeds and set the seed to `42`. It still comes from a random process, but I can reproduce exactly the same environment.

---

## 29 August 2026

The visual problem came back when I started working on the dam.

The top view works well for the river, trees and beaver, but I can't really show dam height properly from above.

So I made a second side view for the dam and water levels.

The first version looked completely wrong because the vertical scale was not consistent with the top view. The water depth could suddenly look enormous and go way too high on the screen.

I definitely need to sort out the scale problems now. I'd like both views to be at a consistent scale, both to reality and to each other.

I think the main problem is that I've been treating those rectangles as whole trees. That is never going to fit the river scale properly.

So from now on I'm going to treat each "tree" in the simulation as a usable piece of wood / log rather than a literal whole tree. The code can still call them trees, but their dimensions represent usable wood.

This also makes the top view and side view much easier to keep in proportion. This is so much clearer. Yay!

---

## 1 September 2026

Started adding water behaviour.

I had an upstream water depth and a downstream water depth. But they are just still rectangles right now. So I looked into how water could move through and over the dam: leakage and overtopping.

---

## 2 September 2026

Added leakage based on Darcy's law.

It is definitely simplified because a real beaver dam is not one uniform porous block.

Also added a hydraulic conductivity parameter `K`. No idea yet what value is sensible enough for the baseline.

Another small complication: the wetted area should depend on how much of the dam is actually underwater, so I can't just use the full dam area all the time.

---

## 3 September 2026

Added overtopping, using a simple weir-style relation where flow increases with overflow depth to the power `3/2`.

The first few versions were mostly me checking that one part wasn't accidentally giving negative flow or letting water "overtop" when it was actually below the relevant level.

The model is starting to feel much more mathematical than it did a week ago :)

---

## 5 September 2026

Added inflow and downstream outflow.

I set both to `0.05 m³/s`.

The reason for making them equal is that I want the system to be able to settle instead of continuously gaining water.

And why 0.05? It is more of a baseline scenario than something calibrated to one real river. I guess the exact value doesn't matter too much for now? I can come back to it later.

---

## 6 September 2026

Worked on the water-balance equations.

Upstream water changes according to inflow minus dam flow.

Downstream water changes according to dam flow minus outflow.

The first time I let it run continuously I kept watching the numbers because I wasn't sure whether the water levels were actually converging or just changing very slowly.

So I started thinking more carefully about equilibrium.

At first I was mostly thinking "the water levels stop changing", but that really means the flows have to balance.

So at equilibrium I want:

`Q_in ≈ Q_dam ≈ Q_out`.

---

## 7 September 2026

Added a settling phase.

Once the beaver has delivered all the trees, the dam stops changing but the water is allowed to continue moving until it settles.

My first equilibrium check was too easy to satisfy for a single instant, so I added a tolerance and made the balance condition hold for a few seconds before accepting equilibrium. Otherwise the model can just pass through the condition for one frame and declare itself finished.

This also means "equilibrium" in the code is numerical rather than perfectly exact, which I need to remember when I compare numbers later.

---

## 8 September 2026

Went back to the dam thickness problem.

Constant thickness still doesn't feel right.

Tried making thickness increase with dam height:

`T = T0 + kH_d`

I don't really know what `k` should be. 

I tried a fairly large value first and the dam looked ridiculous, so I reduced it.

---

## 9 September 2026

Started setting up the experiments separately from the main simulation in `experiment.py`. There wasn't really any reason to make the beaver build the dam from scratch every time I wanted to test one hydraulic parameter.

Instead, each experiment starts with a dam whose geometry I specify directly, resets both water depths to the same initial value, and then lets only the hydrology run until equilibrium.

This also makes the comparisons much cleaner because I can change one parameter at a time while keeping the starting conditions the same.

---

## 10 September 2026

Experiment 1: vary dam height.

Made a first plot of dam height against equilibrium `ΔH`.

I expected higher dams to create a larger difference between upstream and downstream water.

That does happen eventually, but the first few points are almost flat.

Need to look at the actual equations rather than guessing from the graph.

Also started saving the results instead of only printing them, which saves me from copying numbers out of the terminal each time.

---

## 11 September 2026

Looked at the low-height cases more carefully.

For the smallest `H_d` values, the downstream water is still above the dam crest, so the dam is completely submerged.

That at least explains why the regime is different from the higher-dam cases.

The flat part still needs a proper mathematical explanation though. I don't want to just write "the graph looks flat" and leave it there.

Started writing the equilibrium equation in terms of the head difference `ΔH` instead of staring at `H_u` and `H_down` separately.

---

## 12 September 2026

Started Experiment 2: vary hydraulic conductivity `K`.

Made the second plot, this time `K` against equilibrium `ΔH`.

As `K` increases, the head difference gets smaller.

That makes intuitive sense because a more permeable dam can pass the same flow with less pressure / head difference.

But something else happens near the end: overtopping disappears completely and leakage carries everything.

There seems to be a transition value of `K`.

I want to know whether that transition is just a numerical accident or whether I can predict it.

Tried plotting `K` on a log scale at first because the values cover quite a wide range. It technically worked, but the interesting points near the transition got squashed together and the graph was harder to read than it needed to be.

Changed the plotting range and added more `K` values around the transition instead.

---

## 13 September 2026

Cleaned up the experiment/plotting workflow properly. Put the plotting from the last few days into `analysis.py` so I can produce the figures from the saved CSV data without manually copying results.

Workflow is now basically:    `experiment.py → CSV → analysis.py → figures` 

Also did a proper reality check on the dam geometry because the `T = T0 + kH_d` rule was still bothering me.

Found literature suggesting wooden beaver dams are much wider than they are high, with a roughly triangular cross-section and an average width-to-height ratio around `2.9`.

This is annoying because it means the geometry I've been using for the experiments is probably the weakest part of the model.

I could leave it because the code already works, but that feels like a bad reason to keep an assumption.

Decided to change it.

---

## 14 September 2026

Changed the dam from the old rectangular / linear-thickness version to a triangular cross-section with

`T = 2.9H_d`.

This broke more things than I hoped.

The side-view drawing needed changing, the final height changed, and the old experiment results were no longer the results of the final model.

For the picture I made the upstream face shallower and the downstream face steeper. The exact asymmetry is mostly visual, but it looks much more like the dam shape I found in the literature.

The completed seed-42 dam is now only around `0.44 m` high. My first reaction was that 80 logs suddenly looked like "not enough", but increasing the tree count just to make the dam taller would be cheating the model a bit. So I kept it.

Reran Experiment 1 with the new geometry. The low-height plateau is still there, and now I can actually see why: in the fully submerged regime, the `H_d` terms cancel out of the leakage part because wetted area and thickness both scale with dam height.

---

## 15 September 2026

Reran Experiment 2 with the triangular dam and immediately got confused.

I first used roughly the same `K` range as before, but the leakage-only transition had basically disappeared. For a moment I thought I had broken the model again.

So I kept extending the `K` values upwards, eventually found the transition again around `0.31–0.32 m/s`.

That is *way* higher than the old value around `0.046–0.047 m/s`.

After looking back at the geometry, it actually makes sense. The new triangular dam is much thicker, so the same conductivity gives less leakage. `K` has to be much larger before leakage can carry the whole flow by itself.

Worked out the transition analytically and got about `K = 0.312 m/s`, which is almost exactly where the simulation changes regime.

Okay, I think the modelling itself is basically done now.

I should probably stop changing things before I create another problem and start properly documenting what I've actually made.

---

## 21 September 2026

Did a proper final verification run today instead of just assuming everything still worked.

Found two actual bugs: a typo in the equilibrium hold-time variable, and the dam-height calculation wasn't including the initial dam volume correctly.

Fixed both and reran the baseline and experiments again. Everything is reproducing properly now.

---

## 22 September 2026

Started properly cleaning up the documentation.

Went back through the project journal and realised how much of the middle I had never written down at the time.

Also worked through the research notes and tried to separate things I actually found in papers from assumptions I made myself.

---

## 24 September 2026

Cleaned up the mathematical notes and added a short overview of how the behavioural and hydraulic parts connect.

I originally thought I should also make a separate modelling file, but at this point it was mostly repeating the same story again, so I decided against it.

Finished the README.

---

## 28 September 2026

Updated `analysis.py` to use pandas for loading and working with the experiment CSV files.

This made the analysis workflow cleaner without changing the experiment results.

---

## 30 September 2026

Added `verify_equilibrium.py` to check the equilibrium results independently.

Rewrote the equilibrium condition as a one-variable equation in `ΔH` and used SciPy `root_scalar` to solve it directly.

The SciPy results were very close to the original time-stepping results.

Also cleaned up the repository structure and grouped the code and documentation into separate folders.
