import os.path
import re

from setuptools import setup


def get_package_variable(name, rel_path='chinese_whispers/__init__.py'):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), rel_path)

    pattern = re.compile(r'^{}.*?([\'"])(?P<value>.+)\1.*$'.format(re.escape(name)))

    with open(path, 'r', encoding='UTF-8') as f:
        for line in f:
            match = pattern.match(line)

            if match:
                return match.group('value')
        else:
            raise RuntimeError('Unable to find variable: ' + name)


__version__ = get_package_variable('__version__')
__license__ = get_package_variable('__license__')

with open('README.md', 'r', encoding='UTF-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='UTF-8') as f:
    install_requires = f.read()

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
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Typing :: Typed'
      ],
      keywords=['graph clustering', 'unsupervised learning', 'chinese whispers', 'cluster analysis'],
      install_requires=install_requires,
      zip_safe=True)
