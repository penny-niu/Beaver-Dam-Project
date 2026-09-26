# Project Journal

A rough journal of how the project developed from 28 July to 15 September 2026.

Some entries were written at the time, while some dates in the middle were reconstructed afterwards from the order in which I built things. This is not meant to be a formal record — mostly just what I was doing and what I was thinking about along the way.

---

## 28 July 2026

Did some research on beavers, mostly tree choice, how they build dams, what kinds of trees they seem to prefer, etc.

The original thing I was interested in was actually whether a beaver could make things easier for itself by cutting a tree so that it falls towards the river.

Not really sure how I would model that yet. I was thinking maybe cutting angle? centre of mass? direction of fall? It sounds interesting but also immediately feels like it could get very mechanical very quickly.

---

## 29 July 2026

Installed VS Code and got Pygame working.

Mostly just setup today.

---

## 30 July 2026

Made the screen and the river.

Very basic at the moment but at least there is something visible now.

---

## 12 August 2026

Started adding trees.

Used Python's `random` module to generate positions and stopped them from appearing inside the river.

The first version was a bit chaotic because trees could end up too close together or right against the river edge. Added a gap and some simple overlap checks. Not perfect, but much better.

---

## 14 August 2026

Turned the trees into proper objects instead of just drawing random rectangles directly onto the screen.

This made it much easier to give every tree its own position, dimensions and species later.

I'm starting to understand why object-oriented programming is actually useful rather than just something people tell you to use.

---

## 16 August 2026

The view is bothering me. The river is basically top-down, but the trees look more like little rectangles from the side. Should everything really be in one perspective?

Also thought about using different colours for species because beavers have preferences for different species of trees.

Then if I choose realistic species, should I also define a particular geographical location and climate for the whole model?

Probably don't want to go that far. I'll just let the species and their probabilities represent a simplified hypothetical riverside environment.

---

## 17 August 2026

Added different tree species and colours.

Also added random width and height instead of making every tree identical.

I used triangular distributions to make my forest less artificial. I want middle-sized values to be more common but still allow some small and large ones.

Had to remind myself that these dimensions are really more like usable wood dimensions in the model, not literal full-tree measurements. Otherwise the scale starts making no sense again.

---

## 18 August 2026

Spent quite a while thinking about scale.

If I use actual real-life proportions, tree trunks become tiny compared with the river and are basically invisible.

So I think I need to stop treating the drawing scale and the mathematical scale as the same thing.

The visualisation can exaggerate things slightly if it makes the simulation readable. I can still keep the actual model variables in metres later.

Not completely sure how messy this will become when I add the dam.

---

## 20 August 2026

Cleaned up tree generation a bit more.

I kept changing the ranges because some forests looked too uniform while others had a few ridiculous trees dominating everything visually.

This is one of those things that looked simple at first — "just generate some trees" — but it actually took a few passes before it stopped looking obviously artificial.

---

## 22 August 2026

Started thinking properly about how the beaver should choose trees.

From the research I've done, central-place foraging seems useful here: distance matters, but so do the size and species of the tree.

I don't want to pretend I'm modelling the beaver's actual energy budget, so maybe a score is enough.

Still not sure what should go in the numerator and what should count as a cost.

---

## 24 August 2026

Built the first still beaver. It doesn't move yet.

Started thinking more seriously about what the beaver should actually *do* rather than just exist on the screen.

I think the basic loop should be something like: choose a tree → move to it → cut it → take the material to the dam → choose another tree.

That sounds obvious when written down. I suspect coding it will be less obvious.

---

## 25 August 2026

Made a first tree-selection score and got the beaver moving towards the selected tree.

Added rough states for moving and cutting.

The cutting part is extremely simplified. The beaver basically reaches the tree and then the model waits briefly before switching state — I'm not modelling an actual cutting process.

The first version had a fairly stupid problem: after cutting a tree, the beaver would just go on to choosing another tree. I had implemented the selection part before properly implementing the "take it to the dam" part.

So at this point it could forage, but it wasn't really building anything.

The project seems to be turning more into a probability / decision-making problem with a dam-building model attached. But what can I actually do with this mathematically???

---

## 26 August 2026

Tried to fix the missing transport step.

Added a `carrying_to_dam` state so the beaver should move to the dam after cutting a tree instead of immediately selecting another one.

It still didn't behave properly at first. Sometimes it looked like it had stopped, sometimes I couldn't tell whether it was moving to the dam or had already switched to something else.

I realised I was basically debugging a state machine without being able to see the state.

Added the current state as text above the beaver's head: `idle`, `moving`, `cutting`, `carrying_to_dam`.

This looked a bit silly but was genuinely useful. I could finally see exactly when the state changed and work through the transitions one by one.

After a few fixes the whole loop finally worked: choose → move → cut → carry → dam → choose again.

Definitely not something I got right in one go.

---

## 27 August 2026

Connected delivered tree material to the dam.

When a tree reaches the dam I calculate its cylindrical volume and add that material to the dam.

This is the first point where the individual tree dimensions actually affect the dam rather than just the beaver's choice.

Made a first version of the dam. At the moment it is basically rectangular.

Not sure yet what the dam should do with the material volume. Height seems like the most obvious thing to change first.

---

## 28 August 2026

Worked on dam growth.

At first I was basically just increasing the dam height as more material arrived, but then I realised that creates another question: what happens to thickness?

Should thickness stay constant while the dam gets taller? That feels wrong, because adding material should probably make it grow outward as well.

But I also don't know what relationship height and thickness should have.

For now I just need something that works.

---

## 30 August 2026

Came back to the randomness problem.

I originally thought generating a completely new forest every time was a good thing because it made the model less biased towards one arrangement.

But if I want to run experiments, that is actually annoying because changing one parameter also changes the whole forest.

Found out about random seeds and set the seed to `42`.

I really like this idea — it still comes from a random process, but I can reproduce exactly the same environment.

Also reran the beaver loop a few times with the fixed forest. Much easier to tell whether a code change actually improved something when the trees don't move every time I press run.

---

## 31 August 2026

Got the construction sequence working end to end more reliably.

There were still little things I kept adjusting: when exactly a tree disappears, when the beaver counts as having reached the dam, when the next target should be chosen, etc.

None of these was a huge modelling decision, but together they made the difference between something that only *sometimes* worked and something I could actually run repeatedly.

---

## 1 September 2026

The visual problem came back when I started working on the dam.

The top view works well for the river, trees and beaver, but I can't really show dam height properly from above.

Made a second side view for the dam and water levels.

The first version looked completely wrong because the vertical scale was not consistent with the top view. The water depth could suddenly look enormous and go way too high on the screen.

Spent a while matching the side-view scale properly instead of just choosing pixel heights by eye.

Much clearer now.

---

## 2 September 2026

Started adding water behaviour.

I want the dam to actually *do* something rather than just get visually bigger.

So now I have an upstream water depth and a downstream water depth.

At first they were really just numbers being drawn in the side view. I still needed rules for how they change.

There should probably be leakage through the material and overtopping if the upstream water gets above the dam.

---

## 3 September 2026

Added leakage.

I'm using something based on Darcy's law:

`flow ≈ conductivity × area × head difference / thickness`

It is definitely simplified because a real beaver dam is not one uniform porous block.

Also added a hydraulic conductivity parameter `K`.

No idea yet what value is sensible enough for the baseline.

Another small complication: the wetted area should depend on how much of the dam is actually underwater, so I can't just use the full dam area all the time.

---

## 4 September 2026

Added overtopping.

Using a simple weir-style relation where flow increases with overflow depth to the power `3/2`.

Now the total dam flow is leakage + overtopping.

The first few versions were mostly me checking that one part wasn't accidentally giving negative flow or letting water "overtop" when it was actually below the relevant level.

The model is starting to feel much more mathematical than it did a week ago.

---

## 5 September 2026

Added inflow and downstream outflow.

I set both to `0.05 m³/s`.

The reason for making them equal is that I want the system to be able to settle instead of continuously gaining water.

I'm slightly unsure about the actual magnitude of `0.05`. It is more of a baseline scenario than something calibrated to one real river.

I think that's acceptable as long as I say so.

---

## 6 September 2026

Worked on the water-balance equations.

Upstream water changes according to inflow minus dam flow.

Downstream water changes according to dam flow minus outflow.

The first time I let it run continuously I kept watching the numbers because I wasn't sure whether the water levels were actually converging or just changing very slowly.

This is also where I started thinking more carefully about equilibrium.

At first I was mostly thinking "the water levels stop changing", but that really means the flows have to balance.

So at equilibrium I want:

`Q_in ≈ Q_dam ≈ Q_out`.

---

## 7 September 2026

Added a settling phase.

Once the beaver has delivered all the trees, the dam stops changing but the water is allowed to continue moving until it settles.

My first equilibrium check was too easy to satisfy for a single instant, so I added a tolerance and made the balance condition hold for a few seconds before accepting equilibrium.

Otherwise the model can just pass through the condition for one frame and declare itself finished.

This also means "equilibrium" in the code is numerical rather than perfectly exact, which I need to remember when I compare numbers later.

---

## 8 September 2026

Went back to the dam thickness problem.

Constant thickness still doesn't feel right.

Tried making thickness increase with dam height:

`T = T0 + kH_d`

I don't really know what `k` should be.

I tried a fairly large value first and the dam looked ridiculous, so I reduced it.

This is definitely one of those "I need something workable now and I can question it later" choices.

I don't love that I picked `k` partly because the picture looked more reasonable. Need to come back to the geometry properly before calling the project finished.

---

## 9 September 2026

Started setting up experiments rather than only watching the animation.

Made `experiment.py` so I can directly specify dam parameters and wait for equilibrium.

The first version still depended too much on the full interactive simulation, so I separated the controlled experiment more clearly: start with a completed dam, reset both water depths, then let only the hydrology settle.

This is much easier for comparing cases than running the full beaver construction every time.

---

## 10 September 2026

Experiment 1: vary dam height.

I expected higher dams to create a larger difference between upstream and downstream water.

That does happen eventually, but the first few points are almost flat.

I don't really understand why yet.

Could just be because the dam is still submerged?

Need to look at the actual equations rather than guessing from the graph.

Also started saving the results instead of only printing them. Copying numbers out of the terminal is already getting annoying.

---

## 11 September 2026

Looked at the low-height cases more carefully.

For the smallest `H_d` values, the downstream water is still above the dam crest, so the dam is completely submerged.

That at least explains why the regime is different from the higher-dam cases.

The flat part still needs a proper mathematical explanation though. I don't want to just write "the graph looks flat" and leave it there.

Started writing the equilibrium equation in terms of the head difference `ΔH` instead of staring at `H_u` and `H_down` separately.

This is the first time the model feels like it is giving me a maths problem back.

---

## 12 September 2026

Experiment 2: vary hydraulic conductivity `K`.

As `K` increases, the head difference gets smaller.

That makes intuitive sense because a more permeable dam can pass the same flow with less pressure / head difference.

But something else happens near the end: overtopping disappears completely and leakage carries everything.

There seems to be a transition value of `K`.

I want to know whether that transition is just a numerical accident or whether I can predict it.

Tried plotting `K` on a log scale at first because the values cover quite a wide range. It technically worked, but the interesting points near the transition got squashed together and the graph was harder to read than it needed to be.

Changed the plotting range and added more `K` values around the transition instead.

---

## 13 September 2026

Made the analysis script and started producing the figures from CSV data instead of manually copying results.

Workflow is now basically:

`experiment.py → CSV → analysis.py → figures`

Much cleaner.

Also finally did a proper reality check on the dam geometry because the `T = T0 + kH_d` rule was still bothering me.

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

The completed seed-42 dam is now only around `0.44 m` high. My first reaction was that 80 trees suddenly looked like "not enough", but increasing the tree count just to make the dam taller would be cheating the model a bit. So I kept it.

Reran Experiment 1 with the new geometry. The low-height plateau is still there, and now I can actually see why: in the fully submerged regime, the `H_d` terms cancel out of the leakage part because wetted area and thickness both scale with dam height.

That was satisfying because this time the flat section isn't just something I noticed in the plot.

---

## 15 September 2026

Reran Experiment 2 with the final triangular dam.

The mixed-flow → leakage-only transition moved a lot compared with the earlier geometry, now to about `K = 0.31–0.32 m/s`.

At first I thought I might have broken something because the threshold had shifted so much. But the thicker dam reduces leakage for the same conductivity, so it actually makes sense that a much larger `K` is needed before leakage alone can carry the whole flow.

Worked out the threshold analytically and got about `K = 0.312 m/s`, which is very close to what the numerical experiment shows.

Did one more pass through the code and fixed a couple of things that only showed up when I tried to reproduce everything carefully: an equilibrium hold-time variable-name typo, and the dam-height calculation not including the initial dam volume correctly.

Reran the baseline and experiments after the fixes.

Main modelling stage finished.

At this point the project has:

- a reproducible forest;
- a tree-selection rule;
- a beaver state / transport loop;
- dam growth from delivered wood volume;
- a triangular final dam geometry;
- upstream/downstream water storage;
- leakage and overtopping;
- an equilibrium condition;
- two controlled experiments;
- numerical plots and equilibrium analysis.

There are still assumptions I don't fully trust. `K` is only one effective permeability value, the river is basically two storage boxes, the overtopping law is simplified, and the beaver eventually uses every tree anyway.

But I think this is also the point where I should stop adding features and start documenting what I have actually built.

The project ended up being very different from my original tree-fall question.

I don't think that's necessarily bad. It feels more like I followed whatever problem appeared next rather than knowing from the beginning what the final model was supposed to be.
