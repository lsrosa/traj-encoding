from matplotlib import pyplot as plt
plt.rcParams.update({
    "text.usetex": True
})
from bibkeys import get_entry, get_all_keys
import numpy as np
from read_table import get_table_column2
from utils import compare_sets
import os
import regex as re # clean some strins for plots file names
from termcolor import colored


def hist_iil_by_year(iil_excel, bibkeys_latex, db, verbose=False):

    if verbose: print(iil_excel, '\n total: %d' % len(keys))
    
    # make sure the keys from the table are in the text
    latex_keys = get_all_keys(bibkeys_latex)

    # get only keys that are both in the latex and in the table
    keys, excel_notin_latex, latex_notin_excel = compare_sets(iil_excel, latex_keys)

    # print some messages for missing papers
    if(len(excel_notin_latex)):
        print(colored('\nPapers in the g-drive table that do not appear in the survey:', 'red'))
        for k in excel_notin_latex: print(k)
    if(len(latex_notin_excel)): 
        print(colored('\nPapers in the Survey that do not appear in the g-drive table:', 'red'))
        for k in latex_notin_excel: print(k)

    years = np.zeros(len(keys))
    years = [int(get_entry(db, key)['year']) for key in keys]
    if verbose: print('years: ', years, 'min, max = %d, %d' %(min(years), max(years)))
    
    x = range(min(years), max(years)+1, 1)
    bins = np.array(list(x) + [max(x)+1])-0.5
    
    if verbose:
        for year in x:
            print('year: %d - %d papers' %(year, years.count(year)))

    fig = plt.figure()
    plt.grid(axis='y', linestyle='--', zorder=0, color='black', linewidth=0.3)
    plt.hist(years, bins=bins, rwidth=0.9, align='mid', zorder=10, color='#A50034')
    plt.ylabel('Number of papers', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.title('History of Interactive Imitation Learning', fontsize=18)
    plt.xticks(x, rotation='vertical')
    fig.axes[0].spines['left'].set_color('none')
    fig.axes[0].spines['right'].set_color('none')
    fig.axes[0].spines['top'].set_color('none')
    plt.tight_layout()
     
    #plt.show()
    plt.savefig('../images/iil_papers_per_year.pdf', format='pdf', bbox_inches='tight')


def feature_hist(feature, values, bibkeys_latex, iil_excel, db, table_file='IIL survey table.xlsx', verbose=False):
    
    # temp buffers for chapter-wise plot
    iil = []
    labels = []
    if not os.path.exists('plots'): os.mkdir('plots')

    # get features from the table 
    excel_features, features = get_table_column2(['Methods'], feature, table_file, options=True)
    if verbose: print('reading column %s from %s\n' %(feature, table_file), excel_features, features)

    assert len(iil_excel) == len(excel_features), 'features and entries do not have the same size'
    
    # make sure the keys from the table are in the text
    latex_keys = get_all_keys(bibkeys_latex)

    # get only keys that are both in the latex and in the table
    common_keys, excel_notin_latex, latex_notin_excel = compare_sets(iil_excel, latex_keys)

    # print some messages for missing papers
    if(len(excel_notin_latex)):
        print(colored('\nPapers in the g-drive table that do not appear in the survey:', 'red'))
        for k in excel_notin_latex: print(k)
    if(len(latex_notin_excel)): 
        print(colored('\nPapers in the Survey that do not appear in the g-drive table:', 'red'))
        for k in latex_notin_excel: print(k)

    if verbose: print('intesec latex and table: %d' %(len(common_keys)))

    #filter `keys` by the selected feature `values`
    keys_per_value = dict()
    for value in values:
        keys_per_value[value] = []
        for ckey in common_keys:
            idx = iil_excel.index(ckey)
            if excel_features[idx] == value:
                keys_per_value[value].append(ckey)
                if verbose: print('found key %s at position %d' %(ckey, idx))
    
    # Plotting time!
    # Plot the section-wise plots
    fig = plt.figure()
   
    # plot hist for all iil papers
    years = [int(get_entry(db, key)['year']) for key in common_keys]
    x = range(min(years), max(years)+1, 1)
    bins = np.array(list(x) + [max(x)+1])-0.5
    plt.hist(bins=bins, x=years, rwidth=0.9, label='IIL', align='mid')
    plt.xticks(x, rotation='vertical')
    plt.ylabel('# of papers')
    plt.xlabel('year')

    for value in values:
        years = [int(get_entry(db, key)['year']) for key in keys_per_value[value]]
        
        x = range(min(years), max(years)+1)
        plt.hist(bins=bins, x=years, rwidth=0.9, label='IIL + ' + feature, align='mid')

    plt.legend()
    plt.savefig('../images/ill_'+ feature +'.pdf', format='pdf', bbox_inches='tight')
