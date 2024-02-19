Title: Bayes for my Best Workouts
Date: 2024-01-28
Tags: Rlang, Data Science, Fitness
Category: meta
Slug: models-best-workouts
Authors: Alex Liebscher
Summary: Building models to predict my optimal workouts
Status: published
Cover: images/weight-curves.png

## Introduction

Determining the right amount of weight or reps to lift during home workouts can be quite an obstacle. After months of trial and error, I decided to take a systematic, logical, and calculated approach to this dilemma. I've since built a personalized model that guides me through my workouts, blending rigor and intuition for optimal performance.

## The Initial Model

In the early stages of my project, I was looking for a solution that would streamline the decision-making process without sacrificing all the idiosyncracies of each exercise and workout. In December, I developed a basic model that employed linear regressions for each exercise, considering sets, reps, and my perceived exertion level. I could then determine which exercises I wanted to do, along with the reps and sets, and the model would tell me how much weight. While this approach provided some guidance, it felt too rigid and had the opportunity to yield impractical suggestions, such as negative weights.

## The Improved Model

Dissatisfied with the limitations of the initial model, I turned toward more flexible Bayesian modeling that would also help me understand those idiosyncracies I mentioned. This new approach not only accounts for physical constraints (weight must be greater than zero) but also is based on informed priors and physical constraints. By doing so, even exercises with limited data can be predicted accurately. I have two models: one for predicting the target weight of an exercise, the other for predicting the target number of reps (in case I cannot adjust the weight). The Bayesian models represents a step closer to a more nuanced, precise, and flexible workout planning tool.

<img data-src="{static}/images/pred-weights.png"  uk-img/>

### A Few Details

I'm leaving out many of the details, but to start, the target weight prediction model is formulated as follows:

    :::r
    weight ~ 0 + reps + sets + rpe_of_10 + (reps + rpe_of_10|exercise)

In other words, we predict the target weight according the number of reps, sets, and rating of perceived exertion, accounting for baseline variation by exercise and variation in the slope of reps and RPE by exercise. We replace the fixed intercept with random intercepts so that the random intercepts are the baseline weight for each, not the offset from the mean of all. Moreover, after sampling, we reject all posterior samples where the coefficient on sets is greater than zero, the sum of the fixed and random slopes for reps is greater than zero, or the sum of the fixed and random slopes for RPE is less than zero. Ideally we'd constrain the model early on without this ad hoc post-sampling modification, but I've found that too time consuming to figure out. Finally, the likelihood function models a Log-Normal distribution.

We also have a model for predicting the number of total reps for an exercise in the case that the weight in non-adjustable. The model looks like:

    :::r
    total | trials(60) ~ 0 + rpe_of_10 + (rpe_of_10|exercise)

A slightly simpler model, we assume that the number of total reps is some proportion of the possible 60 (chosen arbitrarily). This binomial model is actually far superior to a poisson model, or a negative binomial model, since there's such strong under-dispersion. I constrain post-sampling here as well. 

## Bridging the Gap

One challenge I encountered in this work was the vast disparity between anecdotal gym advice and the highly specialized sports science literature. While internet advice often felt impersonal and arbitrary, academic research was specific to elite athletes and controlled conditions. My attempts aimed to bridge this gap, offering practical solutions grounded in data and applicable to the average home gym enthusiast.

## Ongoing Exploration

As I transition into relying on this new model for my workout planning, the work is far from over. I plan to continuously refine and expand the model by exploring new predictors that could improve its accuracy. Every day I think of predictors and ways of changing the model that could either improve its accuracy or have it reflect real-world constraints even better. The goal is not only to optimize my own workouts but also to share insights that may benefit others seeking a more personalized and data-driven approach to their fitness routines.

One benefit of this work is that I've been even more motivated to workout in order to collect data and sample the space of possible workouts to understand my limits. Possibly a very nerdy thing to admit (workout data collection motivates me to exercise!), but both activities are personal growth so I don't see any pitfalls.

## Conclusion

The intersection of data science and fitness has opened up exciting possibilities for home gym enthusiasts. By leveraging a more sophisticated model, I've aimed to create a tool that strikes a balance between precision and practicality, making the process of determining workout weights both informed and enjoyable. As I continue to experiment and refine my approach, I look forward to sharing the evolution of this project and its impact on my fitness. Stay tuned for more insights and discoveries around data-driven home workouts.

