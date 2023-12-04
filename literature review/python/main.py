from pathlib import Path
import glob, os # get paths

# Reads the latex source files (.bib and .tex)
from bibkeys import get_bib_keys, load_bib_files

# Excel table functions
from excelTableUtils import populate_table

#%% reads latex source

# compose list of .bib files
biblio_files = glob.glob((Path(os.getcwd()).parent/'referencePapers/*/biblio.bib').as_posix())
# Get bibkeys DataBase (db) from biblio.bib (dictionary)
bibfile_db = load_bib_files(biblio_files, verbose=False)  # load paper bibfile

# Get bibkeys from latex (dictionary)
bibkeys_latex = get_bib_keys(verbose=True)

#%% Populate Excel table
excel_file = (Path(os.getcwd())/'surveyTable.xlsx').as_posix()
populate_table(bibkeys_latex, file_name = excel_file,  verbose=True)
