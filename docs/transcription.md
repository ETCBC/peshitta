<img src="images/etcbc.png" align="right"/>
<img src="images/tf.png" align="right"/>

Feature documentation
=====================

Here you find a description of the transcriptions of the Peshitta corpus, the
Text-Fabric model in general, and the node types, features and edges for the
Peshitta corpus in particular.

See also [about](about.md) [text-fabric](textfabric.md)

Conversion from ETCBC/WIT to TF
---------------------------------

Below is an account how we transform ETCBC/WIT transcriptions into
[Text-Fabric](https://dans-labs.github.io/text-fabric/) format by means of
[tfFromPil.py](../programs/tfFromPil.py).

The Text-Fabric model views the text as a series of atomic units, called
*slots*. In this corpus *words* are the slots.
In this version, we are naïve about words: they are what you get if you split
a transcription line on white space. We have not yet made an attempt to split
enclitics off.

On top of that, more complex textual objects can be represented as *nodes*. In
this corpus we have node types for: *word*, *verse*,
*chapter*, and *book*.

The type of every node is given by the feature
[**otype**](https://dans-labs.github.io/text-fabric/Api/General/#node-features).
Every node is linked to a subset of slots by
[**oslots**](https://dans-labs.github.io/text-fabric/Api/General/#edge-features).

Nodes can be related by means of edges.

Nodes and edges can be annotated with features. See the table below.

Text-Fabric supports three customizable section levels. In this corpus they are
*book*, *chapter*, *verse*.

Other docs
----------

[Text-Fabric API](https://dans-labs.github.io/text-fabric/Api/General/)

[Peshitta API](https://dans-labs.github.io/text-fabric/Api/Peshitta/)

Reference table of features
===========================

*(Keep this under your pillow)*

Node type *word*
-------------------------

Basic unit of text. They are separated by spaces and/or punctuation.
We have not yet split off enclitics from words, so words contain their enclitics,
and there is no marking of enclitics.

There is not yet a lemma feature for words. The surface representation of words
is all we got.

feature | values |  description
------- | ------ | ------
**word** | `ܒܪܫܝܬ` | the text of a word as UNICODE string
**trailer** | `.` | after-word material until the next word, as UNICODE string
**word etcbc** | `BRCJT` | the text of a word in ETCBC/WIT transliteration
**trailer etcbc** | `.` | after-word material until the next word, in ETCBC/WIT transliteration

Node type *verse*
-------------------------

Subdivision of a containing *chapter*. 

feature | values | description
------- | ------ | ------
**verse** | `1` | number of the *verse*

Node type *chapter*
-----------------------------

Subdivision of a containing *book*.

feature | values | in ATF | description
------- | ------ | ------
**chapter** | `1` | number of the *chapter*

Node type *book*
-----------------------------

The main entity of which the corpus is composed, representing the transcription
of a complete book.

Some books come in several witnesses, marked as `A`, `B`. 
We treat them as separate books, and augment their names and acronyms with `_A`, `_B`, etc.

feature | values | in ATF | description
------- | ------ | ------
**book** | `Gn` | acronym of the book name
**book@en** | `Genesis` | English name of the book

