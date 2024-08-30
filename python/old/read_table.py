import pandas as pd


def get_complete_key(key, table):
    complete_key = ''
    for name in list(table.columns):
        if name[:len(key)] == key:
            complete_key = name

    return complete_key


def get_table_column(sheet_names, column_name):

    final_column = []

    # Iterate through every sheet and get bib keys
    for sheet_name in sheet_names:
        IIL_table_sheet = pd.read_excel('IIL survey table.xlsx', sheet_name=sheet_name)
        complete_column_name = get_complete_key(column_name, IIL_table_sheet)
        column = IIL_table_sheet.loc[:, complete_column_name].values.tolist()  # get column as list of strings
        final_column += column  # concatenate columns

    if column_name == 'bibtex':
        final_column = bibkeys_from_bibtex(final_column)

    return final_column


def get_table_column2(sheet_names, column_name, table_file='IIL survey table.xlsx', options=False):

    final_column = []

    # Iterate through every sheet and get bib keys
    for sheet_name in sheet_names:
        IIL_table_sheet = pd.read_excel(table_file, sheet_name=sheet_name)
        complete_column_name = get_complete_key(column_name, IIL_table_sheet)
        
        # get column as list of strings
        # 2: to skip the header rows
        column = IIL_table_sheet.loc[2:, complete_column_name].values.tolist()

        final_column += column  # concatenate columns
    if column_name == 'bibtex':
        final_column = bibkeys_from_bibtex(final_column)
        return final_column
    elif options:
        opt = str(IIL_table_sheet.loc[0, complete_column_name]).replace('[','').replace(']','').split(', ')
        return final_column, opt
    else:
        return final_column



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
    
    # List of sheet names
    sheet_names = ['Stateaction - Absolute Feedback',
                'Stateaction - Relative Feedback',    
                'Evaluative Feedback',
                'Preference Feedback',
                'Other Feedback',
                'Surveys']

    bibkeys = get_table_column(sheet_names, 'bibtex')  # get bibtex list
    print(bibkeys)
