from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[
    Extension("chinese_whispers.cyt",
              ["cyt.pyx"],
              optional=True,
              extra_compile_args = ["-fopenmp" ],
              extra_link_args=['-fopenmp'])]

setup(name='chinese-whispers',
      version='0.5',
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
          'Programming Language :: Python :: 3.6',],
      install_requires=['networkx'],
      cmdclass = {"build_ext": build_ext},
      ext_modules = ext_modules,
      zip_safe=True)
