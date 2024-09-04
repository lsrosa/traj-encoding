import pandas as pd
from bibkeys import get_all_keys
from utils import compare_sets

def populate_table(bibkeys, table_file='surveyTable.xlxs', sheet='Sheet1', verbose=False):
    """
        Pupulates the xlxs table with all bibkeys found in the latex files
    """
    keys = get_all_keys(bibkeys)
    keys = list(set(keys))#make an unique list
    if verbose: print('# keys latex:', len(keys))
    
    keys_on_table = get_table_column('bibkey', table_file, sheet, options=False)
    if verbose: print('# keys on table:', len(keys_on_table))
    
    [_, diff_keys, _] = compare_sets(keys, keys_on_table)
    if len(diff_keys) == 0: 
        if verbose: print('All keys already on table. Doing nothing')
        return
    elif verbose: print('Adding keys: ', diff_keys)
    
    with pd.ExcelWriter(table_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        df = pd.DataFrame(diff_keys, columns=['bibkey'])
        df.to_excel(writer, index=False, startrow=2+len(keys_on_table), header=False)

    return

def get_complete_key(key, table):
    complete_key = ''
    for name in list(table.columns):
        if name[:len(key)] == key:
            complete_key = name

    return complete_key

def get_table_column(column_name, table_file='surveyTable.xlxs', sheet='Sheet1', options=False):
    """
    Reads a whole column of the excel table. also gets the options in the first row for each 
    feature defined by a column
    """

    table_sheet = pd.read_excel(table_file, sheet_name=sheet)
    complete_column_name = get_complete_key(column_name, table_sheet)
    
    # get column as list of strings
    # 1: to skip the header rows
    column = table_sheet.loc[1:, complete_column_name].values.tolist()
    
    if options:
        opt = str(table_sheet.loc[0, complete_column_name]).replace('[','').replace(']','').split(', ')
        return column, opt
    else:
        return column

def bibkeys_from_bibtex(bibtex_list):
    bibkeys = []
    for bibtex in bibtex_list:
        if not isinstance(bibtex, str):  # filter NaNs
            continue

        bibkey_start = bibtex.find('{')
        bibkey_end = bibtex.find(',')
        bibkeys.append(bibtex[bibkey_start + 1:bibkey_end])

    return bibkeys


if __name__ == "__main__":
    print('aaaaaaaa')
