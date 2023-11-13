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


    with open(f'runs/SaadZakariaBadreddineIgnacio_{run_id}_{weighting_function}_{granularity}_{stop}_{stem}{parm}.txt', 'a') as file:
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