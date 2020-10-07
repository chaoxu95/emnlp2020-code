#!/usr/bin/env python3
##############################################################################
#       Function: get the morphological transformation of verbs
##############################################################################


def generate_dict_from_text():
    verb_form_dict = {}
    f = open('param/verb.txt', 'r')
    for line in f:
        if line.strip() != "":
            word_list = line.split()
            if len(word_list) > 0:
                verb_form_dict[word_list[0]] = word_list
    f.close()
    return verb_form_dict

def get_morphological_transformation_of_verb(word, tag, verb_form_dict):
    if word in verb_form_dict:
        form_list = verb_form_dict[word]
        if len(form_list) == 5:
            try:
                if tag == 'VBZ':
                    word = form_list[1]
                elif tag == 'VBG':
                    word = form_list[2]
                elif tag == 'VBD':
                    word = form_list[3]
                elif tag == 'VBN':
                    word = form_list[4]
            except:
                print('something wrong happened when getting the morphological transformation of ' +word)
    else:
        print(word, ' is not in the verb.txt file')
    return word

if __name__ == '__main__':

    verb_form_dict = generate_dict_from_text()
    f_write = open('output/verb_dict', 'w')
    for x, y in verb_form_dict.items():
        f_write.write('\''+x+'\':'+str(y)+',\n')
    f_write.close()
    tag_list = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    for tag in tag_list:
        print(tag, get_morphological_transformation_of_verb('test', tag, verb_form_dict))
