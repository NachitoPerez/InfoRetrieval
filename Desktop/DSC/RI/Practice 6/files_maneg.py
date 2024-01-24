import xml.etree.ElementTree as ET
import re
import os
import json

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
            file.write(f"{query_id} Q0 {doc_list[i][0]} {i+1} {doc_list[i][2]} SaadZakariaBadreddineIgnacio {doc_list[i][1]}\n")

def export_file_tag(doc_list, query_id, run_id, weighting_function, granularity,stop, stem, parameters):
    if doc_list is None :
        exit
    
    if parameters != 'noparameters' :
        parm = ''
        for key, value in parameters.items():
            parm += f"_{key}{value}"
    else:
        parm = '_'+parameters


    with open(f'SaadZakariaBadreddineIgnacio_{run_id}_{weighting_function}_{granularity}_{stop}_{stem}{parm}.txt', 'a') as file:
        for i in range(0, len(doc_list)):        
            file.write(f"{query_id} Q0 {doc_list[i][0]} {i+1} {doc_list[i][2]} SaadZakariaBadreddineIgnacio {doc_list[i][1]}\n")

def query_result(doc_list,run_id, query_id):
     with open(f'query_result_{run_id}_Q_{query_id}.txt', 'w') as file:
        file.write("____________________________________\n")
        file.write("|      docno      |      score      |\n")
        for i in range(0,len(doc_list)):
            file.write("____________________________________\n")
            file.write(f"|   {doc_list[i][0]}  |      {doc_list[i][1]}    |\n")
            file.write("____________________________________\n")

def Combine_files_txt (XML_files_paths):

    docnos=[]

    if os.path.exists('utils/Combined_XML_files.txt') and len(docnos)<9804 :
        
        with open('utils/Combined_XML_files.txt', 'r', encoding='utf-8') as file:

            docs = file.read()
            docnos_find= re.findall(r'<doc><docno>.*?</docno>', docs, re.DOTALL)
            for i in docnos_find : 
                search=re.search(r'<doc><docno>(.*?)</docno>', i, re.DOTALL)
                docnos.append(search.group(1))
            file.close()

    for file_path in XML_files_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            xml_content = file.read()

        pattern = re.compile(r'&[^;]+;')
        xml_content = re.sub(pattern, '', xml_content)
        
        root = ET.fromstring(xml_content)

        id_element = root.find('.//id')

        docno = id_element.text

        doc = ET.tostring(root, encoding='unicode', method='text').strip().replace('\n', ' ')

        with open('utils/Combined_XML_files.txt', 'a', encoding='utf-8') as file:
            if docno not in docnos :
                docnos.append(docno)
                file.write("<doc><docno>" + docno + '</docno>\n')
                file.write(doc + '\n')
                file.write('</doc>\n')
            file.close()

def Combine_files_xml (XML_files_paths):

    docnos=[]

    if os.path.exists('utils/Combined_XML.txt') and len(docnos)<9804:
        
        with open('utils/Combined_XML.txt', 'r', encoding='utf-8') as file:

            docs = file.read()
            docnos_find= re.findall(r'<doc><docno>.*?</docno>', docs, re.DOTALL)
            for i in docnos_find : 
                search=re.search(r'<doc><docno>(.*?)</docno>', i, re.DOTALL)
                docnos.append(search.group(1))
            file.close()

    for xml_file in XML_files_paths:

        with open(xml_file, 'r', encoding='utf-8') as file:
            xml_content = file.read()

        pattern = re.compile(r'&[^;]+;')
        xml_content = re.sub(pattern, '', xml_content)
    
        root = ET.fromstring(xml_content)

        id_element = root.find('.//id')

        docno = id_element.text

        with open('utils/Combined_XML.txt', 'a', encoding='utf-8') as file:
            if docno not in docnos :
                docnos.append(docno)
                file.write("<doc><docno>" + docno + '</docno>\n')

                for element in root.findall(".//title"):
                    content = ET.tostring(element, encoding='unicode', method='text').strip().replace('\n', '')
                        
                    file.write('<'+ element.tag + '> ')
                    file.write(content)
                    file.write(' </'+ element.tag + '>' + '\n')

                for element in root.findall(".//bdy/*"):
                    if element.tag == 'p':

                        content = ET.tostring(element, encoding='unicode', method='text').strip().replace('\n', ' ')
                        
                        file.write('<'+ element.tag + '>' + '\n')
                        file.write(content + '\n')
                        file.write('</'+ element.tag + '>' + '\n')
                    elif element.tag == 'sec':
                        file.write('<'+ element.tag + '>' + '\n')
                        for paragraph in element.findall(".//p"):
                            
                            content = ET.tostring(paragraph, encoding='unicode', method='text').strip().replace('\n', ' ')
                        
                            file.write('<p>' + '\n')
                            file.write(content + '\n')
                            file.write('</p>' + '\n')
                        file.write('</'+ element.tag + '>' + '\n')

                file.write('</doc>\n')    

def convert_sets_to_lists(obj):
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {key: convert_sets_to_lists(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_sets_to_lists(element) for element in obj]
    else:
        return obj
    
def export_doc_lenghts(doc_lengths, dic_name):

    doc_lengths_dict = dict(doc_lengths)
    with open(f'utils/doc_lengths_{dic_name}.json', 'w', encoding="utf-8") as file:
        json.dump(doc_lengths_dict, file, indent=2)

def export_index(index, term_frequency, dic_name):

    index_dict = convert_sets_to_lists(dict(index))
    term_frequency_dict = dict(term_frequency)

    with open(f'utils/index_{dic_name}.json', 'w', encoding="utf-8") as file:
        json.dump(index_dict, file, indent=2)

    with open(f'utils/term_frequency_{dic_name}.json', 'w', encoding="utf-8") as file:
        json.dump(term_frequency_dict, file, indent=2)

# Fonction pour convertir list to set inside the index

def convert_lists_to_sets(obj):
    if isinstance(obj, list):
        return set(obj)
    elif isinstance(obj, dict):
        return {key: convert_lists_to_sets(value) for key, value in obj.items()}
    else:
        return obj

def import_index(index_name):
    with open(f'utils/index_{index_name}.json', 'r') as json_file_in:
        data_in = json.load(json_file_in, object_hook=convert_lists_to_sets)

    #index_dictio = dict_to_defaultdict(data_in)

    with open(f'utils/term_frequency_{index_name}.json', 'r') as json_file_tf:
        data_tf = json.load(json_file_tf)

    #tf_dictio = dict_to_defaultdict(data_tf)

    result=(data_in, data_tf)

    return(result)

def import_doc_lengths(dic_name):
    with open(f'utils/doc_lengths_{dic_name}.json', 'r') as json_file_in:
        data_in = json.load(json_file_in)

    return(data_in)