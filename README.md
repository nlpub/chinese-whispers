# Chinese Whispers for Python

This is an implementation of the [Chinese Whispers](https://dl.acm.org/citation.cfm?id=1654774) clustering algorithm in Python. Since this library is based on [NetworkX](https://networkx.github.io/), it is simple to use.

[![Build Status][travis_ci_badge]][travis_ci_link] [![PyPI version][pypi_badge]][pypi_link]

[pypi_badge]: https://badge.fury.io/py/chinese-whispers.svg
[pypi_link]: https://pypi.python.org/pypi/chinese-whispers
[travis_ci_badge]: https://travis-ci.org/nlpub/chinese-whispers-python.svg
[travis_ci_link]: https://travis-ci.org/nlpub/chinese-whispers-python

Given a NetworkX graph `G`, this library can [cluster](https://en.wikipedia.org/wiki/Cluster_analysis) it using the following code:

```python
from chinese_whispers import chinese_whispers
chinese_whispers(G, weighting='top', iterations=20)
```

As the result, each node of the input graph is provided with the `label` attribute that stores the cluster label.

More usage examples are available in the [sample notebook](samples.ipynb).

In case you require higher performance, please consider our Java implementation that also includes other graph clustering algorithms: <https://github.com/nlpub/watset-java>.



## EDIT

Added a [Cython](https://cython.org/) version of the module. 

This allows for performance gains.
It is often 10 to 20 times faster than the pure Python implementation, especially for very large graphs (more than 10 000 nodes, up to millions of edges). Still, about 70% of the computing time is spent on copying the Networkx Graph to C arrays. This means that the more iterations you run, the faster it will be compared to the pure Python implementation.

This is a beta version, which currently supports unweighted and weighted graphs, but only the 'top' algorithm from the original implementation.


To run, do:
```
python3 setup.py install
```
Please note that the Cython implementation also requires numpy and scipy to work. Currently, setup.py doesn't check for this, but you can verify everything works by importing the module in Python:
```python
import chinese_whispers
chinese_whispers.cyt.chinese_whispers(G, it=20, weighted=False, threads=1)
```
where `G` is a Networkx Graph and 20 is the number of iterations. You can switch multi-threading on by changing the `threads` argument. If it has worked, you will see this message:
```
        Successfully imported Cython modules. You can use both implementations: pure Python and Cython

        For pure Python run: chinese_whispers.chinese_whispers(G, weighting='top', iterations=20, seed=None)

        For Cython run: chinese_whispers.cyt.chinese_whispers(G, iterations=20, weighted=False, draw=False, threads=1)
```
Otherwise, you will see this message:
```
    Could not import Cython modules, using pure Python implementation
```

Comments are welcomed, I hope the original developers appreciate the contribution.
