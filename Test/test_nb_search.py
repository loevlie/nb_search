from nb_search import search_todo_util, search_notebook_util, search_heading_util, heading_list, search_data_util, search_todo_util

def test_todo():
    file_list, tag_list = search_todo_util();
    assert len(file_list) == 3 and len(tag_list) == 3

def test_markdown_search():
    file_list = search_notebook_util('Loevlie','markdown')
    assert len(file_list) == 3
    
def test_code_search():
    file_list = search_notebook_util('espyranto','code')
    assert len(file_list) == 2
    
def test_heading_search():
    file_list = search_heading_util('Loevlie')
    assert len(file_list) == 2
    
def test_property1():
    file_list_Au = search_data_util(['Au'])
    file_list_Ga_Au = search_data_util(['Ga','Au'])
    file_list_Au_Hy = search_data_util(['Au','H_max < 30.0'])
    assert len(file_list_Au) == 2
    assert len(file_list_Ga_Au) == 1
    assert len(file_list_Au_Hy) == 1

def test_property2():
    file_list_Ga_Au = search_data_util(['Ga','Au'])
    assert len(file_list_Ga_Au) == 1

def test_property3():
    file_list_Au_Hy = search_data_util(['Au','H_max < 30.0'])
    assert len(file_list_Au_Hy) == 1
    