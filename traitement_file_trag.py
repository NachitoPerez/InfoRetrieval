# this file contains the functions that are responsable of all the pre-processing functions as well as weighting functions

from Porter_Stemming_Algorithm import PorterStemmer
from collections import defaultdict
from math import *

def stemmer_tag(index, term_frequency):

    post_process = defaultdict(lambda: defaultdict(set))
    post_term_frequency = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    stemm = PorterStemmer()
    for term, posting_list in index.items():
        stemmed_term = stemm.stem(term, 0, len(term) - 1)
        for docno, tags in posting_list.items() : 
            for tag in tags : 
                post_process[stemmed_term][docno].add(tag)
                post_term_frequency[stemmed_term][docno][tag]+=term_frequency[term][docno][tag]
    return post_process, post_term_frequency

def SmartLtn (df, tf, n):
    if tf >0:
        wtf= (1+log10(tf))
    else : 
        wtf=0
    if df >0:
        wdf= log10(n/df)
    else : 
        wdf=0
    weight = wtf*wdf
    return weight

def  smart_ltn_weighting_tag (index, term_frequency, n) :

    smart_ltn_dict_tag = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for term, postings_list in index.items():
            df = len(postings_list)
            for docno, tag_set in postings_list.items():
                for tag in tag_set :
                    tf = term_frequency[term][docno][tag]
                    weight = SmartLtn (df, tf, n)
                    smart_ltn_dict_tag [term][docno][tag] = weight
    return smart_ltn_dict_tag

def SmartLtc (tf, somme):
    weight = tf/sqrt(somme)
    return weight

def somme_carre(smart_ltn_dict_tag):
    sums = defaultdict(lambda: defaultdict(float))
    for term, dictio in smart_ltn_dict_tag.items():
        for docno, tag_dic in dictio.items():
            for tag in tag_dic :
                sums[docno][tag]+=(smart_ltn_dict_tag[term][docno][tag]**2)

    sums = dict(sorted(sums.items()))
    return sums

def  smart_ltc_weighting_tag (smart_ltn_dict_tag) :

    smart_ltc_dict_tag = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    s=somme_carre(smart_ltn_dict_tag)
    for term, dictio in smart_ltn_dict_tag.items():
        for docno, tag_dic in dictio.items():
            for tag in tag_dic:
                tf = smart_ltn_dict_tag[term][docno][tag]
                if s[docno][tag]>0 :
                    weight = SmartLtc (tf, s[docno][tag])
                else :
                    weight = 0
                smart_ltc_dict_tag [term][docno][tag] = weight
    return smart_ltc_dict_tag

def BM25_df(df, n):
    bm25df=log10((n-df+0.5)/(df+0.5))
    return bm25df

def BM25_tf(tf, k, b, dl, avdl):
    bm25tf=((tf*(k+1))/((k*((1-b)+(b*(dl/avdl))))+tf))
    return bm25tf

def BM25_weighting_tag (index, term_frequency, n, k, b, avdl, doc_lingth):
    BM25_dict_tag = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for term, postings_list in index.items():
            df = len(postings_list)
            bm25df = BM25_df(df, n)
            for docno, tag_set in postings_list.items():
                dl= doc_lingth[docno]
                for tag in tag_set :
                    tf = term_frequency[term][docno][tag]
                    bm25tf = BM25_tf(tf, k, b, dl, avdl)
                    weight = bm25df*bm25tf
                    BM25_dict_tag [term][docno][tag] = weight
    return BM25_dict_tag

def evaluate_query_tag(query, smart, stem_d, stop_list):
    eval_query = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    doc_scorring = defaultdict(lambda: defaultdict(float))
    query_words = query.split()
    stm_l=[]

    for word in query_words:
        if word in stop_list :
            query_words.remove(word)

    if (stem_d != "nostem"):
        stemm = PorterStemmer()
        for word in query_words:
            stemmed_word = stemm.stem(word, 0, len(word) - 1)
            stm_l.append(stemmed_word)
        query_words=stm_l.copy()

    for word in query_words:
        eval_query[word]=smart[word]
    for word, dictio in eval_query.items():
        for docno, tag_dic in dictio.items() :
            for tag in tag_dic :
                doc_scorring [docno][tag] += eval_query[word][docno][tag]
    
    for docno in doc_scorring.keys():            
        doc_scorring[docno] = dict(sorted(doc_scorring[docno].items(), key=lambda item: item[1], reverse=True)) 
    doc_scorring = dict(sorted(doc_scorring.items(), key=lambda item: max(item[1].values()), reverse=True))
    return doc_scorring