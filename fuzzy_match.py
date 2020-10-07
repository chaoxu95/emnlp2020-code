#!/usr/bin/env python3
##############################################################################
#       Function: fuzzy matching of the constructions
##############################################################################
import itertools

from semantic import *
from nltk.tokenize import sent_tokenize
from classes import *
from mapping import *
SpRl_list = ['on the left', 'on the right']
regular_pattern_dict = {
'MOTION': [['NN','NNS', 'NNP', 'NNPS', 'PRP'],[3], ['motion'], [2], ['RP'], [2], ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']],
'CAUSED_MOTION': [['NN','NNS', 'NNP', 'NNPS', 'PRP', 'WP'],[3],['motion'],[3], ['NN','NNS', 'NNP', 'NNPS', 'PRP'],[3], ['RP'], [2], ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']],
'MOTION_GROUND_OMISSION': [['NN','NNS', 'NNP', 'NNPS', 'PRP'],[3], ['motion'], [2], ['RP']],
'CAUSED_MOTION_GROUND_OMISSION': [['NN','NNS', 'NNP', 'NNPS', 'PRP', 'WP'],[3],['motion'],[3], ['NN','NNS', 'NNP', 'NNPS', 'PRP'],[3], ['RP']],
'NP_PREP_NP' : [['NN','NNS', 'NNP', 'NNPS', 'PRP'],[4], ['RP'], [2], ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']],
'THEREBE' : [['EX'],['BE'],[2], ['NN','NNS', 'NNP', 'NNPS', 'PRP'],[2],  ['RP'],[2], ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']],
'NP_BE_PREP_NP' : [['NN','NNS', 'NNP', 'NNPS', 'PRP', 'WP'], ['BE'],[2],['RP'], [2],['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']],
'NP_STATIVE_PREP_NP' : [['NN','NNS', 'NNP', 'NNPS', 'PRP', 'WP'], [2], ['stative'], [2], ['RP'],[2], ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']],
'RP_NP_STATIVE_NP':[ ['RP'],[2], ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP'],[2], ['stative','BE'],[2],['NN','NNS', 'NNP', 'NNPS', 'PRP', 'WP']],
'SpRL_PATTERN':[ ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP'],[2], ['on the left', 'on the right']]

}

# regular_pattern_dict = {
# 'MOTION': [['NN','NNS', 'NNP', 'NNPS', 'PRP'],[3], ['motion'], [3], ['RP'], [3], ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']],
# 'CAUSED_MOTION': [['NN','NNS', 'NNP', 'NNPS', 'PRP', 'WP'],[3],['motion'],[3], ['NN','NNS', 'NNP', 'NNPS', 'PRP'],[3], ['RP'], [3], ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']],
# 'MOTION_GROUND_OMISSION': [['NN','NNS', 'NNP', 'NNPS', 'PRP'],[3], ['motion'], [2], ['RP']],
# 'CAUSED_MOTION_GROUND_OMISSION': [['NN','NNS', 'NNP', 'NNPS', 'PRP', 'WP'],[3],['motion'],[3], ['NN','NNS', 'NNP', 'NNPS', 'PRP'],[3], ['RP']],
# 'NP_PREP_NP' : [['NN','NNS', 'NNP', 'NNPS', 'PRP'],[4], ['RP'], [3], ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']],
# 'THEREBE' : [['EX'],['BE'],[3], ['NN','NNS', 'NNP', 'NNPS', 'PRP'],[3],  ['RP'],[3], ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']],
# 'NP_BE_PREP_NP' : [['NN','NNS', 'NNP', 'NNPS', 'PRP', 'WP'], ['BE'],[3],['RP'], [3],['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']],
# 'NP_STATIVE_PREP_NP' : [['NN','NNS', 'NNP', 'NNPS', 'PRP', 'WP'], [3], ['stative'], [3], ['RP'],[3], ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']],
# 'RP_NP_STATIVE_NP':[ ['RP'],[3], ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP'],[3], ['stative','BE'],[3],['NN','NNS', 'NNP', 'NNPS', 'PRP', 'WP']]
# }



motion_construction_list = ['MOTION', 'CAUSED_MOTION', 'MOTION_GROUND_OMISSION','CAUSED_MOTION_GROUND_OMISSION' ]
locative_construction_list = ['NP_PREP_NP', 'THEREBE', 'NP_BE_PREP_NP', 'NP_STATIVE_PREP_NP', 'RP_NP_STATIVE_NP', 'SpRL_PATTERN']

statistic_dict = {'MOTION':0,
'CAUSED_MOTION':0,
'MOTION_GROUND_OMISSION':0,
'CAUSED_MOTION_GROUND_OMISSION':0,
'NP_PREP_NP':0,
'THEREBE':0,
'NP_BE_PREP_NP':0,
'NP_STATIVE_PREP_NP':0,
'RP_NP_STATIVE_NP':0,
'SpRL_PATTERN':0}

def get_fuzzy_pattern_dict(regular_pattern_dict):
    fuzzy_pattern_dict = {}
    for constr_type, pattern_list in regular_pattern_dict.items():
        pattern_list = list(itertools.product(*pattern_list))
        fuzzy_pattern_dict[constr_type] = pattern_list
    return fuzzy_pattern_dict

def replace_number_with_star(source_list):
    source_list = list(source_list)
    generate_list = []
    number_flag = 0
    for item in source_list:
        if type(item) == type(1):
            number_flag = 1
    if number_flag == 1:
        for index, item in enumerate(source_list):
            if type(item) == type(1):
                for i in range(item+1):
                    if i == 0:
                        temp_list = source_list.copy()
                        temp_list.pop(index)
                        generate_list.append(temp_list)
                    elif i == 1:
                        temp_list = source_list.copy()
                        temp_list.pop(index)
                        temp_list.insert(index, "*")
                        generate_list.append(temp_list)
                    elif i == 2:
                        temp_list = source_list.copy()
                        temp_list.pop(index)
                        temp_list.insert(index, "*")
                        temp_list.insert(index+1, "*")
                        generate_list.append(temp_list)
                    elif i == 3:
                        temp_list = source_list.copy()
                        temp_list.pop(index)
                        temp_list.insert(index, "*")
                        temp_list.insert(index+1, "*")
                        temp_list.insert(index+2, "*")
                        generate_list.append(temp_list)
                    elif i == 4:
                        temp_list = source_list.copy()
                        temp_list.pop(index)
                        temp_list.insert(index, "*")
                        temp_list.insert(index+1, "*")
                        temp_list.insert(index+2, "*")
                        temp_list.insert(index+3, "*")
                        generate_list.append(temp_list)
                break
    else:
        generate_list.append(source_list)
    return generate_list

def get_exact_pattern_list_for_single_fuzzy_pattern(original_fuzzy_pattern):
    first_level_list = []
    second_level_list = []
    third_level_list = []
    fourth_level_list = []
    first_level_list = replace_number_with_star(original_fuzzy_pattern)
    #print(original_fuzzy_pattern)
    for first in first_level_list:
        temp_list = replace_number_with_star(first)
        second_level_list = second_level_list + temp_list
    for second in second_level_list:
        temp_list = replace_number_with_star(second)
        third_level_list = third_level_list + temp_list
    for third in third_level_list:
        temp_list = replace_number_with_star(third)
        fourth_level_list = fourth_level_list + temp_list
    return fourth_level_list

def get_exact_pattern_dict(fuzzy_pattern_dict):
    exact_pattern_dict = {}
    for constr_type, pattern_list in fuzzy_pattern_dict.items():
        all_exact_pattern_list = []
        for pattern in pattern_list:
            temp_list = get_exact_pattern_list_for_single_fuzzy_pattern(pattern)
            all_exact_pattern_list = all_exact_pattern_list + temp_list
        exact_pattern_dict[constr_type] = all_exact_pattern_list
    return exact_pattern_dict

def get_final_pattern_dict(construction_dict):
    fuzzy_dict = get_fuzzy_pattern_dict(construction_dict)
    exact_dict = get_exact_pattern_dict(fuzzy_dict)
    return exact_dict

def find_all_sublist_in_list(sublist, list):
    all_occ_list = []
    possible_occ_list = [index for index, item in enumerate(list) if item == sublist[0]]
    for index in possible_occ_list:
        if list[index:index+len(sublist)] == sublist:
            all_occ_list.append(range(index, index+len(sublist)))
    return all_occ_list

def replace_irrelevant_component_with_star(clue_list, unit_list):
    temp_list = clue_list.copy()
    for index, clue in enumerate(temp_list):
        if clue not in ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP', 'EX', 'BE', 'RP', 'motion', 'stative'] + verb_tag_list + SpRl_list:
            clue_list[index] = '*'
    return clue_list

def get_prep_position(unit_list):
    position = -1
    for unit in unit_list:
        if unit.get_pos() == 'RP':
            position = unit.get_position()
    return position

def get_stative_position(unit_list):
    position = -1
    for unit in unit_list:
        if unit.get_match_clue() == 'stative':
            position = unit.get_position()
    return position

def get_figure_relation_ground(constr_type, pattern, unit_list):
    for index, clue in enumerate(pattern):
        if clue in ['RP','on the left', 'on the right']:
            prep_unit = unit_list[index]
            if prep_unit.get_word() in only_motion_prep_list:
                return None

    locative_repr = locative({})
    figure_list = []
    ground_list = []
    #get the position of prep

    prep_position = get_prep_position(unit_list)
    stative_position = get_stative_position(unit_list)
    prep_unit = get_unit_by_position(prep_position, unit_list)
    locative_repr.add_relation(prep_unit)


    if constr_type in ['THEREBE', 'NP_BE_PREP_NP', 'NP_STATIVE_PREP_NP']:
        root_unit = get_root_unit(unit_list)
        print(root_unit.info_dict)
        if root_unit != None:
            if 'nsubj' in  root_unit.get_deps():
                position_list = root_unit.get_deps()['nsubj']
                for position in position_list:
                    unit = get_unit_by_position(position, unit_list)
                    if unit != None:
                        figure_list.append(unit)
                        for buddy in get_buddy_list_of_unit(unit):
                            figure_list.append(buddy)
                        # if unit.get_buddy() != None and len(unit.get_buddy()) > 0:
                        #     for item in unit.get_buddy():
                        #         figure_list.append(item.get_word())
            else:
                if stative_position != -1:
                    for unit in unit_list:
                        if unit.get_pos() in NP_tag_list and unit.get_position() < stative_position:
                            figure_list.append(unit)

    elif constr_type in ['NP_PREP_NP', 'SpRL_PATTERN']:
        for unit in unit_list:
            if unit.get_position() < prep_position and unit.get_pos() in NP_tag_list:
                figure_list.append(unit)
                for buddy in get_buddy_list_of_unit(unit):
                    figure_list.append(buddy)
    elif constr_type in ['RP_NP_STATIVE_NP']:
        for unit in unit_list:
            if unit.get_position() > stative_position and unit.get_pos() in NP_tag_list:
                figure_list.append(unit)
                for buddy in get_buddy_list_of_unit(unit):
                    figure_list.append(buddy)


    locative_repr.add_figure(figure_list)

    #get ground
    if constr_type in ['THEREBE', 'NP_BE_PREP_NP', 'NP_STATIVE_PREP_NP', 'NP_PREP_NP']:
        for unit in unit_list:
            if unit.get_position() > prep_position and unit.get_pos() in NP_tag_list:
                ground_list.append(unit)
                for buddy in get_buddy_list_of_unit(unit):
                    ground_list.append(buddy)
    elif constr_type in ['RP_NP_STATIVE_NP']:
        for unit in unit_list:
            if unit.get_position() < stative_position and unit.get_pos() in NP_tag_list:
                ground_list.append(unit)
                for buddy in get_buddy_list_of_unit(unit):
                    ground_list.append(buddy)


    locative_repr.add_ground(ground_list)
    #print('prep_position', prep_position)

    return locative_repr


def print_locative_expr(locative_repr):
    for key, value in locative_repr.info_dict.items():
        print(key, value)



def get_locative_semantic_repr(unit_list, occ_and_pattern_dict):
    occ_and_pattern_dict = remove_overlap_dict(occ_and_pattern_dict)
    locative_repr_list = []
    for occ, type_pattern_tuple in occ_and_pattern_dict.items():
        temp_unit_list = []
        start_position = list(occ)[0]
        end_position = list(occ)[-1]
        constr_type = type_pattern_tuple[0]
        pattern = type_pattern_tuple[1]
        # if type == "NP_STATIVE_PREP_NP":
        #     temp_unit_list = unit_list[0:end_position+1]
        # else:
        #     temp_unit_list = unit_list[start_position:end_position+1]
        temp_unit_list = unit_list[start_position:end_position+1]
        locative_repr = get_figure_relation_ground(constr_type, pattern, temp_unit_list)
        if locative_repr != None:
            locative_repr_list.append(locative_repr)

    return locative_repr_list

def remove_redundant_elements_between_motion_and_RP(clue_list):
    if 'motion' in clue_list:
        motion_index = clue_list.index('motion')
        if 'RP' in clue_list:
            RP_index = clue_list.index('RP')
            first_NP_flag = 0
            first_NP_index = -1
            for index, clue in enumerate(clue_list):
                if index > motion_index and index < RP_index:
                    if first_NP_flag == 1:
                        clue_list[index] = '*'
                    if clue in NP_tag_list and first_NP_flag == 0:
                        first_NP_flag = 1
    return clue_list
# clue_list = ['PRP', 'PRP$', 'NN', 'NN', 'motion', 'NN', 'JJ', 'NNS', 'RP', 'NN', 'RP', 'NN']
# remove_redundant_elements_between_motion_and_RP(clue_list)
def replace_two_adjacent_preps_with_star(clue_list):
    occ_list = find_all_sublist_in_list(['RP', 'RP'], clue_list)
    #print(occ_list)
    for occ in occ_list:
        clue_list[occ[-1]] = '*'
    return clue_list

def get_exact_pattern_list_from_regular_pattern_list(regular_pattern_list):
    fuzzy_pattern_list = list(itertools.product(*regular_pattern_list))
    exact_pattern_list = []
    for pattern in fuzzy_pattern_list:
        temp_list = get_exact_pattern_list_for_single_fuzzy_pattern(pattern)
        exact_pattern_list = exact_pattern_list + temp_list
    return exact_pattern_list

def replace_two_adjacent_nouns_with_star(clue_list, unit_list):
    regular_pattern_list = [['NN','NNS', 'NNP', 'NNPS', 'PRP'],[1], ['NN','NNS', 'NNP', 'NNPS', 'PRP']]
    exact_pattern_list = get_exact_pattern_list_from_regular_pattern_list(regular_pattern_list)
    for pattern in exact_pattern_list:
        occ_list = find_all_sublist_in_list(pattern, clue_list)
        for occ in occ_list:
            first_unit = get_unit_by_position(unit_list[occ[0]].get_position(), unit_list)
            #print('???', first_unit.info_dict)
            if first_unit != None and 'case' not in first_unit.get_deps():
                clue_list[occ[-1]] = '*'
    return clue_list

# clue_list = ['PRP', 'PRP$', 'NN', 'NN', 'motion', 'NN', 'JJ', 'NNS','RP', 'RP', 'NN', 'RP', 'NN']
# clue_list = replace_two_adjacent_preps_with_star(clue_list)
# print(clue_list)


def get_action_unit(unit_list):
    action_unit = semantic_unit({},[])
    for unit in unit_list:
        if unit.get_match_clue() == 'motion':
            action_unit = unit
            break
    return action_unit

def remove_PP_before_motion(semantic_unit_list):

    #get motion position
    motion_position = -1
    for unit in semantic_unit_list:
        if unit.get_match_clue() == 'motion':
            motion_position = unit.get_position()
    prep_list = get_prep_list(semantic_unit_list)
    remove_list = []
    for unit in prep_list:
        prep_position = unit.get_position()
        if prep_position < motion_position:
            remove_list.append(unit)
            for item in semantic_unit_list:
                if item.get_position() > prep_position and item.get_position() < motion_position and item.get_semantic_role() not in ['agent', 'recipient', 'object']:
                    remove_list.append(item)

    for unit in remove_list:
        semantic_unit_list.remove(unit)
    return semantic_unit_list






def get_motion_semantic_repr(all_unit_list, motion_occ_and_pattern_dict):
    motion_event_list = []
    for occ, type_pattern_tuple in motion_occ_and_pattern_dict.items():
        #print(occ, get_min_nsubj_index(all_unit_list))
        constr_type = type_pattern_tuple[0]
        pattern = type_pattern_tuple[1]
        new_motion_event = motion_event({})
        start_position = min(occ[0], get_min_nsubj_index(all_unit_list))
        end_position = list(occ)[-1] +1
        #nsubj_position = get_nsubj_position_list(all_unit_list)
        #print(start_position, end_position)
        pattern_unit_list = all_unit_list[start_position:end_position]
        #print_semantic_unit_list(pattern_unit_list)
        #print('------------')
        # print_semantic_unit_list(all_unit_list)
        print('original clue list .......', get_match_clue_list(pattern_unit_list))
        pattern_unit_list = extend_scope_of_motion_event_pattern(pattern_unit_list, all_unit_list, occ)
        print('extended clue list .......', get_match_clue_list(pattern_unit_list))
        #pattern_unit_list = remove_PP_before_motion(pattern_unit_list)
        #print('remove PP clue list .......', get_match_clue_list(pattern_unit_list))

        action_unit = get_action_unit(pattern_unit_list)
        new_motion_event.add_action(action_unit.get_word())
        new_motion_event = get_all_participants(constr_type, pattern_unit_list, new_motion_event)
        new_motion_event = get_spatial_relations(new_motion_event)
        motion_event_list.append(new_motion_event)

    return motion_event_list


def get_match_clue_list(semantic_unit_list):
    clue_list = []
    for unit in semantic_unit_list:
        clue_list.append(unit.get_match_clue())
    return clue_list

def get_min_nsubj_index(all_unit_list):
    index = 100
    root_unit = get_root_unit(all_unit_list)
    position_list = []
    index_list = []
    if 'nsubj' in root_unit.get_deps():
        position_list = root_unit.get_deps()['nsubj']
        for position in position_list:
            for index, unit in enumerate(all_unit_list):
                if unit.get_position() == position:
                    index_list.append(index)
    if len(index_list) > 0:
        index = min(index_list)

    return index

def extend_scope_of_motion_event_pattern(pattern_unit_list,all_unit_list, occ):
    start_position = occ[0]
    end_position = occ[-1]
    before_list = all_unit_list[0:start_position]
    remaining_list = all_unit_list[end_position+1:]
    prep_unit = semantic_unit({},[])
    verb_position = 100
    #afterward extension
    for unit in remaining_list:
        if unit.get_pos() in verb_tag_list:
            verb_position = unit.get_position()

    for unit in remaining_list:
        if unit.get_word() in only_motion_prep_list and unit.get_position() < verb_position :
            prep_unit = unit
            pattern_unit_list.append(unit)

    prep_position = prep_unit.get_position()
    if prep_position != None:
        for unit in remaining_list:
            if unit.get_position() == prep_position+1 and unit.get_pos() in verb_tag_list:
               pattern_unit_list.remove(prep_unit)
               break
            elif unit.get_position() > prep_position and unit.get_pos() in NP_tag_list and unit.get_position() < verb_position:
                pattern_unit_list.append(unit)
                break

    #backward extension
    # verb_position = -1
    # for unit in before_list:
    #     if unit.get_pos() in verb_tag_list:
    #         verb_position = unit.get_position()
    # if verb_position == -1:
    #     for unit in before_list:
    #         pattern_unit_list.append(unit)
    pattern_unit_list = sorted(pattern_unit_list, key = get_position)
    return pattern_unit_list


def get_final_spatial_representation(unit_list, final_pattern_dict):
    clue_list = []
    for unit in unit_list:
        if unit.get_match_clue() != None:
            clue_list.append(unit.get_match_clue())
    print('clue_list', clue_list)
    clue_list = replace_irrelevant_component_with_star(clue_list, unit_list)
    clue_list = remove_redundant_elements_between_motion_and_RP(clue_list)
    clue_list = replace_two_adjacent_preps_with_star(clue_list)
    print('clue_list', clue_list)
    clue_list = replace_two_adjacent_nouns_with_star(clue_list, unit_list)
    print('clue_list', clue_list)
    locative_occ_and_pattern_dict = {}
    motion_occ_and_pattern_dict = {}
    all_occ_and_pattern_dict = {}
    for constr_type, pattern_list in final_pattern_dict.items():
        for pattern in pattern_list:
            all_occ_list = find_all_sublist_in_list(pattern, clue_list)
            temp_dict = {}
            if len(all_occ_list) != 0:
                #print(all_occ_list, pattern)
                for occ in all_occ_list:
                    temp_dict[occ] = (constr_type, pattern)
                all_occ_and_pattern_dict.update(temp_dict)
    all_occ_and_pattern_dict = remove_overlap_dict(all_occ_and_pattern_dict)
    print('all_occ_and_pattern_dict', all_occ_and_pattern_dict)
    for occ, type_pattern_tuple in all_occ_and_pattern_dict.items():
        if type_pattern_tuple[0] in motion_construction_list:
            statistic_dict[type_pattern_tuple[0]] = statistic_dict[type_pattern_tuple[0]] + 1
            motion_occ_and_pattern_dict[occ] = type_pattern_tuple
        elif type_pattern_tuple[0] in locative_construction_list:
            statistic_dict[type_pattern_tuple[0]] = statistic_dict[type_pattern_tuple[0]] + 1
            locative_occ_and_pattern_dict[occ] = type_pattern_tuple

    print('locative_occ_and_pattern_dict', locative_occ_and_pattern_dict)
    print('motion_occ_and_pattern_dict', motion_occ_and_pattern_dict)

    locative_repr_list = get_locative_semantic_repr(unit_list, locative_occ_and_pattern_dict)
    motion_repr_list = get_motion_semantic_repr(unit_list,motion_occ_and_pattern_dict)
    return locative_repr_list, motion_repr_list





if __name__ == '__main__':
    a = 0
    example = "He got a hole in his sock."
    sentence_list = sent_tokenize(example)

    #sentence = 'There is a dog under the table'
    sentence = "In the storm, the tree and the table fell down and crashed through the roof of my house. Now, I have to get it removed."
    sentence = "The sculpture rolled off the shelf because it wasn't level."
    sentence = "I poured the water from the bottle to the cup"
    sentence = "The sack of potatoes had been placed below the bag of flour, so it had to be moved first."
    sentence = "There is a pillar and a girl between me and the stage, and I can't see it."
    sentence = "The pen fell from the table to the ground."
    sentence = "The new house has a roof on top of the walls."
    sentence = 'when he reached the top of the ladder. He reaches a good score'
    sentence = 'a fountain and cobbled walkway is on the top'
    sentence = 'a dark-skinned , dark-haired boy wearing a light blue tee-shirt is standing in a classroom .'
    sentence = 'a room with a wall made of red bricks ( on the left ) and a white wall with two pictures ( on the right ) '
    sentence = 'a dark-haired baby pointing at the camera .'
    sentence = 'Interior view of a room with a large bed with red bedcovers , a white wooden desk and chair below a TV fixed in the corner , a white fridge and a glass door with a wooden frame leading onto a veranda and garden .'
    sentence = 'one person sitting on a bench in front of the house ( on the left ) .'
    sentence = 'two lane street with large shops on the right and smaller shops on the left .'
    #sentence = 'a wooden bulk bed with grey mattresses and red curtains '
    path_verb_dict = load_path_verb_dict()
    verb_form_dict = load_verb_form_dict()
    sentence = preprocessing_of_sentence(sentence, path_verb_dict, verb_form_dict)
    print(sentence)


    sentence_list = sent_tokenize(sentence.strip())
    final_pattern_dict = get_final_pattern_dict(regular_pattern_dict)
    for sentence in sentence_list:
        sentence = sentence.replace('?', ' ')
        print('************', sentence)
        parse = get_dependency_analysis_of_sentence(sentence)
        semantic_unit_list = get_semantic_unit_list(sentence, parse)
        semantic_unit_list = add_buddy_to_unit(semantic_unit_list)
        word_list = get_word_list(semantic_unit_list)
        #print(all_prep_list)
        semantic_unit_list = construction_recognition(word_list, semantic_unit_list, all_prep_list, 'RP')
        semantic_unit_list = remove_repeating_semantic_unit(semantic_unit_list)
        father_children_dict = get_father_children_list(parse)
        root_list = get_all_root_list(parse)
        root_children_dict = get_root_children_dict(root_list, father_children_dict)
        event_dict = get_event_dict(sentence, root_children_dict, semantic_unit_list)
        for event, children in event_dict.items():
            print(event.info_dict)
            print('-----------  semantic unit list -----------')
            print_semantic_unit_list(children)
            print('-----------  semantic unit list -----------')
            locative_repr_list, motion_repr_list = get_final_spatial_representation(children, final_pattern_dict)
            for locative_repr in locative_repr_list:
                print('-----------  locative construction -----------')
                print_locative_expr(locative_repr)
                print('-----------  locative construction -----------')
            for motion_repr in motion_repr_list:
                print('-----------   motion construction  -----------')
                print_motion_event(motion_repr)
                print('-----------   motion construction  -----------')
