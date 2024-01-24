from index_dic_creator import *
from BM25_tuning import BM25_tuning
from file_process import *
from file_process_xml import *
from traitement_file import *
from files_maneg import *
from traitement_file_sec import *
from traitement_file_par import *
from BM25_Robertson import *
from BM25_Wilkinson import *
import os
import time

############################################################################# Functions ##################################################################

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

# Building the stop words list
stop_list = stop_words()
stop_len=len(stop_list) -1

result = ()
result_tag = ()
n=0
avdl = 0

combine_dis = int(input("Do you want to combine new txt files from the xml files : \n1. Yes(if it's the first time you're using the program)\n2. No(if you have alredy did this part)\n "))
if combine_dis == 1 :
    combine_XML_files()

index_dis = int(input("Do you want to creat new indexes for the treatment : \n1. Yes(if it's the first time you're using the program)\n2. No(if you have alredy did this part)\n "))
if index_dis == 1 :
    index_creator(stop_list)

treatment_type = int(input("Select what type of traitment you want :\n1. Articles only\n2. Sections only\n3. Paragraphs only\n"))

if treatment_type == 1 :

    index_result = import_index("initial")
    process_result_stem = import_index("stemed_with_stop_words")
    process_result_stop_words = import_index("without_stop_words")
    process_result_stop_words_stem = import_index("stemed_without_stop_words")
    doc_lengths_dict = import_doc_lengths("no_tag")
    n=9804
    ################################################################## Quey evaluation ######################################################################## 

    print ('---------------------------------------- Quey evaluation ----------------------------------------\n')

    run=int(input("Choose which weigthing function you want to run :\n 1. Smart Ltn\n 2. Smart Ltc\n 3. BM25\n 4. BM25 Tunning\n 0. To exit\n"))

    while (run > 0 and run < 5) :
        
        # Get the current run counter
        run_index = get_run_counter()

    ################################################################## stemming & stop words ##################################################################

        stop_des = int(input("Do you want to remove the stop words :\n1. Yes\n2. No\n"))

        if (stop_des == 1):
            stop_d=f"stop{stop_len}"
            result = process_result_stop_words
            dls = doc_lengths_dict["stop"]

        else :
            stop_d="nostop"

        stem_des = int(input("Do you want to stem the tokens :\n1. Yes\n2. No\n"))

        if (stem_des == 1 and stop_des == 1):
            stem_d="porter"
            result = process_result_stop_words_stem
            dls = doc_lengths_dict["stop_stem"]
            
        elif (stem_des == 1 and stop_des == 2):
            stem_d="porter"
            result = process_result_stem
            dls = doc_lengths_dict["stem"]

        else :
            stem_d="nostem"
            result = index_result
            dls = doc_lengths_dict["none"]

        avdl= sum(dls.values()) / n

        print("avdl = ", avdl)

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

        ################################################################## Query processing for Smart ltn #########################################################

            for query_id, query in all_querys.items() :

                eval = evaluate_query(query, smart_ltn, stem_d, stop_list,'ltn')
                
                top_1500_docs = top_1500(eval)

                export_file(top_1500_docs, query_id, run_index, "ltn", "article",stop_d, stem_d, 'noparameters')

        if (run==2):
        ################################################################## Smart ltc processing ###################################################################

            start = time.time()
            smart_ltn=smart_ltn_weighting(result[0], result[1],n)

            smart_ltc=smart_ltc_weighting(smart_ltn)
            end = time.time()

            Smart_ltc_execution_time = end-start

            print("Execution time of the SMART_ltc calculations :", Smart_ltc_execution_time, 's\n')


        ################################################################## Query processing for Smart ltc #########################################################

            for query_id, query in all_querys.items() :

                eval = evaluate_query(query, smart_ltc, stem_d, stop_list, 'ltc')

                top_1500_docs=top_1500(eval)

                export_file(top_1500_docs, query_id, run_index, "ltc", "article",stop_d, stem_d, 'noparameters')

                #query_result(top_1500_docs,run_index, query_id)

        if (run == 3):
            k = float(input("Enter the value of k : "))

            b = float(input("Enter the value of b : "))

        ################################################################## BM25 processing ########################################################################

            start = time.time()
            BM25 = BM25_weighting(result[0], result[1], n, k, b, avdl, dls)
            end = time.time()

            BM25_execution_time = end-start

            print("Execution time of the BM25 calculations :", BM25_execution_time, 's\n')

        ################################################################## Query processing for BM25 ###############################################################

            for query_id, query in all_querys.items() :

                eval = evaluate_query(query, BM25, stem_d, stop_list,'BM25')

                top_1500_docs=top_1500(eval)

                export_file(top_1500_docs, query_id, run_index, "BM25", "article",stop_d, stem_d, {'k':k, 'b':b})
                
        if (run == 4):

            start = time.time()
            BM25_tuning(result=result, n=n, dl=dls, avdl=avdl, all_querys=all_querys, stem_d=stem_d, stop_list=stop_list, stop_d=stop_d)
            run_index -= 1    

            end = time.time()

            BM25_tunning_execution_time = end-start

            print("Execution time of the tuned BM25 calculations :", BM25_tunning_execution_time, 's\n')

        result = ()
        result_tag = ()
        
        update_counter(run_index)

        run=int(input("Choose which weigthing function you want to run :\n 1. Smart Ltn\n 2. Smart Ltc\n 3. BM25\n 4. BM25 Tuning\n 0. To exit\n"))

################################################################## XML Tags #############################################################################
else :

    
    index_result_tag = import_index("initial_tag")
    process_result_stem_tag = import_index("stemed_with_stop_words_tag")
    process_result_stop_words_tag = import_index("without_stop_words_tag")
    process_result_stop_words_stem_tag = import_index("stemed_without_stop_words_tag")
    doc_lengths_dict_tag = import_doc_lengths("tag")
    n_tag = 9804
                    
    exit_val = "n"
    while exit_val == "n" :

        if treatment_type == 2 :
        
            ################################################################## Quey evaluation ######################################################################## 

            print ('---------------------------------------- Quey evaluation ----------------------------------------\n')

            run=int(input("Choose which weigthing function you want to run :\n 1. Smart Ltn\n 2. Smart Ltc\n 3. BM25\n 4. BM25 Robertson\n 0. To exit\n"))

            while (run > 0 and run < 5) :
                
                # Get the current run counter
                run_index = get_run_counter()

            ################################################################## stemming & stop words ##################################################################

                stop_des = int(input("Do you want to remove the stop words :\n1. Yes\n2. No\n"))

                if (stop_des == 1):
                    stop_d=f"stop{stop_len}"
                    result_tag = process_result_stop_words_tag
                    dls_tag = doc_lengths_dict_tag["stop"]

                else :
                    stop_d="nostop"

                stem_des = int(input("Do you want to stem the tokens :\n1. Yes\n2. No\n"))

                if (stem_des == 1 and stop_des == 1):
                    stem_d="porter"
                    result_tag = process_result_stop_words_stem_tag
                    dls_tag = doc_lengths_dict_tag["stop_stem"]

                elif (stem_des == 1 and stop_des == 2):
                    stem_d="porter"
                    result_tag = process_result_stem_tag
                    dls_tag = doc_lengths_dict_tag["stem"]

                else :
                    stem_d="nostem"
                    result_tag = index_result_tag
                    dls_tag = doc_lengths_dict_tag["none"]

                print('---------------------------------------------------- Taged Index list ----------------------------------------------------')

                avdl_tag= sum(dls_tag.values()) / n_tag

                print("avdl = ", avdl_tag)

                ################################################################## Quey preparation ########################################################################

                all_querys = defaultdict(str)

                with open('utils/querys.txt', 'r') as allquerys :
                    for query in allquerys:
                        query_components = query.strip().split(maxsplit=1)
                        query_id, query_text = query_components
                        all_querys[query_id] = (query_text)

                if (run==1):

                ################################################################## Smart ltn tag processing ###################################################################

                    start_tag = time.time()
                    smart_ltn_tag=smart_ltn_weighting_sec(result_tag[0], result_tag[1],n_tag)
                    end_tag = time.time()

                    Smart_ltn_execution_time_tag = end_tag-start_tag

                    print("Execution time of the SMART_ltn with tag calculations :", Smart_ltn_execution_time_tag, 's\n')

                ################################################################## Query processing for Smart ltn #########################################################

                    for query_id, query in all_querys.items() :

                        eval_tag = evaluate_query_sec(query, smart_ltn_tag, stem_d, stop_list,'ltn')
                        
                        top_1500_docs_tag=top_1500_sec(eval_tag)

                        export_file_tag(top_1500_docs_tag[:1500], query_id, run_index, "ltn", "element",stop_d, stem_d, 'noparameters')


                if (run==2):

                ################################################################## Smart ltc tag processing ###################################################################

                    start_tag = time.time()
                    smart_ltn_tag=smart_ltn_weighting_sec(result_tag[0], result_tag[1],n_tag)

                    smart_ltc_tag=smart_ltc_weighting_sec(smart_ltn_tag)
                    end_tag = time.time()

                    Smart_ltc_execution_time_tag = end_tag-start_tag

                    print("Execution time of the SMART_ltc with tag calculations :", Smart_ltc_execution_time_tag, 's\n')


                ################################################################## Query processing for Smart ltc #########################################################

                    for query_id, query in all_querys.items() :

                        eval_tag = evaluate_query_sec(query, smart_ltc_tag, stem_d, stop_list,'ltc')

                        top_1500_docs_tag=top_1500_sec(eval_tag)

                        export_file_tag(top_1500_docs_tag[:1500], query_id, run_index, "ltc", "element",stop_d, stem_d, 'noparameters')


                if (run == 3):
                    k = float(input("Enter the value of k : "))

                    b = float(input("Enter the value of b : "))

                    ################################################################## BM25 tag processing ########################################################################

                    start_tag = time.time()
                    BM25_tag = BM25_weighting_sec(result_tag[0], result_tag[1], n_tag, k, b, avdl_tag, dls_tag)
                    end_tag = time.time()

                    BM25_execution_time_tag = end_tag-start_tag

                    print("Execution time of the BM25 with tag calculations :", BM25_execution_time_tag, 's\n')

                ################################################################## Query processing for BM25 ###############################################################

                    for query_id, query in all_querys.items() :

                        eval_tag = evaluate_query_sec(query, BM25_tag, stem_d, stop_list,'BM25')

                        top_1500_docs_tag=top_1500_sec(eval_tag)

                        export_file_tag(top_1500_docs_tag[:1500], query_id, run_index, "BM25", "element",stop_d, stem_d, {'k':k, 'b':b})
                        
                if (run == 4):

                    start = time.time()
                    BM25_Rob = BM25_Robertson(result=result, n=n, dl=dls_tag, avdl=avdl_tag, all_querys=all_querys, stem_d=stem_d, stop_list=stop_list, stop_d=stop_d)

                    end = time.time()

                    BM25_Robertson_execution_time = end-start

                    print("Execution time of the tuned BM25 calculations :", BM25_Robertson_execution_time, 's\n')

                    ################################################################## Query processing for BM25 Robertson ###############################################################

                    for query_id, query in all_querys.items() :

                        eval_tag = evaluate_query_sec(query, BM25_Rob, stem_d, stop_list,'BM25')

                        top_1500_docs_tag=top_1500_sec(eval_tag)

                        export_file_tag(top_1500_docs_tag[:1500], query_id, run_index, "BM25 Robertson", "element",stop_d, stem_d, {'k':k, 'b':b})

                result = ()
                result_tag = ()
                
                update_counter(run_index)

                run=int(input("Choose which weigthing function you want to run :\n 1. Smart Ltn\n 2. Smart Ltc\n 3. BM25\n 4. BM25 Robertson\n 0. To exit\n"))
        
        else :
            ################################################################## Quey evaluation ######################################################################## 

            print ('---------------------------------------- Quey evaluation ----------------------------------------\n')

            run=int(input("Choose which weigthing function you want to run :\n 1. Smart Ltn\n 2. Smart Ltc\n 3. BM25\n 4. BM25 Robertson\n 0. To exit\n"))

            while (run > 0 and run < 5) :
                
                # Get the current run counter
                run_index = get_run_counter()

            ################################################################## stemming & stop words ##################################################################

                stop_des = int(input("Do you want to remove the stop words :\n1. Yes\n2. No\n"))

                if (stop_des == 1):
                    stop_d=f"stop{stop_len}"
                    result_tag = process_result_stop_words_tag
                    dls_tag = doc_lengths_dict_tag["stop"]

                else :
                    stop_d="nostop"

                stem_des = int(input("Do you want to stem the tokens :\n1. Yes\n2. No\n"))

                if (stem_des == 1 and stop_des == 1):
                    stem_d="porter"
                    result_tag = process_result_stop_words_stem_tag
                    dls_tag = doc_lengths_dict_tag["stop_stem"]

                elif (stem_des == 1 and stop_des == 2):
                    stem_d="porter"
                    result_tag = process_result_stem_tag
                    dls_tag = doc_lengths_dict_tag["stem"]

                else :
                    stem_d="nostem"
                    result_tag = index_result_tag
                    dls_tag = doc_lengths_dict_tag["none"]

                print('---------------------------------------------------- Taged Index list ----------------------------------------------------')

                avdl_tag= sum(dls_tag.values()) / n_tag

                print("avdl = ", avdl_tag)

                ################################################################## Quey preparation ########################################################################

                all_querys = defaultdict(str)

                with open('utils/querys.txt', 'r') as allquerys :
                    for query in allquerys:
                        query_components = query.strip().split(maxsplit=1)
                        query_id, query_text = query_components
                        all_querys[query_id] = (query_text)

                if (run==1):

                ################################################################## Smart ltn tag processing ###################################################################

                    start_tag = time.time()
                    smart_ltn_tag=smart_ltn_weighting_par(result_tag[0], result_tag[1],n_tag)
                    end_tag = time.time()

                    Smart_ltn_execution_time_tag = end_tag-start_tag

                    print("Execution time of the SMART_ltn with tag calculations :", Smart_ltn_execution_time_tag, 's\n')

                ################################################################## Query processing for Smart ltn #########################################################

                    for query_id, query in all_querys.items() :

                        eval_tag = evaluate_query_par(query, smart_ltn_tag, stem_d, stop_list,'ltn')
                        
                        top_1500_docs_tag=top_1500_par(eval_tag)

                        export_file_tag(top_1500_docs_tag[:1500], query_id, run_index, "ltn", "element",stop_d, stem_d, 'noparameters')


                if (run==2):

                ################################################################## Smart ltc tag processing ###################################################################

                    start_tag = time.time()
                    smart_ltn_tag=smart_ltn_weighting_par(result_tag[0], result_tag[1],n_tag)

                    smart_ltc_tag=smart_ltc_weighting_par(smart_ltn_tag)
                    end_tag = time.time()

                    Smart_ltc_execution_time_tag = end_tag-start_tag

                    print("Execution time of the SMART_ltc with tag calculations :", Smart_ltc_execution_time_tag, 's\n')


                ################################################################## Query processing for Smart ltc #########################################################

                    for query_id, query in all_querys.items() :

                        eval_tag = evaluate_query_par(query, smart_ltc_tag, stem_d, stop_list,'ltc')

                        top_1500_docs_tag=top_1500_par(eval_tag)

                        export_file_tag(top_1500_docs_tag[:1500], query_id, run_index, "ltc", "element",stop_d, stem_d, 'noparameters')


                if (run == 3):
                    k = float(input("Enter the value of k : "))

                    b = float(input("Enter the value of b : "))

                    ################################################################## BM25 tag processing ########################################################################

                    start_tag = time.time()
                    BM25_tag = BM25_weighting_par(result_tag[0], result_tag[1], n_tag, k, b, avdl_tag, dls_tag)
                    end_tag = time.time()

                    BM25_execution_time_tag = end_tag-start_tag

                    print("Execution time of the BM25 with tag calculations :", BM25_execution_time_tag, 's\n')

                ################################################################## Query processing for BM25 ###############################################################

                    for query_id, query in all_querys.items() :

                        eval_tag = evaluate_query_par(query, BM25_tag, stem_d, stop_list,'BM25')

                        top_1500_docs_tag=top_1500_par(eval_tag)

                        export_file_tag(top_1500_docs_tag[:1500], query_id, run_index, "BM25", "element",stop_d, stem_d, {'k':k, 'b':b})
                        
                if (run == 4):

                    start = time.time()
                    BM25_Rob = BM25_Robertson(result=result, n=n, dl=dls_tag, avdl=avdl_tag, all_querys=all_querys, stem_d=stem_d, stop_list=stop_list, stop_d=stop_d)

                    end = time.time()

                    BM25_Robertson_execution_time = end-start

                    print("Execution time of the tuned BM25 calculations :", BM25_Robertson_execution_time, 's\n')

                    ################################################################## Query processing for BM25 Robertson ###############################################################

                    for query_id, query in all_querys.items() :

                        eval_tag = evaluate_query_par(query, BM25_Rob, stem_d, stop_list,'BM25')

                        top_1500_docs_tag=top_1500_par(eval_tag)

                        export_file_tag(top_1500_docs_tag[:1500], query_id, run_index, "BM25 Robertson", "element",stop_d, stem_d, {'k':k, 'b':b})

                result = ()
                result_tag = ()
                
                update_counter(run_index)

                run=int(input("Choose which weigthing function you want to run :\n 1. Smart Ltn\n 2. Smart Ltc\n 3. BM25\n 4. BM25 Tuning\n 0. To exit\n"))

        exit_val = input("Do you want to end the program (y/n): ")

        if exit_val == "n":
            treatment_type = int(input("Select what type of traitment you want :\n2. Sections only\n3. Paragraphs only\n"))