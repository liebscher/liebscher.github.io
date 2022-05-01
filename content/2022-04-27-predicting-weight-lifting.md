Title: Predicting Weight Lifting
Date: 2022-04-27
Tags: Machine Learning, Data Science, Statistic, Python, Rlang
Category: meta
Slug: predicting-weights
Authors: Alex Liebscher
Summary: Predicitng weights
Status: draft


Basically, I want to predict how much I should lift if I want to feel a certain way. I want this to be on a by-exercise granularity, but incorporate information that's shared across lifts. All the muscles work together, and many lifts will recruit multiples muscles: primary and secondary, or primary and accessory.

I want to build a prediction model so that I can enter how I want to feel on a lift (on an integer scale from 1, "This lift was super easy", to 4, "I couldn't do another rep without breaking form").

In an ideal world, I'd building a mathematical model to replicate the dynamics of the real-world. For example, the monotocity of the ratings with weight. Or, the power law nature of lifting (diminishing returns). Or, the reality of how much a person can lift. Or, that weight doesn't go below 0 in most cases.

I'm also curious about creating the *best* model though: can I use machine learning to build a model with very high accuracy.

The difference between this data-driven approach, or algorithmic approach, and the physical modeling approach is that the latter might be my best interpretation of the dynamics but could be wrong entirely. The former scoots around that in exchange for explainability or surrealism (e.g. suggesting impossible lifts by accident).
