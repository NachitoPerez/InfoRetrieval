from file_process import *
from traitement_file import *
from files_maneg import *

def BM25_tuning(result, n, avdl, dl, all_querys, stem_d, stop_list, stop_d):
    
    run_index = 50

    fixed_k1 = 1.2
    for b in range(0, 11):
        b_value = b / 10.0
        
        BM25 = BM25_weighting(result[0], result[1], n, fixed_k1, b_value, avdl, dl)
        
        for query_id, query in all_querys.items() :

            eval = evaluate_query(query, BM25, stem_d, stop_list)

            top_1500_docs = list(eval.items())[:1500]

            export_file(top_1500_docs, query_id, run_index, "BM25", "article",stop_d, stem_d, {'k':fixed_k1, 'b':b_value})

        run_index -= 1
         
    # Fix b to 0.75 and vary k1 from 0 to 4 with a step of 0.2
    fixed_b = 0.75
    for k in range(0, 21):
        k_value = k / 5.0
        
        BM25 = BM25_weighting(result[0], result[1], n, k_value, fixed_b, avdl, dl)
        
        for query_id, query in all_querys.items() :

            eval = evaluate_query(query, BM25, stem_d, stop_list)

            top_1500_docs = list(eval.items())[:1500]

            export_file(top_1500_docs, query_id, run_index, "BM25", "article",stop_d, stem_d, {'k':k_value, 'b':fixed_b})

        run_index -= 1
