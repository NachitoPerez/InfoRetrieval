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

def index_txt_smart_ltn(index, term_frequency):
    with open('index_collection_smart_ltn.txt', 'w') as file:
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

def index_txt_smart_ltc(index, term_frequency):
    with open('index_collection_smart_ltc.txt', 'w') as file:
        for term, postings_list in index.items():
            df = len(postings_list)
            file.write(f"{df}=df({term})\n")
            for word in postings_list:
                file.write(f"{term_frequency[term][word]} {word}\n")

def index_txt_BM25(index, term_frequency):
    with open('index_collection_BM25.txt', 'w') as file:
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