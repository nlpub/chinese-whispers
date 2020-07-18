Chinese Whispers for Python
===========================

This is an implementation of the `Chinese Whispers`_ clustering
algorithm in Python. Since this library is based on `NetworkX`_, it is
simple to use.

.. _Chinese Whispers: https://doi.org/10.3115/1654758.1654774
.. _NetworkX: https://networkx.github.io/

|Unit Tests| |Read the Docs| |PyPI Version|

.. |Unit Tests| image:: https://github.com/nlpub/chinese-whispers-python/workflows/Unit%20Tests/badge.svg?branch=master
   :target: https://github.com/nlpub/chinese-whispers-python/actions?query=workflow%3A%22Unit+Tests%22
.. |Read the Docs| image:: https://readthedocs.org/projects/chinese-whispers/badge/?version=latest
   :target: https://chinese-whispers.readthedocs.io/en/latest/?badge=latest
.. |PyPI Version| image:: https://badge.fury.io/py/chinese-whispers.svg
   :target: https://pypi.python.org/pypi/chinese-whispers

* :ref:`modindex`
* :ref:`search`

Usage
-----

Given a NetworkX graph ``G``, this library can `cluster`_ it using the
following code:

.. code:: python

   from chinese_whispers import chinese_whispers
   chinese_whispers(G, weighting='top', iterations=20)

As the result, each node of the input graph is provided with the
``label`` attribute that stores the cluster label.

.. _cluster: https://en.wikipedia.org/wiki/Cluster_analysis

The library also offers a convenient command-line interface (CLI) for
clustering graphs represented in the ABC tab-separated format
(source\ ``\t``\ target\ ``\t``\ weight).

.. code:: shell

   # Write karate_club.tsv (just as example)
   python3 -c 'import networkx as nx; nx.write_weighted_edgelist(nx.karate_club_graph(), "karate_club.tsv", delimiter="\t")'

   # Using as CLI
   chinese-whispers karate_club.tsv

   # Using as module (same CLI as above)
   python3 -mchinese_whispers karate_club.tsv

Miscellaneous
-------------

A more complete usage example is available in the `example notebook`_
and at https://nlpub.github.io/chinese-whispers-python/.

In case you require higher performance, please consider our Java
implementation that also includes other graph clustering algorithms:
https://github.com/nlpub/watset-java.

.. _example notebook: https://github.com/nlpub/chinese-whispers-python/blob/master/example.ipynb

Citation
--------

-  Ustalov, D., Panchenko, A., Biemann, C., Ponzetto, S.P.: `Watset:
   Local-Global Graph Clustering with Applications in Sense and Frame
   Induction`_. Computational Linguistics 45(3), 423–479 (2019)

.. code:: bibtex

   @article{Ustalov:19:cl,
     author    = {Ustalov, Dmitry and Panchenko, Alexander and Biemann, Chris and Ponzetto, Simone Paolo},
     title     = {{Watset: Local-Global Graph Clustering with Applications in Sense and Frame Induction}},
     journal   = {Computational Linguistics},
     year      = {2019},
     volume    = {45},
     number    = {3},
     pages     = {423--479},
     doi       = {10.1162/COLI_a_00354},
     publisher = {MIT Press},
     issn      = {0891-2017},
     language  = {english},
   }

.. _`Watset: Local-Global Graph Clustering with Applications in Sense and Frame Induction`: https://doi.org/10.1162/COLI_a_00354
