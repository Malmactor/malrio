---
layout: default
title: Proposal
---

### Summary
The main idea of this project is to create a powerful AI + scalable map generator for Super Mario Playing on Minecraft. For AI, we use the observable map as input, through a deep learning pipeline, to generate an action as output. For the map generator, we use generative adversarial networks, which takes a noise as input and generate a map close to actual Super Mario level. For possible applications, this AI+map method could be inplemented in many actor-based games.

### Algorithms
##### For Actor (Mario)
CNN as encoder -> Attention mapping -> RNN reasoning as decoder -> Action to perform

##### For Level/Map Generator
GAN: Generator - Use CNN to generate the map from noise, Discriminator - Determine difficulty of the map, with average score of the actor

##### For Training
First, actor and map are trained seperately in a supervised fasion. Later, they are trained in turn against each other to achieve the best result.

### Evaluation Plan

##### Quantitative:
 - Metrics: The score achieved by Mario, + for AI and - for Map.
 - Baseline: Mario should at least keep alive, and the map should be solvable.
 - Evaluation: For Mario, we use Q-loss or policy gradient for learning. For Map, we use the Discriminator in GAN.

##### Qualitative
 - AI: In the end, the AI should be able to solve at least Level 1-1 in Super Mario. The quality of the AI can be further examined by more difficult levels.
 - Map: In the end, the map should looks similar to original Super Mario, with controllable difficulty of the map.
 - Moonshot: AI can solve a extremely difficult map that normal players cannot!

### Appointment with the Instructor
TODO
