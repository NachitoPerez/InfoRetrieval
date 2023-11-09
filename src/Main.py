# Importing the re library to make some regex manipulation, the time libary to mesure the execution time, the pyplot
# to build graphycs, and all the functions from the file file_process that we created.

import matplotlib.pyplot as plt
from file_process import *
from traitement_file import *
from files_maneg import *

#-------------------------------------------- Functions --------------------------------------------------------------------

# Function to measure execution time and index the file
def process_file(file_path):
    process=file_processing(file_path)  
    execution_time = process[2]
          
    return execution_time, process

# Function to process the deleted stop words new index list
def stopwords_process(process, stop_list):
    post_process = stop_word_processing(process, stop_list)
    return post_process

# Function to stem the new index list
def stem_process(process):
    post_process=stemmer(process[0],process[1])
    return post_process

# Plotting the evolution of statistics
def statistics_plotting(doc_length, vocabulary_size_list, collection_frequencies):
    plt.figure(figsize=(12, 10))

    plt.subplot(2,1,1)
    plt.bar(doc_length.keys(), doc_length.values(), color='b', width=0.1)
    plt.xlabel('Document number (docno)')
    plt.ylabel('Document Length (Word)')
    plt.title('Documents Lengths of the collection')
    plt.grid(True)

    plt.subplot(2,2,3)
    rang = list(range(1, len(vocabulary_size_list) + 1))
    plt.bar(rang, vocabulary_size_list, color='r', width=0.1)
    plt.xlim(0, 3)
    plt.xlabel('Vocabulary number')
    plt.ylabel('Vocabulary Size')
    plt.title('Vocabulary Size befor (1) and after (2) processing')
    plt.grid(True)
    
    plt.subplot(2, 2, 4)
    rang = list(range(1, len(collection_frequencies) + 1))
    plt.bar(rang, collection_frequencies, color='g', width=0.1)
    plt.xlim(0, 3)
    plt.xlabel('terms')
    plt.ylabel('Collection Frequency of Terms number')
    plt.title('Average Collection Frequency of Terms in the collection befor (1) and after (2) processing')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

#----------------------------------------------- Main --------------------------------------------------------------------

# A list that will contain all the collection paths
all_paths=[]
with open('paths.txt', 'r') as allpaths :
    for path in allpaths:
        all_paths.append(path.strip())

# Building the stop words list
stop_list = stop_words()

result = ()
doc_lengths_list = []
vocabulary_size_list = []
collection_frequencies_list = []
n=0
dl=defaultdict(int)
avdl = 0

################################################################## EXERCICE 1 & 2 ##################################################################

print("Exercice 1 & 2 :\n")
print ('---------------------------------------- without pre-treatment ----------------------------------------\n')
# Loop over different sizes of collections
for file_path in all_paths:
    execution_time, process_result = process_file(file_path)
    result=process_result
    doc_lengths, vocabulary_size, collection_frequencies, statistics_execution_time = statistics(process_result[0], process_result[1])
    n = len(doc_lengths)
    
    print("Statistics : \n")
    print("Execution time of the statistical calculations :", statistics_execution_time, 's\n')
    print (f'The avrege length of a document in the {n} document collection is : ', sum(doc_lengths.values()) / len(doc_lengths), 'Word/Document') # Average document length of a collection
    doc_lengths_list.append(doc_lengths)
    
    print('The size of the vocabulary of the collection is : ', vocabulary_size, 'Word')  # Vocabulary size of a collection
    vocabulary_size_list.append(vocabulary_size)  
    
    avg=sum(collection_frequencies.values()) / len(collection_frequencies)
    print ('The avrege collection frequency of a term in the collection is : ', avg,' Time\n') # Average collection frequency of terms of a collection
    collection_frequencies_list.append(avg) 

#index_txt(result[0], result[1])
# Plots
#statistics_plotting(doc_lengths_list[0], vocabulary_size_list, collection_frequencies_list)

################################################################## EXERCICE 3 ##################################################################

print("Exercice 3 :\n")
print ('---------------------------------------- After pre-treatment (without stop words and after stemming) ----------------------------------------')

# Stop words and Stemming
for file_path in all_paths:

    start_stopword = time.time()
    process_result_stop_words = stopwords_process(result, stop_list)
    end_stopword = time.time()
    start_stemming = time.time()
    process_result_stem = stem_process(process_result_stop_words)
    end_stemming = time.time()

    stop_words_execution_time = end_stopword-start_stopword
    stemming_execution_time = end_stemming-start_stemming

    print("Execution time of the stop words elimination :", stop_words_execution_time, 's\n')
    print("Execution time of the stemming :", stemming_execution_time, 's\n')

    result=process_result_stem
    doc_lengths, vocabulary_size, collection_frequencies, statistics_execution_time = statistics(process_result_stem[0], process_result_stem[1])

    avdl= sum(doc_lengths.values()) / n

    print("Statistics : \n")
    print("Execution time of the statistical calculations :", statistics_execution_time, 's\n')
    print (f'The avrege length of a document in the {n} document collection is : ', avdl, 'Word/Document')
    doc_lengths_list.append(doc_lengths)
    dl=doc_lengths

    print('The size of the vocabulary of the collection is : ', vocabulary_size, 'Word')
    vocabulary_size_list.append(vocabulary_size)  
    
    avg=sum(collection_frequencies.values()) / len(collection_frequencies)
    print ('The avrege collection frequency of a term in the collection is : ', avg,' Time\n') # Average collection frequency of terms of a collection
    collection_frequencies_list.append(avg)

#index_txt_no_stop_words_stem(result[0], result[1])

# Plots
#statistics_plotting(doc_lengths_list[1], vocabulary_size_list, collection_frequencies_list)

################################################################## EXERCICE 4 ##################################################################

print("Exercice 4 :\n")
print ('---------------------------------------- SMART_ltn calculation ----------------------------------------')

start = time.time()
smart_ltn=smart_ltn_weighting(result[0], result[1],n)
end = time.time()

Smart_ltn_execution_time = end-start

print("Execution time of the SMART_ltn calculations :", Smart_ltn_execution_time, 's\n')

#index_txt_smart_ltn (result[0],smart_ltn)

################################################################## EXERCICE 5 ##################################################################

# Query list
queries=[]
with open('querys.txt', 'r') as queries :
    # Create a list of tuples
    query_tuples = [tuple(query.split(' ', 1)) for query in queries]

print("Exercice 5 :\n")
print ('---------------------------------------- SMART_ltn document scoring ----------------------------------------')


file_path = "queryResults/firstTestFile.txt"

with open(file_path, 'w') as file:
    

    for (queryId, query) in query_tuples:
        
        start = time.time()
        eval = evaluate_query(query, smart_ltn)
        end = time.time()

        Smart_ltn_query_execution_time = end-start

        print("Execution time of the SMART_ltn scoring :", Smart_ltn_query_execution_time, 's')

        scores = list(eval.items())
        
        print(f"for {queryId}, result length is {len(scores)}\n")
        
        rank = 1
        for (doc_num, doc_score) in scores:
            file.write(f"{queryId} Q0 {doc_num} {rank} {doc_score} Ignacio /article[1]\n")
            rank += 1

# ################################################################## EXERCICE 6 ##################################################################

# print("Exercice 6 :\n")
# print ('---------------------------------------- SMART_ltc calculation ----------------------------------------')

# start = time.time()
# smart_ltc=smart_ltc_weighting(smart_ltn)
# end = time.time()

# Smart_ltc_execution_time = end-start

# print("Execution time of the SMART_ltn calculations :", Smart_ltc_execution_time, 's\n')

# #index_txt_smart_ltc (result[0],smart_ltc)

# ################################################################## EXERCICE 7 ##################################################################

# print("Exercice 7 :\n")
# print ('---------------------------------------- SMART_ltc document scoring ----------------------------------------')

# start = time.time()
# eval = evaluate_query(query, smart_ltc)
# end = time.time()

# Smart_ltc_query_execution_time = end-start

# print("Execution time of the SMART_ltn scoring :", Smart_ltc_query_execution_time, 's\n')

# top_10_docs = list(eval.items())[:10]

# print("The documents scorring for the querry :", query, "is : ")

# print("____________________________________")
# print("|      docno      |      score      |")
# for i in range(0,len(top_10_docs)):
#     print("____________________________________")
#     print("|   ",top_10_docs[i][0],"  |",top_10_docs[i][1],"|")
# print("____________________________________\n")

# ################################################################## EXERCICE 8 ##################################################################

# print("Exercice 8 :\n")
# print ('---------------------------------------- BM25 calculation ----------------------------------------')

# start = time.time()
# BM25 = BM25_weighting(result[0], result[1], n, 1, 0.5, avdl, dl)
# end = time.time()

# BM25_execution_time = end-start

# print("Execution time of the BM25 calculations :", BM25_execution_time, 's\n')

# #index_txt_BM25 (result[0],BM25)

# ################################################################## EXERCICE 9 ##################################################################

# print("Exercice 9 :\n")
# print ('---------------------------------------- BM25 document scoring ----------------------------------------')

# start = time.time()
# eval = evaluate_query(query, BM25)
# end = time.time()

# BM25_query_execution_time = end-start

# print("Execution time of the BM25 scoring :", BM25_query_execution_time, 's\n')

# top_10_docs = list(eval.items())[:10]

# print("The documents scorring for the querry :", query, "is : ")

# print("____________________________________")
# print("|      docno      |      score      |")
# for i in range(0,len(top_10_docs)):
#     print("____________________________________")
#     print("|   ",top_10_docs[i][0],"  |",top_10_docs[i][1],"|")
# print("____________________________________\n")