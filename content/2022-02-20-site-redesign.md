Title: 2022 Site Redesign
Date: 2022-02-20
Tags: blogging, design, programming
Category: meta
Slug: site-redesign
Authors: Alex Liebscher
Summary: Redesigning and redeveloping my personal site
Status: published

I've set out on redesigning my personal site. Why? I find Jekyll fairly picky, unstable, and hard to work with. Moreover, in using the Jekyll theme that I was ([al-folio](https://github.com/alshedivat/al-folio)), I found that to also be unstable, hard to keep up to date, and kind of clunky. I appreciate all the people that went in to building both of these tools, but neither has really served me as well as I had once hoped they would.

It's time to not only rework the site generation process, but to update the look of my site to better reflect how I feel and what I need to make the best content I can.

I was actually inspired to do this by the typographer [Miklós Tótfalusi Kis](Miklós Tótfalusi Kis). His design of the Janson typeface is beautiful and inspiring, and it forced me to reflect deeply on it. I discovered it in a book I recently started reading, [A Garden of Earthly Delights](https://en.wikipedia.org/wiki/A_Garden_of_Earthly_Delights) by Joyce Carol Oates, in which it is the typefont the book is set in.

So I've embarked on redesigning my site in a way that resembles this spacing, consistency, sophistication, freedom, and elegance.

<hr />

I started out with the simple theme from [Pelican](https://blog.getpelican.com/), a Python static site generator. I pruned back the Pelican dependencies in the source -- the custom classes, specific element IDs, and some HTML that I wasn't interested in.

Then I added [UI Kit](https://getuikit.com/) to the base template. I chose UI Kit because I recently discovered it as an alternative to Bulma. I really like Bulma, but UI Kit so far has seemed less authortarian in the degree which a site can be built. It also seems to have an impressive range of components and standards for how pieces of a site should be built. In other words, it's minimalistic but featureful when you want.

Although UI Kit seemed promising, I quickly realized how much effort it was going to take to update all of my past articles to the new CSS framework. I try not to let the sunken cost fallacy hold me back, and in this case it seemed worth it to expend that effort.

I spent some time looking for an appropriate font, and I landed on Lora from Google Fonts. One day I might leap into full realization of Janson by buying that typefont, but for now, a free font allows me to prototype and iterate quickly.

I then took some time to figure out the code highlighting features of Pelican. While there is inline code, like ``print("text")``, I still haven't figured out how to get syntax highting for these inline snippets. However, there is beautiful looking code block highlighting. For example, some Python:

```python 
    print("Pelican is a static site generator.")
```

and also R:

```r
    var <- as.character(1L)
```

I knew that I would want to write some articles in a Jupyter notebook style, with code blocks and associated outcomes. So I built a custom CSS solution which attaches an output block to any given code block, like so,

    :::python
    print("hello world")

<pre class="code-output">
hello world
</pre>


I snagged this Pygment Github theme from the Pelican theme [attila](https://github.com/arulrajnet/attila).

It's also important to me that there's $\LaTeX$ support, of which there is, both inline $y \sim N(0, 1)$ and block:

$$
y = \beta_0 + \beta_1 x
$$

In order to render this Mathjax though I had to install the `pelican-render-math` plugin.

I realized that reStructredText files, which are common in the Pelican world, are unfamiliar and difficult to use. For example, the syntax between Markdown and RST for a link is wildly different. Everything feels unnatural and forced. But most of all, if I want to port my work over from my last site to this new one, it is easiest if I use Markdown since everything is already written with Markdown.

Next, I moved on to polishing the article page since that would be a crucial aspect of the site design. I tweaked the width of the page so it's about a 2/3 width, which seemed natural to my own eyes. I also justified the text because I think that looks really nice with longer content, almost like one sees in a book. I spent probably too much time figuring out the ideal syntax highlighting stylesheet and making slight modifications to it. For example, I decided that the Github theme was pretty, but its numerals were gray. In contrast, Jupyter Notebooks light them green, which I like better. Therefore I had to get into the stylesheet and update that one span to reflect my tastes.

I also added a modal for the subscribe form. This only took a few minutes with UIKit's built-in `uk-modal` classes and Javascript add-on, which is a huge improvement compared to other solutions out there that'd require custom JS for the click and close events.

I chose an article header image from Unsplash by <a href="https://unsplash.com/@drew_beamer?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Drew Beamer</a>. It took half a dozen tried but I found one with the right texture, energy, and framing that really makes the title pop.

Then I moved over to the tags. I cleaned up the design of the footer on the index page that lists out the tags for quick navigation. I also cleaned up the individual tag page, removing some of the things that the default page had put in. Overall, I'm still not 100% satisfied. Some sort of abaility for the user to rank by number of articles or another heuristic would be ideal. For now though it will stay as a static alphabetical list.

I wanted to embed readers comments on the blog too because it seems like, for those who don't troll, it can be a useful way to quickly and easily give feedback and, well, comments. For some reason it seems like adding a comments section takes my site to a different realm, like adding this level of dynamic interface is breaking the flow or consistency. I found [a quick guide](https://shahayush.com/2020/05/web-pelican-pt5-disqus-analytics/) which I gave a look, and then went to sign up for Disqus. Turns out, Disqus sucks. It's extremely unpleasant to look at. It's slow to load. It makes no commitment to privacy and overall seems nefarious. To top it all off, it's got ads galore. I was hopeful yet was disappointed by their complete lack of innovation, simplicity, and respect. I spent a little more time looking for an alternative service, but I'm not ready to spend money on something I'm not even sure will have success. In an ideal world, there'd be a service which had a free tier for sites with less than 1,000 or 10,000 monthly views, and paid tiers for anything above. I would sign up for this knowing that I could use the service while it suited my needs and easily upgrade when I knew it'd be a worthwhile invest. I think this would also be a good business model because at the point where a site owner wants to upgrade, they've already invested their engineering and social capital into the platform and (if they are looking to upgrade) are very familiar with the effectiveness of the service.

After getting these elements to a comfortable spot, I'm fairly content with how the site looks and feels right now. From my perspective, it's crisp, smooth, and elegant, just like Janson.

I've made a couple other tweaks, but have now been drafting with the design for a few weeks and haven't gotten tired by the look yet. I take this to be a good sign. It's a little rough around the edges (e.g. things like the copyright page and my resources page), but it's in the right direction and an improvement over my previous site's theme.