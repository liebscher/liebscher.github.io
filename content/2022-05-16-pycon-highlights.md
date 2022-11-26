Title: Highlights from PyCon 2022
Date: 2022-05-16
Tags: Python
Category: meta
Slug: pycon-2022-highlights
Authors: Alex Liebscher
Summary: Lessons from 18 talks at this year's three days of Pycon
Status: published
Cover: images/pycon2022logo.png

I was fortunate enough to attend PyCon 2022 this year in Salt Lake City (thanks BetterUp!). This is the annual Python conference, put on by the Python Software Foundation. It was my first time going and I had few expectations going into it. I really enjoyed my time, and learned a number of new things and ways of thinking. Here are some highlights and learnings from a subset of the talks I attended.

## Day 1

<table class="uk-table">
    <thead>
        <tr>
            <th class="uk-width-1-6">Speaker</th>
            <th class="uk-width-1-5">Topic</th>
            <th>Notes</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Łukasz Langa</td>
            <td>Type Annotations</td>
            <td>This was a pretty technical deep-dive into Python's typing system. It was a good reminder to me that this is a (useful) feature in Python that is here to stay. Check out <a href="http://mypy-lang.org/" target="_new">mypy</a> for implementation details. This was my first time hearing of Łukasz, who is a core developer of Python and known by many.</td>
        </tr>
        <tr>
            <td><a href="https://treyhunner.com/" target="_new">Trey Hunner</a></td>
            <td>Python Oddities Explained</td>
            <td>A good reminder that Python is quirky, and to always be on the lookout for things that didn't match your expectations. See also <a href="https://github.com/pablogsal/python-horror-show" target="_new">Python's Horror Show</a> from Pablo S (talk below)</td>
        </tr>
        <tr>
            <td><a href="https://github.com/brandtbucher/" target="_new">Brandt Bucher</a></td>
            <td>Structural Pattern Matching</td>
            <td><a href="https://peps.python.org/pep-0636/" target="_new">Pattern matching</a> (new <code>match</code> keyword) seems like a neat new feature in Python 3.11. Not sure yet how I'd leverage it but I'm happy to know it will exist. It may look like a switch statement, but it's not! It's for flow control and unpacking variables. It's more powerful and flexible than a switch statement, but also serves a slightly different purpose.</td>
        </tr>
        <tr>
            <td>Reuven Lerner</td>
            <td>Understanding Python attributes</td>
            <td>
                <p>Ask yourself, how does a class object, an instance, an instance variable, an attribute, and a descriptor all relate? This is surprisingly complex question, in my opinion. It's one of those oddly confusing computer science-y things (similar to the reasons why I didn't want to study CS). Class objects support two kinds of operations: attribute references and instantiation. With the former, you can access class attributes and variables. With the latter, once we have an instance object, we can only perform attribute reference. There are two instance attribute types: data attributes (sometimes called instance variables or class members) and methods. Instance variables are data unique for an instance, and class variables are data shared by all instances of the class. But what about a descriptor?</p>
                <blockquote>A descriptor is what we call any object that defines `__get__()`, `__set__()`, or `__delete__()` ... The main motivation for descriptors is to provide a hook allowing objects stored in class variables to control what happens during attribute lookup.</blockquote>
                <p>If you're thoroughly confused, I understand. I recommend the Python docs <a href="https://docs.python.org/3/tutorial/classes.html" target="_new">tutorial on classes</a> as a starting point for clarification.</p>
            </td>
        </tr>
        <tr>
            <td>Paul Ganssle</td>
            <td><a href="https://ganssle.io/talks/" target="_new">What to Do When the Bug Is in Someone Else's Code</a></td>
            <td>Somewhat relevant to something I've been doing, a good new way to look at OSS and how to work with it. The speaker discussed five ways that you can overcome bugs in code that you don't maintain. In order of best to worst: patching upstream (fix the bug, then make a PR on the project), wrapper functions (encapsulate buggy code in updated code), monkey patching (assign the global variable a fixed version), vendoring (clone a copy, then patch it locally), and maintaining a fork (fork and patch a copy of the project). I'm guilty of some of the worse behaviors, but now I've got some perspective on why they're "bad" that I didn't have before.</td>
        </tr>
        <tr>
            <td>Nir Barazida</td>
            <td>Dock your Jupyter Notebook</td>
            <td>This talk proposed hosting your Jupyter-based data science and research projects in Docker images. I'd thought of running scripts in containers, but this was specifically about running notebooks. The speaker introduced <a href="https://github.com/jupyter/docker-stacks" target="_new">docker-stacks</a>. I thought this was all very fascinating for creating reproducible research. However, I tried to quickly implement this with my own work and it wasn't so easy. I still find Docker tricky as soon as you want to do even the slightest customizations to the image and runtime. Also, Conda overcomes many barriers to reproducibility and Docker seems to only contribute marginally.</td>
        </tr>
        <tr>
            <td>Maria Jose Molina Contreras</td>
            <td>Creating an indoor air quality monitoring and predictive system</td>
            <td>This was an exposition of a data science project. The speaker basically linked up some CO2 and climate sensors to a microcontroller and slapped a prediction algorithm on top. A couple learnings. First, open the windows, get some air inside your room/office! Second, machine learning projects don't have to be crazy complex. You can get detailed, but it's not necessary to make a point. The most interesting projects are the ones with real world consequences, not just the titanic dataset or housing prices. Third, so much effort goes into everything that sets up any prediction model. Always remember that.</td>
        </tr>
    </tbody>
</table>


# Day 2

<table class="uk-table">
    <thead>
        <tr>
            <th class="uk-width-1-6">Speaker</th>
            <th class="uk-width-1-5">Title</th>
            <th>Notes</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="https://sissaoun.github.io/" target="_new">Sara Issaoun</a></td>
            <td></td>
            <td>Hands down one of the best talks of the weekend. Dr. Issaoun's talk was an inspiration, and for an extremely complex subject (astrophysics, astronomy, blackholes, etc.) she made the audience (or at least me) feel like both experts and curious children. If I had to pick one talk to re-attend, this would be the one. It was the only one where I went up to talk to talk to the speaker at the end.</td>
        </tr>
        <tr>
            <td>Peter Wang</td>
            <td></td>
            <td>Peter gave an introduction to and live-demo of <a href="https://pyscript.net/" target="_new">PyScript</a>, "a framework that allows users to create rich Python applications in the browser using HTML’s interface." This was another extremely inspiring talk. I don't know exactly how I would use Python-in-the-browser but I can imagine it will open a world of possibilities, similar to Node. I'm very eager to see where this project goes, and perhaps sometime soon I'll give it a try and write up my experience.</td>
        </tr>
        <tr>
            <td>Fred Phillips</td>
            <td>Hooking into Imports</td>
            <td>This speaker introduced the idea of "hooking" into the Python import process. For example, it might be necessary to create a blocklist of packages that can't be imported; or load package code from a remote database. In both cases, it can be helpful to modify and overload the default package search and execution process. I currently have no use case for it, but it was good to learn about what's happening under the hood. I had never considered the process with which Python resolves and loads the modules we import.</td>
        </tr>
        <tr>
            <td>Antoine Toubhans</td>
            <td>Flexible ML Experiment Tracking</td>
            <td>Data Version Control (DVC) is something I've been thinking about for years, and just haven't tried it out yet. It seems like it could help solve a number of common data science and machine learning problems. I just need to learn it. I've decided to try it out in a current project I'm working on. There is a learning curve, but not near as confusing as something like Docker; more comparable to git. So far I'm finding some value in the experiment tracking functionality. I don't really want to implement my own visualizations to <a href="https://dvc.org/doc/use-cases/experiment-tracking" traget="_new">track experiments</a>, as was proposed in this talk (with streamlit), and I'm hoping the maintainers of the DVC library add in more viz tools.</td>
        </tr>
        <tr>
            <td>Ryan Kuhl</td>
            <td>GraphQL</td>
            <td>I had heard of GraphQL before but haven't spent anytime learning about it. Therefore I thought this would be a good crash-course on the tool, but it wasn't. GraphQL is a way to query any database (although it works well for graph DBs especially). My takeaways could be summed up as, this is a fascinating technology with a clear implementational benefit over other querying languages, but it seems highly engineered, clunky, and probably only worth it if you're dealing with a lot of data in a production environment.</td>
        </tr>
        <tr>
            <td><a href="https://github.com/pablogsal" target="_new">Pablo Galindo Salgado</a></td>
            <td>Making Python better w/ Errors</td>
            <td>Python 3.11 and 3.12 will contain some big makeovers in the traceback and error diagnostic capabilities in Python. I'm looking forward to having clearer and more specific errors and exceptions.</td>
        </tr>
        <tr>
            <td>Kelly Schuster, Sean Paredes</td>
            <td>Python like a 12-year-old</td>
            <td>The speakers were two Python educators, who have experience teaching Python to middle schoolers. Their top learnings from working with these kids: Be curious! Take risks! Kids think broadly, unlike us adults. Engage all senses, not just what you can see (e.g. build something with your hands). Always be on the lookout for unexpected behavior. When solving a problem, think: what's the worst way to do this? (to force yourself to think in others' shoes.)</td>
        </tr>
        <tr>
            <td>Jeremiah Paige</td>
            <td>Intro to Introspection</td>
            <td>Python has many tools available for debugging, and although Python can be frustrating with its lack of verbosity sometimes, we must remember what we have at our disposal to dissect issues. For example, Python has the <code><a href="https://docs.python.org/3/library/inspect.html" target="_new">inspect</a></code> built-in module to help diagnose runtime issues.</td>
        </tr>
    </tbody>
</table>

## Day 3


<table class="uk-table">
    <thead>
        <tr>
            <th class="uk-width-1-6">Speaker</th>
            <th class="uk-width-1-5">Title</th>
            <th>Notes</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Joseph Lucas</td>
            <td>Serialization</td>
            <td>This talk introduced serialization and ways to do this in Python. Serialization refers to breaking down data and objects (in Python, or elsewhere) and storing it with the intent to deserialize it later for use. The speaker first talked about the built-in <a href="https://docs.python.org/3/library/pickle.html" target="_new">pickle</a> module. This is a Python-specific module for serializing objects and data structures in a compressed byte-stream. Unlike JSON (another serialization format), pickles are binary, not unicode; pickles are not human readable; pickles can represent a wide number of Python objects; and deserializing pickles can pose an execution safety risk, unlike JSON. If we're trying to serialize an object that pickle cannot handle, there is the <a href="https://pypi.org/project/dill/" target="_new">dill</a> module.</td>
        </tr>
        <tr>
            <td>Tetsuya "Jesse" Hirata</td>
            <td>Productionize Research-Oriented Code</td>
            <td>I went into this thinking it would cover how to write research code for your production engineers. Instead, it was how to read research code from your researchers as an engineer. This was a pleasant surprise, and was almost sort of a lesson in empathy. This reinforced my belief that my code and work is most valuable when it can be (quickly and easily) taken to a place of impact. Some reminders for myself: write clean code, and document it; modularize when possible; separate loading, cleaning, processing, and modeling; if you have time, look for ways to refactor.</td>
        </tr>
        <tr>
            <td>Cillian Kieran</td>
            <td>Open-Source Tools For Data Privacy</td>
            <td>The <a href="https://ethyca.com/fides/" target="_new">Ethyca fida</a> folks have laid out a really appealing taxonomy of data privacy in the way of privacy-as-code. I love data privacy, and I lvoe categorizing things, especially data, so this is like candy to me. I don't know if I would try this out in reality, as it seems like a pretty heavy lift, but maybe one day.</td>
        </tr>
    </tbody>
</table>

