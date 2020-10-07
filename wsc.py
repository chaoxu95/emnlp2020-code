#!/usr/bin/env python3
##############################################################################
#       Function: Batch processing of WSC examples
##############################################################################

from fuzzy_match import *


def write_motion_repr_to_file(file_name, motion_event):
    for role, value in motion_event.info_dict.items():
        print_expr = ""

        if role in ['agent', 'figure']:
            for item in value:
                word = item.get_word()
                print_expr = add_str_to_str(print_expr, word,',')

        elif role == 'ground':
            for prep, ground in value.items():
                #print(prep.info_dict, ground.info_dict)
                expr = ""
                if len(ground.info_dict) != 0:
                    expr = prep.get_word()+'/'+ground.get_word()
                else:
                    expr = prep.get_word()+'/ground is omitted'
                print_expr = add_str_to_str(print_expr, expr, ';')
        else:
            print_expr = str(value)

        #print(role+':'+print_expr)
        file_name.write(role+':'+print_expr+'\n')

def write_locative_repr_to_file(file_name, locative_repr):
    for key, value in locative_repr.info_dict.items():
        if isinstance(value, list):
            for item in value:
                if item.get_word() != None:
                    file_name.write(str(key)+':'+item.get_word()+'\n')
                else:
                    file_name.write(str(key)+':'+str(item)+'\n')
        else:
            if value.get_word() != None:
                file_name.write(str(key)+':'+value.get_word()+'\n')
            else:
                file_name.write(str(key)+':'+str(value)+'\n')



f_wsc_log = open('output/wsc_output', 'w')
f = open('param/wsc_examples', 'r')
path_verb_dict = load_path_verb_dict()
verb_form_dict = load_verb_form_dict()
for line in f:
    line = line.strip()
    if line.strip() != "":
        line = preprocessing_of_sentence(line, path_verb_dict, verb_form_dict)
        f_wsc_log.write('begin a WSC example........................................'+'\n')
        f_wsc_log.write(line+'\n')
        sentence_list = sent_tokenize(line)
        final_pattern_dict = get_final_pattern_dict(regular_pattern_dict)
        for sentence in sentence_list:
            f_wsc_log.write('******************** sentence ********************'+'\n')
            f_wsc_log.write(sentence+'\n')
            print('******************** '+sentence+' ********************')


            parse = get_dependency_analysis_of_sentence(sentence)
            semantic_unit_list = get_semantic_unit_list(sentence, parse)
            semantic_unit_list = add_buddy_to_unit(semantic_unit_list)
            lemma_list = get_lemma_list(semantic_unit_list)
            semantic_unit_list = construction_recognition(lemma_list, semantic_unit_list, all_prep_list, 'RP')
            semantic_unit_list = remove_repeating_semantic_unit(semantic_unit_list)
            father_children_dict = get_father_children_list(parse)
            root_list = get_all_root_list(parse)
            root_children_dict = get_root_children_dict(root_list, father_children_dict)
            event_dict = get_event_dict(sentence, root_children_dict, semantic_unit_list)

            for event, children in event_dict.items():
                print('---------------------semantic_unit_list---------------------')
                print_semantic_unit_list(children)
                print('---------------------      end line    ---------------------')

                locative_repr_list, motion_repr_list = get_final_spatial_representation(children, final_pattern_dict)
                for locative_repr in locative_repr_list:
                    print('-----------  locative construction -----------')
                    print_locative_expr(locative_repr)
                    print('-----------  locative construction -----------')
                    f_wsc_log.write('-----------  begin locative construction -----------'+'\n')
                    write_locative_repr_to_file(f_wsc_log, locative_repr)
                    f_wsc_log.write('-----------   end locative construction  -----------'+'\n')
                for motion_repr in motion_repr_list:
                    print('-----------   motion construction  -----------')
                    print_motion_event(motion_repr)
                    print('-----------   motion construction  -----------')
                    f_wsc_log.write('-----------   begin motion construction  -----------'+'\n')
                    write_motion_repr_to_file(f_wsc_log, motion_repr)
                    f_wsc_log.write('-----------    end motion construction   -----------'+'\n')
        f_wsc_log.write('...........................................................'+'\n\n\n\n')

f.close()
f_wsc_log.close()
