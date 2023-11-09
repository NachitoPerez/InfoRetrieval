import time
import re
import nltk
from nltk import PorterStemmer

# The collections library in Python provides a collection of useful and efficient data structures
# beyond the built-in data types like lists, dictionaries, and sets.
# Here, we are goinig to use the defaultdict structure that allows us to specify a default value for new keys,
# and to avoid key errors when accessing dictionary elements.

from collections import defaultdict

# Define the function that will process the different collections 

def file_processing (file_path):

    # Initialize the index and term frequency dictionaries
    # The index dictionary is a dictionary where the default value for new keys is an empty set that will contain
    # all the docno of each index : {'index':{D0, D1, ....},...}

    index = defaultdict(set)

    # The term_frequency dictionary is a dictionary where the default value for new keys is an other dictionary 
    # that will contain the list of docno as values and the frequency of a term in the same document as a key,
    # and that for each term : { 'term' : { 'docno' : frequency (0 by default, ...)}, ...}

    term_frequency = defaultdict(lambda: defaultdict(int))

    # Read the document collection from a file

    with open(file_path, 'r') as file:
        docs = file.read()


    # Set 2 empty string variables that will contain the number of the document and it's words
    
    docno = ''
    words = ''

    # Getting all the document's number and content 

    documents = re.findall(r'<doc><docno>.*?</docno>.*?</doc>', docs, re.DOTALL)
        
    # Going through each document of the documents individually 

    start_time = time.time() # Record indexing start time

    for document in documents:
            
        statement = re.search(r'<docno>(.*?)</docno>(.*?)</doc>', document, re.DOTALL)
        if statement:
            docno = statement.group(1)
            core = statement.group(2)
            words = re.findall(r'\b\w+\b', core.lower())
            for word in words:
                index[word].add(docno)
                term_frequency[word][docno] += 1

    end_time = time.time()  # Record indexing end time
    indexing_time = end_time - start_time  # Calculate indexing time
    
    # Print the indexing execution time 
    print('Execution time of the indexation process : ', indexing_time, 's\n')

    # Sort the index dictionary           
    index = dict(sorted(index.items()))

    return index, term_frequency, indexing_time

def statistics(index, term_frequency):
    
    # The doc_lengths dictionary is a dictionary that will contain the length of each documment based on it's docno
    # Each key will be the docno of the documment and the default value for new keys is 0 
    # doc_lengths : { '1000' : 0, ...}
    start = time.time()
    doc_lengths = defaultdict(int)
    for term, postings_list in index.items():
        for docno in postings_list :
            doc_lengths [docno] += term_frequency[term][docno]

    vocabulary_size = len(index)

    # The collection_frequencies dictionary will contain the frequency of each term in the collection
    collection_frequencies = defaultdict(int)
    for term, postings_list in index.items():
        collection_frequencies[term] = len(postings_list)
    
    end = time.time()
    statistics_execution_time = end - start

    return doc_lengths, vocabulary_size, collection_frequencies, statistics_execution_time
    

def index_printing(index, term_frequency):
    # Choosing if the user want to print the indexs or not
    decision = input(f'Do you want to print the indexes of the collection ? (y or n): ')
    if decision.lower() == 'y' :
        print(f"Indexes of the collection : ")
        # Print the index with document frequencies (df)
        for term, postings_list in index.items():
            df = len(postings_list)
            print(f"{df}=df({term})")
            for docno in postings_list:
                print(f"{term_frequency[term][docno]} {docno}")