---
layout: page
title: "Final Report"
description: "Proudly Introducing Malrio"
header-img: "img/home-bg.jpg"
---

### Video

<iframe src="https://www.youtube.com/embed/JkVa7xYHzVA?VQ=HD1080" width="768" height="432" frameborder="0" allowfullscreen></iframe>

### Project Summary

Our project is a Super Mario Maker™ gameplay simulation in Minecraft, including two pieces of mechanism: a Mario player and a world map generator.

The generator gives random world arrangements like world levels of Super Mario Bros, which are environments that the mario agent interacts with.

The goal for the agent is to reach the end of the level without falling into pits or hitting with enemies. And the agent interacts with the environment like human players do. It sees a part of the world map around it and decides an action to take. Therefore, the agent is a partially observable agent. Specifically, at each time step, it perceives a stack (5) of recent visible frames from the environment that surrounds it and makes a decision for the next action. The overview of the agent input/output is shown below: ![System overview](https://github.com/Malmactor/malrio/blob/master/docs/img/general_3.png?raw=true)

Playing mario with computational algorithms has been an interesting idea for decades, since it is a similar problem to robot maneuvering problems and path-planning problems, which have great significance in real life and are hard to solve with traditional algorithms. Previous methods include a-star and multilayer-perceptrons. However, they either require global map information and manual heuristic design(A*) or lack strong spatial inference capacities. Recent advances in combining reinforcement learning and convolutional neural networks have enabled the method of building an end-to-end neural network with such capacities. Therefore, our project is an end-to-end neural network based AI system to solve the mario playing problem.

### Approaches

__Part I: Environment setup and World Representations__<br>

1. __World representations__: Since the environment is built on Minecraft, common objects in super mario world are represented by similar objects in Minecraft:

    - _Minecraft Bricks_: Ground, ceilings, pipes, anything you cannot bread in super mario world. unbreakable brick in Super Mario Bro.
    - _Minecraft Lava_: Enemies, pits, anything that kills mario.
    - _Minecraft Mushroom_: Goal Flags.

2. __Environment Rules__: Simple rules that the mario world run on.

    - _Movement_: Like any simple objects in real life, the movement of mario is determined by displacement, velocity, and acceleration.
    - _Interaction_: Mario is not ghost and cannot go through walls or enemies. If he hits into a wall, he will stop; if he hits into an enemy, he will die.
    - _Implementation_: Implementation details are covered in the physics simulation section of appendix.

3. __Agent Reward__: Reward function for both the reinforcement learning and A\* heuristics

    - _Definition_: $Reward(state) = \lVert P_{destination} - P_{state} \rVert$

__Part II: Baseline Method__<br>

1. __A\*__: A\* agent is different to the


__Part II: Datasets collection for supervised training__<br>

The dataset has pairs of frame-action correspondences. For each pair, a visible frame is cropped and an action is sampled.

1. __Map Generation__: Before a set of frame-action correspondences is collected, an unique world map is generated for producing the set. Maps are generated from simple obstacles generator or Prim map generator. The simple obstacle generator generates a world with randomly generated blocks and pits patterned like Level 1-1 in Super Mario Bros. The Prim map generator generates a maze-like world with Prim's algorithm, which is harder to solve due to the requirements of spatial reasoning.

2. __Visible Frame Crop__: A square region around Mario is cropped as the perception to agents at a particular time.

3. __Action Labels__: An A-star search with global perception gives a plausible route from the beginning to the end, which consists of a series of actions at each time step. With the one-to-one mapping relationship to time step, action series can be combined with corresponding visible frames to build frame-action pairs.

4. __Action Downsampling__: With the observation that human players usually cannot change actions at every 60 frames in second, we introduce a prior of action downsampling. During a period of time, agents (including a-star search) can only change its action every 5 frames, and gaps between different actions are filled with "remain" actions. This technic is used throughout the whole system. In current design, frames in the gap are discarded and only frames with action labels are used to build the dataset. However, we are planning on building 5frames-action pairs in later development to give temporal information to advanced agents.

__Part III: Supervised Training__<br>

The basic end-to-end neural network modal is a stack of cnn layers trained with supervised training.

1. __Input__: A visible frame at a particular time is defined as a 15 blocks x 15 blocks region around Mario. Therefore, the frame can be represented as a square grid with one-hot encoding, where each cell has 4 features with values of [0, 1], indicating the presence of obstacles, Mario, coins, and enemies. Since the position of Mario is not necessarily aligned with block boundaries, a sampling scheme is used to provide finer details. In particular, each block is represented by 4 x 4 pixels, and the presence of a bounding box would result the feature of covered pixels to be turned on. And ground truth label from the dataset is encoded as 6 dimensional vector using one-hot encoding, where each dimension represents an action. When an action is labeled, the corresponding feature will be turned on to 1, and other features will be turned off to 0. Since the simple model only considers 1frame-1action mapping, inputs and labels can be represented as $$X \in R^{b,60,60,4}, Y \in R^{b,6}, \text{where b is the batch size}$$.

2. __CNN Blocks__: There are two kinds of basic Convolutional Neural Network units used in the model. The first one is a nonlinear stack of convolution, batch normalization, activation function(relu). The second one is a affine linear stack of convolution, batch normalization. Since the batch normalization will shift the covariant statistics within a batch, additional bias would be redundant. The reason for using affine linear cnn layers is that we adopted some ResNet-like structure. Therefore, introduction of nonlinearity into the identity channel would corrupt the residual learning. In addition, we adopted inception-like structures as well. Like inception-resnet-v2, each cnn block is built on several branches of cnn layers with various kernel sizes. For design details, please refer to src/Supervised/cnn_units.py file.

3. __Prediction and Loss__: After stacking CNN blocks, a global average pooling is used to produce a vector. The vector is passed through several small fully-connected layers to generate logits. And final prediction is given by softmaxing the logits. Since the labels and prediction are designed to be a probability distribution over actions, the loss function is defined as the Kullback–Leibler divergence(cross-entropy) between two distributions.

4. __Training__: The model is trained with adam gradient descent optimization to minimize the loss function.

### Evaluation
1. __A-star__: Given enough time, the a star search is able to give a feasible solution. However, it usually takes too long. Thus, we only use a star search to generate examples on small maps to give examples to the cnn model.

2. __CNN__: When trained with the dataset, the prediction accuracy is usually around 80% - 90%. Since we have more data points than the parameters in CNN, it largely prevents overfitting and the test accuracy is very close to the training accuracy. In randomly generated maps, the success rate of CNN model is around 37%. The most frequent failure is getting stuck in corners.

### References
TODO

### Appendix
1. __Physics Engine Implementation__: Since Minecraft physics engine has its own rules, we create a separate physics engine in python including Newtonian mechanical dynamics simulation and rigid body collision resolution. Simulation results are sent to Malmo for each frame. One of the core simulation mechanism is a time variant linear system, where a 3 by 3 matrix represents the Newtonian mechanical dynamics of Mario:
$$\begin{bmatrix}
    X & v_x & a_x \\
    Y & v_y & a_y \\
    Z & v_z & a_z \\
\end{bmatrix}$$, where $$X, v, a$$ denotes displacement, velocity and acceleration respectively.

    - _Status Update_:  For each time step $$\Delta t$$, a matrix multiplication would give the next state by preserving the following equations: $$ v_{t+\Delta t} = v_t + a_t \Delta t$$, $$ X_{t+\Delta t} = X_t + v_t \Delta t + \frac{1}{2} a_t \Delta t^2$$. Parameters of the original SuperMarioBros physics are replicated to reproduce the authentic controlling style of it.
    - _Actor control_: We support a group of actions and action combinations. Like the "LFAB" buttons of original Super Mario Bros game, our control design can make 6 actions: jump, left move, right move, jump with left move, jump with right move, remain. Implementation of actions are achieved by manipulating specific velocity and accelerations of the system.
    - _Collision_: If Mario collide with the ground, y-velocity will be cancelled; if collide up to a brick, y-axis velocity will be inverted; if collide to bricks in sides, x-axis velocity will be cancelled.
