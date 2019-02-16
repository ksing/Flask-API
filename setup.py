from distutils.core import Extension, setup
from Cython.Build import cythonize

ld = Extension(name="process_products_funcs", sources=["process_products.pyx"])

setup(ext_modules=cythonize([ld]))
