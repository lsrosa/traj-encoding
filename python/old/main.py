from utils import sections_in_chapters
from bibkeys import get_bib_keys, load_bib_file
from read_table import get_table_column, bibkeys_from_bibtex
from analysis import internal_analysis, compare_chapters, plot_chapter_histogram, feature_analysis, missing_keys, mult_chapter_not_cited_iil
from simple_parsing import ArgumentParser

# Get arguments
parser = ArgumentParser()
parser.add_argument('--analysis', type=str, default='IIL_papers', help='Options: IIL_papers, feature_study, \"sanity plot\", multi_chap, \"sanity plot\", \"cross chapters\", \"missing keys\"')
parser.add_argument('--chapters', type=str, default='all', help='If analysis is IIL_papers, separate with a comma '
                                                                '(without a space!) the selected chapters. For complete'
                                                                ' analysis write \"all\".\n To request for available '
                                                                'chapters write \"?\"')
parser.add_argument('--sections', type=str, default=None, help='specify sections for the analysis')
parser.add_argument('--feature', type=str, default='Feedback type', help='feature to study when analysis == feature_study')
args = parser.parse_args()

# Get bibkeys from paper latex (dictionary)
bibkeys_latex = get_bib_keys(verbose=False)

# Get bibkeys DataBase (db) from biblio.bib (dictionary)
bibfile_db = load_bib_file(verbose=False)  # load paper bibfile

# Get chapter names
if args.chapters == '?':
    print(list(bibkeys_latex.keys()))
    exit()
elif args.chapters == 'all':
    chapters = list(bibkeys_latex.keys())
else:
    chapters = args.chapters.split(',')

# Parse which specific sections you want to analyse
if args.sections == None:
    sections = None
elif args.sections == "?":
    for chapter in bibkeys_latex:
        print('chapter: ', chapter)
        print(list(bibkeys_latex[chapter]['sections']))
    exit()
elif  args.sections == "all":
    sections = []
    for chapter in bibkeys_latex:
        sections = sections + list(bibkeys_latex[chapter]['sections'].keys())
else:
    sections = args.sections.split(',')

selection = sections_in_chapters(chapters, sections, bibkeys_latex)

if args.analysis == 'IIL_papers':
    # List of sheet names
    sheet_names = ['Methods',
                   'Surveys']

    # Get bibkeys from paper excel (list)
    bibkeys_excel = get_table_column(sheet_names, 'bibtex')  # get bibkeys list
    non_iil_excel = get_table_column(['non IIL'], 'bibtex')

    # Perform intern analysis, for us to check which papers our sections are missing
    internal_analysis(selection, bibkeys_latex, bibkeys_excel, non_iil_excel, bibfile_db)

elif args.analysis == 'multi_chap':
    # Get bibkeys from paper excel (list)
    bibkeys_excel = get_table_column(['Methods'], 'bibtex')  # get bibkeys list
                                                                                          
    # Perform intern analysis, for us to check which papers our sections are missing
    mult_chapter_not_cited_iil(selection, bibkeys_latex, bibkeys_excel, bibfile_db)

elif args.analysis == 'feature_study':
    # List of sheet names
    sheet_names = ['Methods']

    # Get bibkeys from paper excel (list)
    bibkeys_excel = get_table_column(sheet_names, 'bibtex')  # get bibkeys list

    # Get feature
    features_methods = get_table_column(sheet_names, args.feature)  # get features list

    # Run feature analysis
    feature_analysis(args.feature, chapters, bibkeys_latex, bibkeys_excel, features_methods, bibfile_db)

elif args.analysis == 'sanity plot':
    # Get bibkeys from excel (list)
    bibkeys_excel = get_table_column(['Methods'], 'bibtex')  # get bibkeys list
    non_iil_excel = get_table_column(['non IIL'], 'bibtex')
    
    # Plot histogram for a chapter
    plot_chapter_histogram(bibkeys_latex, bibkeys_excel, non_iil_excel, bibfile_db)

elif args.analysis == 'cross chapters':
    if len(chapters) != 2:
        raise Exception('usage: python main.py --analysis "cross chapters" --chapters "<chapterName1>, <chapterName2>"')
    
    # Compare two chapters
    compare_chapters(chapters[0], chapters[1], bibkeys_latex, bibfile_db)

elif args.analysis == 'missing keys':
    missing_keys(bibkeys_latex, bibfile_db)
