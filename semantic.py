#!/usr/bin/env python3
##############################################################################
#       Function: get kparser representation
##############################################################################
from corenlp import *
from classes import *
from itertools import chain, product
from nltk.tokenize import sent_tokenize
from load_file import *
import re

prep_dict = load_motion_prep_dict()
spatial_prep_list = load_all_prep_list()
motion_verb_list = load_motion_verb_list()
caused_motion_verb_list = load_caused_motion_verb_list()
stative_verb_list = load_stative_verb_list()
all_motion_verb_list = motion_verb_list + caused_motion_verb_list
verb_tag_list = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
BE_list = ['is', 'am', 'are', 'was', 'were', 'being', 'been', 'be']
NP_tag_list = ['NN','NNS', 'NNP', 'NNPS', 'PRP']
place_list = ['NN','NNS', 'NNP', 'NNPS', 'place', 'PRP']
locative_prep_list = []
only_motion_prep_list = ['from', 'into', 'onto', 'to', 'towards', 'toward', 'through']
special_construction = ['have to', 'has to', 'had to', '\'s']
non_spatial_prep_list = ['of']
defaultdict = {'word':'', 'lemma':'', 'pos':-1, 'start_position':-1, 'end_position':-1, 'deps':{}, 'root_flag':False, 'ner':'0', 'buddy':[] }
all_prep_list = spatial_prep_list + non_spatial_prep_list

def get_semantic_unit_list(sentence, parse):
    root = parse.root
    parse_dict = get_parse_dict_from_parse(parse)
    semantic_unit_list = []
    for index, node in parse_dict.items():
        unit = semantic_unit({}, [])
        unit.add_word(node['word'])
        unit.add_lemma(node['lemma'])
        unit.add_pos(node['ctag'])
        unit.add_position(node['address'])
        unit.add_start_position(node['address'])
        unit.add_end_position(node['address'])
        if root['address'] == index:
            unit.add_root_flag(True)
        else:
            unit.add_root_flag(False)
        temp_dict = {}
        for item in node['deps']:
            temp_dict[item] = node['deps'][item]
        unit.add_deps(temp_dict)
        semantic_unit_list.append(unit)
    entity_list = get_entity_of_sentence(sentence)
    for word, category in entity_list:
        for unit in semantic_unit_list:
            if unit.info_dict['word'] == word and category != '0':
                unit.add_ner(category)
    return semantic_unit_list

def print_semantic_unit_list(semantic_unit_list):
    for unit in semantic_unit_list:
        print(dict(unit.info_dict))

def get_father_children_list(parse):
    father_children_dict = {}
    parse_dict = get_parse_dict_from_parse(parse)
    for index, node in parse_dict.items():
        temp_list = []
        for rel, value in node['deps'].items():
            if rel not in ['advcl', 'punct', 'cc', 'conj']:
                temp_list.append(value)
            elif rel == 'advcl':
                for advcl_position in value:
                    mark_pos = ""
                    mark_position_list = parse_dict[advcl_position]['deps']['mark']
                    #print('???????', mark_position_list)
                    for mark_position in mark_position_list:
                        mark_node = parse_dict[mark_position]
                        mark_word = mark_node['word']
                        #print('????????////////', mark_pos)
                        if mark_word == 'to':
                            temp_list.append([advcl_position])
            #print(rel, value, temp_list)
        if len(temp_list) > 0:
            temp_list = list(chain.from_iterable(temp_list))
            father_children_dict[index] = temp_list
    print('father_children_dict', father_children_dict)

    return father_children_dict

def get_root_from_root(original, parse):

    node = parse.nodes[original]
    root_list = []
    for rel, value in node['deps'].items():
        if rel in ['advcl', 'conj']:
            root_list.append(value)
    root_list = list(chain.from_iterable(root_list))
    for root in root_list:
        temp_list = get_root_from_root(root, parse)
        root_list = root_list + temp_list
    return root_list

def remove_TODO_root(root_list, parse):
    temp_list = root_list
    for root in temp_list:
        mark_position_list = parse.nodes[root]['deps']['mark']
        for mark_position in mark_position_list:
            mark_node = parse.nodes[mark_position]
            mark_pos = mark_node['ctag']
            if mark_pos == 'TO':
                root_list.remove(root)
    return root_list

def get_new_root_from_parse(parse):
    for index, node in parse.nodes.items():
        if node['ctag'] in verb_tag_list:
            return node

def get_all_root_list(parse):
    root = parse.root
    root_list = []
    if root == None:
        root = get_new_root_from_parse(parse)
    root_position = root['address']
    root_list = get_root_from_root(root_position, parse)
    root_list.append(root_position)
    root_list = remove_TODO_root(root_list, parse)

    root_list = sorted(root_list)
    print('root_list', root_list)

    return root_list

def get_all_reachable_node(original, father_children_dict):
    all_reachable_node = []
    if original in father_children_dict.keys():
        original_list = father_children_dict[original]
        all_reachable_node = all_reachable_node + original_list
        for node in original_list:
            temp_list = get_all_reachable_node(node, father_children_dict)
            all_reachable_node = all_reachable_node + temp_list
    all_reachable_node = sorted(all_reachable_node)
    return all_reachable_node


def get_root_children_dict(root_address_list, father_children_dict):
    root_children_dict = {}
    for root in root_address_list:
        children_list = get_all_reachable_node(root, father_children_dict)
        root_children_dict[root] = children_list
    return root_children_dict

def deal_with_root_in_a_phrase(root, semantic_unit_list):
    position_range_dict = {}

    for unit in semantic_unit_list:
        position_range_dict[unit.get_position()] = range(unit.get_start_position(), unit.get_end_position()+1)
    if root in position_range_dict.keys():
        return root
    else:
        for position, range_x in position_range_dict.items():
            if root in range_x:
                return position

def get_unit_by_position(position, semantic_unit_list):
    for unit in semantic_unit_list:
        if unit.get_position() == position:
            return unit



def get_unit_list_by_position_range(range, semantic_unit_list):
    unit_list = []
    for index in range:
        for unit in semantic_unit_list:
            if unit.get_position() == index:
                unit_list.append(unit)
    return unit_list

def get_position(element):
    if element.get_position() != None:
        return int(element.get_position())
    else:
        return 100

def get_new_event_by_hand(semantic_unit_list):
    for unit in semantic_unit_list:
        if unit.get_pos() in verb_tag_list:
            return unit

# def get_event_dict(root_children_dict, semantic_unit_list):
#     event_dict = {}
#     previous_event_position = -1
#     # if len(root_children_dict) == 1:
#     #     (root, child_dict), = root_children_dict.items()
#     #     event_unit = get_unit_by_position(root, semantic_unit_list)
#     #     semantic_unit_list = get_merged_semantic_unit_list(semantic_unit_list)
#     #     event_dict[event_unit] = semantic_unit_list
#     #     return event_dict
#     for event_position, scope_position_list in root_children_dict.items():
#         print('event_position???', event_position)
#         event_unit = get_unit_by_position(event_position, semantic_unit_list)
#         if event_unit == None: #or event_unit.get_pos() in NP_tag_list:
#             event_unit = get_new_event_by_hand(semantic_unit_list)
#         event_unit.add_root_flag(True)
#         temp_list = scope_position_list + [event_position]
#         #print('temp_list', temp_list)
#         begin_pos = min(temp_list)
#         end_pos = max(temp_list)
#
#         scope_unit_list = get_unit_list_by_position_range(range(begin_pos, end_pos+1), semantic_unit_list)
#         subj_list = [x for x in event_unit.info_dict['deps'] if x in ['nsubj', 'csubj', 'nsubjpass']]
#         if len(subj_list) == 0 and previous_event_position != -1:
#             previous_event_unit = get_unit_by_position(previous_event_position, semantic_unit_list)
#
#             for rel, position_list in previous_event_unit.info_dict['deps'].items():
#                 if rel in ['nsubj', 'csubj', 'nsubjpass']:
#                     subj_position = position_list
#                     break
#             for position in position_list:
#                 unit = get_unit_by_position(position, semantic_unit_list)
#                 if unit != None:
#                     unit.add_added_subj_flag(True)
#                     scope_unit_list.append(unit)
#
#
#         scope_unit_list = get_merged_semantic_unit_list(scope_unit_list)
#         scope_unit_list = sorted(scope_unit_list, key = get_position)
#         print('scope_unit_list', scope_unit_list)
#         event_dict[event_unit] = scope_unit_list
#
#         previous_event_position = event_position
#
#     return event_dict

def add_start_end_index_to_semantic_unit(sentence, semantic_unit_list):
    for unit in semantic_unit_list:
        word = unit.get_word()
        #print('------', word)
        if word != None:
            result = re.search(word, sentence)
            #print('******', result, word, sentence)
            if result != None:
                sentence = re.sub(word, ' '*len(word), sentence, 1)
                #print(result)
                #print(sentence)
                unit.add_start_index(result.span()[0])
                unit.add_end_index(result.span()[1])
    return semantic_unit_list

def get_position_list(semantic_unit_list):
    position_list = []
    for unit in semantic_unit_list:
        #if unit.get_position() > 0:
        position_list.append(unit.get_position())
    return position_list



def get_event_dict(sentence, root_children_dict, semantic_unit_list):
    event_dict = {}
    new_root_children_dict = {}
    previous_event_position = -1
    #if len(root_children_dict) == 1:
    #print_semantic_unit_list(semantic_unit_list)
    position_list = get_position_list(semantic_unit_list)
    position_list = sorted(list(set(position_list)))
    root = -1
    for root_position, children_dict in root_children_dict.items():
        root = root_position
    root = deal_with_root_in_a_phrase(root, semantic_unit_list)


    new_root_children_dict[root] = position_list
    print('new_root_children_dict', new_root_children_dict)

    for event_position, scope_position_list in new_root_children_dict.items():
        print('event_position???', event_position)
        event_unit = get_unit_by_position(event_position, semantic_unit_list)
        if event_unit == None: #or event_unit.get_pos() in NP_tag_list:
            event_unit = get_new_event_by_hand(semantic_unit_list)
        event_unit.add_root_flag(True)
        temp_list = scope_position_list + [event_position]
        #print('temp_list', temp_list)
        begin_pos = min(temp_list)
        end_pos = max(temp_list)

        scope_unit_list = get_unit_list_by_position_range(range(begin_pos, end_pos+1), semantic_unit_list)
        subj_list = [x for x in event_unit.info_dict['deps'] if x in ['nsubj', 'csubj', 'nsubjpass']]
        if len(subj_list) == 0 and previous_event_position != -1:
            previous_event_unit = get_unit_by_position(previous_event_position, semantic_unit_list)

            for rel, position_list in previous_event_unit.info_dict['deps'].items():
                if rel in ['nsubj', 'csubj', 'nsubjpass']:
                    subj_position = position_list
                    break
            for position in position_list:
                unit = get_unit_by_position(position, semantic_unit_list)
                if unit != None:
                    unit.add_added_subj_flag(True)
                    scope_unit_list.append(unit)


        scope_unit_list = get_merged_semantic_unit_list(scope_unit_list)

        scope_unit_list = add_start_end_index_to_semantic_unit(sentence, scope_unit_list)
        scope_unit_list = sorted(scope_unit_list, key = get_position)
        print('scope_unit_list', scope_unit_list)
        event_dict[event_unit] = scope_unit_list

        previous_event_position = event_position

    return event_dict

def get_merged_semantic_unit_list(semantic_unit_list):
    semantic_unit_list = merge_adjacent_unit(semantic_unit_list)
    semantic_unit_list = add_merge_clue_to_semantic_unit(semantic_unit_list)

    semantic_unit_list = remove_repeating_semantic_unit(semantic_unit_list)

    regular_pattern_list = [['NN','NNS', 'NNP', 'NNPS'], ['of'], ['NN','NNS', 'NNP', 'NNPS', 'PRP']]
    semantic_unit_list = merge_special_construction_unit(semantic_unit_list, regular_pattern_list, 'NPofNP')
    regular_pattern_list = [['had', 'have', 'has'], ['to']]
    semantic_unit_list = merge_special_construction_unit(semantic_unit_list, regular_pattern_list, 'HaveTo')
    regular_pattern_list = [['PERSON'], ['\'s']]
    semantic_unit_list = merge_special_construction_unit(semantic_unit_list, regular_pattern_list, 'PersonPos')

    semantic_unit_list = sorted(semantic_unit_list, key = get_position)
    semantic_unit_list = add_buddy_to_unit(semantic_unit_list)
    semantic_unit_list = add_match_clue_to_semantic_unit(semantic_unit_list)
    semantic_unit_list = remove_repeating_semantic_unit(semantic_unit_list)

    return semantic_unit_list


def write_semantic_unit_list_to_file(file_name, semantic_unit_list):
    for unit in semantic_unit_list:
        file_name.write(str(unit.info_dict)+'\n')

def merge_adjacent_unit(semantic_unit_list):

    remove_unit_list = []
    for unit in semantic_unit_list:
        unit_position = unit.get_position()
        merge_list = []
        for rel, position_list in unit.get_deps().items():
            if rel in ['amod', 'det', 'nmod:poss', 'nummod']:
                for position in position_list:
                    if abs(unit_position - position) < 4:
                        temp_unit = get_unit_by_position(position, semantic_unit_list)
                        if temp_unit != None:
                            merge_list.append(temp_unit)

            elif rel == 'compound' and unit.get_pos() in NP_tag_list:
                for position in position_list:
                    if abs(unit_position - position) < 4:
                        temp_unit = get_unit_by_position(position, semantic_unit_list)
                        if temp_unit != None:
                            merge_list.append(temp_unit)
        if len(merge_list) > 0:
            remove_unit_list = remove_unit_list + merge_list
            position_list = []
            position_list.append(unit_position)
            for item in merge_list:
                #print(item.info_dict)
                position_list.append(item.get_start_position())
                position_list.append(item.get_end_position())
            start_position = min(position_list)
            end_position = max(position_list)

            word = ""
            for item in semantic_unit_list:
                if item.get_position() in range(start_position, end_position+1):
                    if item.get_word() == '\'s':
                        word = word+item.get_word()
                    else:
                        word = word + ' ' + item.get_word()

            unit.add_word(word.strip())
            unit.add_start_position(start_position)
            unit.add_end_position(end_position)
            unit.add_children_list(merge_list)
    remove_unit_list = list(set(remove_unit_list))

    for unit in remove_unit_list:
        if unit in semantic_unit_list and unit.get_added_subj_flag() != True:
            semantic_unit_list.remove(unit)

    return semantic_unit_list

def remove_repeating_semantic_unit(semantic_unit_list):

    temp_list = semantic_unit_list.copy()
    remove_unit_list = []
    for unit in temp_list:
        if unit.get_start_position() != None and unit.get_end_position() != None:
            position = unit.get_position()
            start_position = unit.get_start_position()
            end_position = unit.get_end_position()
            if end_position - start_position > 0:
                for position in range(start_position, end_position+1):
                    #print('//////////', unit.get_word(),len( range(start_position, end_position+1)),end_position - start_position, position)
                    temp_unit = get_unit_by_position(position, semantic_unit_list)
                    remove_unit_list.append(temp_unit)
                    if unit in remove_unit_list:
                        remove_unit_list.remove(unit)


    print('remove_unit_list', remove_unit_list)
    for unit in remove_unit_list:
        if unit in semantic_unit_list:
            semantic_unit_list.remove(unit)

    return semantic_unit_list


def add_merge_clue_to_semantic_unit(semantic_unit_list):

    for unit in semantic_unit_list:
        if unit.get_lemma() in ['of', 'have', 'to']:
            unit.add_merge_clue(unit.get_word())
        elif unit.get_word() == '\'s':
            unit.add_merge_clue(unit.get_word())
        elif unit.get_ner() == 'PERSON':
            unit.add_merge_clue('PERSON')
        else:
            unit.add_merge_clue(unit.get_pos())

    return semantic_unit_list


def findall_sublist_in_list(sublist, list):
    all_occ_list = []
    possible_occ_list = [index for index, item in enumerate(list) if item == sublist[0]]
    for index in possible_occ_list:
        if list[index:index+len(sublist)] == sublist:
            all_occ_list.append(range(index, index+len(sublist)))

    return all_occ_list

def remove_overlap_list(source_list):
    temp_list = source_list.copy()
    for index, item in enumerate(temp_list):
        compared_list = source_list.copy()
        for temp in compared_list:
            if set(item) > set(temp):
                source_list.remove(temp)
    return source_list

def remove_overlap_dict(source_dict):
    range_list = []
    target_dict = {}
    for range_x, prep in source_dict.items():
        range_list.append(range_x)
    range_list = remove_overlap_list(range_list)
    for range_x in range_list:
        target_dict[range_x] = source_dict[range_x]
    return target_dict

def merge_special_construction_unit(semantic_unit_list,regular_pattern_list, label ):

    new_semantic_unit_list = []
    range_construction_dict = {}
    all_range_list = []

    merge_clue_list = []
    for unit in semantic_unit_list:
        merge_clue_list.append(unit.get_merge_clue())
    print('merge_clue_list: ', merge_clue_list)

    exact_pattern_list = list(product(*regular_pattern_list))

    for pattern in exact_pattern_list:
        pattern = list(pattern)
        occ_list = findall_sublist_in_list(pattern, merge_clue_list)
        if len(occ_list) != 0:
            for occ in occ_list:
                range_construction_dict[occ] = pattern
                occ = [i+1 for i in occ]
                all_range_list = all_range_list + occ


    all_range_list = sorted(list(set(all_range_list)))
    print('merge_adjacent_unit---all_range_list---'+label, all_range_list)
    range_construction_dict = remove_overlap_dict(range_construction_dict)
    print('merge_adjacent_unit---range_construction_dict---'+label, range_construction_dict)

    remove_list = []
    add_list = []
    for range_x, construction in range_construction_dict.items():
        range_x = list(range_x)
        word = ""
        position_list = []
        children_list = []

        relation_list = []
        if label == "NPofNP":
            relation_list = ['head', 'prep', 'trait']
        elif label == "HaveTo":
            relation_list = ['have', 'to']
        elif label == 'PersonPos':
            relation_list = ['person', 'pos']
        temp = semantic_unit_list[range_x[0]:range_x[-1]+1]
        temp_list = temp.copy()

        for index, unit in enumerate(temp_list):
            #print(unit.get_word())
            if label == 'PersonPos':
                word = word + unit.get_word()
            else:
                word = word + ' ' + unit.get_word()
            position_list.append(unit.get_start_position())
            position_list.append(unit.get_end_position())
            children_list.append((relation_list[index],unit))
            remove_list.append(unit)
        new_unit = semantic_unit(temp_list[0].info_dict, children_list)
        new_unit.add_word(word.strip())
        if label == 'HaveTo':
            new_unit.add_pos(label)
        new_unit.add_start_position(min(position_list))
        new_unit.add_end_position(max(position_list))
        add_list.append(new_unit)

    for unit in remove_list:
        if unit in semantic_unit_list:
            semantic_unit_list.remove(unit)
    for unit in add_list:
        semantic_unit_list.append(unit)

    return semantic_unit_list

def add_buddy_to_unit(semantic_unit_list):
    for unit in semantic_unit_list:
        if unit.get_buddy() != None:
            continue
        buddy_list = []
        if 'conj' in unit.get_deps():
            position_list = unit.get_deps()['conj']
            for position in position_list:
                temp_unit = get_unit_by_position(position, semantic_unit_list)
                if temp_unit != None:
                    buddy_list.append(temp_unit)
        if len(buddy_list) > 0:
            unit.add_buddy(buddy_list)
    return semantic_unit_list

def get_lemma_list(semantic_unit_list):
    lemma_list = []
    for unit in semantic_unit_list:
        lemma_list.append(unit.get_lemma())
    return lemma_list

def get_word_list(semantic_unit_list):
    word_list = []
    for unit in semantic_unit_list:
        word_list.append(unit.get_word())
    return word_list

def construction_recognition(lemma_list, semantic_unit_list, construction_list, label):
    new_semantic_unit_list = []
    range_construction_dict = {}
    all_range_list = []
    for construction in construction_list:
        temp_list = construction.split(' ')
        #print(temp_list)
        occ_list = findall_sublist_in_list(temp_list, lemma_list)
        #print('occ_list', construction, occ_list)
        if len(occ_list) != 0:
            #occ_list = remove_overlap_list(occ_list)
            for occ in occ_list:
                range_construction_dict[occ] = construction
                occ = [i+1 for i in occ]
                all_range_list = all_range_list + occ

    all_range_list = sorted(list(set(all_range_list)))
    print('construction_recognition---all_range_list---'+label, all_range_list)
    range_construction_dict = remove_overlap_dict(range_construction_dict)
    print('construction_recognition---range_construction_dict---'+label, range_construction_dict)
    # for unit in semantic_unit_list:
    #     if unit.get_position() not in all_range_list:
    #         new_semantic_unit_list.append(unit)
    for range_x, construction in range_construction_dict.items():
        if len(range_x) == 1:
            unit = get_unit_by_position(range_x[0]+1, semantic_unit_list)
            if unit.get_lemma() not in non_spatial_prep_list:
                unit.add_pos('RP')
        else:
            print(range_x, construction)
            range_x = list(range_x)
            unit = semantic_unit({},[])

            unit.add_word(construction)
            unit.add_lemma(construction)
            unit.add_pos(label)
            unit.add_position(range_x[0]+1)
            unit.add_start_position(range_x[0]+1)
            unit.add_end_position(range_x[-1]+1)
            unit.add_deps({})
            unit.add_root_flag(False)
            unit.add_ner('0')
            unit.add_buddy([])


            semantic_unit_list.append(unit)
    print_semantic_unit_list(semantic_unit_list)
    return semantic_unit_list

def get_prior_unit(source_unit, semantic_unit_list):
    for index, unit in enumerate(semantic_unit_list):
        if unit == source_unit and index > 0:
            return semantic_unit_list[index-1]

def add_match_clue_to_semantic_unit(semantic_unit_list):
    for unit in semantic_unit_list:
        if unit.get_word() in ['on the left', 'on the right']:
            unit.add_match_clue(unit.get_word())
        elif unit.get_ner() in ['DATE']:
            unit.add_match_clue(unit.get_ner())
        elif unit.get_pos() in verb_tag_list and  unit.get_lemma() in stative_verb_list:
            unit.add_match_clue('stative')
        elif unit.get_pos() in verb_tag_list and  unit.get_lemma() in all_motion_verb_list:
            unit.add_match_clue('motion')
        elif unit.get_pos() in verb_tag_list and  unit.get_lemma() == 'be' and unit.get_root_flag() == True:
            unit.add_match_clue('BE')
        elif unit.get_pos() in verb_tag_list  and unit.get_root_flag() == False:
            prior_unit = get_prior_unit(unit, semantic_unit_list)
            if prior_unit != None and prior_unit.get_pos() != 'RP':
                unit.add_match_clue('*')
            else:
                unit.add_match_clue(unit.get_pos())
        else:
            unit.add_match_clue(unit.get_pos())
    return semantic_unit_list


if __name__ == '__main__':
    a = 0
    #sentence = "Now, it is to the right of the table. In the storm, the tree and the roof fell down and crashed through the Sam's roof of my house. "
    sentence = 'Sam\'s drawing was hung just above Tina\'s and it did look much better with another one above it.'
    sentence = "The sack of potatoes had been placed below the bag of flour, so it had to be moved first."
    sentence = "a house and a green wall with gate in the background ."
    sentence_list = sent_tokenize(sentence.strip())
    for sentence in sentence_list:
        print('************', sentence)
        parse = get_dependency_analysis_of_sentence(sentence)
        semantic_unit_list = get_semantic_unit_list(sentence, parse)
        #lemma_list = get_lemma_list(semantic_unit_list)
        #semantic_unit_list = construction_recognition(lemma_list, semantic_unit_list, all_prep_list, 'RP')
        #semantic_unit_list = remove_repeating_semantic_unit(semantic_unit_list)
        #print_semantic_unit_list(semantic_unit_list)

        father_children_dict = get_father_children_list(parse)
        root_list = get_all_root_list(parse)
        root_children_dict = get_root_children_dict(root_list, father_children_dict)
        print('?????????????????????????1')
        event_dict = get_event_dict(sentence, root_children_dict, semantic_unit_list)
        print('?????????????????????????2')
        for event, unit_list in event_dict.items():
            print('....', event.info_dict)
            #print(children)
            #print_semantic_unit_list(children)
            for unit in unit_list:
                print(unit.info_dict)
                # for child in unit.children:
                #     print('-------**-------')
                #     print(child.info_dict)
                #     print('----------------')




    # f_wsc_log = open('output/dep_test', 'w')
    # f = open('param/wsc_examples', 'r')
    # for line in f:
    #     if line.strip() != "":
    #         f_wsc_log.write(line+'\n')
    #         sentence_list = sent_tokenize(line.strip())
    #         for sentence in sentence_list:
    #             f_wsc_log.write(sentence+'\n')
    #             parse = get_dependency_analysis_of_sentence(sentence)
    #             semantic_unit_list = get_semantic_unit_list(parse)
    #             lemma_list = get_lemma_list(semantic_unit_list)
    #
    #             semantic_unit_list = construction_recognition(lemma_list, semantic_unit_list, all_prep_list, 'RP')
    #             semantic_unit_list = remove_repeating_semantic_unit(semantic_unit_list)
    #
    #             #print_semantic_unit_list(semantic_unit_list)
    #             father_children_dict = get_father_children_list(parse)
    #             root_list = get_all_root_list(parse)
    #             root_children_dict = get_root_children_dict(root_list, father_children_dict)
    #             print(root_children_dict)
    #             event_dict = get_event_dict(root_children_dict, semantic_unit_list)
    #             #event_dict = merge_adjacent_unit(event_dict)
    #             for event, children in event_dict.items():
    #                 print('....', event.info_dict)
    #                 print(children)
    #                 print_semantic_unit_list(children)
    #                 f_wsc_log.write('----------------------------'+'\n')
    #                 f_wsc_log.write(str(event.info_dict)+'\n')
    #                 f_wsc_log.write('----------------------------'+'\n')
    #                 write_semantic_unit_list_to_file(f_wsc_log, children)
    #                 f_wsc_log.write('\n\n\n\n')
    # f_wsc_log.close()
    # f.close()
