#!/usr/bin/env python3
##############################################################################
#       Function: load the parameters to the program from files
##############################################################################
import yaml

def load_verb_form_dict():
    f = open('param/verb_form', 'r')
    verb_form_str = f.read()
    f.close()
    #print(prep_str)
    verb_form_dict = yaml.load(verb_form_str)
    return verb_form_dict

def load_path_verb_dict():
    f = open('param/path_verb', 'r')
    verb_form_str = f.read()
    f.close()
    #print(prep_str)
    verb_form_dict = yaml.load(verb_form_str)
    return verb_form_dict

def load_all_prep_list():
    f = open('param/all_preps', 'r')
    prep_str = f.read()
    f.close()
    #print(prep_str)
    prep_list = yaml.load(prep_str)
    return prep_list
def load_motion_prep_dict():
    f = open('param/motion_prep', 'r')
    prep_str = f.read()
    f.close()
    #print(prep_str)
    prep_dict = yaml.load(prep_str)
    return prep_dict

def load_motion_verb_list():
    f = open('param/spatial_verb', 'r')
    text = f.read()
    f.close()
    all_param_dict = yaml.load(text)
    return all_param_dict['motion_verb']

def load_caused_motion_verb_list():
    f = open('param/spatial_verb', 'r')
    text = f.read()
    f.close()
    all_param_dict = yaml.load(text)
    return all_param_dict['caused_motion_verb']

def load_stative_verb_list():
    f = open('param/spatial_verb', 'r')
    text = f.read()
    f.close()
    all_param_dict = yaml.load(text)
    return all_param_dict['stative_verb']

if __name__ == '__main__':

    print(load_prep_list())
    load_verb_form_dict()
