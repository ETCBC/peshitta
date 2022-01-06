# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# <img align="right" src="images/tf.png" width="150"/>
# <img align="right" src="images/etcbc.png" width="150"/>
# <img align="left" src="images/logo.png" width="300"/>
#
# # Search Introduction
#
# *Search* in Text-Fabric is a
# [template based](https://annotation.github.io/text-fabric/tf/about/searchusage.html)
# way of looking for structural patterns in your dataset.
#
# Within Text-Fabric we have the unique possibility to combine the ease of formulating search templates for
# complicated syntactical patterns with the power of programmatically processing the results.
#
# This notebook will show you how to get up and running.
#
# ## Easy command
#
# Search is as simple as saying (just an example)
#
# ```python
# results = A.search(template)
# A.show(results)
# ```
#
# See all ins and outs in the
# [search template docs]().
#

# # Incantation
#
# The ins and outs of installing Text-Fabric, getting the corpus, and initializing a notebook are
# explained in the [start tutorial](start.ipynb).

# %load_ext autoreload
# %autoreload 2

from tf.app import use

A = use("peshitta:clone", checkout="clone", hoist=globals())
# A = use('peshitta', hoist=globals())

# # Basic search command
#
# We start with the most simple form of issuing a query.
# Let's look for the words in 1 Samuel, chapter 1.
#
# All work involved in searching takes place under the hood.

query = """
book book=Sm1
  chapter chapter=1
    word
"""
results = A.search(query)
A.table(results, end=10, skipCols="1 2")

# The hyperlinks take us all to the beginning of the book of 1 Samuel.
#
# Note that we can choose start and/or end points in the results list.

A.table(results, start=8, end=13, skipCols="1 2")

# We can show the results more fully with `show()`.

A.show(results, start=1, end=3, withNodes=True)

# # Next
#
# You know how to run queries and show off with their results.
#
# The next thing is to dive deeper into the power of templates.
# But for that you have to go to the
# [search tutorial of the BHSA](https://nbviewer.jupyter.org/github/etcbc/bhsa/blob/master/tutorial/search.ipynb)
# since that data set has much more features to play with.
#
# ---
#
# basic
# [BHSA](https://nbviewer.jupyter.org/github/etcbc/bhsa/blob/master/tutorial/search.ipynb)
#
# CC-BY Dirk Roorda
