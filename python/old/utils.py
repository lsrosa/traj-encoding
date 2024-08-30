from bibkeys import get_entry
from termcolor import colored

def sections_in_chapters(chapters, sections, keys):
    # None indicated chapter wise lists, so it should not print the sections
    ret = dict()
    if sections == None:
        for chapter in chapters:
            ret[chapter] = None
    else:
        for chapter in chapters:
            in_chap = set(keys[chapter]['sections']).intersection(sections)
            if len(in_chap) != 0:
                ret[chapter] = list(in_chap)
            else:
                ret[chapter] = None 
                #ret[chapter] = list(keys[chapter]['sections'].keys()) 
    return ret

def compare_sets(a, b):
    '''
    Get intersection, list of elements in A which are not in B, and vice versa
    '''
    a_ = set(a)
    b_ = set(b)

    intersec = a_.intersection(b_)
    a_not_in_b = a_.difference(b_)
    b_not_in_a = b_.difference(a_)

    return list(intersec), list(a_not_in_b), list(b_not_in_a)

def print_list(db, l):
    if type(l) != list: raise ValueError('input should be a list') 
    l.sort()
    for paper in l:
        entry = get_entry(db, paper, False)

        if entry == None:
            print(colored('         - ERROR: This paper is not in the biblio.bib file: %s\n' % paper, 'red'))
        else:
            print(colored('         - %s' % entry['title'], 'yellow'))
            print('              Authors: %s' % entry['author'])
            print('              Year: %s' % entry['year'])
            print('              key: %s\n' % paper)
