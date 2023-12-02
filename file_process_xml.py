import re
import time
import xml.etree.ElementTree as ET

# The collections library in Python provides a collection of useful and efficient data structures
# beyond the built-in data types like lists, dictionaries, and sets.
# Here, we are goinig to use the defaultdict structure that allows us to specify a default value for new keys,
# and to avoid key errors when accessing dictionary elements.

from collections import defaultdict

# Define the function that will process the different collections 

def file_processing_tags (file_path, process):

    # Initialize the index and term frequency dictionaries
    # The index dictionary is a dictionary where the default value for new keys is an empty set that will contain
    # all the docno of each index : {'index':{D0, D1, ....},...}

    index = defaultdict(lambda: defaultdict(set))
    index.update(process[0])

    # The term_frequency dictionary is a dictionary where the default value for new keys is an other dictionary 
    # that will contain the list of docno as values and the frequency of a term in the same document as a key,
    # and that for each term : { 'term' : { 'docno' : frequency (0 by default, ...)}, ...}

    term_frequency = defaultdict(lambda: defaultdict(int))
    term_frequency.update(process[1])

    # Read the document collection from a file

    with open(file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    pattern = re.compile(r'&[^;]+;')
    xml_content = re.sub(pattern, '', xml_content)
    
    root = ET.fromstring(xml_content)

    id_element = root.find('.//id')
    sections = root.findall('.//sec')

    
    # Getting all the document's number, title, and content 
    docno = id_element.text

    doc_xml = defaultdict(lambda: defaultdict(str))
    
    i=1
    
    for section in sections :
        
        paragraphes = section.findall('.//p')


        j=1

        for paragraphe in paragraphes:

            p = ET.tostring(paragraphe, encoding='unicode', method='text').strip().replace('\n', '')

            doc_xml[section.tag +f'[{i}]'][paragraphe.tag +f'[{j}]']=p

            j+=1
        
        i+=1
            
    doc_xml = dict(sorted(doc_xml.items()))

    words = ''
        
    # Going through each document of the documents individually 

    for sec, section in doc_xml.items():

        for p, paragraphe in section.items():

            words = re.findall(r'\b[a-zA-Z_]+\b', paragraphe.lower())

            cleaned_words = [cleaned_word for word in words for cleaned_word in re.split(r'_+', word) if cleaned_word]

            for word in cleaned_words:
                index[word][docno].add('/bdy[1]/' + sec + '/' + p)
                term_frequency[word][docno] += 1


    # Sort the dictionarys           
    index = dict(sorted(index.items()))
    term_frequency = dict(sorted(term_frequency.items()))
    


    return index, term_frequency

def statistics_tags(index, term_frequency):
    
    # The doc_lengths dictionary is a dictionary that will contain the length of each documment based on it's docno
    # Each key will be the docno of the documment and the default value for new keys is 0 
    # doc_lengths : { '1000' : 0, ...}
    start = time.time()
    doc_lengths = defaultdict(int)
    for term, postings_list in index.items():
        for docno in postings_list.keys() :
            doc_lengths [docno] += term_frequency[term][docno]

    vocabulary_size = len(index)

    # The collection_frequencies dictionary will contain the frequency of each term in the collection
    collection_frequencies = defaultdict(int)
    for term, postings_list in index.items():
        collection_frequencies[term] = len(postings_list)
    
    end = time.time()
    statistics_execution_time = end - start

    return doc_lengths, vocabulary_size, collection_frequencies, statistics_execution_time
