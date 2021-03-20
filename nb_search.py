import sys
import os
from IPython.display import HTML, display
import nbformat
import argparse
import re
import pandas as pd
from multiprocessing.dummy import Pool  # This is a thread-based Pool

# HELPFUL FUNCTIONS


def search_util(root='.'):
    """  Recursively find all ipynb files in a directory.
    root - This is the directory you would like to find the files in, defaults to cwd

    Args:
        root (str, optional): The directory you would like to recursively search through. Defaults to '.'.

    Returns:
        list: All Jupyter notebook files under the directory specified
    """
    nb_files = []
    if isinstance(root, list): 
        for file in root:
            if file.endswith('.ipynb') and 'checkpoint.ipynb' not in file:
                nb_files += [file]
    else:
        for r, d, f in os.walk(root):
            for file in f:
                if file.endswith('.ipynb') and 'checkpoint.ipynb' not in file:
                    nb_files += [os.path.join(r, file)]
    return nb_files


def show_files(nb_files):
    """Displays the final list of Jupyter notebook files

    Args:
        nb_files (list): List of queried Jupyter notebook files
    """
    if len(nb_files) == 0:
        nb_files = nb_files
    else:
        if list(nb_files)[0].startswith('/content/drive'):
            from subprocess import getoutput
            nb_files = list(nb_files)
            fids = [getoutput(f"xattr -p 'user.drive.id' '{nbf}' ") for nbf in nb_files]
            for fid,nbf in zip(fids, nb_files):
                display(HTML(f"<a href=https://colab.research.google.com/drive/{fid} target=_blank>{os.path.split(nbf)[-1]}</a>"))
        else:
            [display(HTML(f'<a href="{f}">{f}</a>')) for f in nb_files]
    

def show_files_tags(nb_files,nb_tags,tag): # [due date (datetime)] optional description
    count = 0
    for i,f in enumerate(nb_files):
        if tag in nb_tags[i][1:].strip():
            if '[' in nb_tags[i]:
                m = re.search("[^[]*\[([^]]*)\]", nb_tags[i])
                ss = ''.join(nb_tags[i].split('['+m.groups(1)[0] + ']'))
                description = ''.join(ss.split('%TODO')).strip()
                due_date = pd.to_datetime([m.groups(1)[0]])
                df = pd.DataFrame({'Date':due_date})
                df['diff'] = df - pd.Timestamp.now().normalize() 
                due_days = df['diff'][0].days
                if due_days >= 0:
                    print(description + color.BOLD + color.GREEN + ' (Due in: ' + str(due_days) + ' days)' + color.END)
                    display(HTML(f'<a href="{f}">{f}</a>'))
                else:
                    print(description + color.BOLD + color.RED + ' (Past due by: ' + str(abs(due_days)) + ' days)' + color.END)
                    display(HTML(f'<a href="{f}">{f}</a>'))
            else:
                print(nb_tags[i])
                display(HTML(f'<a href="{f}">{f}</a>'))
        
        
def search_notebook_util(pattern,cell_type,root='.'):
    """ This function searches all the markdown or code cells  
    in the notebooks in the directory and returns the notebooks
    that include the patter input in one or more of the markdown 
    or code cells"""
    
    files = search_util(root)
    global file_list
    file_list = []
    def search_through_files(file):
        global file_list
        Worked = True
        try:
            nb = nbformat.read(file,as_version=4)
        except:
            Worked = False
        
        if Worked:
            for i in nb['cells']:
                if i['cell_type'] == cell_type:
                    text = i['source']
                    if pattern in text:
                        file_list.append(file)
                        break
        else:
            Worked = True
    

    # If there are a ton of files the code could benifit from Parallelization
    if len(files)>500:
        CPU_Amount = os.cpu_count() // 2 # A safe number of usable CPU's
        with Pool(CPU_Amount) as p:
            p.map(search_through_files,files)
    else:
        for file in files:
            search_through_files(file)
    
    return file_list

def search_heading_util(pattern,root='.'):

    files = search_util(root)
    file_list = []
    for file in files:
        nb = nbformat.read(file,as_version=4)
        for i in nb['cells']:
            if i['cell_type'] == 'markdown':
                text = i['source']
                for i in text.split('\n'):
                    try:
                        if i.strip()[0] == '#' and pattern in i:
                            file_list.append(file)
                            break
                    except:
                        None
    return set(file_list)

def heading_list(file):
    """ This function searches all the headings in the notebooks 
    in the directory and returns the notebooks that include the patter 
    input in one or more of the markdown cells"""

    heading_list = []

    nb = nbformat.read(file,as_version=4)
    for i in nb['cells']:
        if i['cell_type'] == 'markdown':
            text = i['source']
            for i in text.split('\n'):
                try:
                    if i.strip()[0] == '#':
                        heading_list.append(i.strip())
                except:
                    None
    return heading_list

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def pretty_print_headings(heading_list):
    for i in heading_list:
        heading_level = len(i.strip().split()[0])
        print(color.BOLD + color.GREEN + '\t'*(heading_level-1) + f'{i.strip()[heading_level+1:]}\n' + color.END)

def search_data_util(props,root='.'):
    """ This function searches the properties cells of the HER notebooks for specific"""

    requirements = len(props)

    files = search_util(root)
    file_list = []
    for file in files:
        nb = nbformat.read(file,as_version=4)
        for i in nb['cells']:
            if i['cell_type'] == 'code':
                if i['source'].startswith('%%properties'):
                    Metal_A = i['source'].split('\n')[1].split()[-1]
                    Metal_B = i['source'].split('\n')[2].split()[-1]
                    Max_H = float(i['source'].split('\n')[3].split()[-1])
                    require = 0
                    for prop in props:
                        if '<' in prop:
                            if Max_H < float(prop.split('<')[-1].strip()):
                                require += 1
                        elif '>' in prop:
                            if Max_H > float(prop.split('>')[-1].strip()):
                                require += 1
                        else: # Assumed the user entered a metal name
                            if prop.upper() == Metal_A.upper() or prop.upper() == Metal_B.upper():
                                require += 1
                    if require == requirements:
                        file_list.append(file)
                        break
    return file_list

def Get_props(file):
    """ This function retreives the information from the property cell of the notebook"""
    no_prop = True
    nb = nbformat.read(file,as_version=4)
    for i in nb['cells']:
        if i['cell_type'] == 'code':
            if i['source'].startswith('%%properties'):
                Metal_A = i['source'].split('\n')[1].split()[-1]
                Metal_B = i['source'].split('\n')[2].split()[-1]
                Max_H = float(i['source'].split('\n')[3].split()[-1])
                result = {'Metal_A':Metal_A,'Metal_B':Metal_B,'Max_H':Max_H}
                no_prop = False
    if no_prop:
        result = None
    
    return result

def search_todo_util(root='.'):
    """ This function searches the properties cells of the HER notebooks for TODO tags"""
        
    files = search_util(root)
    file_list = []
    tag_list = []
    for file in files:
        nb = nbformat.read(file,as_version=4)
        for i in nb['cells']:
            if file in file_list:
                break
            if i['cell_type'] == 'code':
                for line in i['source'].split('\n'):
                    if line.startswith('%TODO') and '%%properties' not in line and '%matplotlib' not in line:
                        tag_list.append(line)
                        file_list.append(file)
                        break
    return file_list,tag_list

class NB: 
    def __init__(self,filename):
        self.filename = filename
        self.property = Get_props(filename)

def fsearch_util(f,root='.'):
    files = search_util(root)
    file_list = []
    for file in files:
        nb = NB(file)
        if nb.property != None:
            if f(nb):
                file_list.append(file)
    return file_list
    
# The Main Functions 

def search_files(root='.'):
    """Displays all Jupyter Notebook files as clickable links under the specified directory

    Args:
        root (str, optional): The directory you would like to recursively search through. Defaults to '.'.

    Returns:
        list: A list of the Jupyter Notebook files that are also displayed as clickable links
    """
    nb_files = search_util(root)
    show_files(nb_files)
    return nb_files
    

def search_notebook(string_pattern,cell_type,root='.'):
    """ Displays all Jupyter Notebook files as clickable links under the specified directory after
        searching through the files for the string pattern in either the code or makedown cells.  

    Args:
        string_pattern (str): The pattern you are searching for in the Jupyter notebooks
        cell_type (str): 'code' or 'markdown' 
        root (str, optional): The directory you would like to recursively search through. Defaults to '.'.

    Returns:
        list: A list of the Jupyter Notebook files that are also displayed as clickable links
    """
    nb_files = search_notebook_util(string_pattern,cell_type,root)
    show_files(nb_files)
    return nb_files

def search_heading(pattern,root='.'):
    """ Displays all Jupyter Notebook files as clickable links under the specified directory after
        searching through the files for the string pattern in the headings.
    Args:
        pattern (str): The pattern you are searching for in the Jupyter notebooks
        root (str, optional): The directory you would like to recursively search through. Defaults to '.'.

    Returns:
        list: A list of the Jupyter Notebook files that are also displayed as clickable links
    """
    nb_files = search_heading_util(pattern,root)
    show_files(nb_files)
    return nb_files

def headings_pprint(file):
    """Produces an indented (based on heading level) "pretty print" of the headings in the file

    Args:
        file (str): The path to the file that you would like to have it's headings pretty printed.
    """
    List = heading_list(file)
    pretty_print_headings(List)

def search_data(props,root='.'):
    """ Displays all Jupyter Notebook files as clickable links under the specified directory after
        searching through the files for the properties specified.   

    Args:
        props (str): The properties you are trying to filter based on.  Can only have and logical operator to query on any combination of two metals and the max_H 
            Ex: 'Au and max_H > 2', Ex: 'Au and Pd and max_H < 30'
        root (str, optional): The directory you would like to recursively search through. Defaults to '.'.

    Returns:
        list: A list of the Jupyter Notebook files that are also displayed as clickable links
    """
    if isinstance(props,list):
        None
    else:
        x = props
        if 'and' in x:
            props1 = x.split('and')
            props = [i.strip() for i in props1]
        else:
            props = [x]
    nb_files = search_data_util(props,root)
    show_files(nb_files)
    return nb_files
        
def search_todo(root='.'):
    """ This function searches all the code cells in the Jupyter Notebooks under the specified the directory and returns 
        the notebooks descriptions and due dates of the notebooks that include a "todo tag" in one or more of the code cells
        a TODO tag may be placed in any code cell at any line with an optional due data and description using the following syntax:

        %TODO [YEAR-MONTH-DAY] Optional Description

    Args:
        root (str, optional): The directory you would like to recursively search through. Defaults to '.'.

    Returns:
        list: All the files that contained TODO tags
    """
    tag='TODO'
    nb_files,nb_tags = search_todo_util(root)
    count = show_files_tags(nb_files,nb_tags,tag)
    return nb_files
        
def fsearch(f,root = '.'):
    """A similar function to search_todo but allows for more advanced querying by taking advantage of pythons built in parser.  
       Ex:
            def f(NB):
                p1 = NB.property['Metal_A'] == 'Pt'
                p2 = NB.property['Metal_B'] == 'Pt'
                p3 = NB.property['Max_H'] > 47
                return (p1 or p2) and p3

    Args:
        f (func): A function where the output is boolean and determines if a notebook should be returned.  The input is a notebook object with a .property attribute that acts as a dictionary with three keys: 'Metal_A', 'Metal_B', and 'Max_H'.
        root (str, optional): The directory you would like to recursively search through. Defaults to '.'.

    Returns:
        list: A list of the Jupyter Notebook files that are also displayed as clickable links
    """
    nb_files = fsearch_util(f,root)
    show_files(nb_files)
    return nb_files

if __name__ == '__main__':
    
    # Collecting the Command Line Inputs
    start = time.time() # For checking how long the script takes

    parser = argparse.ArgumentParser(description='Search Jupyter Notebooks')

    parser.add_argument('--all', nargs='?', const='.')
    parser.add_argument('--markdown',nargs='+')
    parser.add_argument('--code',nargs='+')
    parser.add_argument('--heading',nargs='+')
    parser.add_argument('--heading_pp',nargs='+')
    parser.add_argument('--property',nargs='+')
    parser.add_argument('--todo',nargs='+')
    args = parser.parse_args()

    if args.all: # If you selected "all" you want a list of all of the files in the directory 
        root = args.all # If a root is not given the root is assumed to be the current dir.
        
    if args.markdown:
        root = args.markdown[0]
        string_pattern = args.markdown[1:]
    
    if args.code:
        root = args.code[0]
        string_pattern = args.code[1:]
    
    if args.heading:
        root = args.heading[0]
        string_pattern = args.heading[1:]
    
    if args.heading_pp:
        file_name = args.heading_pp[0]
    
    if args.property:
        root = args.property[0]
        x = ''.join(args.property[1:])
        if 'and' in x:
            List_of_desired_props = x.split('and')
        else:
            List_of_desired_props = [args.property[1]]
            
    if args.todo:
        if len(args.todo) == 1:
            root = args.todo[0]
            tag = 'TODO'
      
    # --------------------------------------------------------------------------------
    if args.all: # If you selected "all" you want a list of all of the files in the directory 
        search_files(root)
    elif args.code: 
        search_notebook(string_pattern[0],'code',root)
    elif args.markdown:
        search_notebook(string_pattern[0],'markdown',root)
    elif args.heading:
        search_heading(string_pattern[0],root)
    elif args.heading_pp:
        headings_pprint(file_name)
    elif args.property:
        search_data(List_of_desired_props,root)
    elif args.todo:
        search_todo(tag,root)
    
    
