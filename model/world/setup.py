from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension("world",
              sources=["world.pyx"],
              include_dirs=[numpy.get_include()],  # Add include directory for NumPy
              language="c++")
]

setup(
    name="WorldModule",
    ext_modules=cythonize(extensions)
)