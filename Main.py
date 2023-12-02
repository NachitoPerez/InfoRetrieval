# Importing the re library to make some regex manipulation, the time libary to mesure the execution time, the pyplot
# to build graphycs, and all the functions from the file file_process that we created.

from BM25_tuning import BM25_tuning
from file_process import *
from file_process_xml import *
from traitement_file import *
from files_maneg import *
import copy
import os
import time

############################################################################# Functions ##################################################################

# Function to measure execution time and index the file
def process_file(file_path):
    
    start_in = time.time()

    process = file_processing(file_path)  
    
    end_in = time.time()

    execution_time = end_in - start_in
          
    return execution_time, process

# Function to measure execution time and index the file with tags
def process_file_tags(files_paths):
    
    start_in = time.time()

    process = ({},{})
    i=0
    for path in files_paths :
        process = file_processing_tags(path, process)  
        i+=1
        print(i)
    
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
def stem_process_tags(process):
    post_process=stemmer(process[0],process[1])
    return post_process

def get_run_counter():
    counter_file_path = 'utils/run_counter.txt'

    # Check if the counter file exists
    if not os.path.exists(counter_file_path):
        # If not, create the file and initialize the counter to 1
        with open(counter_file_path, 'w') as counter_file:
            counter_file.write('1')
        return 1

    # If the file exists, read the counter value and increment it
    with open(counter_file_path, 'r') as counter_file:
        counter = int(counter_file.read())
        counter += 1    

    return counter

def update_counter(new_counter:int):
    counter_file_path = 'utils/run_counter.txt'
    
    with open(counter_file_path, 'w') as counter_file:
        counter_file.write(str(new_counter))

############################################################################# Main #######################################################################

# A list that will contain all the collection paths

start_xml_comb_files=time.time()

XML_files_path_base = "utils/XML_Coll_withSem/"

XML_files_paths=set()

for xml_doc in os.listdir(XML_files_path_base):
    if xml_doc.endswith(".xml"):
        XML_path = os.path.join(XML_files_path_base, xml_doc)
        XML_files_paths.add(XML_path)

Combine_files_txt(XML_files_paths)

Combine_files_xml(XML_files_paths)

end_xml_comb_files=time.time()
Comb_time = end_xml_comb_files-start_xml_comb_files

print("Execution time to generate a txt doc that contains all the xml documents is : ", Comb_time, ' s')

# Building the stop words list
stop_list = stop_words()
stop_len=len(stop_list) -1

result = ()
n=0
dl=defaultdict(int)
avdl = 0

################################################################## Indexation #############################################################################
index_d=int(input("Choose which indexing function you want to run :\n 1. Without XML tags\n 2. With XML tags\n"))

while (index_d > 0 and index_d < 3) :

    if index_d == 1 :
        execution_time, process_result = process_file('utils/Combined_XML_files.txt')

        print("Execution time of the indixation is :", execution_time, 's\n')

        print ('---------------------------------------- without pre-treatment ----------------------------------------\n')

        index_result=process_result

        result = copy.deepcopy(index_result)

        doc_lengths, vocabulary_size, collection_frequencies, statistics_execution_time = statistics(process_result[0], process_result[1])
        n = len(doc_lengths)
            
        print("Statistics : \n")
        print("Execution time of the statistical calculations :", statistics_execution_time, 's\n')
        print (f'The avrege length of a document in the {n} document collection is : ', sum(doc_lengths.values()) / len(doc_lengths), 'Word/Document') # Average document length of a collection
            
        print('The size of the vocabulary of the collection is : ', vocabulary_size, 'Word')  # Vocabulary size of a collection
            
        avg=sum(collection_frequencies.values()) / len(collection_frequencies)
        print ('The avrege collection frequency of a term in the collection is : ', avg,' Time\n') # Average collection frequency of terms of a collection

        #index_txt(result[0], result[1])

    if index_d == 2 :

        execution_time, process_result = process_file_tags(XML_files_paths)

        print("Execution time of the indixation is :", execution_time, 's\n')

        print ('---------------------------------------- without pre-treatment ----------------------------------------\n')

        index_result=process_result

        result = copy.deepcopy(index_result)

        doc_lengths, vocabulary_size, collection_frequencies, statistics_execution_time = statistics_tags(process_result[0], process_result[1])
        n = len(doc_lengths)
            
        print("Statistics : \n")
        print("Execution time of the statistical calculations :", statistics_execution_time, 's\n')
        print (f'The avrege length of a document in the {n} document collection is : ', sum(doc_lengths.values()) / len(doc_lengths), 'Word/Document') # Average document length of a collection
            
        print('The size of the vocabulary of the collection is : ', vocabulary_size, 'Word')  # Vocabulary size of a collection
            
        avg=sum(collection_frequencies.values()) / len(collection_frequencies)
        print ('The avrege collection frequency of a term in the collection is : ', avg,' Time\n') # Average collection frequency of terms of a collection
    
    index_d=int(input("Choose which indexing function you want to run :\n 1. Without XML tags\n 2. With XML tags\n"))


################################################################## Quey evaluation ######################################################################## 

print ('---------------------------------------- Quey evaluation ----------------------------------------\n')

run=int(input("Choose which weigthing function you want to run :\n 1. Smart Ltn\n 2. Smart Ltc\n 3. BM25\n 4. BM25 Tuning\n 0. To exit\n"))

while (run > 0 and run < 5) :
    
    # Get the current run counter
    run_index = get_run_counter()

################################################################## stemming & stop words ##################################################################

    stop_des = int(input("Do you want to remove the stop words :\n1. Yes\n2. No\n"))

    if (stop_des == 1):
        stop_d=f"stop{stop_len}"
        process_result_stop_words = stopwords_process(result, stop_list)
        result = process_result_stop_words
        #index_txt_no_stop_words_stem(result[0], result[1])

    else :
        stop_d="nostop"

    stem_des = int(input("Do you want to stem the tokens :\n1. Yes\n2. No\n"))

    if (stem_des == 1):
        stem_d="porter"
        process_result_stem = stem_process(result)
        result = process_result_stem
        #index_txt_no_stop_words_stem(result[0], result[1])

    else :
        stem_d="nostem"

    doc_lengths, vocabulary_size, collection_frequencies, statistics_execution_time = statistics(result[0], result[1])

    print("Statistics : \n")
    print("Execution time of the statistical calculations :", statistics_execution_time, 's\n')
    print (f'The avrege length of a document in the {n} document collection is : ', sum(doc_lengths.values()) / len(doc_lengths), 'Word/Document') # Average document length of a collection
    
    print('The size of the vocabulary of the collection is : ', vocabulary_size, 'Word')  # Vocabulary size of a collection
    
    avg=sum(collection_frequencies.values()) / len(collection_frequencies)
    print ('The avrege collection frequency of a term in the collection is : ', avg,' Time\n') # Average collection frequency of terms of a collection

    avdl= sum(doc_lengths.values()) / n

    dl=doc_lengths

    ################################################################## Quey preparation ########################################################################

    all_querys = defaultdict(str)

    with open('utils/querys.txt', 'r') as allquerys :
        for query in allquerys:
            query_components = query.strip().split(maxsplit=1)
            query_id, query_text = query_components
            all_querys[query_id] = (query_text)

    if (run==1):

    ################################################################## Smart ltn processing ###################################################################

        start = time.time()
        smart_ltn=smart_ltn_weighting(result[0], result[1],n)
        end = time.time()

        Smart_ltn_execution_time = end-start

        print("Execution time of the SMART_ltn calculations :", Smart_ltn_execution_time, 's\n')

        #index_txt_smart_ltn(result[0],smart_ltn,run_index)

    ################################################################## Query processing for Smart ltn #########################################################

        for query_id, query in all_querys.items() :

            eval = evaluate_query(query, smart_ltn, stem_d, stop_list)

            top_1500_docs = list(eval.items())[:1500]

            export_file(top_1500_docs, query_id, run_index, "ltn", "article",stop_d, stem_d, 'noparameters')

            #query_result(top_1500_docs,run_index, query_id)

    if (run==2):
    ################################################################## Smart ltc processing ###################################################################

        start = time.time()
        smart_ltn=smart_ltn_weighting(result[0], result[1],n)

        smart_ltc=smart_ltc_weighting(smart_ltn)
        end = time.time()

        Smart_ltc_execution_time = end-start

        print("Execution time of the SMART_ltc calculations :", Smart_ltc_execution_time, 's\n')
        #index_txt_smart_ltc(result[0],smart_ltc,run_index)

    ################################################################## Query processing for Smart ltc #########################################################

        for query_id, query in all_querys.items() :

            eval = evaluate_query(query, smart_ltc, stem_d, stop_list)

            top_1500_docs = list(eval.items())[:1500]

            export_file(top_1500_docs, query_id, run_index, "ltc", "article",stop_d, stem_d, 'noparameters')

            #query_result(top_1500_docs,run_index, query_id)

    if (run == 3):
        k = float(input("Enter the value of k : "))

        b = float(input("Enter the value of b : "))

    ################################################################## BM25 processing ########################################################################

        start = time.time()
        BM25 = BM25_weighting(result[0], result[1], n, k, b, avdl, dl)
        end = time.time()

        BM25_execution_time = end-start

        print("Execution time of the BM25 calculations :", BM25_execution_time, 's\n')

    ################################################################## Query processing for BM25 ###############################################################

        for query_id, query in all_querys.items() :

            eval = evaluate_query(query, BM25, stem_d, stop_list)

            top_1500_docs = list(eval.items())[:1500]

            export_file(top_1500_docs, query_id, run_index, "BM25", "article",stop_d, stem_d, {'k':k, 'b':b})
            
    if (run == 4):

        start = time.time()
        BM25_tuning(result=result, n=n, dl=dl, avdl=avdl, all_querys=all_querys, stem_d=stem_d, stop_list=stop_list, stop_d=stop_d)
        run_index -= 1    

        end = time.time()

        BM25_tunning_execution_time = end-start

        print("Execution time of the tuned BM25 calculations :", BM25_tunning_execution_time, 's\n')

    result = copy.deepcopy(index_result)
    
    update_counter(run_index)

    run=int(input("Choose which weigthing function you want to run :\n 1. Smart Ltn\n 2. Smart Ltc\n 3. BM25\n 4. BM25 Tuning\n 0. To exit\n"))