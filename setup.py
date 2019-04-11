from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[
    Extension("chinese_whispers_cython",
              ["chinese-whispers-cython.pyx"],
              extra_compile_args = ["-fopenmp" ],
              extra_link_args=['-fopenmp']
              ) 
]

setup( 
  name = "chinese-whispers-cython",
  version = "0.2",
  description = "An implementation of the Chinese Whispers clustering algorithm in Cython, for better performance",
  install_requires = ["networkx", "scipy", "numpy", "cython"],
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)
