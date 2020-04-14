import codecs
import os.path

from setuptools import setup

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_package_var(name, rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith(name):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

init_path = "chinese_whispers/__init__.py"

__version__ = get_package_var("__version__", init_path)
__license__ = get_package_var("__license__", init_path)

with open('README.md', 'r', encoding='UTF-8') as f:
    long_description = f.read()

setup(name='chinese-whispers',
      version=__version__,
      description='An implementation of the Chinese Whispers clustering algorithm.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/nlpub/chinese-whispers-python',
      author='NLPub',
      maintainer='Dmitry Ustalov',
      license=__license__,
      packages=['chinese_whispers'],
      entry_points={'console_scripts': ['chinese-whispers = chinese_whispers.__main__:main']},
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
      ],
      keywords=['graph clustering', 'unsupervised learning', 'chinese whispers', 'cluster analysis'],
      install_requires=[
          'networkx >= 2.1,<3.0',
      ],
      zip_safe=True)
