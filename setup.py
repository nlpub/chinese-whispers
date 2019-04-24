from setuptools import setup
from setuptools.extension import Extension
from os import path

here = path.abspath(path.dirname(__file__))

try:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext
    print('Cython is installed, building extension.')
    USE_CYTHON=True
except ImportError:
    print('Cython is not installed, using pre-built C file if available.')

if USE_CYTHON:
    ext_modules=[
         Extension("chinese_whispers.cyt", ["cyt.pyx"], optional=True, extra_compile_args = ["-fopenmp" ], extra_link_args=['-fopenmp'])]
    cmdclass = {'build_ext': build_ext}
    opts = {"ext_modules": ext_modules, "cmdclass": cmdclass}
elif path.isfile(path.join(here, 'cyt.c')):
    print("Found pre-built C file")
    ext_modules = [Extension('chinese_whispers.cyt', ['cyt.c'])]
    cmdclass = {}
    opts = {"ext_modules": ext_modules, "cmdclass": cmdclass}
else:
    print("Pre-built C file is not available. Using pure Python implementation")
    opts = {}

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
      zip_safe=True,
      **opts)
