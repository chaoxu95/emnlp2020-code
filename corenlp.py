#!/usr/bin/env python3
##############################################################################
#       Function: stanford parser and tagger
##############################################################################

from nltk.parse.corenlp import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
from stanfordcorenlp import StanfordCoreNLP
import json
from conjugate import *
from load_file import *



verb_tag_list = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

def get_dependency_analysis_of_sentence(sentence):
    #dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    dep_parser = CoreNLPDependencyParser(url='http://0.0.0.0:9000')
    parse = DependencyGraph()
    try:
        parse, = dep_parser.raw_parse(sentence)
    except:
        print('Some error happend when runing the dependency parser.....')
    #print('parse......',parse)
    # print('parser.to_conll......', parse.to_conll(4))
    # print('parse.tree......', parse.tree())
    # for governor, dep, dependent in parse.triples():
    #     print(governor, dep, dependent)
    return parse

def get_entity_of_sentence(sentence):
    ner_tagger = CoreNLPParser(url='http://0.0.0.0:9000', tagtype='ner')
    entity_list = ner_tagger.tag(sentence.split())
    return entity_list

def get_parse_dict_from_parse(parse):
    parse_dict = {}
    for i, node in sorted(parse.nodes.items()):
        if node['tag'] != 'TOP':
            parse_dict[i] = node
    return parse_dict

def get_annotation_of_sentence(sentence):
    nlp = StanfordCoreNLP('http://0.0.0.0', port=9000, timeout=10000)

    # Define proporties needed to get lemma
    props = {'annotators': 'lemma',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'}

    parsed_str = nlp.annotate(sentence, properties=props)
    parsed_dict = json.loads(parsed_str)
    return parsed_dict

def get_replace_dict(sentence, path_verb_dict, verb_form_dict):
    parsed_dict = get_annotation_of_sentence(sentence)
    replace_dict = {}
    for sentence_item in parsed_dict['sentences']:
        for token in sentence_item['tokens']:
            if token['lemma'] in path_verb_dict:
                pos = token['pos']
                if pos in verb_tag_list:
                    replace_phrase = path_verb_dict[token['lemma']]
                    temp_list = replace_phrase.split()
                    temp_list[0] = get_morphological_transformation_of_verb(temp_list[0], pos,verb_form_dict)
                    replace_phrase = ' '.join(temp_list)

                    replace_dict[token['word']] = replace_phrase
    return replace_dict

def preprocessing_of_sentence(sentence, path_verb_dict, verb_form_dict):
    replace_dict = get_replace_dict(sentence, path_verb_dict, verb_form_dict)
    print(replace_dict)
    for word, replace_phrase in replace_dict.items():
        sentence = sentence.replace(word, replace_phrase)
    return sentence


if __name__ == '__main__':
    a = 0
    sentence = 'when he reached the top of the ladder'
    # parse = get_dependency_analysis_of_sentence(sentence)
    # print(get_entity_of_sentence(sentence))
    # print(parse.nodes[0])
    # print(parse.root)
    # print(get_element_dict_from_parse(parse))
    # print(get_root_from_parse(parse))
    #sentence = ""
    path_verb_dict = load_path_verb_dict()
    verb_form_dict = load_verb_form_dict()
    sentence = preprocessing_of_sentence(sentence, path_verb_dict,verb_form_dict )
    print(sentence)
