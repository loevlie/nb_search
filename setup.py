from setuptools import setup,find_packages

setup(name='nb_search',
      version='0.1.1',
      description='Module for searching through Jupyter Notebooks in a provided directory',
      author='Dennis Loevlie',
      author_email='loevliedenny@gmail.com',
      #packages=['nb_search'],
      packages=find_packages(include=['nb_search','nb_search.*']),
      install_requires=['IPython', 'matplotlib', 'numpy', 'nbformat', 'pandas'],
    )
