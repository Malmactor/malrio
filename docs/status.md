---
layout: default
title: Status
---

### Project Summary

Our project is a Super Mario Maker™ gameplay simulation in minecraft, including two pieces of mechanism: a mario player and a world map generator.

The player is a partially observable agent. For each time step, it perceives a visible frame from the world map and makes a decision for the next action. We provides both deep-learning based AI and A-star searching AI for the agent. Users can also control Mario with keyboards based on our physical engine.

The generator will randomly generate a minecraft world similar to maps in Super Mario Bros. We provides both simple obstacles generator and Prim map generator. Each map is associated with a goal - red mushroom - for Mario to reach.

The ultimate goal of this project is to train the malrio agent with supervised learning so that, given a random world, it can make decisions based on what it perceives, and try to find and reach the goal state.

### Approach

#### Part I: The Physics Simulator

1. The physical world: In the physics simulator, we attempt to simulate a Mario world inside Minecraft:

    1. Brick Block: It simulates ground or unbrokable block in Super Mario Bros. All bricks are colored brown in Malrio, and are unbrokable. When hitting a brick with feet, Mario will land on it. When hitting a brick with head, Mario will fall back. When hitting a brick block with each side of the body, Mario will ???.

    2. Lava: It simulates items that will kill Mario, such as piranha plant or lava in Super Mario Bros.

    3. Mushroom: It simulates the goal flag in Super Mario Bros.

2. Control and collision: Since physical engine in Minecraft is limited and rigid, we create our own physical enginee for movement of player as well as collision reaction.

    1. States of actor: We use a 3 by 3 matrix to represent the state of the actor: 
    $$\begin{bmatrix}
        p_x & v_x & a_x \\
        p_y & v_y & a_y \\
        p_z & v_z & a_z \\
    \end{bmatrix}$$

#### Part II: Dataset

To prepare dataset for supervised learning, we need both maps and corresponding actions to train the actor.

1. Maps: Maps are generated using either simple obstacles generator and Prim map generator. The simple obstacles generator generates a world with blocks and lavas whose positions and sizes similar to those of Level 1-1 in Super Mario Bros, by randomly creating obstacles and floating tiles. The Prim map generator generates a maze-like world with Prim's algorithm, which is much harder to solve but guarenteed to be solvable.

2. Actions: We use A-star search as the action generator for each visible area of each map. Our A-star algorithm cooperate closely with our physical enginee by using the provided actions to generate frontiers of each state. Since A-star is guaranteed to be optimal, it serves as an ideal way to generate action labels to get to the goal. We also pre-select the maps that feasible for A-star to run, in terms of sovability and time cost.

#### Part III: Supervised Training
// TODO

### Evaluation
// TODO

### Remaining Goals and Challenges
// TODO
