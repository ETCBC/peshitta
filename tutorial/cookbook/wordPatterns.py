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

# # Use Text-Fabric search to find word patterns
#
# Prompted by [Paul Noorlander](https://cambridge.academia.edu/PaulNoorlander), answered by Dirk Roorda

# # Getting data and using the TF browser
#
# It is convenient to have the Text-Fabric browser on the side to make quick excursions through the data.
#
# So, go off to a terminal and give the command
#
# ```tf peshitta:latest --checkout=latest```
#
# This fetches the latest version of the Peshitta app and data.
#
# After that, you can just say
#
# ```tf peshitta```
#
# until you got word that a new version of app and/or data has become available.

from tf.app import use

A = use("ETCBC/peshitta", hoist=globals())

# ## string `JBW L` in the text

# Assuming `JBW` is a single word and L is a single word:

query = """
word word_etcbc=JBW
<: word word_etcbc=L
"""

results = A.search(query)

# That does not help. At least one of the assumptions leads to nowhere.
# At this point it might help to use the TF browser to conduct some experiments on the side line.
#
# Running `word word_etcbc=L|JBW` shows that there are no words whose full text is either `L` or `JBW`.
#
# But there are plenty of words starting with a `L`.
#
# ```
# text-fabric peshitta
# ```
#
# You get something like this
#
# ![tfb](images/start-l.png)
#
#
# See
# [search with regular expressions](https://annotation.github.io/text-fabric/tf/about/searchusage.html#feature-specifications)
# for how you can use search patterns to look within feature values.

# The query is `word word_etcbc~^L`, the anatomy of which reads:
#
# * look for a word with a constraint on its feature `word_etcbc`.
# * the constraint is that it should match the regular expression `^L`:
# * the `^` matches the beginning of the string, the `L` matches just an `L`,
# * resulting in the condition: `word_etcbc` starts with an `L`.
#
# Likewise, `$` matches the end of the string, so `word word_etcbc~JBW$` matches each word whose etcbc-transcription ends in `JBW`.
#
# If you try that, you get 58 results:
#
# ![tfb](images/end-jbw.png)
#
# Good. Let's see whether there are combined results.
#
# We do that here, in the notebook.

query = """
word word_etcbc~JBW$
<: word word_etcbc~^L
"""

results = A.search(query)

# Lo and behold:

A.table(results, fmt="text-trans-full")

# We get the transcription by asking for text format `text-trans-full`.
#
# The available text formats can be found in the TF browser, under options (see screenshot above).

# ## word starting with '<:L' followed by an other word starting with `<:L`

query = """
word word_etcbc~^<:L
<: word word_etcbc~<:L
"""

results = A.search(query)

# I suspect the `:` spoils things. How many words contain `:`?
#
# Fire `word word_etcbc~:` and you get only 6.
#
# Let's leave out the `:`:

query = """
word word_etcbc~^<L
<: word word_etcbc~<L
"""

results = A.search(query)

A.table(results, fmt="text-trans-full", start=0, end=20)

# ## word containing root `HWY`

# The current Peshitta data set is not up to this question, because lemma's and roots are not marked.
# The best we can do is to try for a set of surface patterns.
#
# Playing around (in the TF browser) yields this:
#
# * `word word_etcbc~HWY` 0 results! Could it be that you meant `HWJ`?
# * `word word_etcbc~HWJ` 673 results! Business.

query = """
word word_etcbc~HWJ
"""

results = A.search(query)

A.table(results, fmt="text-trans-full", start=0, end=20)

# We can look for the *bare* occurrences of `HWJ`:
#
# * `word word_etcbc~^HWJ$` 42 occurrences, or simpler:
# * `word word_etcbc=HWJ` idem

# ## word containing several roots
#
# You can look for several roots at the same time, e.g. `HWJ` and `RHV`:
#
# * `word word_etcbc=HWJ|RHV` 54 occurrences
#
# If you want the non-bare occurrences also, we are helped by the fact that you can use `|` inside regular expressions as well:
#
# * `word word_etcbc~HWJ|RHV` 791 results
#
# We show results 4 and 5 here, not as table but in pretty display, by using the function `show()` instead of
# `table()`:

query = """
word word_etcbc~HWJ|RHV
"""

results = A.search(query)

A.show(results, fmt="text-trans-full", start=4, end=5)

# If you want all results in an Excel table, do this

A.export(results)

# Find it in your downloads folder:
#
# ![tsv](images/results.png)
#
# You can open it directly in Excel:
#
#
# ![xls](images/resultsx.png)
#
# See also the
# [documentation of export()](https://annotation.github.io/text-fabric/tf/advanced/display.html#tf.advanced.display.export)
#
# You can also make these exports directly from the TF browser:
#
# ![export](images/export.png)
#
# Look for a file with a name like `peshitta-default.zip` in your Downloads folder.
# In it is a file `resultsx.tsv` with the same content.
