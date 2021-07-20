# nb_search.py [![Travis CI w/ Logo](https://img.shields.io/travis/loevlie/nb_search/master.svg?logo=travis)](https://travis-ci.com/loevlie/nb_search) [![Issues](https://img.shields.io/github/issues-raw/loevlie/nb_search.svg?maxAge=25000)](https://github.com/loevlie/nb_search/issues) [![GitHub pull requests](https://img.shields.io/github/issues-pr/loevlie/nb_search.svg?style=flat)]() [![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com) [![GitHub contributors](https://img.shields.io/github/contributors/loevlie/nb_search.svg?style=flat)]() [![PyPi Version](https://img.shields.io/pypi/v/nb-search.svg)](https://pypi.org/project/nb-search/)[![GitHub last commit](https://img.shields.io/github/last-commit/loevlie/nb_search.svg?style=flat)]()[![GitHub commit activity the past week, 4 weeks](https://img.shields.io/github/commit-activity/y/loevlie/nb_search.svg?style=flat)]()

Have you ever needed to find a old Jupyter Notebook file but forgot where you put it :grimacing: ?  Do you remember the packages you used :thinking: or maybe some of the terms you may have put in the markdown?  If so then this package will be a useful tool for you!  After learning the uses of this package you can even save valuable notebooks for later use by adding TODO tags.  This is all explained in detail below.  

### High Level Description

This is a package that can be used to search through jupyter notebooks at or below a specified directory.  There are many different ways to use the package to refine the search or visualize the notebooks.  I will go through most of them below.  

## Installing __nb_search__

```bash
$ pip install nb_search
``` 

## Uses

All of the uses below (except for fsearch) can be used in IPython console and in a Jupyter Notebook itself.  Using it in a Jupyter Notebook is straight forward.  To use it in a IPython console start by entering `%run nb_search.py` into the IPython console along with the optional arguments and directory (or list of files) you would like to search through.

### all

This is the most basic argument and does not allow any further arguments with it.  It simply searches the desired directory for all of the notebook files and displays them as clickable HTML links to the notebooks.  The syntax for using this is shown below:


* **IPython Console**
	```python3
	%run nb_search.py --all
	```


* **Jupyter Notebook**
	```python3
	from nb_search import search_files
	files = search_files('PATH_TO_DIRECTORY')
	```
	^^ You may simply run the function without any arguments.  This will recursively search through the current directory.  


### code 

This argument will allow you to search all of the code cells of the notebooks in your specified directory for a string given and will return the notebooks that have the string in one or more of their cells.  An example of using this to search for the variable "x" is shown below:


* **IPython Console**
	```python3
	%run nb_search.py --code '.' x
	```


* **Jupyter Notebook**
	```python3
	from nb_search import search_notebook
	files = search_notebook('x','code','PATH_TO_DIRECTORY')
	```


### markdown

This is the same concept as the code argument but in the markdown cells.  
An example of using this to search the markdown cells for the word "title" is shown below:

* **IPython Console**
	```python3
	%run nb_search.py --markdown '.' title
	```

* **Jupyter Notebook**
	```python3
	from nb_search import search_notebook
	files = search_notebook('title','markdown','PATH_TO_DIRECTORY')
	```


### heading

This is close to the markdown argument but instead of searching the entire markdown cell it only looks in the headings.  An example of using this to find the word "title" is shown below:


* **IPython Console**
	```python3
	%run nb_search.py --heading '.' title
	```


* **Jupyter Notebook**
	```python3
	from nb_search import search_heading
	files = search_heading('title','PATH_TO_DIRECTORY')
	```

### heading_pp

Once you have found a jupyter notebook you want to know more about but don't want to open yet you can use __heading_pp___ to get a pretty printed display of the headings in the file.  An example of how to do that is shown below:


* **IPython Console**
	```python3
	%run nb_search.py --heading_pp './notebook.ipynb'
	```

* **Jupyter Notebook**
	```python3
	from nb_search import heading_pprint
	files = heading_pprint('PATH_TO_DIRECTORY')
	```

### property

For my research groups HER project this is the most refined search.  You are able to search based on one to three things which must be seperated by an "and".  

1. Metal A - You can specify a metal to search the notebooks for.  
2. Metal B - You can specify a second metal you would like the search for. 
3. Max_H - You may specify the max Hydrogen to be below or above a certain value with the logical operators "<" and ">"

The order in which you enter the metals or even the Max_H does not matter as long as each specification is seperated by an "and".

Below are 2 examples of using the property argument.  The first is just to find any notebook with the metal Mo in it.  The second is to find any notebook with Mo and a Max_H of below 8.0 micromoles.

* **IPython Console**
	```python3
	%run nb_search.py --property '.' Mo
	```
	```python3
	%run nb_search.py --property '.' Mo and Max_H < 8.0
	```

* **Jupyter Notebook**
	```python3
	from nb_search import search_data
	files = search_data('Mo and Max_H < 8.0','PATH_TO_DIRECTORY')
	```

### todo

If you have a specific notebook you would like to tag as TODO then you can search for it with this.  You can also put an optional description and due date (in brackets) that will be displayed above the notebook link.  The syntax for this is shown below and can be put in any code cell in a notebook:

```python3
%TODO [YEAR-MONTH-DAY] Optional Description
```

The todo option is simple and only requires the user input the directory they would like to search through or '.' for the current one as shown below:


* **IPython Console**
	```python3
	%run nb_search.py --todo '.'
	```


* **Jupyter Notebook**
	```python3
	from nb_search import search_todo
	files = search_todo('PATH_TO_DIRECTORY')
	```

### fsearch

This is the exact same concept as the property option but can allow for more complicated queries of the three properties.  The user must input a function that returns True for the files he would like to view.  An example of the syntax of this function is shown below:

```python3
def f(NB):
    p1 = NB.property['Metal_A'] == 'Pt'
    p2 = NB.property['Metal_B'] == 'Pt'
    p3 = NB.property['Max_H'] > 47
    return (p1 or p2) and p3
```
	
Then the user can search for files in the current directory that have 'Pt' as either metal A or metal B, as well as, a max_H greater that 47 micromoles by using the function as shown below:

```python3
from nb_search import fsearch
files = fsearch(f,'.')
```


## Demonstration of Use

Most of the search functions output a list of the files that can then be used instead of a directory path to refine a search.  That capability along with the TODO search are shown below:

![gif](https://github.com/loevlie/nb_search/blob/master/nb_search.gif)
## Developing nb_search
To install nb_search, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```

