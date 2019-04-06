## Physics-Driven Randomly Exploring Random Trees

A collection of physics-based [rapidly exploring random trees (RRTs).](https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree)

In short: An undirected RRT is a graph where vertices are randomly generated off randomly chosen base vertices, each in a random direction. Typically, if there are no rules about where those vertices are spawned, the graph does not expand around its starting region; more interesting things happen when some ruleset is applied, e.g. "expand in the direction least explored."

I made this mostly to simulate [Lichtenberg figures](https://en.wikipedia.org/wiki/Lichtenberg_figure) and to gain more insight into how they work, but honestly after just a bit of prototyping, I'm partly just doing this to make cool-looking patterns.

## Required packages

`numpy` (required for the vector calculations)

`graphviz` (for visualization; none of the internal math requires this)

## Lichtenberg figures (on wood)

Though Lichtenberg figures can be made in a variety of materials, the ones made in wood are my favorite (partially because I have the tools to make them). Their creation is pretty simple; just add ~2 tablespoons baking soda to a glass of water, then wipe that mixture over the surface of the wood you are working with, then hook up high voltage transformer leads to each side. [Here's a video of one as it grows.](https://www.youtube.com/watch?v=XupIgTwv_Qk) You can see that there is an obvious "active" current pathway, but also that this path sometimes shifts, either burning into an unexplored area or reverting back to a previously active path. Sometimes arcing is visible on off-path regions too, suggesting that the visibly active pathway is not the only conductive region. Additionally, if the piece is set to cool down overnight then restarted, it will sometimes start its growth from a previously-burnt pathway. From these things, I've come to a few theories on what's going on here:

1. The baking soda/water/wood material mixture is conductive, but with (fairly) high resistance. Not sure how much exactly; the voltmeter I have can't measure it.

2. The mixture becomes more conductive at higher temperatures - hence the visible "active" path, and how when a burning link establishes itself between the links, there is no further branching.

3. During the burning process, some kind of chemical reaction occurs that produces a material with higher conductivity that sticks around permanently.

# Basic inverse-square-law, no-vertex-collisions-allowed, simple exponential temperature-decay, all-repulsion single-sided prototype

All in all, the above ideas led me to create a pretty simple first-revision simulation. There are *numerous* differences between it and the physical reality - that is to say, it's more art than physics. Nonetheless, it *does* produce very pretty pictures :)
