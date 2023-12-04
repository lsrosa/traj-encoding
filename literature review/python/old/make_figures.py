from bibkeys import load_bib_file, get_bib_keys
from read_table import get_table_column2
from figures import hist_iil_by_year, feature_hist

bibkeys_latex = get_bib_keys(verbose=False)
db = load_bib_file(verbose=False)  # load paper bibfile
iil_excel = get_table_column2(['Methods'], 'bibtex')

# all papers classified as IIL in the g-drive table
hist_iil_by_year(iil_excel, bibkeys_latex, db)

feature = 'RL'
#values = ['yes', 'no']
values = ['yes']
feature_hist(feature, values, bibkeys_latex, iil_excel, db, table_file='IIL survey table.xlsx')
