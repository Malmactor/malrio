---
layout: page
title: "Status Report"
description: "What we have done by late May"
header-img: "img/home-bg.jpg"
---
### Demo Video

<iframe src="https://www.youtube.com/embed/8IkFP0T3yOA?VQ=HD1080" width="768" height="432" frameborder="0" allowfullscreen></iframe>

### Project Summary

Our project is a Super Mario Maker™ gameplay simulation in Minecraft, including two pieces of mechanism: a Mario player and a world map generator. We also provide an original physics engine to simulate actions of Mario.

The player is a partially observable agent. For each time step, it perceives a visible frame from the world map and makes a decision for the next action. We provides both deep-learning based AI and A-star searching AI for the agent. Manual control through keyboard is also implemented.

The generator will randomly generate a Minecraft world similar to maps in Super Mario Bros. We provides both simple obstacles generator and Prim map generator. Each map is associated with a goal - red mushroom - for Mario to reach.

The ultimate goal of this project is to train the malrio agent with reinforcement learning initialized by supervised learning so that, given a random world, it can play the Mario to the goal by making decisions based on perceptions.

### Approach

__Part I: Environment setup and Physics Simulation__<br>

1. __World representations__: In the physics simulator, we attempt to simulate a Mario world inside Minecraft:

    - _Brick_: It simulates ground or unbreakable brick in Super Mario Bros. All bricks are colored brown in Malrio, and are unbreakable. When hitting a brick with feet, Mario will land on it. When hitting a brick with head, Mario will fall back. When hitting a brick with each side of the body, Mario will stop.
    - _Lava_: It simulates items that will kill Mario, such as pits or lava in Super Mario Bros.
    - _Mushroom_: It simulates the goal flag in Super Mario Bros.

2. __Control and collision__: Since Minecraft physics engine has its own rules, we create a separate physics engine in python including Newtonian mechanical dynamics simulation and rigid body collision resolution. Simulation results are sent to Malmo for each frame. One of the core simulation mechanism is a time variant linear system, where a 3 by 3 matrix represents the Newtonian mechanical dynamics of mario:
$$\begin{bmatrix}
    X & v_x & a_x \\
    Y & v_y & a_y \\
    Z & v_z & a_z \\
\end{bmatrix}$$, where $$X, v, a$$ denotes displacement, velocity and acceleration respectively.

    - _Status Update_:  For each time step $$\Delta t$$, a matrix multiplication would give the next state by preserving the following equations: $$ v_{t+\Delta t} = v_t + a_t \Delta t$$, $$ X_{t+\Delta t} = X_t + v_t \Delta t + \frac{1}{2} a_t \Delta t^2$$. Parameters of the original SuperMarioBros physics are replicated to reproduce the authentic controling style of it.
    - _Actor control_: We support a group of actions and action combinations. Like the "⬅️➡️AB" buttons of original Super Mario Bros game,  our control design can make 6 actions: jump, left move, right move, jump with left move, jump with right move, remain. Implementation of actions are achieved by manipulating specific velocity and accelerations of the system.
    - _Collision_: If Mario collide with the ground, y-velocity will be cancelled; if collide up to a brick, y-axis velocity will be inverted; if collide to bricks in sides, x-axis velocity will be cancelled.

__Part II: Datasets collection for supervised training__<br>

The dataset has pairs of frame-action correspondences. For each pair, a visible frame is cropped and an action is sampled.

1. __Map Generation__: Before a set of frame-action correspondences is collected, an unique world map is generated for producing the set. Maps are generated from simple obstacles generator or Prim map generator. The simple obstacle generator generates a world with randomly generated blocks and pits patterned like Level 1-1 in Super Mario Bros. The Prim map generator generates a maze-like world with Prim's algorithm, which is harder to solve due to the requirements of spatial reasoning.

2. __Visible Frame Crop__: A square region around mario is cropped as the perception to agents at a paricular time.

3. __Action Labels__: An A-star search with global perception gives a plausible route from the beginning to the end, which consists of a series of actions at each time step. With the one-to-one mapping relationship to time step, action series can be combined with corresponding visible frames to build frame-action pairs.

4. __Action Downsampling__: With the observation that human players usually cannot change actions at every 60 frames in second, we introduce a prior of action downsampling. During a period of time, agents (including a-star search) can only change its action every 5 frames, and gaps between different actions are filled with "remain" actions. This technic is used throughtout the whole system. In current design, frames in the gap are discarded and only frames with action labels are used to build the dataset. However, we are planning on building 5frames-action pairs in later development to give temporal information to advanced agents.

__Part III: Supervised Training__<br>

The basic end-to-end neural network modal is a stack of cnn layers trained with supervised training.

1. __Input__: A visible frame at a particular time is defined as a 15 blocks x 15 blocks region around mario. Therefore, the frame can be represented as a square grid with one-hot encoding, where each cell has 4 features with values of [0, 1], indicating the presence of obstacles, mario, coins, and enemies. Since the position of mario is not neccessarily aligned with block boundaries, a sampling scheme is used to provide finer details. In particular, each block is represented by 4 x 4 piexels, and the presence of a bounding box would result the feature of covered pixels to be turned on. And ground truth label from the dataset is encoded as 6 dimensional vector using one-hot encoding, where each dimension represents an action. When an action is labeled, the corresponding feature will be turned on to 1, and other features will be turned off to 0. Since the simple model only considers 1frame-1action mapping, inputs and labels can be represented as $$X \in R^{b,60,60,4}, Y \in R^{b,6}, \text{where b is the batch size}$$.

2. __CNN Blocks__: There are two kinds of basic Convolusional Neural Network units used in the model. The first one is a nonlinear stack of convolution, batch normalization, activation function(relu). The second one is a affine linear stack of convolution, batch normalization. Since the batch normalization will shift the covariant statistics within a batch, additional bias would be redundent. The reason for using affine linear cnn layers is that we adopted some ResNet-like structure. Therefore, introduction of nonlinearity into the indentity channel would corrupt the residual learning. In addition, we adopted inception-like structures as well. Like inception-resnet-v2, each cnn block is built on serveral branches of cnn layers with various kernel sizes. For design details, please refer to src/Supervised/cnn_units.py file.

3. __Prediction and Loss__: After stacking CNN blocks, a global average pooling is used to produce a vector. Thie vector is passed through serveral small fully-connected layers to generate logits. And final prediction is given by softmaxing the logits. Since the labels and prediction are designed to be a probability distribution over actions, the loss function is defined as the Kullback–Leibler divergence(cross-entropy) between two distributions.

4. __Training__: The model is trained with adam gradient descent optimization to minimize the loss function.

### Evaluation
1. __A-star__: Given enough time, the a star search is able to give a feasible solution. However, it usually takes too long. Thus, we only use a star search to generate examples on small maps to give examples to the cnn model.

2. __CNN__: When trained with the dataset, the prediction accuracy is usually around 80% - 90%. Since we have more data points than the parameters in CNN, it does not exibit overfitting and the test accuracy is very close to the training accuracy. In randomly generated maps, the success rate of CNN model is around 37%. The most frequent failure is getting stuck in corners.

### Remaining Goals and Challenges
Currently, our prototype is limited to small maps only, and our deep learning models are still primary. For remaining weeks, we plan to

- Revise our deep neural networks. We will improve quality and accuracy of our current convolutional neural networks, and will also examine on other models. The baseline is able to solve 50 percent of maps solvable by A-star search in our datasets.
- Generate more complex map datasets. The baseline is Level 1-1 in Super Mario Bros.
- If time permits, change to q-learning.

By the time our final report is due, we should be able to achieve an intelligent AI that could solve around 50 to 90 percent of maps of our dataset, where maps are at least as complex as Level 1-1 in Super Mario Bros. The major difficulty lies in the model training and supervised label generation (since it directly determines the training result). Also, there could be still bugs or foibles in our physics engine.

To deal with them, we will divide our work into three major parts: model training, dataset generating and system revision, and assign them to different team members. Since our code is written in greatest modularity possible, it is easy to cooperate by providing functions and interfaces as negotiated.
