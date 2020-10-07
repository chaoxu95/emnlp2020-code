#!/usr/bin/env python3
##############################################################################
#       Function: map the kparser representation to motion_event representation
##############################################################################
from semantic import *
from classes import *
from nltk.tokenize import sent_tokenize
from fuzzy_match import *

def get_separate_event_expr(sentence, semantic_unit_list):
    sentence = get_complete_expr_of_abbr(sentence)
    word_list = word_tokenize(sentence)
    data = get_json_from_kparser(sentence)
    get_all_unit_position_list(data)
    #print(all_unit_position_dict)
    break_point = get_break_point_position(all_unit_position_dict, semantic_unit_list)
    #print('break_point', children)
    first_word_list = []
    second_word_list = []
    event_list = []
    for index, word in enumerate(word_list):
        if index < break_point-1:
            first_word_list.append(word)
        elif index > break_point-1:
            second_word_list.append(word)

    first_event = ' '.join(first_word_list)
    second_event = ' '.join(second_word_list)
    event_list.append(first_event)
    event_list.append(second_event)
    return event_list

def get_prep_list(semantic_unit_list):
    prep_list = []
    motion_position = -1
    for unit in semantic_unit_list:
        if unit.get_match_clue() == 'motion':
            motion_position = unit.get_position()
    for unit in semantic_unit_list:
        if unit.get_pos() == 'RP' and unit.get_position() > motion_position:
            prep_list.append(unit)
    return prep_list

def get_prep_list_in_occ(occ, semantic_unit_list):
    position_list = [i+1 for i in occ]
    print(position_list)
    prep_list = []
    for unit in semantic_unit_list:
        #print('???????', unit.get_word())
        if unit.get_pos() == 'RP' and unit.get_position() in position_list:
            prep_list.append(unit)
    return prep_list

def get_ground_for_prep(prep_unit, semantic_unit_list):
    ground = semantic_unit({},[])
    #print(prep_unit.info_dict)
    prep_position = prep_unit.get_position()
    #print(prep_position)
    for unit in semantic_unit_list:
        #print(unit.get_position(), unit.get_pos())
        if unit.get_position() > prep_position and unit.get_pos() in ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']:
            ground = unit
            break
    return ground

def remove_components_after_prep(semantic_unit_list):
    prep_list = get_prep_list(semantic_unit_list)
    prep_position = 100
    remaining_list = []
    if len(prep_list) != 0:
        prep_position = prep_list[0].get_position()
    for unit in semantic_unit_list:
        if unit.get_position() < prep_position:
            remaining_list.append(unit)
    return remaining_list

def get_participant_role_list(semantic_unit_list):
    semantic_role_list = []
    for unit in semantic_unit_list:
        if unit.get_semantic_role() in ['agent', 'recipient', 'object']:
            semantic_role_list.append(unit.get_semantic_role())
    semantic_role_list = list(set(semantic_role_list))
    return semantic_role_list

def get_passive_voice_flag(semantic_unit_list):
    passive_voice_flag = 0
    for unit in semantic_unit_list:
        if unit.get_semantic_role() ==  'passive_supporting_verb':
            passive_voice_flag = 1
    return passive_voice_flag

def get_root_unit(semantic_unit_list):
    root_list = []
    for unit in semantic_unit_list:
        if unit.get_root_flag() == True:
            root_list.append(unit)
    if len(root_list) == 0:
        for unit in semantic_unit_list:
            if unit.get_pos() in verb_tag_list:
                root_list.append(unit)
                break
    return root_list[0]

def get_buddy_list_of_unit(unit):
    buddy_list = []
    if unit.get_buddy() != None:
        buddy_list = unit.get_buddy()
    return buddy_list

def get_NP_list_before_verb(semantic_unit_list):
    NP_list = []
    verb_position = -1
    for unit in semantic_unit_list:
        if unit.get_pos() in verb_tag_list:
            verb_position = unit.get_position()
    for unit in semantic_unit_list:
        if unit.get_pos() in NP_tag_list and unit.get_position()< verb_position:
            NP_list.append(unit)
            buddy_list = get_buddy_list_of_unit(unit)
            NP_list = NP_list + buddy_list
    NP_list = list(set(NP_list))
    return NP_list

def get_NP_list_between_verb_and_prep(semantic_unit_list):
    NP_list = []
    verb_position = -1
    prep_position = -1
    for unit in semantic_unit_list:
        if unit.get_pos() in verb_tag_list:
            verb_position = unit.get_position()
        elif unit.get_pos() == 'RP':
            prep_position = unit.get_position()
    for unit in semantic_unit_list:
        position = unit.get_position()
        if unit.get_pos() in NP_tag_list and position > verb_position and position < prep_position:
            NP_list.append(unit)
            buddy_list = get_buddy_list_of_unit(unit)
            NP_list = NP_list + buddy_list
    NP_list = list(set(NP_list))
    return NP_list




def get_agent_and_figure(constr_type, semantic_unit_list):
    motion_constr_list = ['MOTION', 'MOTION_GROUND_OMISSION']
    caused_motion_constr_list = ['CAUSED_MOTION', 'CAUSED_MOTION_GROUND_OMISSION']
    #print_semantic_unit_list(semantic_unit_list)
    agent_list = []
    figure_list = []
    root_unit = get_root_unit(semantic_unit_list)
    if root_unit != None:
        if 'nsubj' in root_unit.get_deps():
            position_list = root_unit.get_deps()['nsubj']
            for position in position_list:
                unit = get_unit_by_position(position, semantic_unit_list)
                #print('??', unit.info_dict)
                unit_list = []
                if unit != None:
                    unit_list.append(unit)
                    if unit.get_buddy() != None and len(unit.get_buddy()) > 0:
                        for item in unit.get_buddy():
                            unit_list.append(item)
            if constr_type in motion_constr_list:
                figure_list = unit_list
            elif constr_type in caused_motion_constr_list:
                agent_list = unit_list

        if 'dobj' in root_unit.get_deps():
            position_list = root_unit.get_deps()['dobj']
            for position in position_list:
                unit = get_unit_by_position(position, semantic_unit_list)
                unit_list = []
                if unit != None:
                    unit_list.append(unit)
                    if unit.get_buddy() != None and len(unit.get_buddy()) > 0:
                        for item in unit.get_buddy():
                            unit_list.append(item)

            if constr_type in caused_motion_constr_list:
                figure_list = unit_list

        if constr_type in caused_motion_constr_list and len(agent_list) == 0:
            NP_list = get_NP_list_before_verb(semantic_unit_list)
            agent_list = NP_list

        if len(figure_list) == 0:
            if constr_type in  motion_constr_list:
                NP_list = get_NP_list_before_verb(semantic_unit_list)

            elif constr_type in caused_motion_constr_list:
                NP_list = get_NP_list_between_verb_and_prep(semantic_unit_list)
            figure_list = NP_list
    return agent_list, figure_list

def add_str_to_str(final_str, single_str, split_symbol):
    if final_str == "":
        final_str = single_str
    else:
        final_str = final_str + split_symbol + single_str
    return final_str

def print_motion_event(motion_event):
    for role, value in motion_event.info_dict.items():
        print_expr = ""
        if value != None:
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
        else:
            print_expr = 'unknown'

        print(role+':'+print_expr)


def get_all_participants(constr_type, semantic_unit_list, motion_event):
    prep_list = get_prep_list(semantic_unit_list)
    ground_dict = {}
    #print_semantic_unit_list(semantic_unit_list)
    for prep in prep_list:
        ground = get_ground_for_prep(prep, semantic_unit_list)
        ground_dict[prep] = ground
    motion_event.add_ground(ground_dict)

    #part_semantic_unit_list = remove_components_after_prep(semantic_unit_list)

    agent_list, figure_list = get_agent_and_figure(constr_type, semantic_unit_list)
    motion_event.add_agent(agent_list)
    motion_event.add_figure(figure_list)
    return motion_event

def remove_repeating_and_unknown(spatial_list):
    spatial_list = list(set(spatial_list))
    if 'unknown' in spatial_list and len(spatial_list) >1:
        spatial_list.remove('unknown')
    return spatial_list

def get_spatial_relations(motion_event):
    SVGP_list = ['in', 'into', 'inside', 'out of', 'onto', 'to', 'from', 'through', 'up', 'down', 'over', 'by', 'out']
    orientation_list = ['toward', 'away from']
    path_list = ['along', 'around']
    ground_dict = motion_event.get_ground()
    source_list = []
    via_list = []
    goal_list = []
    path_list = []
    toward_list = []
    away_from_list = []
    for prep, ground in ground_dict.items():
        prep_word = prep.get_word()
        ground_word = ground.get_word()
        if ground_word == None:
            ground_word = "unknown ground"

        if prep_word in SVGP_list:
            source_word = prep_dict[prep_word]['source']
            via_word = prep_dict[prep_word]['via']
            goal_word = prep_dict[prep_word]['goal']
            path_word = prep_dict[prep_word]['path']
            if source_word == 'unknown':
                source = 'unknown'
            else:
                if source_word == 'self':
                    source = ground_word
                elif prep_word in ['up','down', 'over']:
                    source = source_word
                else:
                    source = source_word + ' of ' + ground_word
            source_list.append(source)

            if goal_word == 'unknown':
                goal = 'unknown'
            else:
                if goal_word == 'self':
                    goal = ground_word
                elif prep_word in ['up','down', 'over']:
                    goal = goal_word
                else:
                    goal = goal_word + ' of ' + ground_word
            goal_list.append(goal)

            if path_word == 'unknown':
                path = 'unknown'
            else:
                if path_word == 'self':
                    path = ground_word
                elif path_word in ['up','down', 'over']:
                    path = path_word
                else:
                    path = path_word + ' of ' + ground_word
            path_list.append(path)

            if via_word == 'unknown':
                via = 'unknown'
            else:
                if via_word == 'self':
                    via = ground_word
                elif prep_word in ['up','down', 'over']:
                    via = via_word
                elif via_word == 'new point':
                    via = 'a new point ' + prep_dict[prep_word]['position'] + ' ' + ground_word
                else:
                    via = via_word + ' of ' + ground_word
            via_list.append(via)
        elif prep_word in orientation_list:
            toward_word = prep_dict[prep_word]['toward']
            away_from_word = prep_dict[prep_word]['away from']
            if toward_word == 'unknown':
                toward = 'unknown'
            else:
                toward = ground_word
            toward_list.append(toward)

            if away_from_word == 'unknown':
                away_from = 'unknown'
            else:
                away_from = ground_word
            away_from_list.append(away_from)

        elif prep_word in path_list:
            path_word = prep_dict[prep_word]['path']
            if path_word == 'unknown':
                path = 'unknown'
            else:
                path = path_word
            path_list.append(path)


    source_list = remove_repeating_and_unknown(source_list)
    goal_list = remove_repeating_and_unknown(goal_list)
    via_list = remove_repeating_and_unknown(via_list)
    path_list = remove_repeating_and_unknown(path_list)
    toward_list = remove_repeating_and_unknown(toward_list)
    away_from_list = remove_repeating_and_unknown(away_from_list)
    motion_event.add_source(source_list)
    motion_event.add_goal(goal_list)
    motion_event.add_via(via_list)
    motion_event.add_path(path_list)
    motion_event.add_toward(toward_list)
    motion_event.add_away_from(away_from_list)
    return motion_event

if __name__ == '__main__':

    prep_dict = load_motion_prep_dict()

    example = 'Tom throw his schoolbag down to Ray when he got to the top of the ladder.'
    #example = "Tom run into a school"
    #example = "Tom move it to a box"
    #example = "I and Tom threw the apples and bottles through window"
    #example = 'Tom and I poured the water and other drinks from the bottle to the cup'
    example = 'Tom throw his schoolbag down to Ray when he got to the top of the ladder. Tom and I poured the water and other drinks from the bottle to the cup'
    example = 'The customer walked into the bank and stabbed one of the tellers. He was immediately taken to the police station.'
    example = "Tom and I walked into police station near to his house and then move the box into it"
    sentence_list = sent_tokenize(example)
    sentence_index = 0
    final_pattern_dict = get_final_pattern_dict(regular_pattern_dict)
    for sentence in sentence_list:
        event_dict = {}
        motion_event_list = []

        print('******************** '+sentence+' ********************')
        parse = get_dependency_analysis_of_sentence(sentence)
        semantic_unit_list = get_semantic_unit_list(sentence, parse)
        lemma_list = get_lemma_list(semantic_unit_list)
        semantic_unit_list = construction_recognition(lemma_list, semantic_unit_list, all_prep_list, 'RP')
        semantic_unit_list = remove_repeating_semantic_unit(semantic_unit_list)
        father_children_dict = get_father_children_list(parse)
        root_list = get_all_root_list(parse)
        root_children_dict = get_root_children_dict(root_list, father_children_dict)
        event_dict = get_event_dict(root_children_dict, semantic_unit_list)
        for event, children in event_dict.items():
            print_semantic_unit_list(children)
