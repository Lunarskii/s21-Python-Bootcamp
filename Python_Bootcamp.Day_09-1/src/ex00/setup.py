from distutils.core import setup, Extension


setup(
    name='calculator',
    version='0.1',
    description='Python interface for the calculator library',
    author='lunarskii',
    ext_modules=[Extension('calculator', ['calculator.c'])]
)
