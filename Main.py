# Importing the re library to make some regex manipulation, the time libary to mesure the execution time, the pyplot
# to build graphycs, and all the functions from the file file_process that we created.

from file_process import *
from traitement_file import *
from files_maneg import *
import copy

############################################################################# Functions ##################################################################

# Function to measure execution time and index the file
def process_file(file_path):
    process=file_processing(file_path)  
          
    return process

# Function to process the deleted stop words new index list
def stopwords_process(process, stop_list):
    post_process = stop_word_processing(process, stop_list)
    return post_process

# Function to stem the new index list
def stem_process(process):
    post_process=stemmer(process[0],process[1])
    return post_process


############################################################################# Main #######################################################################

# A list that will contain all the collection paths
file_path = "Text_Only_Ascii_Coll_NoSem"

# Building the stop words list
stop_list = stop_words()
stop_len=len(stop_list) -1

result = ()
n=0
dl=defaultdict(int)
avdl = 0

################################################################## Indexation #############################################################################

process_result = process_file(file_path)

index_result=process_result

result = copy.deepcopy(index_result)

doc_lengths = statistics(process_result[0], process_result[1])

n = len(doc_lengths)

#index_txt(result[0], result[1])

################################################################## Quey evaluation ######################################################################## 

run_index=1

run=int(input("Choose wich weigthing function you want to run :\n 1. Smart Ltn\n 2. Smart Ltc\n 3. BM25\n 4. To exit\n"))

while (run != 4) :

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

    doc_lengths = statistics(result[0], result[1])

    avdl= sum(doc_lengths.values()) / n

    dl=doc_lengths

    ################################################################## Quey preparation ########################################################################

    all_querys = defaultdict(str)

    with open('querys.txt', 'r') as allquerys :
        for query in allquerys:
            query_components = query.strip().split(maxsplit=1)
            query_id, query_text = query_components
            all_querys[query_id] = (query_text)

    if (run==1):

    ################################################################## Smart ltn processing ###################################################################

        smart_ltn=smart_ltn_weighting(result[0], result[1],n)

        #index_txt_smart_ltn(result[0],smart_ltn,run_index)

    ################################################################## Query processing for Smart ltn #########################################################

        for query_id, query in all_querys.items() :

            eval = evaluate_query(query, smart_ltn)

            top_1500_docs = list(eval.items())[:1500]

            export_file(top_1500_docs, query_id, run_index, "ltn", "article",stop_d, stem_d, 'noparameters')

            #query_result(top_1500_docs,run_index, query_id)


    if (run==2):
    ################################################################## Smart ltc processing ###################################################################

        smart_ltn=smart_ltn_weighting(result[0], result[1],n)
        
        smart_ltc=smart_ltc_weighting(smart_ltn)

        #index_txt_smart_ltc(result[0],smart_ltc,run_index)

    ################################################################## Query processing for Smart ltc #########################################################

        for query_id, query in all_querys.items() :

            eval = evaluate_query(query, smart_ltc)

            top_1500_docs = list(eval.items())[:1500]

            export_file(top_1500_docs, query_id, run_index, "ltc", "article",stop_d, stem_d, 'noparameters')

            #query_result(top_1500_docs,run_index, query_id)



    if (run == 3):

        k = float(input("Enter the value of k : "))

        b = float(input("Enter the value of b : "))

    ################################################################## BM25 processing ########################################################################

        BM25 = BM25_weighting(result[0], result[1], n, k, b, avdl, dl)

        #index_txt_BM25(result[0],BM25,run_index)

    ################################################################## Query processing for BM25 ###############################################################

        for query_id, query in all_querys.items() :

            eval = evaluate_query(query, BM25)

            top_1500_docs = list(eval.items())[:1500]

            export_file(top_1500_docs, query_id, run_index, "BM25", "article",stop_d, stem_d, {'k':k, 'b':b})

            #query_result(top_1500_docs,run_index, query_id)

    
    run_index+=1

    result = copy.deepcopy(index_result)

    run=int(input("Choose wich weigthing function you want to run :\n 1. Smart Ltn\n 2. Smart Ltc\n 3. BM25\n 4. To exit\n"))