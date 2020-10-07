#!/usr/bin/env python3
##############################################################################
#       Function: Evaluation on SemEval 2017 Spatial Roles Labeling
##############################################################################
from fuzzy_match import *
import re
from lxml import etree
import nltk
#from nltk import sent_tokenize, word_tokenize

def generate_relation_list(relation_trajector_landmark_list):
    for item in relation_trajector_landmark_list:
        if len(item) == 0:
            return []

    relation_list = list(itertools.product(*relation_trajector_landmark_list))
    return relation_list

def insert_relation_into_node(node, relation_list, relation_index):
    for relation, trajector, landmark in relation_list:
        rel_node = etree.SubElement(node, 'RELATION')
        rel_node.set('id', 'SR'+str(relation_index) )
        rel_node.set('trajector_id', trajector)
        rel_node.set('landmark_id', landmark)
        rel_node.set('spatial_indicator_id', relation)
        rel_node.set('general_type', '')
        rel_node.set('specific_type', '')
        rel_node.set('RCC8_value', '')
        rel_node.set('FoR', '')
        relation_index = relation_index +1
    return node, relation_index




def get_indicator_trajactor_landmark(motion_file, number, relation_index, sentence, node):
    parse = get_dependency_analysis_of_sentence(sentence)
    semantic_unit_list = get_semantic_unit_list(sentence, parse)
    semantic_unit_list = add_buddy_to_unit(semantic_unit_list)
    word_list = get_word_list(semantic_unit_list)
    semantic_unit_list = construction_recognition(word_list, semantic_unit_list, all_prep_list, 'RP')
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
            relation_trajector_landmark_list = []
            number = number+1
            relation_index = relation_index +1
            print('-----------  locative construction -----------')
            print_locative_expr(locative_repr)

            relation = locative_repr.get_relation()
            spatial_indicator = etree.SubElement(node, 'SPATIALINDICATOR')
            spatial_indicator.set('id', 'S'+str(number))
            spatial_indicator.set('start', str(relation.get_start_index()))
            spatial_indicator.set('end', str(relation.get_end_index()))
            spatial_indicator.set('text', relation.get_word())

            figure_list = list(set(locative_repr.get_figure()))
            ground_list = list(set(locative_repr.get_ground()))
            prep_id_list = ['S'+str(number)]
            trajector_id_list = []
            landmark_id_list = []
            for figure in figure_list:
                if figure.get_start_index() != None:
                    print(figure.get_word(), figure.get_start_index(), figure.get_end_index())
                    trajector = etree.SubElement(node, 'TRAJECTOR')
                    trajector.set('id', 'T'+str(number))
                    trajector.set('start', str(figure.get_start_index()))
                    trajector.set('end', str(figure.get_end_index()))
                    trajector.set('text', figure.get_word())
                    trajector_id_list.append('T'+str(number))
                if len(figure_list) > 1:
                    number = number+1

            if len(ground_list) == 0:
                landmark = etree.SubElement(node, 'LANDMARK')
                landmark.set('id', 'L'+str(number))
                landmark.set('start', '-1')
                landmark.set('end', '-1')
                landmark_id_list.append('L'+str(number))
            else:
                for ground in ground_list:
                    print(ground.get_word(), ground.get_start_index(), ground.get_end_index())
                    if ground.get_start_index() != None:
                        landmark = etree.SubElement(node, 'LANDMARK')
                        landmark.set('id', 'L'+str(number))
                        landmark.set('start', str(ground.get_start_index()))
                        landmark.set('end', str(ground.get_end_index()))
                        landmark.set('text', str(ground.get_word()))
                        landmark_id_list.append('L'+str(number))
                    if len(ground_list) > 1:
                        number = number+1


            print(prep_id_list, trajector_id_list, landmark_id_list)
            relation_trajector_landmark_list.append(prep_id_list)
            relation_trajector_landmark_list.append(trajector_id_list)
            relation_trajector_landmark_list.append(landmark_id_list)
            relation_list = generate_relation_list(relation_trajector_landmark_list)
            print(relation_list)
            node, relation_index = insert_relation_into_node(node, relation_list, relation_index)
            if len(motion_repr_list) > 1:
                relation_index = relation_index +1
            print('-----------  locative construction -----------')

        for motion_repr in motion_repr_list:
            relation_trajector_landmark_list = []
            number = number+1
            relation_index = relation_index +1
            print('-----------   motion construction  -----------')
            print_motion_event(motion_repr)

            trajector_id_list = []
            landmark_id_list = []
            prep_id_list = []
            figure_list = motion_repr.get_figure()

            for relation, ground in motion_repr.get_ground().items():
                if ground.get_start_index() != None:
                    landmark = etree.SubElement(node, 'LANDMARK')
                    landmark.set('id', 'L'+str(number))
                    landmark.set('start', str(ground.get_start_index()))
                    landmark.set('end', str(ground.get_end_index()))
                    landmark.set('text', str(ground.get_word()))
                    landmark_id_list.append('L'+str(number))



                if relation.get_start_index() != None:
                    spatial_indicator = etree.SubElement(node, 'SPATIALINDICATOR')
                    spatial_indicator.set('id', 'S'+str(number))
                    spatial_indicator.set('start', str(relation.get_start_index()))
                    spatial_indicator.set('end', str(relation.get_end_index()))
                    spatial_indicator.set('text', relation.get_word())
                    prep_id_list.append('S'+str(number))

                if len(motion_repr.get_ground()) > 1:
                    number = number+1
                motion_file.write(sentence)
                motion_file.write('\n')



            for figure in figure_list:
                if figure.get_start_index() != None:
                    print(figure.get_word(), figure.get_start_index(), figure.get_end_index())
                    trajector = etree.SubElement(node, 'TRAJECTOR')
                    trajector.set('id', 'T'+str(number))
                    trajector.set('start', str(figure.get_start_index()))
                    trajector.set('end', str(figure.get_end_index()))
                    trajector.set('text', figure.get_word())
                    trajector_id_list.append('T'+str(number))
                if len(figure_list) > 1:
                    number = number+1
            print(prep_id_list, trajector_id_list, landmark_id_list)
            relation_trajector_landmark_list.append(prep_id_list)
            relation_trajector_landmark_list.append(trajector_id_list)
            relation_trajector_landmark_list.append(landmark_id_list)
            relation_list = generate_relation_list(relation_trajector_landmark_list)
            print(relation_list)
            node, relation_index = insert_relation_into_node(node, relation_list, relation_index)
            relation_index = relation_index +1

            print('-----------   motion construction  -----------')
    return node, number, relation_index


final_pattern_dict = get_final_pattern_dict(regular_pattern_dict)
#file_name = 'semeval2017/train.xml'
file_name = 'param/SpRL_test.xml'
motion_file = open('output/motion.xml','w')
xml_file = open(file_name, 'rb')
xml_str = xml_file.read()
xml_file.close()

root = etree.fromstring(xml_str)
scene_list = root.findall('SCENE')
number = 0
relation_index = 0
#
# sentence_number = 0
# word_number = 0
# for scene in scene_list:
#     sentence_list = scene.findall('SENTENCE')
#     number = number + len(sentence_list)
#     #print(type(sentence_list), len(sentence_list), sentence_list)
#     for sentence in sentence_list:
#
#         sentence_number = sentence_number + 1
#         text_str = sentence.find('TEXT').text
#         word_list = nltk.word_tokenize(str(text_str))
#         word_number = word_number + len(word_list)
# print('sentence_number', sentence_number)
# print('word_number', word_number)
# print('average length', str(word_number/sentence_number))



for scene in scene_list:
    sentence_list = scene.findall('SENTENCE')
    number = number + len(sentence_list)
    #print(type(sentence_list), len(sentence_list), sentence_list)
    for sentence in sentence_list:

        text_str = sentence.find('TEXT').text
        id = sentence.get('id')
        start = sentence.get('start')
        end = sentence.get('end')
        sentence.clear()
        sentence.set('id', id)
        sentence.set('start', start)
        sentence.set('end', end)
        id = sentence.get('id')

        text = etree.SubElement(sentence, 'TEXT')
        text_str = text_str.replace('?', ' ')
        text.text = text_str
        sentence,number, relation_index = get_indicator_trajactor_landmark(motion_file, number, relation_index, text_str, sentence)
        number = number+1
        relation_index = relation_index +1


tree = etree.ElementTree(root)
if file_name == 'param/SpRL_test.xml':
    tree.write('output/test-output.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
motion_file.close()
f_statistic = open('output/statistic', 'w')
f_statistic.write(str(statistic_dict))
f_statistic.close()
print(statistic_dict)
