from setuptools import setup,find_packages

with open("README.md","r") as fh:
    long_description = fh.read()

setup(name='nb_search',
      version='1.0.0',
      description='Module for searching through Jupyter Notebooks in a provided directory',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Dennis Loevlie',
      author_email='loevliedenny@gmail.com',
      py_modules=["nb_search"],
      install_requires=['IPython', 'matplotlib', 'numpy', 'nbformat', 'pandas'],
      extras_require = {
          "dev": [
              "pytest",
          ],
      },
    )
