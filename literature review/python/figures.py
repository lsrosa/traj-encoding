from matplotlib import pyplot as plt
plt.rcParams.update({
    "text.usetex": True
})

from bibkeys import get_entry, get_all_keys
import numpy as np
from excelTableUtils import get_table_column
from utils import compare_sets
import os
from termcolor import colored
from math import isnan


def feature_hist(feature, bibkeys_latex, db, table_file='surveyTable.xlsx', sheet='Sheet1', verbose=False):
    
    # temp buffers for chapter-wise plot
    if not os.path.exists('plots'): os.mkdir('plots')

    # get features from the table 
    excel_keys = get_table_column('bibkey', table_file, sheet, options=False)
    excel_features, features = get_table_column(feature, table_file, sheet, options=True)
    if verbose: print('reading column %s from %s\n' %(feature, table_file), excel_features, features)

    assert len(excel_keys) == len(excel_features), 'features and entries do not have the same size'
    
    # make sure the keys from the table are in the text
    latex_keys = get_all_keys(bibkeys_latex)

    # get only keys that are both in the latex and in the table
    common_keys, excel_notin_latex, latex_notin_excel = compare_sets(excel_keys, latex_keys)

    # print some messages for missing papers
    if(len(excel_notin_latex)):
        print(colored('\nPapers in the table that do not appear in the survey:', 'red'))
        for k in excel_notin_latex: print(k)
    if(len(latex_notin_excel)): 
        print(colored('\nPapers in the Survey that do not appear in the table:', 'red'))
        for k in latex_notin_excel: print(k)

    if verbose: print('intesec latex and table: %d' %(len(common_keys)))

    #filter `keys` by the selected feature `values`
    keys_per_feature = dict()
    for feature in features:
        keys_per_feature[feature] = []
        for ckey in common_keys:
            idx = excel_keys.index(ckey)
            if excel_features[idx] == feature:
                keys_per_feature[feature].append(ckey)
                if verbose: print('found key %s at position %d' %(ckey, idx))
    
    # Plotting time!
    # Plot the section-wise plots
    fig = plt.figure()
   
    # plot hist for all iil papers
    years = [int(get_entry(db, key)['year']) for key in common_keys]
    x = range(min(years), max(years)+1, 1)
    bins = np.array(list(x) + [max(x)+1])-0.5
    plt.xticks(x, rotation='vertical')
    plt.ylabel('\# of papers')
    plt.xlabel('year')
    
    years = []
    for feature in features:
        if len(keys_per_feature[feature]) == 0: continue
        years.append([int(get_entry(db, key)['year']) for key in keys_per_feature[feature]])
        
    plt.hist(bins=bins, x=years, rwidth=0.9, label=feature, alpha=0.5, histtype='bar')

    plt.legend()
    plt.savefig('../images/'+ feature +'.pdf', format='pdf', bbox_inches='tight')
    
    return