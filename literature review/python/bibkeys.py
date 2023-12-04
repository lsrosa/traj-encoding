import bibtexparser
import os
from pathlib import Path
import regex as re

'''
    Reads the tex files and saves the citations for each chapter/section
    Also save \sanity comments, which can be used to flag specific papers

Output format:
    (dict) keys{
        (str) chapter_title : (dict) {
            (list) keys
            (list) sanity
            (dict) sanity_sections {
                (str) section_name : (list) keys
            }
            (dict) sections {
                (str) section_name : (list) keys
            }
        }
    }
'''
def get_bib_keys(use_chapter=False, verbose=False):
    # get the current dir and sections folder
    root = Path(os.getcwd()).parent
    sections_folder = root / 'sections'

    files_list = []
    for root, dirs, files in os.walk(sections_folder):
        for f in files:
            if '.tex' not in f: continue #skip not .tex files
            elif 'abstract.tex' in f: continue
            files_list.append( root + '/' + f )
    
    keys = dict() # list for saving the UNIQUE keys by chapter (before section) and by section
    
    
    # Init dictionaries if there are no chapters (a paper)
    if not use_chapter:
        chapter_title = 'root'
        keys[chapter_title] = { 'keys': [], # acc for this chapter, before sections
                                'sanity' : [], # acc for checked papers
                                'sanity_sections': dict(),
                                'sections': dict() }

        current_acc = keys[chapter_title]['keys']
        current_sanity = keys[chapter_title]['sanity']
    
    for tex_file in files_list:
        file_name = str(tex_file).replace(str(sections_folder)+'/', '')
        if 'abstract.tex' in file_name: continue #skipping abstract

        if verbose:
            print('---')
            print('processing ', file_name)
            
        with Path(tex_file).open() as f:
            for line in f:
                # (?<!^\%.*) excludes lines which start with %
                # \\section | \\citep?t? matches '\section', '\citeX'
                #\{[^\}.]*\} any number of any characters which are not '}' followed by '}'
                line_chapter = re.findall(r'(?<!^\%.*)\\chapter\{[^\}.]*\}', line) # gets \section
                line_section = re.findall(r'(?<!^\%.*)\\section\{[^\}.]*\}', line) # gets \section
                line_cites = re.findall(r'(?<!^\%.*)\\citep?t?\{[^\}.]*\}', line) # gets \cite, \citep, \citet
                line_sanity = re.findall(r'^\%\\sanity\{[^\}.]*\}', line) # gets \sanity
            
                # assuming \cite, \section, and \chapter do not happen in the same line
                if line_chapter != []:
                    # clear string
                    chapter_title = line_chapter[0].replace('\\chapter{', '')\
                                                    .replace('}', '')
                    if verbose: print('chapter: ', chapter_title)
                    keys[chapter_title] = { 'keys': [], # acc for this chapter, before sections
                                            'sanity' : [], # acc for checked papers
                                            'sanity_sections': dict(),
                                            'sections': dict() }

                    current_acc = keys[chapter_title]['keys']
                    current_sanity = keys[chapter_title]['sanity']
                elif line_section != []:
                    # clear string (lazy)
                    section_title = line_section[0].replace('\\section{', '')\
                                                    .replace('}', '')
                    if verbose: print('section: ', section_title)
                    keys[chapter_title]['sections'][section_title] = [] #create acc for this section
                    keys[chapter_title]['sanity_sections'][section_title] = [] #create acc for this section
                    current_acc = keys[chapter_title]['sections'][section_title]
                    current_sanity = keys[chapter_title]['sanity_sections'][section_title]

                elif line_sanity != []:
                    #proccess cites
                    for citation in line_sanity: # iterate over all \citeX in a line
                        # clear string (lazy)
                        keys_in_sanity = citation.replace(' ', '')\
                                                 .replace('%\sanity{','')\
                                                 .replace('}', '')

                        # split and concatenate
                        for k in keys_in_sanity.split(','):
                            current_sanity.append(k)

                elif line_cites != []:
                    #proccess cites
                    for citation in line_cites: # iterate over all \citeX in a line
                        # clear string (lazy)
                        keys_in_cite = citation.replace(' ', '')\
                                                .replace('\cite{','')\
                                                .replace('\citep{', '')\
                                                .replace('\citet{', '')\
                                                .replace('}', '') 
                        # break multiple keys \citeX{aaa, bbb} cases
                        for k in keys_in_cite.split(','):
                            current_acc.append(k)
                            
    if verbose: print('--- post processing ---')

    # post process to make unique lists
    for chapter in keys.keys():
        keys[chapter]['keys'] = list(set(keys[chapter]['keys']))
        keys[chapter]['sanity'] = list(set(keys[chapter]['sanity']))
        if verbose: 
            print('-------------------------------------------')
            print('chapter: ', chapter)
            print('keys: ', keys[chapter]['keys'])
            print('sanity: ', keys[chapter]['sanity'])
            print('---')
        
        for section in keys[chapter]['sections'].keys():
            keys[chapter]['sections'][section] = list(set(keys[chapter]['sections'][section]))
            if verbose: 
                print('section: ', section)
                print('keys: ', keys[chapter]['sections'][section])
                print('sanity: ', keys[chapter]['sanity_sections'][section])
                print('---')
    return keys

def get_chapter_sanity(keys, chapter, verbose=False):
    chapter_acc =  keys[chapter]['sanity']
    if verbose:
        print('---')
        print('chapter: ', chapter)
        print('sanity: ', keys[chapter]['sanity'])
    
    for section in keys[chapter]['sanity_sections']:
        chapter_acc = chapter_acc + keys[chapter]['sanity_sections'][section]
        if verbose:
            print('section: ', )
            print('sanity: ', keys[chapter]['sanity_sections'][section])

    chapter_acc = list(set(chapter_acc))
    if verbose: 
        print('---')
        print('final: ', chapter_acc)
    return chapter_acc

def get_chapter_keys(keys, chapter, verbose=False):
    chapter_acc =  keys[chapter]['keys']
    if verbose:
        print('---')
        print('chapter: ', chapter)
        print('keys: ', keys[chapter]['keys'])
    
    for section in keys[chapter]['sections']:
        chapter_acc = chapter_acc + keys[chapter]['sections'][section]
        if verbose:
            print('section: ', section)
            print('keys: ', keys[chapter]['sections'][section])

    chapter_acc = list(set(chapter_acc))
    if verbose:
        print('---')
        print('final: ', chapter_acc)

    return chapter_acc

def get_all_keys(keys, verbose=False):
    acc = []
    for chapter in keys:
        chap_keys = get_chapter_keys(keys, chapter)
        
        if verbose: print('keys for chapter %s:' %chapter, chap_keys)
        
        acc = acc + chap_keys
    return list(set(acc))

def load_bib_files(bib_files, verbose=False):
    # empty dict for concatenating the bib files
    db = dict()
    
    for bib_file in bib_files:
        if verbose:
            print(bib_file)
        with open(bib_file) as f:
            db.update(bibtexparser.load(f).entries_dict)
            print(len(db))
    return db


def get_entry(db, key, verbose=False):
    # if the key is not in the DB, we have a problem
    if key not in db.keys():
        print('key %s not in table' % key)
        return None

    if verbose:
        print(db[key])
    db[key]['title'] = db[key]['title'].replace('{', '').replace('}','')
    if 'booktitle' in db[key].keys():
        db[key]['booktitle'] = db[key]['booktitle'].replace('{', '').replace('}','')
    if verbose:
        print(db[key])
    
    return db[key]




















