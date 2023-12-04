from bibkeys import get_chapter_keys, get_chapter_sanity, get_entry
from termcolor import colored
from matplotlib import pyplot as plt
from utils import compare_sets, print_list

import numpy as np  # array processing
import regex as re  # clean some strins for plots file names
import os  # creating foldes for the plots


def internal_analysis(selection, bibkeys_latex, iil_excel, non_iil_excel, bibfile_db):
    print('total iil papers: ', len(iil_excel))
    print('total non iil papers: ', len(non_iil_excel))
    
    chapters = list(selection.keys())
    for chapter in chapters:
        chapter_bibkeys = get_chapter_keys(bibkeys_latex, chapter, False)
        chapter_sanity = get_chapter_sanity(bibkeys_latex, chapter, False)
        
        _, iil_not_in_chapter, _ = compare_sets(iil_excel, chapter_bibkeys + chapter_sanity)
        _, _, unclassified = compare_sets(iil_excel + non_iil_excel, chapter_bibkeys)
        
        print('\n\n---------------------------------------------------------------------------------------------------------------')
        print(colored('Chapter: %s' % chapter, 'blue'))
        print('---------------------------------------------------------------------------------------------------------------')
        # None means to consider only the Chapter as a whole, not individual sections
        if selection[chapter] == None: 
            print('\n IIL papers not cited in this chapter - total: %i/%i' % (len(iil_not_in_chapter), len(chapter_bibkeys)))
            print_list(bibfile_db, iil_not_in_chapter)
        
            print('\n Unclassified papers in chapter - total: %i/%i' %(len(unclassified), len(chapter_bibkeys)) )
            print_list(bibfile_db, unclassified)
        else:
            for section in selection[chapter]:
                section_bibkeys = bibkeys_latex[chapter]['sections'][section]
                section_sanity = bibkeys_latex[chapter]['sanity_sections'][section]
                _, iil_not_in_section, _ = compare_sets(iil_excel, section_bibkeys + section_sanity)
                _, _, unclassified = compare_sets(iil_excel + non_iil_excel, section_bibkeys)

                print('\n   -----------------------------------------')
                print(colored('    Section: %s' % section, 'green'))
                print('\n IIL papers not cited in this section - total: %i/%i' % (len(iil_not_in_section), len(section_bibkeys)))
                print_list(bibfile_db, iil_not_in_section)
                
                print('\n Unclassified papers in section - total: %i/%i' %(len(unclassified), len(section_bibkeys)) )
                print_list(bibfile_db, unclassified)
    return

def mult_chapter_not_cited_iil(selection, bibkeys_latex, iil_excel, bibfile_db, verbose=False):
    chapters = list(selection.keys())
    
    acc = []
    for chapter in chapters:
        chapter_bibkeys = get_chapter_keys(bibkeys_latex, chapter, False)
        chapter_sanity = get_chapter_sanity(bibkeys_latex, chapter, False)
        
        _, iil_not_in_chapter, _ = compare_sets(iil_excel, chapter_bibkeys + chapter_sanity)
        
        if selection[chapter] == None: 
            acc.append(iil_not_in_chapter)
        
        else:
            for section in selection[chapter]:
                section_bibkeys = bibkeys_latex[chapter]['sections'][section]
                section_sanity = bibkeys_latex[chapter]['sanity_sections'][section]
                _, iil_not_in_section, _ = compare_sets(iil_excel, section_bibkeys + section_sanity)
                acc.append(iil_not_in_section)
    
    intersec = set(acc[0])
    if verbose: print('acc: ', acc)
    if verbose: print('\n---\n', 0, intersec)
    for i in range(len(acc)-1):
        if verbose: print('\n---\n',i+1, acc[i+1])
        intersec = intersec.intersection(acc[i+1])
    if verbose: print('\nresult: ', intersec)
   
    print('     -----------------------------------------')
    print(colored('\n %d IIL papers not cited in common in: ' %(len(intersec))), selection)
    print('\n   -----------------------------------------')
    print_list(bibfile_db, list(intersec))
    return

def compare_chapters(c1, c2, bibkeys_latex, bibfile_db):
    c1_bibkeys = get_chapter_keys(bibkeys_latex, c1, False)
    c2_bibkeys = get_chapter_keys(bibkeys_latex, c2, False)
    
    intersec, c1_not_in_c2, c2_not_in_c1 = compare_sets(c1_bibkeys, c2_bibkeys)
    
    print('\n\n---------------------------------------------------------------------------------------------------------------')
    print(colored('Chapter %s VS Chapter %s' %(c1, c2), 'blue'))
    print('---------------------------------------------------------------------------------------------------------------')
    
    print(colored('\n Papers in Chapters %s and %s' %(c1, c2), 'green')) 
    print_list(bibfile_db, intersec)
        
    print('\n   -----------------------------------------')
    print(colored('\n Papers in %s which are NOT in %s' %(c1, c2), 'green')) 
    print_list(bibfile_db, c1_not_in_c2)

    print('\n   -----------------------------------------')
    print(colored('\n Papers in %s which are NOT in %s' %(c2, c1), 'green')) 
    print_list(bibfile_db, c2_not_in_c1)
    
    return


def get_cited_papers_feature_info(chapter, feature_name, features_methods, bibkeys_excel, chapter_bibkeys, bibfile_db, indentation=''):
    # Get indexes of methods in excel that are cited in this chapter
    index_bibkeys_chapter = [index for index, element in enumerate(bibkeys_excel) if element in set(chapter_bibkeys)]
    index_bibkeys_non_chapter = [index for index, element in enumerate(bibkeys_excel) if element not in set(chapter_bibkeys)]

    # Get feature values of cited papers
    feature_methods_clean = [str(feature).split(' (')[0].split(',')[0] for feature in features_methods]
    feature_methods_chapter = list(np.array(feature_methods_clean)[index_bibkeys_chapter])
    feature_methods_non_chapter = list(np.array(feature_methods_clean)[index_bibkeys_non_chapter])

    # Get types of features
    feature_types = list(set(feature_methods_chapter))

    # Get corresponding methods to feature_methods_clean
    methods_chapter_with_feature = list(np.array(bibkeys_excel)[index_bibkeys_chapter])
    methods_non_chapter_with_feature = list(np.array(bibkeys_excel)[index_bibkeys_non_chapter])

    # Iterate over every feature type
    methods_with_feature_per_type = []
    for feature_type in feature_types:
        print(colored('\n' + indentation + feature_type + '\n', 'yellow'))

        # Print methods that have this feature
        methods_with_feature_type = []
        methods_with_feature_type_bibkey = ''
        for i in range(len(feature_methods_chapter)):
            if feature_type == feature_methods_chapter[i]:
                paper_title = get_entry(bibfile_db, methods_chapter_with_feature[i], False)['title']
                print(colored(indentation + '     - %s' % paper_title, 'green'), '\n              bibkey: %s' % methods_chapter_with_feature[i])
                methods_with_feature_type.append(paper_title)
                methods_with_feature_type_bibkey += '\citet{' + methods_chapter_with_feature[i] + '},\n'

        for i in range(len(feature_methods_non_chapter)):
            if feature_type == feature_methods_non_chapter[i]:
                paper = get_entry(bibfile_db, methods_non_chapter_with_feature[i], False)
                paper_title = paper['title']
                print(colored(indentation + '     - %s' % paper_title, 'red'), '\n              bibkey: %s' % methods_non_chapter_with_feature[i])
                #methods_with_feature_type.append(paper_title)

        methods_with_feature_per_type.append(methods_with_feature_type)
        print('Summary methods with feature:\n', methods_with_feature_type_bibkey )
    # Process and show data
    print(colored('\nMethods per feature', 'blue'))
    number_methods_per_feature = []
    for i in range(len(feature_types)):
        number_of_methods_with_feature = len(methods_with_feature_per_type[i])
        number_methods_per_feature.append(number_of_methods_with_feature)
        print(colored('     - %s:' % feature_types[i], 'yellow'), '%s' % number_of_methods_with_feature)

    x_plot = range(len(feature_types))
    plt.bar(x_plot, number_methods_per_feature)
    plt.xticks(x_plot, feature_types)
    plt.ylabel('Number of methods')
    plt.xlabel('Feature classes')
    plt.title('Histogram of feature "%s" in chapter "%s"' % (feature_name, chapter))
    plt.show()


def feature_analysis(feature_name, chapters, bibkeys_latex, bibkeys_excel, features_methods, bibfile_db, include_sections=True):
    print('\n\n\n -------------------------------- Start analysis --------------------------------\n')

    # Iterate over chapters
    for chapter in chapters:
        # Get and print chapter statistics
        print('\n\n---------------------------------------------------------------------------------------------------------------')
        print(colored('Chapter: %s' % chapter, 'blue'))
        print('---------------------------------------------------------------------------------------------------------------')

        # Get chapter bibkey dict
        chapter_bibkeys = get_chapter_keys(bibkeys_latex, chapter, verbose=False)

        # Get info
        indentation = '      '
        get_cited_papers_feature_info(chapter, feature_name, features_methods, bibkeys_excel, chapter_bibkeys, bibfile_db, indentation)

        # Get chapter bibkey dict
        chapter_bibkeys_dict = bibkeys_latex[chapter]

        if include_sections:
            # Iterate over sections
            sections = list(chapter_bibkeys_dict['sections'].keys())
            for section in sections:
                section_bibkeys = chapter_bibkeys_dict['sections'][section]
                print('\n   -----------------------------------------------------')
                print(colored('     Section: %s' % section, 'green'))
                print('   -----------------------------------------------------')

                # Get info
                indentation = '          '
                get_cited_papers_feature_info(chapter, feature_name, features_methods, bibkeys_excel, section_bibkeys, bibfile_db, indentation)


def plot_chapter_histogram(bibkeys_latex, iil_excel, non_iil_excel, bibfile_db):
    # temp buffers for chapter-wise plot
    iil = []
    noniil = []
    unc = []
    labels = []
    if not os.path.exists('plots'): os.mkdir('plots')

    for chapter in bibkeys_latex:
        # get the chapter-wise keys
        chapter_bibkeys = get_chapter_keys(bibkeys_latex, chapter, False)
        
        # get number os citations (classified as iil, or not, or unclassified)
        temp1, _, _ = compare_sets(chapter_bibkeys, iil_excel)
        temp2, _, _ = compare_sets(chapter_bibkeys, non_iil_excel)
        _, temp3, _ = compare_sets(chapter_bibkeys, iil_excel + non_iil_excel)
         
        iil.append(len(temp1))
        noniil.append(len(temp2))
        unc.append(len(temp3))
        labels.append(chapter)
       
        # temp buffers for section-wise plots
        iil_sec = [len(temp1)]
        noniil_sec = [len(temp2)]
        unc_sec = [len(temp3)]
        labels_sec = [chapter]

        for section in bibkeys_latex[chapter]['sections']:
            section_bibkeys = bibkeys_latex[chapter]['sections'][section]
            
            # get number os citations (classified as iil, or not, or unclassified)
            temp1, _, _ = compare_sets(section_bibkeys, iil_excel)
            temp2, _, _ = compare_sets(section_bibkeys, non_iil_excel)
            _, temp3, _ = compare_sets(section_bibkeys, iil_excel + non_iil_excel)

            iil_sec.append(len(temp1))
            noniil_sec.append(len(temp2))
            unc_sec.append(len(temp3))
            labels_sec.append(section)

        # Plot the section-wise plots
        fig = plt.figure(chapter)
        x = range(len(iil_sec))
        plt.bar(x, iil_sec, label='iil papers')
        plt.bar(x, noniil_sec, label='non iil papers', bottom=iil_sec)
        plt.bar(x, unc_sec, label='unclassified', bottom=np.array(iil_sec)+np.array(noniil_sec))
        for (xx,l) in zip(x, labels_sec): plt.text(xx, 2, l, rotation=90) 
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off    
        plt.xlabel('sections')
        plt.ylabel('# papers')
        plt.legend()
                                                                                     
        plt.savefig('plots/'+re.sub('[^A-Za-z0-9]+', '', chapter)+'.pdf', format='pdf', bbox_inches='tight')
    
    # plot the chapter-wise version

    fig = plt.figure()    
    x = range(len(iil))  
    # Plot the per chapter
    plt.bar(x, iil, label='iil papers')
    plt.bar(x, noniil, label='non iil papers', bottom=iil)
    plt.bar(x, unc, label='unclassified', bottom=np.array(iil)+np.array(noniil))
    for (xx,l) in zip(x, labels): plt.text(xx, 2, l, rotation=90) 
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off    
    plt.xlabel('chapters')
    plt.ylabel('# papers')
    plt.legend()
    #plt.show()

    plt.savefig('plots/chapters.pdf', format='pdf', bbox_inches='tight')



def missing_keys(keys, db, verbose=True):
    # acc all keys in the text
    text_keys = []
    for chapter in keys:
        text_keys = text_keys + keys[chapter]['keys']
        for section in keys[chapter]['sections']:
            text_keys = text_keys + keys[chapter]['sections'][section]
    
    # eliminate duplicates
    text_keys = list(set(text_keys))

    # compute which keys in the text are missing in the DB
    _, missing_keys, _ = compare_sets(text_keys, db.keys())

    if verbose: print(missing_keys)

    # iterate over chapters and sections
    # and check if missing keys are present

    for chapter in keys:
        missing_here = set(missing_keys).intersection(keys[chapter]['keys'])
        
        # print the missing ones
        if len(missing_here) > 0: 
            print('\n\n---------------------------------------------------------------------------------------------------------------')
            print(colored('Chapter: %s' % chapter, 'blue'))
            print('---------------------------------------------------------------------------------------------------------------')
            for key in missing_here:
                print('missing: ' + key + '\n')
        
        for section in keys[chapter]['sections']:
            missing_here = set(missing_keys).intersection(keys[chapter]['sections'][section])
            if len(missing_here) > 0:
                print('\n   -----------------------------------------------------')
                print(colored('     Section: %s' % section, 'green')+ colored(' in Chapter: %s' % chapter, 'blue'))
                print('   -----------------------------------------------------')

                for key in missing_here:
                    print('missing: ' + key + '\n')




