---
layout: page
title: "Status Report"
description: "What we have done by late May"
header-img: "img/home-bg.jpg"

---

### Demo Video
<iframe src="https://www.youtube.com/embed/31aoE43Ke2g" width="640" height="360" frameborder="0" allowfullscreen></iframe>

### Project Summary

Our project is a Super Mario Maker™ gameplay simulation in Minecraft, including two pieces of mechanism: a Mario player and a world map generator. We also provide an original physics engine to simulate actions of Mario.

The player is a partially observable agent. For each time step, it perceives a visible frame from the world map and makes a decision for the next action. We provides both deep-learning based AI and A-star searching AI for the agent. Users can also control Mario with keyboards based on our physics engine.

The generator will randomly generate a Minecraft world similar to maps in Super Mario Bros. We provides both simple obstacles generator and Prim map generator. Each map is associated with a goal - red mushroom - for Mario to reach.

The ultimate goal of this project is to train the malrio agent with reinforcement learning initialized by supervised learning so that, given a random world, it can play the Mario to the goal by making decisions based on perceptions.

### Approach

__Part I: Environment setup and Physics Simulation__<br>

1. __The physical world__: In the physics simulator, we attempt to simulate a Mario world inside Minecraft:
    - _Brick Block_: It simulates ground or unbreakable block in Super Mario Bros. All bricks are colored brown in Malrio, and are unbreakable. When hitting a brick with feet, Mario will land on it. When hitting a brick with head, Mario will fall back. When hitting a brick block with each side of the body, Mario will ???.
    - _Lava_: It simulates items that will kill Mario, such as piranha plant or lava in Super Mario Bros.
    - _Mushroom_: It simulates the goal flag in Super Mario Bros.

2. __Control and collision__: Since physics engine in Minecraft is limited to its rules, we create our own physics engine including Newtonian mechanical dynamics simulation and rigid body collision resolution.
    - _Representation_: 3 by 3 matrix representations for Newtonian mechanical dynamics:
    $$\begin{bmatrix}
        X & V_x & a_x \\
        Y & V_y & a_y \\
        Z & V_z & a_z \\
    \end{bmatrix}$$, where $$X, V, a$$ denotes displacement, velocity and acceleration respectively. For each time step $$\Delta t$$, a matrix multiplication would give the next state by preserving the following equations: $$ v_{t+\Delta t} = v_t + a_t \Delta t$$, $$ p_{t+\Delta t} = p_t + v_t \Delta t + \frac{1}{2} a_t \Delta t^2$$. Actions and action combinations (left, right, button A, button B) would be reflected upon changes to corresponding accelerations and velocity. We adopt similar hyperparameters of physical settings as Super Mario Bros.
    - _Actor control_: //TODO
    - _Collision_: //TODO

__Part II: Datasets collection for supervised training__<br>

To prepare datasets for supervised learning, we need both maps and corresponding actions to train the actor.

1. __Maps__: Maps are generated using either simple obstacles generator and Prim map generator. The simple obstacles generator generates a world with blocks and lavas whose positions and sizes similar to those of Level 1-1 in Super Mario Bros, by randomly creating obstacles and floating tiles. The Prim map generator generates a maze-like world with Prim's algorithm, which is much harder to solve but guaranteed to be solvable.

2. __Actions__: We use A-star search as the action generator for each visible area of each map. Our A-star algorithm cooperate closely with our physics engine by using the provided actions to generate frontiers of each state. Since A-star is guaranteed to be optimal, it serves as an ideal way to generate action labels to get to the goal. We also pre-select the maps that feasible for A-star to run, in terms of solvability and time cost.

__Part III: Supervised Training__<br>
// TODO

### Evaluation
// TODO

### Remaining Goals and Challenges
Currently, our prototype is limited to small maps only, and our deep learning models are still primary. For remaining weeks, we plan to

- Revise our deep neural networks. We will improve quality and accuracy of our current convolutional neural networks, and will also examine on other models. The baseline is able to solve 50 percent of maps solvable by A-star search in our datasets.
- Generate more complex map datasets. The baseline is Level 1-1 in Super Mario Bros.
- If time permits, change to q-learning.

By the time our final report is due, we should be able to achieve an intelligent AI that could solve around 50 to 90 percent of maps of our dataset, where maps are at least as complex as Level 1-1 in Super Mario Bros. The major difficulty lies in the model training and supervised label generation (since it directly determines the training result). Also, there could be still bugs or foibles in our physics engine.

To deal with them, we will divide our work into three major parts: model training, dataset generating and system revision, and assign them to different team members. Since our code is written in greatest modularity possible, it is easy to cooperate by providing functions and interfaces as negotiated.
