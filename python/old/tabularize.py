from bibkeys import get_chapter_keys, get_entry
from read_table import get_table_column2
from utils import compare_sets
from termcolor import colored
import math

def get_iil_keys_features_chapter(chapter_keys, excel_features, excel_keys, verbose=False):
    iil_keys_in_chapter, _, _ = compare_sets(chapter_keys, excel_keys)
    iil_features_in_chapter = []

    # get the features for each IIL paper in this chapter
    for key in iil_keys_in_chapter:
        if key in excel_keys: # if this key is an IIL paper
            idx = excel_keys.index(key)
            if verbose: print(key, idx, excel_features[idx], '\n')
            iil_features_in_chapter.append(excel_features[idx])

    return iil_keys_in_chapter, iil_features_in_chapter

def get_papers_with_features(feature, keys, features, feature_name, verbose=False):
    ret = []
    for k, f in zip(keys, features):
        
        #print(f, type(f))
        
        if (type(f) == float and math.isnan(f)) or f == "?":
            print(colored('found missing feature ', 'green') + colored('%s' %feature_name, 'red') + colored(' for ', 'green') + colored('%s' %k, 'red') + colored(' !!!!', 'green') )
        elif f.find(feature) >= 0:
            if verbose: print('found: %s in' %feature, ' key: %s' %k, 'features: %s' %f)
            ret.append(k)
    return ret

def key_list_to_latex(keys, db):
    # sort by year
    years = []
    for key in keys:
        years.append(int(get_entry(db, key)['year']))
    
    # sorting according to year
    tuples = sorted(zip(years, keys))
    sorted_keys = [t[1] for t in tuples]
    
    ret = ''
    for key in sorted_keys:
        ret = ret + '\\citet{%s}, '%key
    ret = ret[:-2] # remove trailing comma

    return ret

def feature_to_latex(feature):
    # TODO: more cases might appear
    return feature.replace('_', ' ').replace('>', '$>$').replace('<', '$<$')

def clear_str(string):
    # TODO: more cases might appear
    return string.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')

def make_table(chapter, feature_name, keys_latex, db, table_file = 'IIL survey table.xlsx', verbose=False):
    excel_bibtex = get_table_column2(['Methods'], 'bibtex', table_file)
    excel_features, features = get_table_column2(['Methods'], feature_name, table_file, options=True)

    chapter_bibkeys = get_chapter_keys(keys_latex, chapter, verbose=verbose)
    chap_iil_keys, chap_iil_feats = get_iil_keys_features_chapter(chapter_bibkeys, excel_features, excel_bibtex, verbose=verbose)
    filename = '../sections/summary_tables/' + clear_str(chapter) + clear_str(feature_name) + '.tex' 
    f = open(filename, 'w')
    
    f.write('\\begin{table}\n')
    f.write('\\centering')
    f.write('\t\\caption{List of \\gls{iil} papers in Chapter %s}\n' % chapter)
    f.write('\t\\label{tab: summary chap %s}\n' % chapter)
    
    column_tabs = '|'
    f.write('\t\\begin{tabulary}{\\linewidth}{|c|L|}\n')
    f.write('\t\t\\toprule\n')
    f.write('\t\t\\textbf{features} & \\textbf{List of Papers}\\\\\n')
    f.write('\t\t\\midrule\n')
   
    # for each class we will have a line in the table
    rows = []
    for feat in features:
        # skip >1
        if feat == '>1': continue

        #### get papers which feat list contains feat
        key_list = get_papers_with_features(feat, chap_iil_keys, chap_iil_feats, feature_name, verbose=verbose)

        latex_key_list = key_list_to_latex(key_list, db) #sorts by year
        latex_feature = feature_to_latex(feat)
        #print(latex_key_list)

        rows.append('\t\t%s & %s \\\\\\hline\n' %(latex_feature, latex_key_list) ) 
   
    # remove extra \hline and write the rows after cleaning up
    rows[-1] = rows[-1][:-7]
    for row in rows: f.write(row)

    f.write('\t\t\\bottomrule\n')
    f.write('\t\\end{tabulary}\n')
    f.write('\\end{table}\n')

    f.close()

'''
# not finished yet, hopefully not necessary
def make_table_transposed(chapter, keys_latex, options, features, bibtex, filename='table.tex'):
    chapter_bibkeys = get_chapter_keys(keys_latex, chapter, verbose=verbose)

    f = open(filename, 'w')
    
    f.write('\\begin{table}\n')
    f.write('\t\\caption{\color{Red}ADD CAPTION and LABEL\color{black}}\n')
    f.write('\t\\label{xxx}\n')
    
    column_tabs = '|'
    for i in range(len(options)):
        column_tabs = column_tabs + 'c|'

    f.write('\t\\begin{tabular}{%s}\n' % column_tabs)
    f.write('\t\t\\toprule\n')
    
    header = ''
    for opt in options:
        header = header + opt + ' & ' 
    header = header[:-2] + '\\\\'
    f.write('\t\t%s\n' %header)

    f.write('\t\t\\midrule\n')

    f.write('\t\t\n')
    
    f.write('\t\t\\bottomrule\n')
    f.write('\t\\end{tabular}\n')
    f.write('\\end{table}\n')


    f.close()
'''
