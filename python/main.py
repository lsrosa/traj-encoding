from pathlib import Path
import glob, os # get paths

# Reads the latex source files (.bib and .tex)
from bibkeys import get_bib_keys, load_bib_files

# Excel table functions
from excelTableUtils import populate_table, get_table_column

# Citation Maps
from citationMap import build, draw

#%% reads latex source

# compose list of .bib files
biblio_files = glob.glob((Path(os.getcwd()).parent/'referencePapers/*/biblio.bib').as_posix())
# Get bibkeys DataBase (db) from biblio.bib (dictionary)
bibfile_db = load_bib_files(biblio_files, verbose=False)  # load paper bibfile

# Get bibkeys from latex (dictionary)
bibkeys_latex = get_bib_keys(verbose=False)

#%% Populate Excel table
excel_file = (Path(os.getcwd())/'surveyTable.xlsx').as_posix()
populate_table(bibkeys_latex, table_file=excel_file,  verbose=True)

#%% Read a Colunm of the table and options
col_keys = get_table_column('bibkey', excel_file, options=False)
col_scope, scopes = get_table_column('Scope', excel_file, options=True)

#%% Try plotting the citation maps
build(bibfile_db)
draw()
