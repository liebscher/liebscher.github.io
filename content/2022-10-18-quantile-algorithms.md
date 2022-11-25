Title: Estimating Quantiles
Date: 2022-11-05
Tags: Statistics, Rlang
Category: meta
Slug: estimating-quantiles
Authors: Alex Liebscher
Summary: What are quantiles, and what's happening underneath the hood of quantile()?
Status: published

<style>
#avkrsexhvb .gt_table {
  display: table;
  border-collapse: collapse;
  margin-left: auto;
  margin-right: auto;
  color: #333333;
  font-size: 14px;
  font-weight: normal;
  font-style: normal;
  background-color: #FFFFFF;
  width: auto;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #A8A8A8;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #A8A8A8;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
}

#avkrsexhvb .gt_heading {
  background-color: #FFFFFF;
  text-align: center;
  border-bottom-color: #FFFFFF;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
}

#avkrsexhvb .gt_title {
  color: #333333;
  font-size: 125%;
  font-weight: initial;
  padding-top: 4px;
  padding-bottom: 4px;
  border-bottom-color: #FFFFFF;
  border-bottom-width: 0;
}

#avkrsexhvb .gt_subtitle {
  color: #333333;
  font-size: 85%;
  font-weight: initial;
  padding-top: 0;
  padding-bottom: 6px;
  border-top-color: #FFFFFF;
  border-top-width: 0;
}

#avkrsexhvb .gt_bottom_border {
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}

#avkrsexhvb .gt_col_headings {
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
}

#avkrsexhvb .gt_col_heading {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: normal;
  text-transform: inherit;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 6px;
  padding-left: 5px;
  padding-right: 5px;
  overflow-x: hidden;
}

#avkrsexhvb .gt_column_spanner_outer {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: normal;
  text-transform: inherit;
  padding-top: 0;
  padding-bottom: 0;
  padding-left: 4px;
  padding-right: 4px;
}

#avkrsexhvb .gt_column_spanner_outer:first-child {
  padding-left: 0;
}

#avkrsexhvb .gt_column_spanner_outer:last-child {
  padding-right: 0;
}

#avkrsexhvb .gt_column_spanner {
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 5px;
  overflow-x: hidden;
  display: inline-block;
  width: 100%;
}

#avkrsexhvb .gt_group_heading {
  padding: 8px;
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: middle;
}

#avkrsexhvb .gt_empty_group_heading {
  padding: 0.5px;
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  vertical-align: middle;
}

#avkrsexhvb .gt_from_md > :first-child {
  margin-top: 0;
}

#avkrsexhvb .gt_from_md > :last-child {
  margin-bottom: 0;
}

#avkrsexhvb .gt_row {
  padding-top: 6px;
  padding-bottom: 6px;
  padding-left: 5px;
  padding-right: 5px;
  margin: 10px;
  border-top-style: solid;
  border-top-width: 1px;
  border-top-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: middle;
  overflow-x: hidden;
}

#avkrsexhvb .gt_stub {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-right-style: solid;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  padding-left: 12px;
}

#avkrsexhvb .gt_summary_row {
  color: #333333;
  background-color: #FFFFFF;
  text-transform: inherit;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
}

#avkrsexhvb .gt_first_summary_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
}

#avkrsexhvb .gt_grand_summary_row {
  color: #333333;
  background-color: #FFFFFF;
  text-transform: inherit;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
}

#avkrsexhvb .gt_first_grand_summary_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-top-style: double;
  border-top-width: 6px;
  border-top-color: #D3D3D3;
}

#avkrsexhvb .gt_striped {
  background-color: rgba(128, 128, 128, 0.05);
}

#avkrsexhvb .gt_table_body {
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}

#avkrsexhvb .gt_footnotes {
  color: #333333;
  background-color: #FFFFFF;
  border-bottom-style: none;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
}

#avkrsexhvb .gt_footnote {
  margin: 0px;
  font-size: 90%;
  padding: 4px;
}

#avkrsexhvb .gt_sourcenotes {
  color: #333333;
  background-color: #FFFFFF;
  border-bottom-style: none;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
}

#avkrsexhvb .gt_sourcenote {
  font-size: 90%;
  padding: 4px;
}

#avkrsexhvb .gt_left {
  text-align: left;
}

#avkrsexhvb .gt_center {
  text-align: center;
}

#avkrsexhvb .gt_right {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

#avkrsexhvb .gt_font_normal {
  font-weight: normal;
}

#avkrsexhvb .gt_font_bold {
  font-weight: bold;
}

#avkrsexhvb .gt_font_italic {
  font-style: italic;
}

#avkrsexhvb .gt_super {
  font-size: 65%;
}

#avkrsexhvb .gt_footnote_marks {
  font-style: italic;
  font-weight: normal;
  font-size: 65%;
}
</style>

We see medians, quartiles, percentiles, and quantiles everywhere we look. For example, we see them [sports](https://nypost.com/2022/11/02/astros-vs-phillies-prediction-game-4-odds-and-pick-today/) ("the native of the Dominican Republic ranked in the... 95th percentile in expected slugging percentage and 82nd percentile in hard-hit rate"), [finance](https://www.marketwatch.com/story/heres-strong-new-evidence-that-a-u-s-stock-market-rally-is-coming-soon-11667526884) ("the index currently stands at just the 20th percentile of the historical distribution"), and [real estate](https://richmond.com/business/local/central-virginia-housing-market-cools-median-price-still-32-000-higher-than-last-year/article_68219452-3f66-58f0-9c4d-9addd67e6dcc.html) ("median price still $32,000 higher than last year"). For those who've taken a probability course, quantiles must sound familiar. But, what *is* a quantile, or a percentile? And how do we compute and interpret them?

This came up for me and my colleagues at BetterUp recently. We had run a typical analysis and ended up computing some important quantiles of the data. To ensure our story was clear and crisp, we asked, What exactly happens when we run `quantile()` in R? What does the output really mean? We all sort of knew, but I wish I'd firmly known the answer.

Let's take a look at two examples that help show what sorts of questions can arise when computing quantiles.

First, in example A, consider the 0th, 25th, 50th (median), 75th, and 100th quantiles of the numbers 0 through 10:

    :::r
    quantile(c(0,1,2,3,4,5,6,7,8,9,10))

<pre class="code-output">
  0%  25%  50%  75% 100%
 0.0  2.5  5.0  7.5 10.0
</pre>

And now in example B, let's look at the same quantiles for just three numbers, 0, 1, and 2:

    :::r
    quantile(c(0,1,2))

<pre class="code-output">
  0%  25%  50%  75% 100%
 0.0  0.5  1.0  1.5  2.0
</pre>

Some questions that come to my mind include, how can we have a quantile that's not in the original data (e.g. 7.5 in example A)? How can 50% of our data in example B be less than 1, when we know that one out of three numbers in the data are less than 1? If the 0th-quantile means 0% of the data is less than 0, how can we have it such that 100% of the data is less than the maximum (but not include the maximum)?

In this article we will explore and learn about what quantiles are (since I seem to have forgotten), and will dissect the `quantile()` function in R. 

# What's a Quantile?

We'll talk about quantiles here, but there's a summary below about medians, quartiles, and percentiles. To begin though, I've found [Gilchrist's (2000)](https://www.google.com/books/edition/Statistical_Modelling_with_Quantile_Func/7c1LimP_e-AC?hl=en&gbpv=1&pg=PP1&printsec=frontcover) definition of a quantile the easiest to understand:

> A quantile is simply the value that corresponds to a specified proportion of a sample or population.

A couple things stand out to me here. First, I like his use of "proportion" — this feels to me like the easiest-to-understand term to use. Second, notice the use of both sample and population. We know going forward then that we need to consider both.

A quantile is best seen as a function, where we put in a proportion from 0 to 1 (inclusive) and the output denotes the value of the data that has that proportion of data less than it.

As [the R documentation](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/quantile.html) for the quantile function puts it:

> The generic function `quantile` produces sample quantiles corresponding to the given probabilities. The smallest observation corresponds to a probability of 0 and the largest to a probability of 1.

They refer to the proportions as probabilities, and specifically indicate this function produces sample quantiles. What importance does the sample quantile hold for us? [Hyndman and Fan (1996)](https://www.maths.usyd.edu.au/u/UG/SM/STAT3022/r/current/Misc/Sample%20Quantiles%20in%20Statistical%20Packages.pdf) specifies:

> Sample quantiles provide nonparametric estimators of their population counterparts.

Here we have a very critical relationship: the sample quantile estimates the population quantile. Like the standard deviation, or even the mean, we have definitions for the sample estimators in the event we don't have the population parameters (which is almost always the case). [Sample estimators](https://en.wikipedia.org/wiki/Estimator) aim to fulfill a number of qualities that make one better than another.

This means it's an open question *how* to estimate the population parameters. Over many decades, many researchers have identified multiple ways we can do that. Hyndman and Fan (1996) review nine different ways to estimate the sample quantiles. R implements these and sets a default for the user.

**In review, a quantile is the value that corresponds to a specified proportion of the sample data or population.** Almost never do we know the population parameters, so we must rely on estimating them with sample estimators. The `quantile` funciton in R provides nine different quantile sample estimator functions for the user to choose from.

<details>
<summary>What are the median, quartiles, and percentiles?</summary>

<p>We can refer to Gilchrist (2000) for the definition of the median:</p>

<blockquote>
Thus the median of a sample of data is the quantile corresponding to a proportion of 0.5 of the ordered data. For a theoretical population it corresponds to the quantile with probability of 0.5.
</blockquote>

<p>Quartiles correspond to proportions of the data at 0.25 and 0.75 as well. Percentiles correspond to proprtions of the data every 1-percentage points. So, the 50th-percentile corresponds to the 50th-quantile which corresponds to the 2nd-quartiles which corresponds to the median.</p>

</details>

<!-- ## Formulation

So if Q(p) is the quantile function, the median is Q(0.5).

The Quantile Function, denoted $Q(p)$:

$x_p =$ the value of $x$ for which $P(X \le x_p) = p$

$x_p$ is called the p-quantile of the population. $Q(p) = x_p$. -->

## Population Quantiles

In this example, we'll look at population quantiles for the normal distribution. In this case we know how to parameterize the distribution and we have a continuous equation for the distribution. Both make the following case possible.

Here is the normal (gaussian) distribution, which you might be familiar with:

<img data-src="{static}/images/quantiles-fig1.png" class="uk-align-center" width="80%" height="" alt="" uk-img>

Most of the density of this distribution is between about -3 and 3. If we were to draw a random number from this distribution, it'd probably be close to 0. After many draws, about 95% would be between -1.96 and 1.96. I drew this plot in R with the `dnorm` function.

If you've taken an intro probability course, you might recognize that with the [density function](https://en.wikipedia.org/wiki/Cumulative_distribution_function) (like the one above), we can take the integral and compute the [cumulative density function](https://en.wikipedia.org/wiki/Cumulative_distribution_function) (CDF). We do so here:

<img data-src="{static}/images/quantiles-fig2.png" class="uk-align-center" width="80%" height="" alt="" uk-img>

This makes the y-axis our cumulative density, and we know that the cumulative density describes at each value the proportion of data up to that value. So here I've labeled the median, which describes 50% of the data up to that point. I drew this plot in R with the `pnorm` function.

But as you can see, our median isn't yet an easily computed result of a function. We'd have to take the y-axis value, 0.5, and compute the x-axis value of the blue line at that value. How do we make this easier to compute and interpret?

The answer is the take the inverse of the cumulative distribution, which is known as the Quantile Function.
<!-- , $Q(p) = F^{-1}(p)$. -->

<img data-src="{static}/images/quantiles-fig3.png" class="uk-align-center" width="80%" height="" alt="" uk-img>

It's possible to visualize this plot because the equation for the normal distribution has an inverse. Now, it's easy to take a proportion, say 0.5, and use that equation to quickly and easily output the value of the data that corresponds with it. I drew this plot in R with the `qnorm` function.

## Sample Estimation of Quantiles with Real Data

Let's play with some real data. Here we'll take the publication dates of the top 20 most cited scientific papers in history. The years these papers were published are, in chronological order,

```
1951, 1957, 1958, 1959, 1962, 1970, 1975, 1975, 1976, 1977, 1979, 1987, 1987, 1988, 1990, 1993, 1994, 1996, 1997, 2008
```

This data was put together in 2014 by Thompson Reuters/Web of Science and [written up by a few at Nature](https://www.nature.com/news/the-top-100-papers-1.16224). There's an alternative list put together by [Google Scholar](https://www.nature.com/news/the-top-100-papers-1.16224#/alternative).

<details>
<summary>What are the most cited scientific papers?</summary>

According to the list I found, the top three most cited papers are:
<ol>
<li>305,148 citations: Lowry, O. H. (1951). Protein measurement with the Folin phenol reagent. J biol Chem, 193, 265-275.</li>
<li>213,005 citations: Laemmli, U. K. (1970). Cleavage of structural proteins during the assembly of the head of bacteriophage T4. Nature, 227(5259), 680-685.</li>
<li>155,530 citations: Bradford, M. M. (1976). A rapid and sensitive method for the quantitation of microgram quantities of protein utilizing the principle of protein-dye binding. Analytical biochemistry, 72(1-2), 248-254.</li>
</ol>

</details>

This is 1-dimensional data, and here's a visualization of the dates:

<img data-src="{static}/images/quantiles-fig4.png" class="uk-align-center" width="80%" height="" alt="" uk-img>

For illustration purposes I've added a little random horizontal jitter. You can see that our oldest paper was published in the 50s, and the most recent just before 2010.

Creating a denisty plot is fairly easy; we just create a histogram of the data.

<img data-src="{static}/images/quantiles-fig5.png" class="uk-align-center" width="80%" height="" alt="" uk-img>

We've bucketed in 10-year increments, and we can see that each decade from 1950 to 2010 has at least one paper which made it to the top 20 papers. The decade with the most top papers is the 1970s, with 6 papers.

Now knowing how we progressed from density function to cumulative density function in the population example above, we have to do a similar step here. To do this, we sort our data and assign each a number in ascending order, up to 20. We know that 100% of our data lies less than or equal to 20 and above 0, so we can normalize the y-axis to set 20 to 1.0. This also holds with our definition of the Quantile Function above (the probability that data is less than or equal to 20 is 1.0).

<img data-src="{static}/images/quantiles-fig6.png" class="uk-align-center" width="80%" height="" alt="" uk-img>

I found it confusing how the smallest data point, 1951, falls at $p=0.05$. Why not 0? We're saying that the probability that the data are less than 1951 is one-twentieth or less. Or, equivalently, that 95% or more of the data are 1951 or more recent. As you can tell, it's very important to have the incusivity of range boundaries defined. We can see this slightly better in the next section.

We can though interpret this graph a little for some interesting results. For example, in this sample, see can see that about 50% of the data lie before 1980. Almost all of the data lie before 2000. All of the data lie after 1950.

The next step is to formalize these conclusions into a formula that we can use to plug in numbers like 0.5, 0.95, or 0.0 to come to similar conclusions.

How we do this is where things get interesting!

### Sample Estimation of Quantiles

Unlike our theoretical population example, whose density function is based off a continuous equation, the sample density function is not defined by an invertible function. This is always true when working with a set of raw sample data.

Because the sample density function, and thus CDF, are step functions, we can't take the inverse. This would lead to some input values resulting in multiple output values, which means this cannot be a function.

Instead, we need to estimate the population quantile function using one of many estimation methods. Sample quantiles provide nonparametric estimators of their population counterparts. Researchers have created these estimators over the years, and popular packages like the `stats` package in R allow the user to choose one from a subset of these. We'll take a look at three such methods.

#### Discontinuous Sample Quantiles

The easiest and least useful way to compute sample quantiles is to take our ordered step data and compute quantiles for only those data points along the step function.

Here is a table of our ordered data, the index of that year, and the computed quantile of that year (the index divided by N):

<div id="avkrsexhvb">
<table class="gt_table">
  
  <thead class="gt_col_headings">
    <tr>
      <th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1">Year</th>
      <th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1">Index</th>
      <th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1">Quantile</th>
    </tr>
  </thead>
  <tbody class="gt_table_body">
    <tr><td class="gt_row gt_right">1951</td>
<td class="gt_row gt_right">1</td>
<td class="gt_row gt_right">0.05</td></tr>
    <tr><td class="gt_row gt_right">1957</td>
<td class="gt_row gt_right">2</td>
<td class="gt_row gt_right">0.10</td></tr>
    <tr><td class="gt_row gt_right">1958</td>
<td class="gt_row gt_right">3</td>
<td class="gt_row gt_right">0.15</td></tr>
    <tr><td class="gt_row gt_right">1959</td>
<td class="gt_row gt_right">4</td>
<td class="gt_row gt_right">0.20</td></tr>
    <tr><td class="gt_row gt_right">1962</td>
<td class="gt_row gt_right">5</td>
<td class="gt_row gt_right">0.25</td></tr>
    <tr><td class="gt_row gt_right">1970</td>
<td class="gt_row gt_right">6</td>
<td class="gt_row gt_right">0.30</td></tr>
    <tr><td class="gt_row gt_right">1975</td>
<td class="gt_row gt_right">7</td>
<td class="gt_row gt_right">0.35</td></tr>
    <tr><td class="gt_row gt_right">1975</td>
<td class="gt_row gt_right">8</td>
<td class="gt_row gt_right">0.40</td></tr>
    <tr><td class="gt_row gt_right">1976</td>
<td class="gt_row gt_right">9</td>
<td class="gt_row gt_right">0.45</td></tr>
    <tr><td class="gt_row gt_right">1977</td>
<td class="gt_row gt_right">10</td>
<td class="gt_row gt_right">0.50</td></tr>
    <tr><td class="gt_row gt_right">1979</td>
<td class="gt_row gt_right">11</td>
<td class="gt_row gt_right">0.55</td></tr>
    <tr><td class="gt_row gt_right">1987</td>
<td class="gt_row gt_right">12</td>
<td class="gt_row gt_right">0.60</td></tr>
    <tr><td class="gt_row gt_right">1987</td>
<td class="gt_row gt_right">13</td>
<td class="gt_row gt_right">0.65</td></tr>
    <tr><td class="gt_row gt_right">1988</td>
<td class="gt_row gt_right">14</td>
<td class="gt_row gt_right">0.70</td></tr>
    <tr><td class="gt_row gt_right">1990</td>
<td class="gt_row gt_right">15</td>
<td class="gt_row gt_right">0.75</td></tr>
    <tr><td class="gt_row gt_right">1993</td>
<td class="gt_row gt_right">16</td>
<td class="gt_row gt_right">0.80</td></tr>
    <tr><td class="gt_row gt_right">1994</td>
<td class="gt_row gt_right">17</td>
<td class="gt_row gt_right">0.85</td></tr>
    <tr><td class="gt_row gt_right">1996</td>
<td class="gt_row gt_right">18</td>
<td class="gt_row gt_right">0.90</td></tr>
    <tr><td class="gt_row gt_right">1997</td>
<td class="gt_row gt_right">19</td>
<td class="gt_row gt_right">0.95</td></tr>
    <tr><td class="gt_row gt_right">2008</td>
<td class="gt_row gt_right">20</td>
<td class="gt_row gt_right">1.00</td></tr>
  </tbody>
</table>
</div>

With this we basically have a look-up table of quantiles. It turns out that we can compute a few common quantiles, like the median and two other quartiles. Based on this table, 50% of the data come before 1977. We can compute these quantiles in R with `quantile(data, p, type=1)`.

<img data-src="{static}/images/quantiles-fig7.png" class="uk-align-center" width="80%" height="" alt="" uk-img>

But with this method, computing quantiles relies on the step function nature of the data. Quantiles are just rounded up, which isn't very accurate or "sophisticated", and leads to jumps in quantiles.  Let's move onto a more useful estimator.

#### Linear Interpolation

One of the next simplest quantile estimators for a sample of data is linear interpolation. Under this method, we draw a line between each point and compute $x_p$ based on evaluating the line between two p-quantiles.

Let's say we wanted to compute the 97.5th-quantile. We know the 95th-quantile is 1997 and the 100th-quantile is 2008. With the above method, the 97.5th-quantile would be 2008. But we can try to more accurately estimate the population by interpolating between the two years. Consider the following equation to interpolate:

$$
x_p = X^n \frac{p_{k+1} - p}{p_{k+1} - p_k} + X^{n+1} \frac{p - p_k}{p_{k+1} - p_k}
$$

The equation between 1997 and 2008 is like: $x_p = 1997(1 - p)/(1 - 0.95) + 2008(p - 0.95)/(1 - 0.95)$, where $p \in [0.95, 1.0]$. Thus, for the 97.5th-quantile, $x_p = 2002.5$. Similarly, with the right values from the table above, $Q(0.475) = x_p = 1976.5$ We can confirm this in R:

    :::r
    quantile(data$year, c(0.475, 0.975), type=4)

<pre class="code-output">
 47.5%  97.5% 
1976.5 2002.5
</pre>

We can visualize both of these calculations like so:

<img data-src="{static}/images/quantiles-fig8.png" class="uk-align-center" width="80%" height="" alt="" uk-img>

We can now flip the axes to illustrate the functional nature (i.e. inverting the function) of this interpolation method:

<img data-src="{static}/images/quantiles-fig9.png" class="uk-align-center" width="80%" height="" alt="" uk-img>

I find it very fascinating to see the lower end of the data start to make itself clear. What before we saw as the quantiles "starting" at 0.05, we now see as just the result of the quantiles evaluating to the same value (1951).

#### Mode-based Estimate

Another way to write the above linear interpolation equation is like the following:

$$
x_p = x_{\lfloor h \rfloor} + (h - \lfloor h \rfloor)(x_{\lceil h \rceil} - x_{\lfloor h \rfloor})
$$
where $h = Np$. For example, for 20 data points and the quantile 0.55, we have $x_p=1979$.

This formula has the benefit of being slightly more general, and is the form that five commonly used estimators use. One of these is the mode-based estimator. This is the default in R when we use the `quantile` function, so it's very important we understand it.

The mode-based estimator has $h = (N - 1)p + 1$. Thus, when $p=0.55$ we have $x_p = 1982.6$. We can confirm this with R:

    :::r
    quantile(data$year, 0.55) # type = 7

<pre class="code-output">
   55%
1982.6
</pre>

It's amazing how different this value is, a full three and a half years different from the linear interpolation method!

<img data-src="{static}/images/quantiles-fig10.png" class="uk-align-center" width="80%" height="" alt="" uk-img>

This estimation method takes care of the lower end of the data phenomenon that we ran into with linear interpolation. Mode-based estimation also appears somewhat smoother.

Hyndman and Fan (1996) outlined six characteristics that a sample quantile estimator should possess. The mode-based estimator satisfied five of six. Although it is distribution-free and generally a fine method to use, it is not unbiased. The best contender in my opinion is the median-based estimate (type 8 in R) since it would be approximately median unbiased.

### Estimation Evaluation

Just for fun, we'll compare how the quantile estimators evaluate when generalized to the remaining top 80 papers.

For example purposes, we'll consider only papers published after 1940. Here are the linear interpolation sample quantiles for the top 20 papers (blue) and all top 100 papers (gray):

<img data-src="{static}/images/quantiles-fig11.png" class="uk-align-center" width="80%" height="" alt="" uk-img>

It looks like when we have more data, the quantile line is more linear, with fewer jumps. This is because we have more data to fill in some of those date gaps that showed up in the smaller sample. Remember that points here denote percentiles, not sample data.

It's not incredibly useful in this situation, but we can also visualize a Q-Q plot to visualize the differences between the two sample distributions:

<img data-src="{static}/images/quantiles-fig12.png" class="uk-align-center" width="80%" height="" alt="" uk-img>

The dashed line is $y=x$. Based on this image, we can tell that the two sample distributions are fairly similar, but not exactly the same. Each point represents a percentile (thus, 100 points shown). Areas of the graph where the points line up on the $y=x$ line indicate points in the distributions that have the same proportion of data below them. For example, you can see that 1975 or so is one of these points: about the same amount of data is before 1975 in both distributions. Areas where the line is steeper than $y=x$ indicate areas where the data in the vertical distribution is more dispersed than the horizontal. Likewise, those flat parts indicate the data is more dispersed in the horizontal distribution.

If we considered the top 100 papers as the theoretical population, we might choose not to use the top 20 papers to estimate quantiles of the population.

To round everything out, let's calculate the sample median of the top 20 papers using a few different methods and compare that to our "population" median (from all 100 papers):

    :::r
    quantile(all_paper_years, 0.5, type = 1)

<pre class="code-output">
 50%
1983
</pre>

This is our "population" median (I use type 1 because this is avoids any interpolation at all of the quantiles). Now, our sample median estimates:

    :::r
    types <- c(1,4,7,8)
    quantiles <- sapply(types, function(t) quantile(top_20_paper_years, 0.5, type = t, names = F))
    names(quantiles) <- types
    quantiles

<pre class="code-output">
   1    4    7    8
1977 1977 1978 1978
</pre>

As you can see, types 7 and 8 are closest to our "population" median by a full year. If we are concerned about an area with more dispersion in the sample data, for example at $p=0.55$, then we actually see type 8 with an estimation error of only ten months. Type 7 has an error of 17 months, and types 4 and 1 have an error of five years! Clearly the latter are not particularly (and relatively) good (unbiased) estimators in this case.

# Review

A few key takeaways from this article:

- A quantile is the value that corresponds to a specified proportion of the sample data or population.
- We usually rely on estimating quantiles with a sample estimator.
- The `quantile` function in R provides nine different quantile sample estimator functions for the user to choose from. The default is mode-based estimation, which may not be the best estimator for your problem.
- Consider a type 1 (inverse CDF) estimator if you want no interpolation of quantiles; type 4 (linear interpolation) if you want to be able to easily explain the mechanics of the interpolation; type 7 (mode-based estimation) if you want your results to match anyone who uses the default in R; and type 8 (median-based estimation) if you'd like to push for a more unbiased estimator.