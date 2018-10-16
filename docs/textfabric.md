<img src="images/tf-small.png" align="right" width="20%"/>
<img src="images/dans.png" align="right" width="20%"/>

Text-Fabric
===========

[Text-Fabric](https://github.com/Dans-labs/text-fabric) is a model for textual
data with annotations that is optimized for efficient data analysis. Not only
that, it also facilitates the creation of new, derived data, which can be added
to the original data. Data combination is a feature of Text-Fabric.

Text-Fabric is being used for the [Hebrew Bible](https://github.com/ETCBC/bhsa)
and a large body of linguisitic annotations on top of it. The researchers of the
[ETCBC](http://etcbc.nl) thought that a plain database is not a satisfactory
text model, and that XML is too limited too express multiple hierarchies in a
text smoothly.

That's why they adopted a model by
[Doedens](http://books.google.nl/books?id=9ggOBRz1dO4C) that reflects more of
the essential properties of text (sequence, embedding). This model is the basis
of MQL, a working text-database system. Text-Fabric is based on the same
[model](https://dans-labs.github.io/text-fabric/Model/Data-Model/), and once the
data is in Text-Fabric, it can be exported to MQL.

See more on the effort of modeling the Hebrew Bible in Dirk's article
[The Hebrew Bible as Data: Laboratory - Sharing - Experiences](https://doi.org/10.5334/bbi.18)

With data in Text-Fabric, it becomes possible to build rich online interfaces on
the data of ancient texts. For the Hebrew Bible, we have built
[SHEBANQ](https://shebanq.ancient-data.org).

Working with TF is a bit like buying from IKEA. You get your product in bits and
pieces, and you assemble it yourself. TF decomposes any dataset into its
components, nicely stacked per component, with every component uniquely labeled.
You go to the store, make your selection, enter the warehouse, collect your
parts, and, at home, assemble your product.

In order to enjoy an IKEA product, you do not need to be a craftsman, but you do
need to be able to handle a screw driver.

In the TF world, it is the same. You do not have to be a professional
programmer, but you do need to be able to program little things. A first course
in Python is enough.

Another parallel: in IKEA you take a package with components home, and there you
assemble it. In TF it is likewise: you download the TF data, and then you write
a little program. Inside that program you can call up the Text-Fabric tool,
which act as the IKEA user manual. But your program takes control, not
Text-Fabric.

The best environment to enjoy Text-Fabric is in Python programs that you develop
in a [Jupyter Notebook](http://jupyter.readthedocs.io/en/latest/). This tutorial
is such a notebook. If you are reading it online, you see text bits and code
bits, but you cannot execute the code bits.

Chances are that a bit of reading about the underlying
[data model](https://dans-labs.github.io/text-fabric/Model/Data-Model/) helps you
to follow the exercises below, and vice versa.

Start
[here](http://nbviewer.jupyter.org/github/etcbc/peshitta/blob/master/tutorial/start.ipynb).

