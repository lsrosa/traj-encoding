from bibkeys import get_bib_keys, load_bib_file
from tabularize import make_table

keys = get_bib_keys(verbose=False)
db = load_bib_file(verbose=False)  # load paper bibfile

table_file = 'IIL survey table.xlsx'

chapter = 'Modalities of Interaction'
feature = 'Feedback type'
make_table(chapter, feature, keys, db, table_file=table_file)

chapter = 'Behavior Representations Learned from Interactions'
feature = 'Model Learned'
make_table(chapter, feature, keys, db, table_file=table_file)

chapter = 'Auxiliary Models'
feature = 'Model Learned'
make_table(chapter, feature, keys, db, table_file=table_file)

chapter = 'Reinforcement Learning with Human-in-the-Loop'
feature = 'RL'
make_table(chapter, feature, keys, db, table_file=table_file)

chapter = 'Model Representations (Function Approximation)'
feature = 'Function Approximator'
make_table(chapter, feature, keys, db, table_file=table_file)
