import sys
import os
from IPython.display import HTML, display
import nbformat
import argparse
import re
import pandas as pd

# HELPFUL FUNCTIONS

def search_util(root='.'):
    """Recursively find all ipynb files in a directory.
    root - This is the directory you would like to find the files in, defaults to cwd""" 
    nb_files = []
    for r, d, f in os.walk(root):
        for file in f:
            if file.endswith('.ipynb') and 'checkpoint.ipynb' not in file:
                nb_files += [os.path.join(r, file)]
    return nb_files

def show_files(nb_files):
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
    return nb_files
        
        
def search_notebook_util(pattern,cell_type,root='.'):
    """ This function searches all the markdown or code cells  
    in the notebooks in the directory and returns the notebooks
    that include the patter input in one or more of the markdown 
    or code cells"""

    files = search_util(root)
    file_list = []
    for file in files:
        nb = nbformat.read(file,as_version=4)
        for i in nb['cells']:
            if i['cell_type'] == cell_type:
                text = i['source']
                if pattern in text:
                    file_list.append(file)
                    break
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

def search_todo_util(root='.'):
    """ This function searches the properties cells of the HER notebooks for specific"""
        
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
    
# The Main Functions 

def search_files(root='.'):
    nb_files = search_util(root)
    show_files(nb_files)
    

def search_notebook(string_pattern,cell_type,root='.'):
        """ Cell_type can be 'code' or 'markdown' """
        nb_files = search_notebook_util(string_pattern,cell_type,root)
        show_files(nb_files)

def search_heading(pattern,root='.'):
    """ This function searches all the headings in the notebooks 
    in the directory and returns the notebooks that include the patter 
    input in one or more of the markdown cells"""
    nb_files = search_heading_util(pattern,root)
    show_files(nb_files)

def headings_pprint(file):
    """ This function produces an indented (based on heading level) "pretty print" of the headings in the file given """
    List = heading_list(file)
    pretty_print_headings(List)

def search_data(props,root='.'):
    """ This function searches all the headings in the notebooks 
    in the directory and returns the notebooks that include the patter 
    input in one or more of the markdown cells"""
    nb_files = search_data_util(props,root)
    show_files(nb_files)
        
def search_todo(tag='TODO',root='.'):
    """ This function searches all the code cells in the notebooks 
    in the directory and returns the notebooks descriptions and due dates of the notebooks that include the todo tag in one or more of the code cells"""
    nb_files,nb_tags = search_todo_util(root)
    count = show_files_tags(nb_files,nb_tags,tag)
    return count
        
if __name__ == '__main__':
    
    # Collecting the Command Line Inputs

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