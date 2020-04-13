from setuptools import setup

from chinese_whispers import __version__, __license__

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
