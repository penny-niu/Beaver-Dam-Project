# Project Journal

A rough journal of how the project developed from 28 July to 15 September 2026.

Some entries were written at the time, while some dates in the middle were reconstructed afterwards from the order in which I built things. This is not meant to be a formal record — mostly just what I was doing and what I was thinking about along the way.

---

## 28 July 2026

Did some research on beavers, mostly tree choice, how they build dams, what kinds of trees they seem to prefer etc.

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

Used Python's `random` module to generate positions and stopped them from appearing in the river.


---

## 16 August 2026

The view is bothering me. The river is basically top-down, but the trees look more like little rectangles from the side. Should everything really be in one perspective?

Also thought about using different colours for species because beavers have their preferences towards different species of trees.

Then if I choose realistic species, should I also define a particular geographical location and climate for the whole model?

Probably don't want to go that far. I'll just let the species and their probabilities represent a simplified hypothetical riverside environment.

---

## 17 August 2026

Added different tree species and colours.

Also added random width and height instead of making every tree identical.

I used triangular distributions to make my forest less artificial. I want middle-sized values to be more common but still allow some small and large ones.

---

## 18 August 2026

Spent quite a while thinking about scale.

If I use actual real-life proportions, tree trunks become tiny compared with the river and are basically invisible.

So I think I need to stop treating the drawing scale and the mathematical scale as the same thing.

The visualisation can exaggerate things slightly if it makes the simulation readable. I can still keep the actual model variables in metres later.

Not completely sure how messy this will become when I add the dam.

---

## 24 August 2026

Build the first still beaver, not made it move yet.

Started thinking more seriously about what the beaver should actually *do*.

From the research I've done, I learnt that the beavers follow centre-foraging theory for their tree selecting, so maybe it's time to implement this to the model?


## 25 August 2026

Made a first tree-selecting score

Got the beaver moving towards selected trees.

Added different states for moving, cutting and carrying.

The cutting part is extremely simplified. The beaver basically reaches the tree and then the model switches state — I'm not modelling an actual cutting process.

The project seems to be turning more into a probability problem? like tree-selection mechanisms and dam-building model. But what can I do with this???

---

## 25 August 2026

Connected the tree to the dam.

When a tree reaches the dam I calculate its cylindrical volume and add that material to the dam.

This is the first point where the individual tree dimensions actually affect the dam rather than just the beaver's choice.

Not sure yet what shape the dam should be. For now I'm keeping it very simple.

---

## 27 August 2026

Made a first version of the dam.

At the moment it is basically rectangular.

I also started thinking about thickness.

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

---

## 1 September 2026

The visual problem came back when I started working on the dam.

The top view works well for the river, trees and beaver, but I can't really show dam height properly from above.

I think I need a second view.

Made a side view for the dam and water levels.

This feels much clearer already.

---

## 2 September 2026

Started adding water behaviour.

I want the dam to actually *do* something rather than just get visually bigger.

So now I have an upstream water depth and a downstream water depth.

Still trying to decide exactly how water should pass through the dam.

There should probably be leakage through the material and overtopping if the upstream water gets above the dam.

---

## 3 September 2026

Added leakage.

I'm using something based on Darcy's law:

`flow ≈ conductivity × area × head difference / thickness`

It is definitely simplified because a real beaver dam is not one uniform porous block.

But I think it's a reasonable way of giving permeability a clear role.

Also added a hydraulic conductivity parameter `K`.

No idea yet what value is sensible enough for the baseline.

---

## 4 September 2026

Added overtopping.

Using a simple weir-style relation where flow increases with overflow depth to the power `3/2`.

Now the total dam flow is leakage + overtopping.

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

This is also where I started thinking more carefully about equilibrium.

At first I was mostly thinking "the water levels stop changing", but that really means the flows have to balance.

So at equilibrium I want:

`Q_in ≈ Q_dam ≈ Q_out`.

---

## 7 September 2026

Added a settling phase.

Once the beaver has delivered all the trees, the dam stops changing but the water is allowed to continue moving until it settles.

I added a tolerance and made the balance condition hold for a few seconds before accepting equilibrium.

Otherwise it can just pass through the condition for one frame.

---

## 8 September 2026

Went back to the dam thickness problem.

Constant thickness still doesn't feel right.

Tried making thickness increase with dam height:

`T = T0 + kH_d`

I don't really know what `k` should be.

I tried a fairly large value first and the dam looked ridiculous, so I reduced it.

This is definitely one of those "I need something workable now and I can question it later" choices.

---

## 9 September 2026

Started setting up experiments rather than only watching the animation.

Made `experiment.py` so I can directly specify dam parameters and wait for equilibrium.

This is much easier for comparing cases than running the full beaver construction every time.

---

## 10 September 2026

Experiment 1: vary dam height.

I expected higher dams to create a larger difference between upstream and downstream water.

That does happen eventually, but the first few points are almost flat.

I don't really understand why yet.

Could just be because the dam is still submerged?

Need to look at the actual equations rather than guessing from the graph.

---

## 11 September 2026

Looked at the low-height cases more carefully.

For `H_d = 0.20`, `0.30`, etc. the downstream water is actually still above the dam crest.

So the dam is completely submerged.

Once I substitute the triangular/height-dependent geometry into the leakage equation, the height seems to cancel in this regime.

That might explain why the first part of the curve is flat.

This was not something I intended when I wrote the model, which is kind of interesting.

---

## 12 September 2026

Experiment 2: vary hydraulic conductivity `K`.

As `K` increases, the head difference gets smaller.

That makes intuitive sense because a more permeable dam can pass the same flow with less pressure/head difference.

But something else happens near the end: overtopping disappears completely and leakage carries almost everything.

There seems to be a transition value of `K`.

I want to know whether that transition is just a numerical accident or whether I can predict it.

---

## 13 September 2026

Made the analysis script and started producing the final plots from CSV data instead of manually copying results.

Workflow is now basically:

`experiment.py → CSV → analysis.py → figures`

This is much cleaner.

Also started paying more attention to the transition regions instead of only the overall curves.

---

## 14 September 2026

Spent most of today trying to explain the results mathematically.

For Experiment 1, the submerged plateau now makes more sense.

For Experiment 2, I can estimate the point where the upstream water surface drops to the dam crest. That should be exactly where overtopping becomes zero.

I didn't expect to end up doing this much equilibrium analysis when I started the project.

At the beginning I was mostly worried about getting a beaver to move towards a tree.

---

## 15 September 2026

Main modelling stage finished.

At this point the project has:

- a reproducible forest;
- a tree-selection rule;
- beaver transport;
- dam growth;
- upstream/downstream water storage;
- leakage and overtopping;
- an equilibrium condition;
- two controlled experiments;
- numerical plots and equilibrium analysis.

There are still assumptions I don't fully trust, especially dam geometry and some of the physical parameter choices.

But I think that is also the point where I should stop adding features and start checking what I have actually built.

The project ended up being very different from my original tree-fall question.

I don't think that's necessarily bad. It feels more like I followed whatever problem appeared next rather than knowing from the beginning what the final model was supposed to be.
