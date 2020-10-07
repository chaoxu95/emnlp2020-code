#!/usr/bin/env python3
##############################################################################
#       Function: get motion and caused motion verbs in VerbNet
##############################################################################
import os
from xml.dom import minidom

verbnet_caused_motion_verb_list = ['put-9.1', 'put_spatial-9.2', 'funnel-9.3', 'put_direction-9.4', 'pour-9.5', 'coil-9.6', 'spray-9.7', 'fill-9.8', 'butter-9.9', 'pocket-9.10', 'remove-10.1', 'banish-10.2', 'clear-10.3', 'wipe_manner-10.4.1', 'wipe_inst-10.4.2', 'steal-10.5', 'cheat-10.6', 'pit-10.7', 'debone-10.8', 'mine-10.9', 'fire-10.10', 'resign-10.11', 'send-11.1', 'slide-11.2', 'bring-11.3', 'carry-11.4', 'drive-11.5', 'push-12', 'concealment-16', 'throw-17.1', 'pelt-17.2', 'hit-18.1', 'swat-18.2', 'spank-18.3', 'bump-18.4', 'poke-19', 'escape-51.1', 'leave-51.2', 'roll-51.3.1',  'rush-53.2']
verbnet_motion_verb_list = ['escape-51.1', 'leave-51.2',  'roll-51.3.1', 'run-51.3.2', 'vehicle-51.4.1', 'nonvehicle-51.4.2', 'waltz-51.5', 'chase-51.6', 'accompany-51.7', 'reach-51.8', 'linger-53.1', 'rush-53.2',]
verbnet_stative_verb_list = ['assuming_position-50', 'spatial_configuration-47.6']

def get_word_list_from_verbnet(file_name):
    #f_css = open('category_syntax_semantic', 'w')
    lex_name_list = []
    xmldoc = minidom.parse(file_name)
    lexunit_list = xmldoc.getElementsByTagName('MEMBER')
    for lexunit in lexunit_list:
        lex_name = lexunit.attributes['name'].value
        #lex_name = lex_name.encode('ascii', 'ignore')
        lex_name_list.append(lex_name)

    return lex_name_list


motion_verb_list = []
motion_verb_dict = {}
g = os.walk('param/vn')
for path,dir_list,file_list in g:
    for file_name in file_list:
        word_list = []
        full_file_name = os.path.join(path, file_name)
        if '.xml' in full_file_name and '51' in full_file_name:
            word_list = get_word_list_from_verbnet(full_file_name)
            motion_verb_list = motion_verb_list + word_list
            motion_verb_dict[file_name] = word_list

print(len(motion_verb_list), motion_verb_list)
print(motion_verb_dict)

word_list = ['zoom', 'crash', 'throw', 'get', 'roll', 'hang', 'pour', 'put', 'take', 'lie', 'run', 'fall', 'walk', 'move', 'carry', 'come', 'tuck', 'place', 'stick', 'pull', 'pass', 'lift']
for word in word_list:
    if word in motion_verb_list:
        print(word)

# f = open('param/verbnet', 'r')
# text = f.read()
# text = text.replace('\n', ' ')
# print(text)
# causative_verb_motion_list = []
# causative_verb_motion_list = text.split(' ')
# print(causative_verb_motion_list)


caused_motion_verb_list = []
caused_motion_verb_dict = {}
g = os.walk('param/vn')
file_list = []
for (dirpath, dirnames, filenames) in g:
    file_list.extend(filenames)
    break
print(file_list)
print("-----------------caused motion verb-----------------")
for file_name in verbnet_caused_motion_verb_list:
    if file_name + '.xml' in file_list:
        full_file_name = 'param/vn/'+ file_name +'.xml'
        #print(full_file_name)
        word_list = get_word_list_from_verbnet(full_file_name)
        caused_motion_verb_list = caused_motion_verb_list + word_list
        caused_motion_verb_dict[file_name] = word_list
    else:
        print(file_name)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
caused_motion_verb_list = sorted(list(set(caused_motion_verb_list)))
print(len(caused_motion_verb_list), caused_motion_verb_list)
print(caused_motion_verb_dict)
print("-----------------    motion verb  -----------------")
motion_verb_list = []
motion_verb_dict = {}
for file_name in verbnet_motion_verb_list:
    if file_name + '.xml' in file_list:
        full_file_name = 'param/vn/'+ file_name +'.xml'
        #print(full_file_name)
        word_list = get_word_list_from_verbnet(full_file_name)
        motion_verb_list = motion_verb_list + word_list
        motion_verb_dict[file_name] = word_list
    else:
        print(file_name)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
motion_verb_list = sorted(list(set(motion_verb_list)))
print(len(motion_verb_list), motion_verb_list)
print(motion_verb_dict)
print("-----------------  stative verb  -----------------")
stative_verb_list = []
stative_verb_dict = {}
for file_name in verbnet_stative_verb_list:
    if file_name + '.xml' in file_list:
        full_file_name = 'param/vn/'+ file_name +'.xml'
        #print(full_file_name)
        word_list = get_word_list_from_verbnet(full_file_name)
        stative_verb_list = stative_verb_list + word_list
        stative_verb_dict[file_name] = word_list
    else:
        print(file_name)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
stative_verb_list = sorted(list(set(stative_verb_list)))
print(len(stative_verb_list), stative_verb_list)
print(stative_verb_dict)
