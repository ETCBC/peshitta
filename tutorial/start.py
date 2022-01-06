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
# # Tutorial
#
# This notebook gets you started with using
# [Text-Fabric](https://annotation.github.io/text-fabric/) for coding in the Peshitta,
# the Syriac Old Testament.
#
# Familiarity with the underlying
# [data model](https://annotation.github.io/text-fabric/tf/about/datamodel.html)
# is recommended.

# ## Installing Text-Fabric
#
# ### Python
#
# You need to have Python on your system. Most systems have it out of the box,
# but alas, that is python2 and we need at least python **3.6**.
#
# Install it from [python.org](https://www.python.org) or from
# [Anaconda](https://www.anaconda.com/download).
#
# ### TF itself
#
# ```
# pip3 install text-fabric
# ```
#
# ### Jupyter notebook
#
# You need [Jupyter](http://jupyter.org).
#
# If it is not already installed:
#
# ```
# pip3 install jupyter
# ```

# ## Tip
# If you start computing with this tutorial, first copy its parent directory to somewhere else,
# outside your `peshitta` directory.
# If you pull changes from the `peshitta` repository later, your work will not be overwritten.
# Where you put your tutorial directory is up till you.
# It will work from any directory.

# %load_ext autoreload
# %autoreload 2

import os
import collections

from tf.app import use

# # Load Features
# The data of the corpus is organized in features.
# They are *columns* of data.
# Think of the text as a gigantic spreadsheet, where row 1 corresponds to the
# first word, row 2 to the second word, and so on, for all 400,000+ words.
#
# The letters of each word is a column `form` in that spreadsheet.
#
# The corpus contains ca. 10 columns, not only for the words, but also for
# textual objects, such as *books*, *chapters*, and *verses*.
#
# Instead of putting that information in one big table, the data is organized in separate columns.
# We call those columns **features**.

# For the very last version, use `hot`.
#
# For the latest release, use `latest`.
#
# If you have cloned the repos (TF app and data), use `clone`.
#
# If you do not want/need to upgrade, leave out the checkout specifiers.

A = use("peshitta:clone", checkout="clone", hoist=globals())
# A = use('peshitta:hot', checkout="hot", hoist=globals())
# A = use('peshitta:latest', checkout="latest", hoist=globals())
# A = use('peshitta', hoist=globals())

# The result of this all is that we have a bunch of special variables at our disposal
# that give us access to the text and data of the Hebrew Bible.

# ## API
#
# At this point it is helpful to throw a quick glance at the text-fabric API documentation
# (see the links under **API Members** above).
#
# The most essential thing for now is that we can use `F` to access the data in the features
# we've loaded.
# But there is more, such as `N`, which helps us to walk over the text, as we see in a minute.

# # Counting
#
# In order to get acquainted with the data, we start with the simple task of counting.
#
# ## Count all nodes
# We use the
# [`N.walk()` generator](https://annotation.github.io/text-fabric/tf/core/nodes.html#tf.core.nodes.Nodes.walk)
# to walk through the nodes.
#
# We compared corpus to a gigantic spreadsheet, where the rows correspond to the words.
# In Text-Fabric, we call the rows `slots`, because they are the textual positions that can be filled with words.
#
# We also mentioned that there are also more textual objects.
# They are the verses, chapters and books.
# They also correspond to rows in the big spreadsheet.
#
# In Text-Fabric we call all these rows *nodes*, and the `N()` generator
# carries us through those nodes in the textual order.
#
# Just one extra thing: the `info` statements generate timed messages.
# If you use them instead of `print` you'll get a sense of the amount of time that
# the various processing steps typically need.

# +
A.indent(reset=True)
A.info("Counting nodes ...")

i = 0
for n in N.walk():
    i += 1

A.info("{} nodes".format(i))
# -

# ## What are those nodes?
# Every node has a type, like word, or phrase, sentence.
# We know that we have approximately 100,000 words and a few other nodes.
# But what exactly are they?
#
# Text-Fabric has two special features, `otype` and `oslots`, that must occur in every Text-Fabric data set.
# `otype` tells you for each node its type, and you can ask for the number of `slot`s in the text.
#
# Here we go!

F.otype.slotType

F.otype.maxSlot

F.otype.maxNode

F.otype.all

C.levels.data

# This is interesting: above you see all the textual objects, with the average size of their objects,
# the node where they start, and the node where they end.

# ## Count individual object types
# This is an intuitive way to count the number of nodes in each type.
# Note in passing, how we use the `indent` in conjunction with `info` to produce neat timed
# and indented progress messages.

# +
A.indent(reset=True)
A.info("counting objects ...")

for otype in F.otype.all:
    i = 0
    A.indent(level=1, reset=True)

    for n in F.otype.s(otype):
        i += 1

    A.info("{:>7} {}s".format(i, otype))

A.indent(level=0)
A.info("Done")
# -

# # Viewing textual objects
#
# We use the A API (the extra power) to peek into the corpus.

# Let's inspect some words.

wordShow = (1000, 10000, 100000)
for word in wordShow:
    A.pretty(word, withNodes=True)

# # Feature statistics
#
# `F`
# gives access to all features.
# Every feature has a method
# `freqList()`
# to generate a frequency list of its values, higher frequencies first.
# Here are the words in etcbc transliteration, only the top 10:

F.word_etcbc.freqList()[0:10]

# # Layer API
# We travel upwards and downwards, forwards and backwards through the nodes.
# The Layer-API (`L`) provides functions: `u()` for going up, and `d()` for going down,
# `n()` for going to next nodes and `p()` for going to previous nodes.
#
# These directions are indirect notions: nodes are just numbers, but by means of the
# `oslots` feature they are linked to slots. One node *contains* an other node, if the one is linked to a set of slots that contains the set of slots that the other is linked to.
# And one if next or previous to an other, if its slots follow of precede the slots of the other one.
#
# `L.u(node)` **Up** is going to nodes that embed `node`.
#
# `L.d(node)` **Down** is the opposite direction, to those that are contained in `node`.
#
# `L.n(node)` **Next** are the next *adjacent* nodes, i.e. nodes whose first slot comes immediately after the last slot of `node`.
#
# `L.p(node)` **Previous** are the previous *adjacent* nodes, i.e. nodes whose last slot comes immediately before the first slot of `node`.
#
# All these functions yield nodes of all possible otypes.
# By passing an optional parameter, you can restrict the results to nodes of that type.
#
# The result are ordered according to the order of things in the text.
#
# The functions return always a tuple, even if there is just one node in the result.
#
# ## Going up
# We go from the first word to the book it contains.
# Note the `[0]` at the end. You expect one book, yet `L` returns a tuple.
# To get the only element of that tuple, you need to do that `[0]`.
#
# If you are like me, you keep forgetting it, and that will lead to weird error messages later on.

firstBook = L.u(1, otype="book")[0]
print(firstBook)

# And let's see all the containing objects of word 3:

w = 3
for otype in F.otype.all:
    if otype == F.otype.slotType:
        continue
    up = L.u(w, otype=otype)
    upNode = "x" if len(up) == 0 else up[0]
    print("word {} is contained in {} {}".format(w, otype, upNode))

# ## Going next
# Let's go to the next nodes of the first book.

afterFirstBook = L.n(firstBook)
for n in afterFirstBook:
    print(
        "{:>7}: {:<13} first slot={:<6}, last slot={:<6}".format(
            n,
            F.otype.v(n),
            E.oslots.s(n)[0],
            E.oslots.s(n)[-1],
        )
    )
secondBook = L.n(firstBook, otype="book")[0]

# ## Going previous
#
# And let's see what is right before the second book.

for n in L.p(secondBook):
    print(
        "{:>7}: {:<13} first slot={:<6}, last slot={:<6}".format(
            n,
            F.otype.v(n),
            E.oslots.s(n)[0],
            E.oslots.s(n)[-1],
        )
    )

# ## Going down

# We go to the chapters of the second book, and just count them.

chapters = L.d(secondBook, otype="chapter")
print(len(chapters))

# ## The first verse
# We pick the first verse and the first word, and explore what is above and below them.

for n in [1, L.u(1, otype="verse")[0]]:
    A.indent(level=0)
    A.info("Node {}".format(n), tm=False)
    A.indent(level=1)
    A.info("UP", tm=False)
    A.indent(level=2)
    A.info("\n".join(["{:<15} {}".format(u, F.otype.v(u)) for u in L.u(n)]), tm=False)
    A.indent(level=1)
    A.info("DOWN", tm=False)
    A.indent(level=2)
    A.info("\n".join(["{:<15} {}".format(u, F.otype.v(u)) for u in L.d(n)]), tm=False)
A.indent(level=0)
A.info("Done", tm=False)

# # Text API
#
# So far, we have mainly seen nodes and their numbers, and the names of node types.
# You would almost forget that we are dealing with text.
# So let's try to see some text.
#
# In the same way as `F` gives access to feature data,
# `T` gives access to the text.
# That is also feature data, but you can tell Text-Fabric which features are specifically
# carrying the text, and in return Text-Fabric offers you
# a Text API: `T`.
#
# ## Formats
# Syriac text can be represented in a number of ways:
#
# * in transliteration, or in Syriac characters,
# * showing the actual text or only the lexemes,
#
# If you wonder where the information about text formats is stored:
# not in the program text-fabric, but in the data set.
# It has a feature `otext`, which specifies the formats and which features
# must be used to produce them. `otext` is the third special feature in a TF data set,
# next to `otype` and `oslots`.
# It is an optional feature.
# If it is absent, there will be no `T` API.
#
# Here is a list of all available formats in this data set.

sorted(T.formats)

# ## Using the formats
#
# We can pretty display in other formats:

for word in wordShow:
    A.pretty(word, fmt="text-trans-full")

# Now let's use those formats to print out the first verse of the Hebrew Bible.

for fmt in sorted(T.formats):
    print("{}:\n\t{}".format(fmt, T.text(range(1, 12), fmt=fmt)))

# If we do not specify a format, the **default** format is used (`text-orig-full`).

print(T.text(range(1, 12)))

# ## Whole text in all formats in less than two seconds
# Part of the pleasure of working with computers is that they can crunch massive amounts of data.
# The text of the Hebrew Bible is a piece of cake.
#
# It takes just ten seconds to have that cake and eat it.
# In nearly a dozen formats.

# +
A.indent(reset=True)
A.info("writing plain text of whole Peshitta in all formats")

text = collections.defaultdict(list)

for v in F.otype.s("verse"):
    words = L.d(v, "word")
    for fmt in sorted(T.formats):
        text[fmt].append(T.text(words, fmt=fmt))

A.info("done {} formats".format(len(text)))

for fmt in sorted(text):
    print("{}\n{}\n".format(fmt, "\n".join(text[fmt][0:5])))
# -

# ### The full plain text
# We write a few formats to file, in your `Downloads` folder.
#
# There is one subtlety: some books come in two versions, A and B, which are based on different sets of manuscripts (witnesses).
# We will export two Peshitta's: one where for each book the A version is chosen, and one where for each book the B version is chosen.
#
# We also write out book names, chapter and verse numbers.

orig = "text-orig-full"
trans = "text-trans-full"
for fmt in (orig, trans):
    for witness in ("A", "B"):
        with open(
            os.path.expanduser(f"~/Downloads/Peshitta-{witness}-{fmt}.txt"), "w"
        ) as f:
            for b in F.otype.s("book"):
                thisWitness = F.witness.v(b)
                if thisWitness and thisWitness != witness:
                    continue
                book = T.sectionFromNode(b)[0]
                acro = F.book.v(b)
                f.write(f"{book} ({acro})\n\n")
                for c in L.d(b, otype="chapter"):
                    f.write(f"{acro} {F.chapter.v(c)}\n\n")
                    for v in L.d(c, otype="verse"):
                        f.write(f"{F.verse.v(v)} {T.text(v, fmt=fmt, descend=True)}\n")
                f.write("\n")
            f.write("\n")

# !head -n 20 ~/Downloads/Peshitta-A-{orig}.txt

# !head -n 20 ~/Downloads/Peshitta-B-{trans}.txt

# !sed -n '29196,29216p' ~/Downloads/Peshitta-A-{orig}.txt

# !sed -n '29196,29216p' ~/Downloads/Peshitta-B-{orig}.txt

# ## Book names
#
# For Bible book names, we can use several languages.
# Well, in this case we have just English.
#
# ### Languages
# Here are the languages that we can use for book names.
# These languages come from the features `book@ll`, where `ll` is a two letter
# ISO language code. Have a look in your data directory, you can't miss them.

T.languages

# ## Sections
#
# A section is a book, a chapter or a verse.
# Knowledge of sections is not baked into Text-Fabric.
# The config feature `otext.tf` may specify three section levels, and tell
# what the corresponding node types and features are.
#
# From that knowledge it can construct mappings from nodes to sections, e.g. from verse
# nodes to tuples of the form:
#
#     (bookName, chapterNumber, verseNumber)
#
# Here are examples of getting the section that corresponds to a node and vice versa.
#
# **NB:** `sectionFromNode` always delivers a verse specification, either from the
# first slot belonging to that node, or, if `lastSlot`, from the last slot
# belonging to that node.

for x in (
    ("section of first word", T.sectionFromNode(1)),
    ("node of Genesis 1:1", T.nodeFromSection(("Genesis", 1, 1))),
    ("node of book Genesis", T.nodeFromSection(("Genesis",))),
    ("node of chapter Genesis 1", T.nodeFromSection(("Genesis", 1))),
    ("section of book node", T.sectionFromNode(109641)),
    ("idem, now last word", T.sectionFromNode(109641, lastSlot=True)),
    ("section of chapter node", T.sectionFromNode(109668)),
    ("idem, now last word", T.sectionFromNode(109668, lastSlot=True)),
):
    print("{:<30} {}".format(*x))

# # Next steps
#
# By now you have an impression how to compute around in the text.
# While this is still the beginning, I hope you already sense the power of unlimited programmatic access
# to all the bits and bytes in the data set.
#
# Here are a few directions for unleashing that power.
#
# ## Search
# Text-Fabric contains a flexible search engine, that does not only work for this data,
# but also for data that you add to it.
# There is a tutorial dedicated to [search](search.ipynb).
#
# ## Add your own data
# If you study the additional data, you can observe how that data is created and also
# how it is turned into a text-fabric data module.
# The last step is incredibly easy. You can write out every Python dictionary where the keys are numbers
# and the values string or numbers as a Text-Fabric feature.
# When you are creating data, you have already constructed those dictionaries, so writing
# them out is just one method call.
#
# You can then easily share your new features on GitHub, so that your colleagues everywhere
# can try it out for themselves.

# ## Export to Emdros MQL
#
# [EMDROS](http://emdros.org), written by Ulrik Petersen,
# is a text database system with the powerful *topographic* query language MQL.
# The ideas are based on a model devised by Christ-Jan Doedens in
# [Text Databases: One Database Model and Several Retrieval Languages](https://books.google.nl/books?id=9ggOBRz1dO4C).
#
# Text-Fabric's model of slots, nodes and edges is a fairly straightforward translation of the models of Christ-Jan Doedens and Ulrik Petersen.
#
# [SHEBANQ](https://shebanq.ancient-data.org) uses EMDROS to offer users to execute and save MQL queries against the Hebrew Text Database of the ETCBC.
#
# So it is kind of logical and convenient to be able to work with a Text-Fabric resource through MQL.
#
# If you have obtained an MQL dataset somehow, you can turn it into a text-fabric data set by `importMQL()`,
# which we will not show here.
#
# And if you want to export a Text-Fabric data set to MQL, that is also possible.
#
# After the `Fabric(modules=...)` call, you can call `exportMQL()` in order to save all features of the
# indicated modules into a big MQL dump, which can be imported by an EMDROS database.

TF.exportMQL("peshitta", "~/Downloads")

# Now you have a file `~/Downloads/peshitta.mql` of 61 MB.
# You can import it into an Emdros database by saying:
#
#     cd ~/Downloads
#     rm peshitta
#     mql -b 3 < peshitta.mql
#
# The result is an SQLite3 database `peshitta` in the same directory (24 MB).
# You can run a query against it by creating a text file test.mql with this contents:
#
#     select all objects where
#     [book book=Gn
#       [chapter chapter=1
#         [verse verse=1
#           [word]
#         ]
#       ]
#     ]
#
# And then say
#
#     mql -b 3 -d peshitta test.mql
#
# You will see raw query results: all words in Genesis 1:1.
#
# It is not very pretty, and probably you should use a more visual Emdros tool to run those queries.
# You see a lot of node numbers, but the good thing is, you can look those node numbers up in Text-Fabric.

# ---
#
# CC-BY Dirk Roorda
