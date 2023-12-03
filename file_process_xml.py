import re
import time
import xml.etree.ElementTree as ET
from files_maneg import *

from collections import defaultdict

def file_processing_tags (file_path):

    index = defaultdict(lambda: defaultdict(set))

    term_frequency = defaultdict(lambda: defaultdict(int))

    with open(file_path, 'r', encoding='utf-8') as file:
        docs = file.read()
    
    docno = ''
    words = ''

    documents = re.findall(r'<doc><docno>.*?</docno>.*?</doc>', docs, re.DOTALL)

    for document in documents:
            
        statement = re.search(r'<docno>(.*?)</docno>(.*?)</doc>', document, re.DOTALL)
        if statement:
            docno = statement.group(1)
            doc = statement.group(2)

        tags_sec = re.findall(r'<sec>(.*?)</sec>', doc, re.DOTALL)
        if tags_sec:
            sections=tags_sec

        doc_xml = defaultdict(lambda: defaultdict(str))
        
        i=1

        for section in sections :

            tags_p = re.findall(r'<p>(.*?)</p>', section, re.DOTALL)
            if tags_p:
                paragraphs=tags_p

            j=1

            for paragraph in paragraphs:

                doc_xml['sec'+f'[{i}]']['p' +f'[{j}]']=paragraph

                j+=1
            
            i+=1
        
        tags_op = re.findall(r'<p>(.*?)</p>', document, re.DOTALL)
        if tags_op:
            o_paragraphs=tags_op
            k=1
            
            for o_paragraph in o_paragraphs:

                if o_paragraph not in paragraphs :

                    doc_xml['bdy[1]']['p' +f'[{k}]']=o_paragraph

                    k+=1

        doc_xml = dict(sorted(doc_xml.items()))
        
        for sec, section in doc_xml.items():

            for p, paragraphe in section.items():

                words = re.findall(r'\b[a-zA-Z_]+\b', paragraphe.lower())

                cleaned_words = [cleaned_word for word in words for cleaned_word in re.split(r'_+', word) if cleaned_word]

                for word in cleaned_words:

                    if sec != 'bdy[1]' :
                        index[word][docno].add('/bdy[1]/' + sec + '/' + p)
                        term_frequency[word][docno] += 1
                    else :
                        index[word][docno].add(sec + '/' + p)
                        term_frequency[word][docno] += 1

    index = dict(sorted(index.items()))
    term_frequency = dict(sorted(term_frequency.items()))

    return index, term_frequency

def statistics_tags(index, term_frequency):
 
    start = time.time()
    doc_lengths = defaultdict(int)
    for term, postings_list in index.items():
        for docno in postings_list.keys() :
            doc_lengths [docno] += term_frequency[term][docno]

    vocabulary_size = len(index)

    collection_frequencies = defaultdict(int)
    for term, postings_list in index.items():
        collection_frequencies[term] = len(postings_list)
    
    end = time.time()
    statistics_execution_time = end - start

    return doc_lengths, vocabulary_size, collection_frequencies, statistics_execution_time
