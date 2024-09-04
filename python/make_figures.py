from bibkeys import load_bib_files, get_bib_keys
from excelTableUtils import get_table_column
from figures import feature_hist
from pathlib import Path
import os, glob

# Get all cite in the latex document
bibkeys_latex = get_bib_keys(verbose=True)


# load biblio.bib files
biblio_files = glob.glob((Path(os.getcwd()).parent/'biblio.bib').as_posix())
db = load_bib_files(biblio_files, verbose=True)  # load paper bibfile

# Excel file name and feature
excel_file = (Path(os.getcwd())/'Traj Encoding Survey Table.xlsx').as_posix()
feature = 'Scope'

# Plot the histogram
feature_hist(feature, bibkeys_latex, db, table_file=excel_file, sheet='social navigation', verbose=True)
quit()
