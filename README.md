# Chinese Whispers for Python

This is an implementation of Chinese Whispers in Python based on the NetworkX graph structures. 

[![PyPI version][pypi_badge]][pypi_link] [![Build Status][travis_ci_badge]][travis_ci_link]

[pypi_badge]: https://badge.fury.io/py/chinese-whispers.svg
[pypi_link]: https://pypi.python.org/pypi/chinese-whispers
[travis_ci_badge]: https://travis-ci.org/nlpub/chinese-whispers-python.svg
[travis_ci_link]: https://travis-ci.org/nlpub/chinese-whispers-python

To cluster a graph G represented in a networkx format use the following code:

```python
from chinese_whispers import chinese_whispers
chinese_whispers(G, weighting="top", iterations=20)
```

The clustering results are saved in the "label" attribute of each node.

More usage examples are available in the [sample notebook](samples.ipynb).
