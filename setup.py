from setuptools import setup

setup(name='chinese-whispers',
      version='0.6.2',
      description='An implementation of the Chinese Whispers clustering algorithm.',
      url='https://github.com/nlpub/chinese-whispers-python',
      author='NLPub',
      license='MIT',
      packages=['chinese_whispers'],
      scripts=['bin/chinese-whispers'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ],
      install_requires=[
          'networkx >= 2.1,<3.0',
      ],
      zip_safe=True)
