from setuptools import setup

setup(name='chinese-whispers',
      version='0.4',
      description='An implementation of the Chinese Whispers clustering algorithm.',
      url='https://github.com/nlpub/chinese-whispers-python',
      author='Dmitry Ustalov, Alexander Panchenko',
      author_email='dmitry.ustalov@gmail.com',
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
          'networkx',
      ],
      zip_safe=True)
