Chinese Whispers for Python
===========================

This is an implementation of the `Chinese Whispers`_ clustering
algorithm in Python. Since this library is based on `NetworkX`_, it is
simple to use.

|Unit Tests| |Read the Docs| |PyPI Version|

Given a NetworkX graph ``G``, this library can `cluster`_ it using the
following code:

.. code:: python

   from chinese_whispers import chinese_whispers
   chinese_whispers(G, weighting='top', iterations=20)

As the result, each node of the input graph is provided with the
``label`` attribute that stores the cluster label.

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

A more complete usage example is available in the `example notebook`_
and at https://nlpub.github.io/chinese-whispers-python/.

In case you require higher performance, please consider our Java
implementation that also includes other graph clustering algorithms:
https://github.com/nlpub/watset-java.

.. _Chinese Whispers: https://doi.org/10.3115/1654758.1654774
.. _NetworkX: https://networkx.github.io/
.. _cluster: https://en.wikipedia.org/wiki/Cluster_analysis
.. _example notebook: example.ipynb

.. |Unit Tests| image:: https://github.com/nlpub/chinese-whispers-python/workflows/Unit%20Tests/badge.svg?branch=master
   :target: https://github.com/nlpub/chinese-whispers-python/actions?query=workflow%3A%22Unit+Tests%22
.. |Read the Docs| image:: https://readthedocs.org/projects/chinese-whispers/badge/?version=latest
   :target: https://chinese-whispers.readthedocs.io/en/latest/?badge=latest
.. |PyPI Version| image:: https://badge.fury.io/py/chinese-whispers.svg
   :target: https://pypi.python.org/pypi/chinese-whispers