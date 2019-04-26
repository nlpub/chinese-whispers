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
    USE_CYTHON = False
try:
    import numpy
    NUMPY_THERE = True
except ImportError:
    NUMPY_THERE = False
    print('Numpy is not installed, falling back to pure Python implementation')

if USE_CYTHON and NUMPY_THERE:
    ext_modules=[
         Extension("chinese_whispers.cyt", ["cyt.pyx"], 
                   include_dirs=[numpy.get_include()],
                   optional=True, 
                   extra_compile_args = ["-fopenmp" ], 
                   extra_link_args=['-fopenmp'])]
    cmdclass = {'build_ext': build_ext}
    install_requires=['networkx','scipy','numpy']
    opts = {"install_requires": install_requires, "ext_modules": ext_modules, "cmdclass": cmdclass}
elif path.isfile(path.join(here, 'cyt.c')) and NUMPY_THERE:
    print("Found pre-built C file")
    ext_modules = [Extension('chinese_whispers.cyt', ['cyt.c'], 
                             include_dirs=[numpy.get_include()]
                            )]
    install_requires=['networkx','scipy','numpy']
    cmdclass = {}
    opts = {"install_requires": install_requires, "ext_modules": ext_modules, "cmdclass": cmdclass}
else:
    print("Pre-built C file is not available. Using pure Python implementation")
    install_requires=['networkx']
    opts = {"install_requires": install_requires}

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
      zip_safe=True,
      **opts)
