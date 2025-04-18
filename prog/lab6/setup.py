from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("cy_factorization.pyx", annotate=True, language_level=3),
) 