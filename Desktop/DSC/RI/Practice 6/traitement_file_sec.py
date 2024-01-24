from Porter_Stemming_Algorithm import PorterStemmer
from collections import defaultdict
from math import *

def stemmer_tag(index, term_frequency):

    post_process = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
    post_term_frequency = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))
    stemm = PorterStemmer()
    for term, posting_list in index.items():
        stemmed_term = stemm.stem(term, 0, len(term) - 1)
        for docno, tags in posting_list.items() : 
            for tag, paragraphes in tags.items() : 
                for paragraphe in paragraphes :
                    post_process[stemmed_term][docno][tag].add(paragraphe)
                    post_term_frequency[stemmed_term][docno][tag][paragraphe]+=term_frequency[term][docno][tag][paragraphe]
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

def SmartLtc (tf, somme):
    weight = tf/sqrt(somme)
    return weight

def BM25_df(df, n):
    bm25df=log10((n-df+0.5)/(df+0.5))
    return bm25df

def BM25_tf(tf, k, b, dl, avdl):
    bm25tf=((tf*(k+1))/((k*((1-b)+(b*(dl/avdl))))+tf))
    return bm25tf

def  smart_ltn_weighting_sec (index, term_frequency, n) :

    smart_ltn_dict_sec = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

    for term, postings_list in index.items():
            df = len(postings_list)
            for docno, tag_set in postings_list.items():
                for tag, pars in tag_set.items() :
                    if tag != "/article[1]/bdy[1]":
                        tf=0
                        for par in pars : 
                            tf += term_frequency[term][docno][tag][par]
                        weight = SmartLtn (df, tf, n)
                        smart_ltn_dict_sec [term][docno][tag] = weight
    return smart_ltn_dict_sec

def somme_carre_sec(smart_ltn_dict_sec):
    sums = defaultdict(lambda: defaultdict(float))
    for term, dictio in smart_ltn_dict_sec.items():
        for docno, tag_dic in dictio.items():
            for tag in tag_dic :
                sums[docno][tag]+=(smart_ltn_dict_sec[term][docno][tag]**2)

    sums = dict(sorted(sums.items()))
    return sums

def  smart_ltc_weighting_sec (smart_ltn_dict_sec) :

    smart_ltc_dict_sec = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    s=somme_carre_sec(smart_ltn_dict_sec)
    for term, dictio in smart_ltn_dict_sec.items():
        for docno, tag_dic in dictio.items():
            for tag in tag_dic :
                tf = smart_ltn_dict_sec[term][docno][tag]
                if s[docno][tag]>0 :
                    weight = SmartLtc (tf, s[docno][tag])
                else :
                    weight = 0
                smart_ltc_dict_sec [term][docno][tag] = weight
    return smart_ltc_dict_sec

def BM25_weighting_sec (index, term_frequency, n, k, b, avdl, doc_length):
    BM25_dict_sec = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for term, postings_list in index.items():
            df = len(postings_list)
            bm25df = BM25_df(df, n)
            for docno, tag_set in postings_list.items():
                dl= doc_length[docno]
                for tag, pars in tag_set.items() :
                    if tag != "/article[1]/bdy[1]":
                        tf=0
                        for par in pars :
                            tf += term_frequency[term][docno][tag][par]
                        bm25tf = BM25_tf(tf, k, b, dl, avdl)
                        weight = bm25df*bm25tf
                        BM25_dict_sec [term][docno][tag] = weight
    return BM25_dict_sec

def evaluate_query_sec(query, smart, stem_d, stop_list, fun):
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
                if fun == 'ltc' :
                    doc_scorring [docno][tag] += (eval_query[word][docno][tag]*(1/sqrt(len(query_words))))
                else:
                    doc_scorring [docno][tag] += eval_query[word][docno][tag]
    
    for docno in doc_scorring.keys() :       
        doc_scorring[docno] = dict(sorted(doc_scorring[docno].items(), key=lambda item: item[1], reverse=True)) 
        
    doc_scorring = dict(sorted(doc_scorring.items(), key=lambda item: max(item[1].values()), reverse=True)) 

    return doc_scorring

def top_1500_sec (eval_tag):

    top_1500_docs_tag=[]
    docnos = []

    for docno in eval_tag.keys():

        docnos.append(docno)

    i=0

    for docno, dict in eval_tag.items():
        i+=1
        for balise, score in dict.items():

            if i < len(docnos):
                next_docno = docnos[i]

                valeur = list(eval_tag[next_docno].items())[0]
                next_high_value = valeur[1]

                if score >= next_high_value:
                    top_1500_docs_tag.append((docno,balise,score))
                else:
                    continue
            else:
                top_1500_docs_tag.append((docno,balise,score))

    return (top_1500_docs_tag)
