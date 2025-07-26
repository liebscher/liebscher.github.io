Title: A Map of New York City Bookshops
Date: 2025-07-26
Tags: data science, Rlang, books & literature
Category: meta
Slug: nyc-bookshops
Authors: Alex Liebscher
Summary: A map of almost all bookshops in NYC, whether they have a cafe or a bar, and how I used R to visualize this hand-curated dataset
Status: published
Cover: /images/bookshops/cover.png

<iframe src="{static}/static/coords.html" width="100%" height="500px"></iframe>

# NYC Bookshops

I really love bookshops. Bookshops are places of serendipity, knowledge, and craft. They're multi-sensory (reminder: smell old books) and generally attract an interesting crowd.

For these reasons and more, I was curious about where all the bookshops are in New York City. I saw an opportunity to appreciate bookshops from a different perspective by simply looking them all up and drawing them on a map.

I did a quick Google search to see if others had done this, and I found one (aged) list, and no robust map (update: just before publishing, I found [this great resource](https://www.nycbookstores.org/)). Feeling like there was a gap here, I started searching for bookshops nearby and recording them in a spreadsheet.

I recorded 38 bookshops on one day, and 18 on another. A good number since then too. It might not be every bookstore in the city, but it's many of them. Some bookshops have a cafe, or a bar, or both inside too. I made note of this, since these are often great spaces to spend time. I chose to focus only on general, independent bookstores, not Barnes & Noble or bookstores that cater to, for example, cookbooks only (sorry [Archestratus](http://www.archestrat.us/))

I hope that this map is useful to some, and just interesting or inspiring to others.

The rest of this article details my process for visualizing the bookshops. I'm a research scientist by day, and I love a good data visualization problem. I don't often work with spatial data though, so it was a learning experience for me.

## Technical Project

In addition to this being a bibliophile's project, I also was hoping to learn how to create good maps with R. So, below I'll explain a bit of the technical side of the project for anyone interested.

At first, I was looking at tidygeocoder. I planned to manually record and load in a few data points to start, and if I liked what I saw, I'd try to automate the bookshop search. I ended up never automating the search, because I enjoyed the process of finding the bookstores through a more intentional process. This meant using Google and Google Maps to find bookstores, as well as paying closer attention in conversations and while walking through neighborhoods. Manually compiling my list gave me the opportunity to look far and wide in unconventional places, both online and in the real world, and to meticulously curate the list.

As mentioned, I chose to keep track of a few extra variables that matter to me. In addition to the presence of a cafe or bar in the bookstore, I recorded their address; opening year; whether they sold new, used, or both; and whether I had visited or not.

It turned out quickly that geocoding from the address worked great on the first time through with the freely available OSM. I ended up creating a method to cache the coordinates, so I wouldn't have to repeatedly call the API for all addresses when I wanted to generate a new one, which would take too much time.

I thought about how I might get these coordinates on a map of NYC. I decided it might be nice to plot borough boundaries, or neighborhood boundaries, as well, for better spatial orientation. I learned that neighborhood boundaries are more ambiguous, especially with the many social and historical contexts here in NYC. I also thought it might be nice to plot subway lines, or the nearest subway lines to each bookstore. I didn't get around to this piece, but maybe in the future.

I searched the internet, mostly on the NYC gov website for data to leverage--map data, public transit data, and sociodemographic data. I discovered that approximate neighborhoods are called Public Use Microdata Areas (PUMAs). There are also [NYC Community Districts](https://www.nyc.gov/assets/planning/download/pdf/data-maps/nyc-population/census2010/puma_cd_map.pdf) (CDs).

I faced a problem though: it was very hard to find a usable file of neighborhoods. There were lots of broken links with the opendata site.

As I was looking for workarounds, I found `nycgeo`. Given the scale of NYC, I had a feeling someone had solved my problem before. After a fairly straightforward install process, here is how I ended up visualizing the boundary shapefiles from the package:

    :::r
    boundaries |>
        ggplot(aes(fill = borough_name)) +
        geom_sf(linewidth = 1/10, show.legend = F) +
        scale_fill_manual(values = c("#ccd5ae", "#e9edc9", "#fefae0", "#f5ebe0", "#faedcd")) +
        theme_void()

<img data-src="{static}/images/bookshops/nta-boundaries.png" width="640px" class="uk-align-center" uk-img/>


Originally, based on the addresses, the bookshop coordinates were very, very wrong. I couldn't figure out why though. I checked the data that OSM gave and it seemed right. I thought maybe I needed to convert the lat/long to shapefile geometry for a correct overlay. I tried using `st_as_sf`, but this was also very wrong.

I searched high and low on StackOverflow, but still could not figure out how to correctly plot the coordinates on the above map. Almost ready to just throw in the towel, I went to ChatGPT and told it my issue. Miraculously, it suggested that long and lat might be reversed in my map call. That was correct, and after switching those I could see the bookstores show up on my map!

However, it was too zoomed out. I was curious if there was an easy way to just "zoom" in. I found a little code snippet online to do that zooming around a centroid coordinate, and this ended up working great.

At this point, I still only had a few data points (bookstores) to work with, and this was all taking place on a non-interactive map. It was now time to go and actually fill out the dataset.

I soon discovered that there are _a lot_ of bookshops in NYC. I decided to focus my work to the generalist book shops, not specialty ones (cooking, performance arts, etc.).

I had some of the data visualized on the map, and then I discovered `mapview`. This package handled **a lot** of the manual work of plotting data on a map, plus it included interactivity which was extremely nice. This package is ultimately what I've ended up using to plot the bookshops. Importantly though, the interactive map at the top is embedded on this static website. This is different from showing up interactively in my R session. To accomplish this, luckily `mapview` has an export-to-HTML function:

    :::r
    coords_sf |>
        select(-c(id, has_cafe, has_bar, geometry)) |>
        mapview(label = 'name', zcol = "type", burst = FALSE, map.types = c("CartoDB.Positron", "OpenStreetMap")) |>
        mapshot(url = "coords.html")

Here, `coords_sf` has a column `geometry` that contains each bookstores' coordinates point.

With the data I've compiled, I can explore NYC bookshops on a bigger scale. For example, here is a distribution of when all the currently open bookshops opened their doors (I pulled this data from the bookstore's website or from new articles of its opening):

<img data-src="{static}/images/bookshops/opening-years.png" width="640px" class="uk-align-center" uk-img/>

Here is a map showing the count of bookshops within neighborhood boundaries:

<img data-src="{static}/images/bookshops/neighborhood-count.png" width="640px" class="uk-align-center" uk-img/>

The top six neighborhoods containing the most bookshops are:

<table style="width: 100%; border-collapse: collapse;">
  <thead>
    <tr>
      <th style="padding: 6px; background-color: #f2f2f2; border-right: 1px solid #333333; border-bottom: 1px solid #333333;">Neighborhood</th>
      <th style="padding: 6px; background-color: #f2f2f2; border-left: 1px solid #333333; border-right: 1px solid #333333; border-bottom: 1px solid #333333;">Count</th>
      <th style="padding: 6px; background-color: #f2f2f2; border-left: 1px solid #333333; border-bottom: 1px solid #333333;">Bookshops</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom: 1px solid #333333;">
      <td style="padding: 6px; border-right: 1px solid #333333;">West Village</td>
      <td style="padding: 6px; border-left: 1px solid #333333; border-right: 1px solid #333333;">5</td>
      <td style="padding: 6px; border-left: 1px solid #333333;">Strand Book Store, Mercer Street Books & Records, Alabaster Bookshop, Three Lives & Company, Codex</td>
    </tr>
    <tr style="border-bottom: 1px solid #333333;">
      <td style="padding: 6px; border-right: 1px solid #333333;">Bushwick North</td>
      <td style="padding: 6px; border-left: 1px solid #333333; border-right: 1px solid #333333;">4</td>
      <td style="padding: 6px; border-left: 1px solid #333333;">Human Relations, Molasses Books, Mil Mundos Books, Hive Mind Books & Coffee Shop</td>
    </tr>
    <tr style="border-bottom: 1px solid #333333;">
      <td style="padding: 6px; border-right: 1px solid #333333;">Williamsburg</td>
      <td style="padding: 6px; border-left: 1px solid #333333; border-right: 1px solid #333333;">3</td>
      <td style="padding: 6px; border-left: 1px solid #333333;">Spoonbill & Sugartown Books, Quimby's Bookstore NYC, Book Thug Nation</td>
    </tr>
    <tr style="border-bottom: 1px solid #333333;">
      <td style="padding: 6px; border-right: 1px solid #333333;">East Village</td>
      <td style="padding: 6px; border-left: 1px solid #333333; border-right: 1px solid #333333;">3</td>
      <td style="padding: 6px; border-left: 1px solid #333333;">Book Club Bar, East Village Books, Mast Books</td>
    </tr>
    <tr style="border-bottom: 1px solid #333333;">
      <td style="padding: 6px; border-right: 1px solid #333333;">UES</td>
      <td style="padding: 6px; border-left: 1px solid #333333; border-right: 1px solid #333333;">3</td>
      <td style="padding: 6px; border-left: 1px solid #333333;">James Cummins Bookseller, Shakespeare & Co, The Corner Bookstore</td>
    </tr>
    <tr>
      <td style="padding: 6px; border-right: 1px solid #333333;">Ridgewood</td>
      <td style="padding: 6px; border-left: 1px solid #333333; border-right: 1px solid #333333;">3</td>
      <td style="padding: 6px; border-left: 1px solid #333333;">Topos Bookstore Cafe, Topos Too, Honey Moon Coffee Shop</td>
    </tr>
  </tbody>
</table>

NYC residents might quible with the neighborhood boundaries, but boundaries are [nearly impossible to get exact](https://www.nytimes.com/interactive/2023/10/29/upshot/new-york-neighborhood-guide.html) so this is just a rough approximation that is hopefully still a little helpful.