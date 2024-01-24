# Importing the re library to make some regex manipulation, the time libary to mesure the execution time, the pyplot
# to build graphycs, and all the functions from the file file_process that we created.

from file_process import *
from file_process_xml import *
from traitement_file import *
from traitement_file_sec import *
import time

############################################################################# Functions to index , stop, stemming ##################################################################

# Function to measure execution time and index the file
def process_file(file_path):
    
    start_in = time.time()

    process = file_processing(file_path)  
    
    end_in = time.time()

    execution_time = end_in - start_in
          
    return execution_time, process

# Function to measure execution time and index the file with tags
def process_file_tags(files_path):
    
    start_in = time.time()

    process = file_processing_tags(files_path)  
    
    end_in = time.time()

    execution_time = end_in - start_in
          
    return execution_time, process

# Function to process the deleted stop words new index list
def stopwords_process(process, stop_list):
    post_process = stop_word_processing(process, stop_list)
    return post_process

# Function to stem the new index list
def stem_process(process):
    post_process=stemmer(process[0],process[1])
    return post_process

# Function to stem the new index list with tags
def stem_process_tag(process):
    post_process=stemmer_tag(process[0],process[1])
    return post_process

# Function that combines all the xml files
def combine_XML_files():

    XML_files_path_base = "utils/XML_Coll_withSem/"

    XML_files_paths=set()

    for xml_doc in os.listdir(XML_files_path_base):
        if xml_doc.endswith(".xml"):
            XML_path = os.path.join(XML_files_path_base, xml_doc)
            XML_files_paths.add(XML_path)

    start_xml_comb_files=time.time()

    Combine_files_txt(XML_files_paths) #Generate the txt file of all the XML docs without taking the tags into consideration

    end_xml_comb_files=time.time()
    Comb_time = end_xml_comb_files-start_xml_comb_files

    start_xml_comb_files_tag=time.time()

    Combine_files_xml(XML_files_paths) #Generate the txt file of all the XML docs wiht taking the tags into consideration

    end_xml_comb_files_tag=time.time()
    Comb_time_tag = end_xml_comb_files_tag-start_xml_comb_files_tag

    print("Execution time to generate the txt files that contains all the xml documents without taking xml tags into consideration is : ", Comb_time, ' s\n')
    print("Execution time to generate the txt files that contains all the xml documents with taking xml tags into consideration is : ", Comb_time_tag, ' s\n')

# Function to generate index dictios and export them into JSON files.
def index_creator(stop_list):
    ################################################################## Indexation #############################################################################

    ################################################################## No XML Tags #############################################################################

    execution_time, process_result = process_file('utils/Combined_XML_files.txt')

    doc_lengths = doc_length(process_result[0], process_result[1])

    print("Execution time of the indixation without xml tags is :", execution_time, 's\n')

    lengths_dict = defaultdict(lambda: defaultdict(int))

    lengths_dict["none"] = doc_lengths

    process_result_stem = stem_process(process_result)
    doc_lengths_stem = doc_length(process_result_stem[0], process_result_stem[1])
    lengths_dict["stem"] = doc_lengths_stem
    
    process_result_stop_words = stopwords_process(process_result, stop_list)
    doc_lengths_stop_words = doc_length(process_result_stop_words[0], process_result_stop_words[1])
    lengths_dict["stop"] = doc_lengths_stop_words

    process_result_stop_words_stem = stem_process(process_result_stop_words)
    doc_lengths_stop_words_stem = doc_length(process_result_stop_words_stem[0], process_result_stop_words_stem[1])
    lengths_dict["stop_stem"] = doc_lengths_stop_words_stem

    export_doc_lenghts(lengths_dict, "no_tag")

    execution_time, process_result = process_file('utils/Combined_XML_files.txt')

    querys_words = []

    with open('utils/querys.txt', 'r') as allquerys :
        for query in allquerys:
            query_components = query.strip().split(maxsplit=1)
            query_id, query_text = query_components
            querys_words.append(query_text.strip().split())

    index = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
    term_f = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))

    for word_list in querys_words:
        for word in word_list:
            for dic_words in process_result[0].keys():
                if word == dic_words:
                    index[word] = process_result[0][word]
                    term_f[word] = process_result[1][word]

    index_result = (index, term_f)

    print("============================= Creating the multiple indexes dictionaries : ============================= \n")

    print("index dic created")
    export_index(index_result[0],index_result[1],"initial")
    print("index dic exported\n")

    st=time.time()
    process_result_stem = stem_process(index_result)
    fn=time.time()
    print("stem dic created in ", fn-st)
    export_index(process_result_stem[0], process_result_stem[1],"stemed_with_stop_words")
    print("stem dic exported\n")

    st=time.time()
    process_result_stop_words = stopwords_process(index_result, stop_list)
    fn=time.time()
    print("stop dic created in ", fn-st)
    export_index(process_result_stop_words[0], process_result_stop_words[1], "without_stop_words")
    print("stop dic exported\n")

    st=time.time()
    process_result_stop_words_stem = stem_process(process_result_stop_words)
    fn=time.time()
    print("stopstem dic created in ", fn-st)
    export_index(process_result_stop_words_stem[0], process_result_stop_words_stem[1], "stemed_without_stop_words")
    print("stopstem dic exported\n")

    ################################################################## XML Tags #############################################################################

    execution_time_tag, process_result_tag = process_file_tags('utils/Combined_XML.txt')

    doc_lengths_tag = doc_length_tag(process_result_tag[0], process_result_tag[1])

    print("Execution time of the indixation without xml tags is :", execution_time_tag, 's\n')

    lengths_dict_tag = defaultdict(lambda: defaultdict(int))

    lengths_dict_tag["none"] = doc_lengths_tag

    process_result_stem_tag = stem_process_tag(process_result_tag)
    doc_lengths_stem_tag = doc_length_tag(process_result_stem_tag[0], process_result_stem_tag[1])
    lengths_dict_tag["stem"] = doc_lengths_stem_tag
    
    process_result_stop_words_tag = stopwords_process(process_result_tag, stop_list)
    doc_lengths_stop_words_tag = doc_length_tag(process_result_stop_words_tag[0], process_result_stop_words_tag[1])
    lengths_dict_tag["stop"] = doc_lengths_stop_words_tag

    process_result_stop_words_stem_tag = stem_process_tag(process_result_stop_words_tag)
    doc_lengths_stop_words_stem_tag = doc_length_tag(process_result_stop_words_stem_tag[0], process_result_stop_words_stem_tag[1])
    lengths_dict_tag["stop_stem"] = doc_lengths_stop_words_stem_tag

    export_doc_lenghts(lengths_dict_tag, "tag")

    execution_time_tag, process_result_tag = process_file_tags('utils/Combined_XML.txt')

    querys_words = []

    with open('utils/querys.txt', 'r') as allquerys :
        for query in allquerys:
            query_components = query.strip().split(maxsplit=1)
            query_id, query_text = query_components
            querys_words.append(query_text.strip().split())

    index_tag = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
    term_fr_tag = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))

    for word_list in querys_words:
        for word in word_list:
            for dic_words in process_result_tag[0].keys():
                if word in dic_words:
                    index_tag[word] = process_result_tag[0][word]
                    term_fr_tag[word] = process_result_tag[1][word]

    index_result_tag = (index_tag, term_fr_tag)

    print("============================= Creating the multiple indexes dictionaries : ============================= \n")

    print("index dic created")
    export_index(index_result_tag[0],index_result_tag[1],"initial_tag")
    print("index dic exported\n")

    st=time.time()
    process_result_stem_tag = stem_process_tag(index_result_tag)
    fn=time.time()
    print("stem dic created in ", fn-st)
    export_index(process_result_stem_tag[0], process_result_stem_tag[1], "stemed_with_stop_words_tag")
    print("stem dic exported\n")

    st=time.time()
    process_result_stop_words_tag = stopwords_process(index_result_tag, stop_list)
    fn=time.time()
    print("stop dic created in ", fn-st)
    export_index(process_result_stop_words_tag[0],process_result_stop_words_tag[1],"without_stop_words_tag")
    print("stop dic exported\n")

    st=time.time()
    process_result_stop_words_stem_tag = stem_process_tag(process_result_stop_words_tag)
    fn=time.time()
    print("stopstem dic created in ", fn-st)
    export_index(process_result_stop_words_stem_tag[0],process_result_stop_words_stem_tag[1], "stemed_without_stop_words_tag")
    print("stopstem dic exported\n")