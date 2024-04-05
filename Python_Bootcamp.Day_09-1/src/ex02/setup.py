from setuptools import setup
from Cython.Build import cythonize


setup(
    name='cython_mul',
    ext_modules=cythonize("multiply.pyx")
)
