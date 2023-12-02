import xml.etree.ElementTree as ET
import re
import os

# This file contains two functions, the first one exports the Indexes in a text file with a similar format
# to the one in the index_printing function. The seconde one outputs a text file that contains the indexex in the
# same type of the varibale "idex" (dictionary).

def index_txt(index, term_frequency):    
    with open('index_collection.txt', 'w') as file:
        for term, postings_list in index.items():
            df = len(postings_list)
            file.write(f"{df}=df({term})\n")
            for word in postings_list:
                file.write(f"{term_frequency[term][word]} {word}\n")

def index_txt_smart_ltn(index, term_frequency,run_index):
    with open(f'index_collection_smart_ltn_{run_index}.txt', 'w') as file:
        for term, postings_list in index.items():
            df = len(postings_list)
            file.write(f"{df}=df({term})\n")
            for word in postings_list:
                file.write(f"{term_frequency[term][word]} {word}\n")
                

def index_txt_no_stop_words_stem(index, term_frequency):
    with open('index_collection_no_stop_words_stem.txt', 'w') as file:
        for term, postings_list in index.items():
            df = len(postings_list)
            file.write(f"{df}=df({term})\n")
            for word in postings_list:
                file.write(f"{term_frequency[term][word]} {word}\n")

def index_txt_smart_ltc(index, term_frequency,run_index):
    with open(f'index_collection_smart_ltc_{run_index}.txt', 'w') as file:
        for term, postings_list in index.items():
            df = len(postings_list)
            file.write(f"{df}=df({term})\n")
            for word in postings_list:
                file.write(f"{term_frequency[term][word]} {word}\n")

def index_txt_BM25(index, term_frequency,run_index):
    with open(f'index_collection_BM25_{run_index}.txt', 'w') as file:
        for term, postings_list in index.items():
            df = len(postings_list)
            file.write(f"{df}=df({term})\n")
            for word in postings_list:
                file.write(f"{term_frequency[term][word]} {word}\n")

def export_file(doc_list, query_id, run_id, weighting_function, granularity,stop, stem, parameters):
    if list is None :
        exit
    
    if parameters != 'noparameters' :
        parm = ''
        for key, value in parameters.items():
            parm += f"_{key}{value}"
    else:
        parm = '_'+parameters


    with open(f'SaadZakariaBadreddineIgnacio_{run_id}_{weighting_function}_{granularity}_{stop}_{stem}{parm}.txt', 'a') as file:
        for i in range(0, len(doc_list)):        
            file.write(f"{query_id} Q0 {doc_list[i][0]} {i+1} {doc_list[i][1]} SaadZakariaBadreddineIgnacio /article[1]\n")

def query_result(doc_list,run_id, query_id):
     with open(f'query_result_{run_id}_Q_{query_id}.txt', 'w') as file:
        file.write("____________________________________\n")
        file.write("|      docno      |      score      |\n")
        for i in range(0,len(doc_list)):
            file.write("____________________________________\n")
            file.write(f"|   {doc_list[i][0]}  |      {doc_list[i][1]}    |\n")
            file.write("____________________________________\n")

def Combine_files (file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    pattern = re.compile(r'&[^;]+;')
    xml_content = re.sub(pattern, '', xml_content)
    
    root = ET.fromstring(xml_content)

    id_element = root.find('.//id')

    docno = id_element.text

    doc = ET.tostring(root, encoding='unicode', method='text').strip().replace('\n', ' ')

    docnos=[]

    if os.path.exists('utils/Combined_XML_files.txt') :
        
        with open('utils/Combined_XML_files.txt', 'r', encoding='utf-8') as file:

            docs = file.read()
            docnos_find= re.findall(r'<doc><docno>.*?</docno>', docs, re.DOTALL)
            for i in docnos_find : 
                search=re.search(r'<doc><docno>(.*?)</docno>', i, re.DOTALL)
                docnos.append(search.group(1))
            file.close()

    with open('utils/Combined_XML_files.txt', 'a', encoding='utf-8') as file:
        if docno not in docnos :
            file.write("<doc><docno>" + docno + '</docno>\n')
            file.write(doc + '\n')
            file.write('</doc>\n')
        file.close()

