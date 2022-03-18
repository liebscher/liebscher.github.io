Title: Linear Regression: Parameter Estimation
Date: 2022-02-21
Tags: statistics, python
Category: meta
Slug: linear-regression-parameters
Authors: Alex Liebscher
Summary: Three methods of fitting a line to data
Status: published


<img class="uk-align-center" width="90%" height="" src="{static}/images/regr-header.png" uk-img>
<div class="caption">
Image by Alex Liebscher
</div>

Truly understanding the workings of linear regression isn't as straightforward as an introductory stats class makes it out to be. Because of its utility and storied history, linear regression can now be understood in too many ways for most scientists and data-folks to fully grasp.

This article makes a chip away at this complexity by explaining three routine methods for estimating linear regression parameters. We'll discuss Least Squares, Gradient Descent, and Bayesian estimation.

We'll walk through each with code examples notebook-style and some sparse math to help illustrate what's happening. Before we get started, we've got a few packages to load up. If you don't have them installed, create a `conda` environment and `pip install` them.

    :::python
    import numpy as np
    import matplotlib.pyplot as plt

    from scipy.optimize import minimize

    import pymc3 as pm

    rng = np.random.default_rng(42)

## <a name="s1"></a>Creating our Data

We will first create a fake dataset, also known as a simulated dataset. We do this so later on we can compare our model results to the true data generation process. Imagine a phenomenom that, when nothing happens, with an input of 0, the output is 5. Now imagine that when the process is input with -1, the output is 3; and when input with 1, the output is 7. We can build this simulation by specifying a line like $y = 5 + 2x + \epsilon$, where $\epsilon$ is some random error on each output (for example $\pm 1$).

    :::python
    alpha, beta = 5, 2
    sigma = 0.5

    N = 20

    X = rng.random((N, ))
    y = alpha + beta * X + rng.normal(0, sigma, N)

We can then plot these predictor values, ordered by which the data were generated,

    :::python
    plt.scatter(range(N), X)
    plt.xlabel("Index")
    plt.ylabel("X value");

<pre class="code-output">
    <img src="{static}/images/regression-fig1.svg" uk-svg >
</pre>

and also related with the outcome values,

    :::python
    plt.scatter(X, y)
    plt.xlabel("X")
    plt.ylabel("y");

<pre class="code-output">
    <img src="{static}/images/regression-fig2.svg" uk-svg >
</pre>

The human eye easily picks up a pattern here. There're data that, when the horizontal variable increases, corresponds to an increase in the vertical variable. The pattern looks linear. There also appears to be some noise in the data; one data point doesn't relate to the next in an exactly predictable way.

You're likely familiar with this scenario. As taught (either through instruction or experience), you'd next feel a craving to model this pattern using a linear regression model. This would help you describe, in numerical terms, exactly the pattern you see. If you're jumping the gun, you'd probably dart your eyes to those p-values too. This article won't discuss p-values, but it will discuss how our coefficients are determined.

## Estimating $\alpha$ and $\beta$

Given these simulated data, what can we do to understand what the pattern we see?

### Least Squares

The first and most transparent method for understanding the relationship we see is called Least Squares, or Ordinary Least Squares.

It's called least squares because our goal with this method is to find the line which <span style="color: red;">minimizes</span> the <span style="color: purple;">sum</span> of the <span style="color: orange;">squares</span> of the residuals--the <span style="color: blue;">true outcome</span> minus the <span style="color: green;">model prediction</span>:

$$
\color{red}{\text{argmin}}_{\alpha, \beta} \color{purple}{\sum}_{i=1}^N \color{orange}{(}\color{blue}{y_i} - (\color{green}{\alpha + \beta x_i})\color{orange}{)^2}
$$

The parameter values, or **regression coefficients**, are defined as the best solution to this minimization problem.

#### Algabraic Solution

Our first stop is the algabraic solution to regression. By taking [some calculus](https://seismo.berkeley.edu/~kirchner/eps_120/Toolkits/Toolkit_10.pdf) for granted, we arrive at a solution that requires nothing more than algebra.

In code, we can use our `X` and `y` vectors to compute the values for $\alpha$ and $\beta$ quite easily,

    :::python
    x_mean = X.mean()

    beta_hat = ((X - x_mean)*y).sum() / ((X - x_mean)**2).sum()
    alpha_hat = y.mean() - beta_hat*x_mean

    alpha_hat, beta_hat

<pre class="code-output">(4.441, 2.789)</pre>

To visually assess the fit of this model, let's plot the fitted regression line on the data as well as the true data generation line,

    :::python
    plt.scatter(X, y)

    xp = np.array([0, 1])
    plt.plot(xp, alpha + beta*xp, c = "k", linestyle="--", label="Truth")

    plt.plot(xp, alpha_hat + beta_hat*xp, c = "r", linestyle="-", label="Estimated")

    plt.legend(loc="upper left")
    plt.xlabel("X")
    plt.ylabel("y");

<pre class="code-output">
    <img src="{static}/images/regression-fig3.svg" uk-svg >
</pre>

And that's it, we've calculated a fitted line to the data at hand. As you can see, we came quite close to the true data generation line. Unfortunately, this method really only works if you only have a single predictor, which in many cases is too much of a constraint.

#### Measuring Error

It's common to assess the fit of the model by aggregating the *residuals*. The residuals are the difference between either the true in-sample outcomes or a set of out-of-sample outcomes, and the predicted outcomes for those observations. Since we're not working with any out-of-sample data (like a testing or hold-out set), let's just calculate the in-sample residuals:

    :::python
    y_pred = alpha_hat + beta_hat*X

    residuals = y - y_pred

With this `residuals` vector, we can compute the Mean Squared Error ($\text{MSE} = \frac{1}{df}\sum_{i=0}^n(residuals_i^2)$), Root Mean Squared Error ($\text{RMSE} = \sqrt{\text{MSE}}$), or Mean Absolute Error. [Each of these](http://zerospectrum.com/2019/06/02/mae-vs-mse-vs-rmse/) is a method for quantitatively assessing how well the model fit the data. If we had a test set of data, we could assess how well the model fits new data, i.e. its ability to generalize.

The error in the model $\epsilon$ is assumed to be normally distributed, and there is in fact a strong relationship between how the variance of a Gaussian sample can be computed and the formula for the MSE. Both are drawn from the idea that the squared difference between the true value (the true $x$ or true $y$) and the mean or predicted value ($\mu$ or $\hat{y}$) is a meaningful quantity of dispersion. The general form for either the sample variance or the MSE is

$$
\text{Var}(\theta) = \text{MSE}(\theta) = \mathbb{E}_\theta[(\theta - \hat{\theta})^2]
$$

which can be defined then for either the sample variance

$$
\text{Var}(X) = \mathbb{E}_X[(X - \mu)^2] = \frac{1}{n}\sum_{i=0}^n (x_i - \mu)^2
$$

or the MSE, where $p$ is the number of model parameters (and the 1 indicates a degree of freedom for the intercept)

$$
\text{MSE}(y) = \mathbb{E}_y[(y - \hat{y})^2] = \frac{1}{n-p-1}\sum_{i=0}{n} (y_i - \hat{y_i})^2
$$

The ability of the model to minimize the squared error is also closely related to how well the model captures variance in the data. This is known as the [coefficient of determination](https://en.wikipedia.org/wiki/Coefficient_of_determination) $r^2$, and can be computed like

    :::python
    1 - np.sum((y_pred - y.mean())**2) / np.sum((y - y.mean())**2)

<pre class="code-output">
0.3728
</pre>

This says that, on a scale from 0 to 1, the model captures about 37% of the variance in the response data. Normally we'd need to place this in the context of other studies or research to decide if it's good or bad, but here we know the true data generation process. It's lower than I would have expected, but still it's good to see that the model captures some degree of variance.

#### Linear Algebraic Solution

The algabraic method is good pedalogically, but suffers at estimation when we want more than a single predictor and two parameters. So we'll graduate to a new method, which is actually equivalent to the algabraic method. We'll start by putting our intercept data (just 1's <sup class="uk-link" uk-tooltip="Why 1's? To estimate a constant intercept, the data shouldn't change the estimate when multiplied. The one number which satisfies that identity mapping is 1.">✳︎</sup>) and $X$ data into a matrix $M$

    :::python
    M = np.ndarray((N, 2))
    M[:, 0] = 1
    M[:, 1] = X
    M[:5, :]

<pre class="code-output">
[[1.        , 0.77395605],
 [1.        , 0.43887844],
 [1.        , 0.85859792],
 [1.        , 0.69736803],
 [1.        , 0.09417735]]
</pre>

From this we multiply the transpose of this matrix $M$ by $M$ itself. If $M$ is originally $N$ by $2$, then this creates a $2$ by $2$ matrix. We then invert this matrix. There are tricks to doing this for models with many parameters, such as the LU decomposition or Cholesky decomposition, which I won't go into detail about here. With the inverse, we multiply this by $M$ transpose to get an $2 \times N$. Lastly, this is multiplied by $\bf{y}$ to get our parameter solution, a $2 \times 1$ vector.

$$
\require{boldsymbol}
\boldsymbol{\hat{\beta}} = (M^TM)^{-1}M^T\boldsymbol{y}
$$

in one line of Python this looks like

    :::python
    np.matmul(np.matmul(np.linalg.inv(np.matmul(M.T, M)), M.T), y)

This is an excellent progression from the algabraic solution we just had because this allows us to find the parameter values for an arbitrarily large model, constrained only by our ability to take the inverse of a potentially large matrix. Luckily, as I mentioned, modern methods have tricks to increase the power of this method.

This matrix multiplication method is what R is doing when you call `lm()` with a formula and a data frame. Granted, under the hood of this function there're layers of optimization and numerical tricks, but it's conceptually the same. For an excellent dive into the machinery behind `lm` I highly recommend [this blog article](https://madrury.github.io/jekyll/update/statistics/2016/07/20/lm-in-R.html) on the matter.

### Gradient Descent

Least squares is sufficient for your typical linear regression model, and has the great benefit of having an analytical solution. But other regression models require other forms of finding the best parameter values.

One such alternative form is Gradient Descent.

First, a function to calculate the mean squared error.

    :::python
    def mean_squared_error(Beta):
        residuals = y - (np.matmul(M, Beta))
        return np.mean(residuals**2)

We need to set uniform random initial values for our parameters <sup class="uk-link" uk-tooltip="True, you could start with any values between -Inf and Inf, but most models don't have parameter estimates that large (if they do, you might consider transforming/scaling your data.">✳︎</sup>, $\alpha$ and $\beta$, or in this case $\hat{\beta}$.

    :::python
    beta_hat = rng.random((2,))
    beta_hat

<pre class="code-output">
[0.437, 0.832]
</pre>

This means that without fitting the model to our data, we believe the intercept is 0.437 and the slope is 0.832. Compared to the true values (5 and 2, respectively), this is a very bad model. But that's expected; we haven't fit the model. How do we use the data to find parameter values that generalize better to the data?

The basic idea is to measure how bad the current parameter values are, and over many iterations, slowly adjust these parameter values in a better direction. Commonly, this is depicted like a person walking down a mountain in the dark with just a flashlight. The person can't see exactly where the bottom of the mountain is, but with their flashlight, they can look around them and move in a direction that takes them down. Sometimes, if the mountain is rocky, they'll hit a plateau or even start going uphill again. This is called a *local minimum*. They really should get to the *global minimum*. How can we prevent hitting local minima and get to the global minima? There's no perfect answer, but two answers do come up first: step size (how long are the hiker's legs?) and number of iterations (how many steps does the hiker take before they stop walking and throw their hands up?).

The step size, also called the *learning rate*, is usually very small. The smaller it is, the more likely it is the hiker won't miss the right trail down; the larger it is, the faster they could reach the bottom, if they don't hit a local minima on their way. In our case, we'll set our learning rate to 0.01. This was chosen by running the cell a few times with values from 0.1 to 0.00001 and seeing how much progress we made down the mountain (i.e. did we barely move from the randomly set parameter values, or did they overshoot the true model?).

The number of iterations is somewhat inversely related to our step size. If you don't take very big steps, you'll need more steps to get to the bottom of the mountain. If you take big steps, you'll need fewer. We chose 1000 steps here, found by trial and error.

How do we decide which direction to step in? By computing the *gradient* of the least squares error function. Computing the gradient means taking the partial derivate of a function $\mathcal{f}$ at values $p$, written as $\nabla \mathcal{f}(p)$. In our case of least squares errors, $\mathcal{f}(p) = \mathcal{f}(\beta) = \sum_{i=0}^N E_i(\beta)$ where $E_i(\beta)$ is the error of our model at the $i$ observation given the parameters $\beta$.

In notation, we have the least squares error function, and 

$$
\mathcal{f}(\beta) = \sum_{i=0}^N (y_i - \beta \, X_i)^2
$$

The gradient with respect to $\beta$ (our only parameter) is

$$
\begin{align}
\nabla_\beta \; \mathcal{f}(\beta) &= \frac{\partial}{\partial \beta} \; \mathcal{f} \\
&= \sum_{i=0}^N 2(y_i - \beta \, X_i)(-X_i) \\
&= -2 \sum_{i=0}^N (y_i - \hat{y_i})(X_i) \\
&= -2 \sum_{i=0}^N r_i X_i \\
&= -2 \, X^T \, \boldsymbol{r}
\end{align}
$$

where $r_i$ is the residual value for the $i$th observation. We can then scale this down according to our step size and subtract it from our current parameter values to move in the "downhill" direction.

We would write this like

    :::python
    beta_hat_copy = beta_hat.copy()

    learning_rate = 0.01

    history = {'gradient': [], 'beta_hat': [], 'mse': []}

    for epoch in range(1000):
        
        residuals = y - np.matmul(X_mtx, beta_hat_copy)
        gradient = 2/len(y) * np.matmul(X_mtx.T, residuals)
        beta_hat_copy = beta_hat_copy - learning_rate*gradient
        
        if (epoch % 10) == 0:
            history['gradient'].append(gradient)
            history['beta_hat'].append(beta_hat_copy)
            history['mse'].append(mean_squared_error(beta_hat_copy))
            
    history['beta_hat'][-1]

<pre class="code-output">
[4.898, 2.244]
</pre>

And then we can plot the altitude of our hiker as they traversed down the mountain

    :::python
    print('MSE:\t', round(history['mse'][-1], 3))
    plt.xlabel("Iteration")
    plt.ylabel("Mean Squared Error")
    plt.plot(range(0, 1000, 10), history['mse'])

<pre class="code-output">
MSE:	 0.163

<img src="{static}/images/regression-fig5.svg" uk-svg >
</pre>

As you can see, gradient descent looks like it found the bottom of the mountain! The final parameter values it determined were $\alpha = 4.898$ and $\beta = 2.244$, which is close to the true values of 5 and 2.

How does the fitted model look compared to our sample and true data generation line?

    :::python
    plt.scatter(X, y)

    xp = np.array([0, 1])
    plt.plot(xp, alpha + beta*xp, c = "k", linestyle="--", label="Truth")

    plt.plot(xp, np.matmul(history["beta_hat"][-1], [[1, 1], [0, 1]]), c = "r", linestyle="-", label="Estimated")

    plt.legend(loc="upper left")
    plt.xlabel("X")
    plt.ylabel("y");

<pre class="code-output">
    <img src="{static}/images/regression-fig6.svg" uk-svg >
</pre>

Not too bad, given the low number of observations.

Although this is intuitive, researchers have developed far more efficient and less problematic methods for large datasets and models with many parameters. Gradient descent can [out-perform least squares](https://stats.stackexchange.com/questions/278755/why-use-gradient-descent-for-linear-regression-when-a-closed-form-math-solution) in a number of situations, which is part of the reason why I included it here. Bonus concept: this is essentially the backdown of most modern AI, being a critical ingredient of neural networks and forming [the workhorse of backpropogation](https://brilliant.org/wiki/backpropagation/).

### Bayes

The third and last method of parameter estimation I'll talk about is the Bayesian form.

Unlike the past two models, Bayesian estimation puts a lot more emphasis on building the right model. This includes the distributions of parameters and the way they relate, which in frequentist linear regression seems typically taught as assumed or given.

A Bayesian linear model has two to three key components: the outcome distribution, the linear model, and if necessary, the variance parameter. In some linear models, the last two are combined. For example, in a Poisson regression there's only a single parameter, $\lambda$, whereas in a Gaussian regression there're both $\mu$ and $\sigma$.

The first component though is the outcome distribution. If we're modeling a phenomenon that is real-valued and continuous, and tends to not be too skewed or dispersed, then a Gaussian outcome distribution might be a good first attempt. If we're modeling a phenomenon that consists of positive, integer count data, then a Poisson distribution might be most appropriate. There are a plethora of options here, but we'll stick with the Gaussian example.

The Gaussian distribution is parameterized by $\mathcal{N}(\mu, \sigma)$. Instead of finding the one value that maximizes some function for both of these parameters, we'll consider each of these parameters as functions of other values <sup class="uk-link" uk-tooltip="I recognize this is confusing, put another way, these mu and sigma values are not computed directly, and they're not even values. They're distributions, and we compute them through other, more descriptive parameters.">✳︎</sup>.

It's called a linear model because in this case, we'll define $\mu$ as the **function of a linear combination of other parameters**. For example, we might say $\mu = 5$. This is a linear combination of exactly one value and a terrible model because it always will predict something around the value 5. We could add a parameter though, and fit the parameter to the data, like $\mu = \alpha$. Then with *only* our outcome data we'd figure out what $\alpha$ could be. But if we want to use other data to predict our outcome, we need to include that, like $\mu = \alpha + \beta \, X$. Now we have two parameters to fit, and our new one will be fit so as to reflect the relationship between our outcome and $X$.

As you can see though, $\mu$ is just a linear combination. In other models, like the Poisson or a binomial/logistic, we'd need to transform $\mu$ so that it lines up with what the outcome distribution expects for parameters. For example, in the binomial model we'd need $\mu$ to be a probability, which wouldn't line up if we just let it vary as high or low as $\alpha$, $\beta$, and $X$ want it to go. Therefore we'd need a [logit function](https://en.wikipedia.org/wiki/Logit) to constrain those values back to the model parameter space.

But what are $\alpha$ and $\beta$? They are parameters we must estimate. How? By letting them reflect certain distributions. Which distributions? Well, we must consider what values these parameters can take on. What's reasonable given our problem? Let's say we know from theory that our data very rarely exceed -50 or 50. That means if there's no relationship between our outcome and $X$, we might expect $\alpha$ to be approximated by $\mathcal{N}(0, 20)$. Why 20? In a normal distribution with mean 0, there's about 99% of the density between -50 and 50 with a standard deviation of 20. What about $\beta$ though? Suppose we don't expect the rate of change between $X$ and $y$ to be more than 5 units. So if $X$ increases by 1 unit, we shouldn't expect $y$ to increase by more than 5 or decrease by more than -5. Therefore, $\beta$ may be approximated by $\mathcal{N}(0, 2)$.

The other component we know of is $\sigma$. We don't really think $\sigma$ will vary with any data, so we can represent $\sigma$ as a value or a space of values (a distribution). For example, in $\mathcal{N}(\mu, \sigma)$ we could say $\sigma=2$ if we knew that the variance of the Gaussian was 2, or we could say $\sigma \sim \text{Exp}(1)$, as in $\sigma$ reflects values from an exponential distribution with rate 1.

Bringing it all together, we can write out our linear model like so
$$
\begin{aligned}
y & \sim \mathcal{N}(\mu, \sigma)\\
\mu & = \alpha + \beta X\\
\alpha & \sim \mathcal{N}(0, 20)\\
\beta & \sim \mathcal{N}(0, 2)\\
\sigma & \sim \text{Exp}(1)
\end{aligned}
$$

At the end of the day though, enough data will allow this model to fit very well and the distributions we used for $\alpha$, $\beta$, and $\sigma$ will get washed out by the data. In other words, their only function will be to constrain the shape of the parameter, not necessary its values.

What does this model look like in code?

    :::python
    with pm.Model() as model:
        alpha = pm.Normal("alpha", mu=0, sigma=20)
        beta = pm.Normal("beta", mu=0, sigma=2)
        sigma = pm.HalfNormal("sigma", sigma=1)
        
        mu = alpha + X@beta
        y_pred = pm.Normal("y_pred", mu=mu, sigma=sigma, observed=y)
        
        posterior = pm.sample(chains=1, return_inferencedata=True)

Running this cell fits the model and its parameters to the data. The model works by guessing random numbers in a related sequence for the parameters. As it guesses these numbers, it starts to figure out what the space of the parameter distribution looks like, or what the most likely numbers are in the distribution if you were to pull from it at random.

If we pull out the parameters, you'll find that they're each actually a vector. This is that set of numbers the model guessed and identified as best representative of the distribution. It contains the sampling noise that comes with observing a natural phenomenon. Everything is a little noisy after all.

If we want to get just one number for our parameters, we can take the mean of the parameter vectors:

    :::python
    np.mean(posterior.posterior.alpha).values, posterior.posterior.beta.mean().values, posterior.posterior.sigma.mean().values

<pre class="code-output">
[5.207, 1.734, 0.431]
</pre>

In other words, the model believes $\alpha$ is centered around 5.2, $\beta$ around 1.7, and our variance around 0.4. Compared to the true values of 5, 2, and 0.5, this is not bad given only 20 observations.

Another way to see what the model found is by plotting the distributions of the parameters. Here they are with the *mode* of the distribution overlaid in black. I picked the mode because this is then the [Maximum a Posteriori estimate](https://en.wikipedia.org/wiki/Maximum_a_posteriori_estimation).

    :::python
    fig, ax = plt.subplots(1,3, figsize=(12,4), layout='tight', sharey=True)

    ax[1].set_title("Estimated Parameter Values")

    v = posterior.posterior.alpha[0]
    ax[0].hist(v, bins=30, color='lightblue')
    ax[0].vlines(mode(v.round(1)).mode[0], 0, 110, color='black')
    ax[0].set_xlabel("Posterior alpha values")
    ax[0].set_ylabel("Frequency")

    v = posterior.posterior.beta[0]
    ax[1].hist(v, bins=30, color='lightblue')
    ax[1].vlines(mode(v.round(1)).mode[0], 0, 110, color='black')
    ax[1].set_xlabel("Posterior beta values")
    ax[1].set_ylabel("Frequency")

    v = posterior.posterior.sigma[0]
    ax[2].hist(v, bins=30, color='lightblue')
    ax[2].vlines(mode(v.round(1)).mode[0], 0, 110, color='black')
    ax[2].set_xlabel("Posterior sigma values")
    ax[2].set_ylabel("Frequency")

<pre class="code-output">
    <img src="{static}/images/regression-fig7.svg" uk-svg >
</pre>

This may be confusing because compared to our previous two methods of parameter estimation where we had a single estimate for each parameter, now we see a histogram for each. Like I said, this is because a Bayesian model determines the values of parameters through random sampling. There was no random sampling in Least Squares and Gradient Descent. Because of the random sampling, we never know the exact values. This is unhelpful conceptually, but practically it provides us with concrete and sane estimates of *uncertainty*. Now we can compute the single parameter values using the mean, median, or mode; and we can also easily compute how accurate those measures are.

Don't let the histograms make you believe anything conceptually different is happening: we're still figuring out what the parameters should be, now we just have more information about each.

#### Measuring Error

We've estimated the parameters using Bayes and random sampling, and just like the previous two sections, we'd like to measure the error of the model and see how closely it matched the true data generator.

We're going to do this a little different to get more utility out of the Bayesian framework.

For each point, we can calculate the *posterior predictive outcome*. An outcome like this is what the model believes the outcome could be knowing the (un)certainty of the outcomes to begin with.

The posterior predictive accounts for all the uncertainty in $\alpha$, $\beta$, and $\sigma$ to produce a distribution *for each observation*. The uncertainty in the distributions get propogated through the linear model and into the outcome distribution. Through this propogation of uncertainty, each of our 20 observations can be given a distribution. This distribution says, "Given a predictor value for the model, here are roughly the most likely outcomes values of that predictor."

In the following code chunk, we sample and compute the posterior predictive values for each observed predictor. This produces a matrix of 20 observations and many possible outcomes for each observation. We take the 95% interval of each of those points (plus the median), and plot the median point and credible intervals around each point.

    :::python
    with model:
        post_pred = pm.sample_posterior_predictive(posterior.posterior)
    
    plt.plot([min(y), max(y)], [min(y), max(y)], linestyle='--', color='gray', zorder=0)

    plt.scatter(y, np.quantile(post_pred['y_pred'], 0.5, axis=0), zorder=2, color="#2777b4")

    for y_i, point in zip(y, post_pred['y_pred'].T):
        q025 = np.quantile(point, 0.025)
        q975 = np.quantile(point, 0.975)
        q050 = np.quantile(point, 0.5)
        plt.vlines(y_i, q025, q975, color="black", linewidth=0.5, zorder=1)
        
    plt.xlabel("True y value")
    plt.ylabel("Posterior predicted value")
    plt.suptitle("Posterior predicted values")
    plt.title("with 95% credible intervals", fontsize=10)

<pre class="code-output">
    <img src="{static}/images/regression-fig8.svg" uk-svg >
</pre>

This is arguably the most interesting plot of the entire article! Here we see on the x-axis the true data generator value. On the y-axis is the posterior predictive outcome. Each point is what the model believes the outcome should be for that observation's predictors (which we don't see anything of in this plot). And then for each point there's also a representation of the uncertainty of that estimate. The estimate can be interpreted as saying, this observation's outcome is most likely to be this red point, but there's a 95% probability it falls somewhere in the line range." This is of course dependent on the model (so really, there's a 95% probability *given this model*).

A perfectly accurate model would have all the blue points exactly on the dashed line. A perfectly precise model would have very small error bars. A perfectly accurate and precise model would have the blue poitns right on the line and very small error bars.

We see all the error bars include the line at some point, which signals this model seems to be doing pretty good!

## Overview

We've gone over three (really four) methods for estimating the parameters of a linear regression model. We had the least squares method (both formulated through algabra and matrices), gradient descent, and a Bayesian method. It's also possible to think of estimating linear regression parameters using [geometry](https://kaomorphism.com/socraticregression/ols.html) and [calculus](https://www.cs.toronto.edu/~rgrosse/courses/csc321_2017/readings/L02%20Linear%20Regression.pdf). Not too mention the many methods of regularization, like [LASSO and ridge regression](https://en.wikipedia.org/wiki/Linear_regression#Maximum-likelihood_estimation_and_related_techniques), and [robust estimation](https://en.wikipedia.org/wiki/Linear_regression#Other_estimation_techniques). This is all to say that linear regression is a topic with great complexity, making it a daunting, mysterious, and fruitful concept for data-folk to study.