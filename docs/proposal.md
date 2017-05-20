---
layout: default
title: Proposal
---

### Summary
Our project is a Super Mario Maker™ gameplay simulation in minecraft, including two pieces of mechanism: a world map generator and a mario player. All pieces of them are designed to be end-to-end neural-network-based systems. The player would be a partially observable agent. For each time step, it would be able to perceive a visible frame from the world map and make a decision for the next action. The generator would draw a random sample and generate a full world map for players.

### Algorithm Design
__Mario Player__<br>
 - Extract feature maps with Convnets, generate a sequence of spatial segments by Region-Of-Interest proposal layer/ soft attention, decode by LSTM/ConvLSTM/DNC/ConvDNC with or without attention, and regress a probability distribution over action choices with fully connected layers or global average pooling layers.
 - Training methods include supervised learning for parameter initialization, reinforcement learning for fine tuning and transfer learning for benefiting from pre-trained parameters.

__World Map Generator__<br>
 - A GAN to generate full-sized world maps.
 - During the training process of the generator, legitimacy of the generated map and performances of well-trained mario players on the map would be taken into account for labeling the discriminator and judging the desired sample distributions.
 - Backup alternatives: A\* search / spanning tree based map generator.

### Evaluation Plan

__Mario Player__<br>
- There are several potential metrics that can be used to evaluate the mario player. The most important one is reward scores used in reinforcement learning stages. The score would be a weighted sum of longest distance agents reach, time taken to reach goals, items they collect (mushrooms, coins, etc.), special movements they perform (shell jump, bomb jump, wall jump, p switch jump, etc.), and enemies they advance_frame into or kill (goombas, koopas, bowsers, etc.). Another metric is the convergency of the model during training time (diverging, slowly converging, quickly converging, etc.). The convergency can be analyzed by loss-epoch curves and score-epoch curves. The baseline model is multi-layered perceptrons -- fully connected layer only -- trained with supervised learning only. We expect that our player models would have better convergency and higher scores without dying.
- Basic sanity cases include that players reach goals in provided maps within given time limits. The moonshot cases would be that players are able to consecutively perform skillful jumps, learn to do speed running, collect red coins and find hidden key to solve puzzles, use p switches to solve puzzles, etc. Visualizations might include interpretable feature maps and filters from convnets, soft attention spatial weights or bounding boxes of ROI proposals emphasizing on crucial positions, sequential model attentions over given positions, DNC memory read/write matrices over time steps, and histograms of weights and activations (not necessarily all of them).

__Map Generator__<br>
- The major metric of map generators would be the percentage of legitmate maps generated. In addition, the variety and difficulty of maps can also be considered as potential metrics. The percentage can be simply measured by counting numbers of legitmate ones; the variety of generated maps can be measured by statistics of cosine similarities between generated ones and provided ones or covariance matrices of the difference between provided ones and generated ones; difficulty can be measured as the negative score of a well-trained player running on generated maps. The baseline model is A\* search / spanning tree based map generator. We expect our model would have larger variety of generated samples and higher difficulty.
- Basic sanity case would be the model generating legitmate maps at a significant percentage such as 60%-75%, and it should be able to generate some maps not provided. Moonshot cases would include that the generate is able to design seed running levels and puzzles using hidden key tricks, p switch tricks, shell jump tricks, etc. Visualizations would still include feature maps and fiters of transposed convolution layers, histograms of weights and activations. If we choose some GAN models with interpretable input dimensions such as info-GAN, the generated maps on the input vector space can also be visualized.

### Appointment with the Instructor
 - 3PM on April 25th, at DBH 4204
