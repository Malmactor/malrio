---
layout: default
title: Status
---

### Demo Video
[![Malrio: Play Super Mario with AI in Minecraft](https://img.youtube.com/vi/xnTv_D9pXnI/0.jpg)](https://www.youtube.com/watch?v=StTqXEQ2l-Y "Malrio: Play Super Mario with AI in Minecraft")

### Project Summary

Our project is a Super Mario Maker™ gameplay simulation in minecraft, including two pieces of mechanism: a mario player and a world map generator. We also provide an original physics engine to simulate actions of Mario.

The player is a partially observable agent. For each time step, it perceives a visible frame from the world map and makes a decision for the next action. We provides both deep-learning based AI and A-star searching AI for the agent. Users can also control Mario with keyboards based on our physics engine.

The generator will randomly generate a minecraft world similar to maps in Super Mario Bros. We provides both simple obstacles generator and Prim map generator. Each map is associated with a goal - red mushroom - for Mario to reach.

The ultimate goal of this project is to train the malrio agent with reinforcement learning initialized by supervised learning so that, given a random world, it can play the mario to the goal by making decisions based on perceptions.

### Approach

#### Part I: Environment setup and Physics Simulation

1. The physical world: In the physics simulator, we attempt to simulate a Mario world inside Minecraft:

    1. Brick Block: It simulates ground or unbrokable block in Super Mario Bros. All bricks are colored brown in Malrio, and are unbrokable. When hitting a brick with feet, Mario will land on it. When hitting a brick with head, Mario will fall back. When hitting a brick block with each side of the body, Mario will ???.

    2. Lava: It simulates items that will kill Mario, such as piranha plant or lava in Super Mario Bros.

    3. Mushroom: It simulates the goal flag in Super Mario Bros.

2. Control and collision: Since physics engine in Minecraft is limited to its rules, we create our own physics engine including Newtonian mechanical dynamics simulation and rigid body collision resolution.

    1. Representation: 3 by 3 matrix representations for Newtonian mechanical dynamics: 
    $$\begin{bmatrix}
        X & V_x & a_x \\
        Y & V_y & a_y \\
        Z & V_z & a_z \\
    \end{bmatrix}$$, where $$X, V, a$$ denotes displacement, velocity and acceleration respectively. For each time step $$\Delta t$$, a matrix multiplication would give the next state by preserving the following equations: $$ v_{t+\Delta t} = v_t + a_t \Delta t$$, $$ p_{t+\Delta t} = p_t + v_t \Delta t + \frac{1}{2} a_t \Delta t^2$$. Actions and action combinations (left, right, button A, button B) would be reflected upon changes to corresponding accelerations and velocity. We adopt similar hyperparameters of physical settings as Super Mario Bros.
    
    2. Actor control: \\TODO
    
    3. Collision: \\TODO

#### Part II: Datasets collection for supervised training

To prepare datasets for supervised learning, we need both maps and corresponding actions to train the actor.

1. Maps: Maps are generated using either simple obstacles generator and Prim map generator. The simple obstacles generator generates a world with blocks and lavas whose positions and sizes similar to those of Level 1-1 in Super Mario Bros, by randomly creating obstacles and floating tiles. The Prim map generator generates a maze-like world with Prim's algorithm, which is much harder to solve but guarenteed to be solvable.

2. Actions: We use A-star search as the action generator for each visible area of each map. Our A-star algorithm cooperate closely with our physics enginee by using the provided actions to generate frontiers of each state. Since A-star is guaranteed to be optimal, it serves as an ideal way to generate action labels to get to the goal. We also pre-select the maps that feasible for A-star to run, in terms of sovability and time cost.

#### Part III: Supervised Training
// TODO

### Evaluation
// TODO

### Remaining Goals and Challenges
// TODO
