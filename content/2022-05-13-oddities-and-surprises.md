Title: Oddities and Surprises: Unusual Behaviors in R and Python
Date: 2022-05-13
Tags: Python, Rlang
Category: meta
Slug: oddities-and-surprises
Authors: Alex Liebscher
Summary: Questioning the developers of our favorite languages
Status: draft

This document is a collection of unexpected behaviors in R and Python. It's inspired by [Python Oddities](https://treyhunner.com/python-oddities/resources.html) and [Python's horror show](https://github.com/pablogsal/python-horror-show). I will add to it over time.

# Python

## String Strip

### Behavior

Let's say we have a string:

    :::python
    sentence = 'I love when monkeys write'

When we run `sentence.rstrip('new york times')`, as if we wanted to remove any case of "new york times" from the string, we would expect the string to go unchanged. After all, "new york times" is not mentioned anywhere in `sentence`. Instead though, we get this:

    :::python
    sentence.rstrip('new york times')

<pre class="code-output">'I love wh'</pre>

### Explanation

Unlike how one might guess based on their names, Python's `rstrip` and similar string methods don't remove *suffixes*. Instead, they remove trailing characters in the list provided. And as it turns out, "New York Times" is [an anagram](https://en.wikipedia.org/wiki/Anagram) of "monkeys write" (plus the "en" in "when"). Therefore all of the characters in the former get found in the latter.

From the documentation,

> The chars argument is not a suffix; rather, all combinations of its values are stripped

What's the "right" way to remove a suffix? The docs recommend [str.removesuffix()](https://docs.python.org/3/library/stdtypes.html#str.removesuffix). This is only implemented in Python 3.9 and above.