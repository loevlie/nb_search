# nb_search.py 

This is a command line function that can be used to search through jupyter notebooks at or below a specified directory.  There are different ways to use the function to refine the search or visualize the notebooks.  I will go through them each below.  

## Uses

All of the uses below require the user to start by entering `%run nb_search.py` into the IPython console and then the optional arguments.  I will explain based off of the different options arguments to nb_search.

### all

This is the most basic argument and does not allow any further arguments with it.  It simply searches the desired directory for all of the notebook files and displays them as clickable HTML links to the notebooks.  The syntax for using this is shown below:

`%run nb_search.py --all`

### code 

This argument will allow you to search all of the code cells of the notebooks in your specified directory for a string given and will return the notebooks that have the string in one or more of their cells.  An example of using this to search for the variable "x" is shown below:

`%run nb_search.py --code '.' x`

### markdown

This is the same concept as the code argument but in the markdown cells.  
An example of using this to search the markdown cells for the word "title" is shown below:

`%run nb_search.py --markdown '.' title`

### heading

This is close to the markdown argument but instead of searching the entire markdown cell it only looks in the headings.  An example of using this to find the word "title" is shown below:

`%run nb_search.py --heading '.' title`

### heading_pp

Once you have found a jupyter notebook you want to know more about but don't want to open yet you can use __heading_pp___ to get a pretty printed display of the headings in the file.  An example of how to do that is shown below:

`%run nb_search.py --heading_pp './notebook.ipynb'`

### property

For my research groups HER project this is the most refined search.  You are able to search based on one to three things which must be seperated by an "and".  

1. Metal A - You can specify a metal to search the notebooks for.  
2. Metal B - You can specify a second metal you would like the search for. 
3. Max_H - You may specify the max Hydrogen to be below or above a certain value with the logical operators "<" and ">"

The order in which you enter the metals or even the Max_H does not matter as long as each specification is seperated by an "and".

Below are 2 examples of using the property argument.  The first is just to find any notebook with the metal Mo in it.  The second is to find any notebook with Mo and a Max_H of below 8.0 micromoles.

1. `%run nb_search.py --property '.' Mo`
2. `%run nb_search.py --property '.' Mo and Max_H < 8.0`

### todo

If you have a specific notebook you would like to tag as TODO then you can search for it with this.  You can also put an optional description that will be displayed above the notebook link.  The syntax for this is shown below and can be put in any code cell in a notebook:

`%TODO Optional Description`

The todo option is simple and only requires the user input the directory they would like to search through or '.' for the current one as shown below:

`%run nb_search.py --todo '.'`

