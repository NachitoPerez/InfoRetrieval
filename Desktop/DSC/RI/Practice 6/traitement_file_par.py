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

def  smart_ltn_weighting_par (index, term_frequency, n) :

    smart_ltn_dict_par = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float))))
    for term, postings_list in index.items():
            df = len(postings_list)
            for docno, tag_set in postings_list.items():
                for tag, pars in tag_set.items() :
                    for par in pars : 
                        tf = term_frequency[term][docno][tag][par]
                        weight = SmartLtn (df, tf, n)
                        smart_ltn_dict_par [term][docno][tag][par] = weight
    return smart_ltn_dict_par

def SmartLtc (tf, somme):
    weight = tf/sqrt(somme)
    return weight

def somme_carre_par(smart_ltn_dict_par):
    sums = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for term, dictio in smart_ltn_dict_par.items():
        for docno, tag_dic in dictio.items():
            for tag, pars in tag_dic.items() :
                for par in pars:
                    sums[docno][tag][par]+=(smart_ltn_dict_par[term][docno][tag][par]**2)

    sums = dict(sorted(sums.items()))
    return sums

def  smart_ltc_weighting_par (smart_ltn_dict_par) :

    smart_ltc_dict_par = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float))))
    s=somme_carre_par(smart_ltn_dict_par)
    for term, dictio in smart_ltn_dict_par.items():
        for docno, tag_dic in dictio.items():
            for tag, pars in tag_dic.items():
                for par in pars :
                    tf = smart_ltn_dict_par[term][docno][tag][par]
                    if s[docno][tag][par]>0 :
                        weight = SmartLtc (tf, s[docno][tag][par])
                    else :
                        weight = 0
                    smart_ltc_dict_par [term][docno][tag][par] = weight
    return smart_ltc_dict_par

def BM25_df(df, n):
    bm25df=log10((n-df+0.5)/(df+0.5))
    return bm25df

def BM25_tf(tf, k, b, dl, avdl):
    bm25tf=((tf*(k+1))/((k*((1-b)+(b*(dl/avdl))))+tf))
    return bm25tf

def BM25_weighting_par (index, term_frequency, n, k, b, avdl, doc_length):
    BM25_dict_par = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float))))
    for term, postings_list in index.items():
            df = len(postings_list)
            bm25df = BM25_df(df, n)
            for docno, tag_set in postings_list.items():
                dl= doc_length[docno]
                for tag, pars in tag_set.items() :
                    for par in pars :
                        tf = term_frequency[term][docno][tag][par]
                        bm25tf = BM25_tf(tf, k, b, dl, avdl)
                        weight = bm25df*bm25tf
                        BM25_dict_par [term][docno][tag][par] = weight
    return BM25_dict_par

def evaluate_query_par(query, smart, stem_d, stop_list, fun):
    eval_query = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda : defaultdict(float))))
    doc_scorring = defaultdict(lambda: defaultdict(lambda : defaultdict(float)))
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
            for tag, pars in tag_dic.items() :
                for par in pars:
                    if fun == 'ltc' :
                        doc_scorring [docno][tag][par] += (eval_query[word][docno][tag][par]*(1/sqrt(len(query_words))))
                    else:
                        doc_scorring [docno][tag][par] += eval_query[word][docno][tag][par]
    
    for docno, tag_list in doc_scorring.items(): 
        for tag in tag_list.keys():           
            doc_scorring[docno][tag] = dict(sorted(doc_scorring[docno][tag].items(), key=lambda item: item[1], reverse=True)) 
        doc_scorring[docno] = dict(sorted(doc_scorring[docno].items(), key=lambda item: max(item[1].values()), reverse=True)) 

    doc_scorring = dict(sorted(doc_scorring.items(), key=lambda item: max(val for sub_dict in item[1].values() for val in sub_dict.values()), reverse=True))

    return doc_scorring

def top_1500_par (eval_tag):

    top_1500_docs_tag=[]
    docnos = []

    for docno in eval_tag.keys():

        docnos.append(docno)

    i=0

    for docno, dict in eval_tag.items():
        i+=1
        for sec, dictio in dict.items():
            for par, score in dictio.items():

                if i < len(docnos):
                    next_docno = docnos[i]

                    values = list(eval_tag[next_docno].items())[0]
                    dictio = values[1]
                    next_high_value = list(dictio.values())[0]

                    if score > next_high_value:
                        top_1500_docs_tag.append((docno,sec+par,score))
                    else:
                        continue
                else:
                    top_1500_docs_tag.append((docno,sec+par,score))

    return (top_1500_docs_tag)

################################################################################## top 1500 ##################################################################################
# This part contains problems that we're trying to fix

# def top_1500_sec (eval, eval_sec):
#     top_1500_docs_sec =[]
#     eval_s={}

#     doc_list=[]

#     for docno in eval.keys():
#         doc_list.append(docno)
#         if docno in eval_sec.keys():
#             eval_s[docno]=eval_sec[docno]

#     i=0

#     for docno, tag_dic in eval_s.items():
#         d = 0
#         if (doc_list[i] == docno) and (doc_list[i+1] in eval_s.keys()):
#             next_doc_max_value = list(eval_s[doc_list[i+1]].values())[0]
#             for tag, tag_score in tag_dic.items():
#                 if tag_score > eval[doc_list[i]] and tag_score > next_doc_max_value :
#                     top_1500_docs_sec.append((docno, tag, tag_score))
#                     d = 1
#                 else : 
#                     continue
#             if d == 0:
#                 top_1500_docs_sec.append(((doc_list[i]), '/article[1]', eval[docno]))
                    
#         else:
#             top_1500_docs_sec.append(((doc_list[i]), '/article[1]', eval[docno]))

#         i+=1

#     o_docnos = []

#     for docno, tag_dic in eval_sec.items():
#         if docno not in doc_list:
#             o_docnos.append(docno)

#     for docno in o_docnos :
#         j=0
#         for score in top_1500_docs_sec :
#             for sec, sec_value in eval_sec[docno].items():
#                 if docno in doc_list :
#                     if (sec_value>score[2]) and (j==j+1) :
#                         j=score.index()
#                         top_1500_docs_sec.insert(j,(docno, sec, sec_value))
#                 else :
#                     if sec_value>score[2]:
#                         j=top_1500_docs_sec.index(score)
#                         top_1500_docs_sec.insert(j,(docno, sec, sec_value))
#                         doc_list.append(docno)
    
#     return(top_1500_docs_sec)

# def top_1500_par (eval, eval_tag):
#     top_1500_docs_tag =[]
#     eval_p={}

#     doc_list=[]

#     for docno in eval.keys():
#         doc_list.append(docno)
#         if docno in eval_tag.keys():
#             eval_p[docno]=eval_tag[docno]

#     i=0

#     for docno, tag_dic in eval_p.items():
#         d = 0
#         if (doc_list[i] == docno) and (doc_list[i+1] in eval_p.keys()):
#             next_doc_max_value = list(eval_p[doc_list[i+1]].values())[0]
#             for tag, tag_score in tag_dic.items():
#                 if tag_score > eval[doc_list[i]] and tag_score > next_doc_max_value :
#                     top_1500_docs_tag.append((docno, tag, tag_score))
#                     d = 1
#                 else : 
#                     continue
#             if d == 0:
#                 top_1500_docs_tag.append(((doc_list[i]), '/article[1]', eval[docno]))
                    
#         else:
#             top_1500_docs_tag.append(((doc_list[i]), '/article[1]', eval[docno]))

#         i+=1
#     return(top_1500_docs_tag)
