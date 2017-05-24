---
layout: default
title: Status
---

# Malrio Status Report

## Project Summer

Our project is a **Mario** simulation game in Minecraft. We have built a generator that generates random mario world, on which the agent is run to find the best routes to the goal state (the mushroom). A* search is used to find the best route in the random map, which serve as a sample training data for the Supervised Learning.

The ultimate goal of this project is to train the malrio agent with SL so that, given a random world, it can make decisions based on what it perceives, and try to find and reach the goal state (find the mushroom). 

## Approach

### The Physics Simulator

#### The physical world

In the physics simulator, we attempt to simulate a Mario world inside Minecraft. In particular, four parts are introduced in the physical layer:

1. Brick Blocks. All bricks are colored brown in Malrio, and are unbrokable. Upon encourtering a brick block, the only way to get cross it is to jump over it.

2. Lava, or traps.

3. Wall, which is piles of brick blocks that cannot be jumped. Upon encourtering it, the agent can either have to fall back, or turn left or right.

4. Mushroom, or the goal state.

#### Control and collision 

//TODO

### Supervised Learning

#### Dataset

In the first stage, A random map is generated using Prim's algorithms. Out of all the random maps that are generated, we would only pick up maps that meet certain requirements, for instance, the the start position and the mushroom should be on the same line.

in the second stage, A* search is used in find the optimal path in those selected map. The path, and the map, along with other relevant data ( e.g. result, rewards), are added to the sample training data.

#### Training

//TODO

#### Learning Curve

//TODO
