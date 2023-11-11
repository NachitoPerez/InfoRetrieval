# Importing the re library to make some regex manipulation, the time libary to mesure the execution time, the pyplot
# to build graphycs, and all the functions from the file file_process that we created.

from file_process import *
from traitement_file import *
from files_maneg import *

#-------------------------------------------- Functions --------------------------------------------------------------------

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


#----------------------------------------------- Main --------------------------------------------------------------------

# A list that will contain all the collection paths
all_paths=[]
with open('paths.txt', 'r') as allpaths :
    for path in allpaths:
        all_paths.append(path.strip())

# Building the stop words list
stop_list = stop_words()

result = ()
n=0
dl=defaultdict(int)
avdl = 0

################################################################## EXERCICE 1 & 2 ##################################################################

# Loop over different sizes of collections
for file_path in all_paths:
    process_result = process_file(file_path)
    result=process_result
    doc_lengths, vocabulary_size, collection_frequencies = statistics(process_result[0], process_result[1])
    n = len(doc_lengths)
    index_txt(process_result[0], process_result[1])

################################################################## EXERCICE 3 ##################################################################

# Stop words and Stemming
for file_path in all_paths:

    process_result_stop_words = stopwords_process(result, stop_list)
    process_result_stem = stem_process(process_result_stop_words)

    result=process_result_stem
    doc_lengths, vocabulary_size, collection_frequencies = statistics(process_result_stem[0], process_result_stem[1])

    avdl= sum(doc_lengths.values()) / n

    dl=doc_lengths

    index_txt_no_stop_words_stem(result[0], result[1])

################################################################## EXERCICE 4 ##################################################################

smart_ltn=smart_ltn_weighting(result[0], result[1],n)

index_txt_smart_ltn(result[0],smart_ltn)

################################################################## EXERCICE 5 ##################################################################

query = "olive oil health benefit"

eval = evaluate_query(query, smart_ltn)

top_1500_docs = list(eval.items())[:1500]

################################################################## EXERCICE 6 ##################################################################

smart_ltc=smart_ltc_weighting(smart_ltn)

index_txt_smart_ltc(result[0],smart_ltc)

################################################################## EXERCICE 7 ##################################################################

eval = evaluate_query(query, smart_ltc)

top_1500_docs = list(eval.items())[:1500]

################################################################## EXERCICE 8 ##################################################################

BM25 = BM25_weighting(result[0], result[1], n, 1.2, 0.69, avdl, dl)

index_txt_BM25(result[0],BM25)

################################################################## EXERCICE 9 ##################################################################

eval = evaluate_query(query, BM25)

top_1500_docs = list(eval.items())[:1500]