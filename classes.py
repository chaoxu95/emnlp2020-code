#!/usr/bin/env python3
##############################################################################
#       Function: semantic_unit class, and motion_event class
##############################################################################
from collections import defaultdict
class semantic_unit:
    def __init__(self,info_dict={}, children = []):
        self.info_dict = info_dict
        self.children = children

    def get_word(self):
        if 'word' in self.info_dict:
            return self.info_dict['word']
        else:
            return None
    def get_lemma(self):
        if 'lemma' in self.info_dict:
            return self.info_dict['lemma']
        else:
            return None

    def get_position(self):
        if 'position' in self.info_dict:
            return self.info_dict['position']
        else:
            return None

    def get_start_position(self):
        if 'start_position' in self.info_dict:
            return self.info_dict['start_position']
        else:
            return None
    def get_end_position(self):
        if 'end_position' in self.info_dict:
            return self.info_dict['end_position']
        else:
            return None

    def get_pos(self):
        if 'pos' in self.info_dict:
            return self.info_dict['pos']
        else:
            return None

    def get_deps(self):
        if 'deps' in self.info_dict:
            return self.info_dict['deps']
        else:
            return None

    def get_added_subj_flag(self):
        if 'added_subj_flag' in self.info_dict:
            return self.info_dict['added_subj_flag']
        else:
            return None

    def get_semantic_role(self):
        if 'semantic_role' in self.info_dict:
            return self.info_dict['semantic_role']
        else:
            return None

    def get_root_flag(self):
        if 'root_flag' in self.info_dict:
            return self.info_dict['root_flag']
        else:
            return None

    def get_is_subclass_of(self):
        if 'is_subclass_of' in self.info_dict:
            return self.info_dict['is_subclass_of']
        else:
            return None

    def get_refer_to(self):
        if 'refer_to' in self.info_dict:
            return self.info_dict['refer_to']
        else:
            return None

    def get_ner(self):
        if 'ner' in self.info_dict:
            return self.info_dict['ner']
        else:
            return None

    def get_match_clue(self):
        if 'match_clue' in self.info_dict:
            return self.info_dict['match_clue']
        else:
            return None

    def get_merge_clue(self):
        if 'merge_clue' in self.info_dict:
            return self.info_dict['merge_clue']
        else:
            return None

    def get_buddy(self):
        if 'buddy' in self.info_dict:
            return self.info_dict['buddy']
        else:
            return None
    def get_start_index(self):
        if 'start_index' in self.info_dict:
            return self.info_dict['start_index']
        else:
            return None
    def get_end_index(self):
        if 'end_index' in self.info_dict:
            return self.info_dict['end_index']
        else:
            return None

    def get_children_position_list(self):
        if 'children_position_list' in self.info_dict:
            return self.info_dict['children_position_list']
        else:
            return None


    def add_word(self, word):
        self.info_dict['word'] = word

    def add_lemma(self, lemma):
        self.info_dict['lemma'] = lemma

    def add_position(self, position):
        self.info_dict['position'] = position

    def add_start_position(self, start_position):
        self.info_dict['start_position'] = start_position

    def add_end_position(self, end_position):
        self.info_dict['end_position'] = end_position

    def add_pos(self, pos):
        self.info_dict['pos'] = pos

    def add_deps(self, deps):
        self.info_dict['deps'] = deps

    def add_added_subj_flag(self, added_subj_flag):
        self.info_dict['added_subj_flag'] = added_subj_flag

    def add_semantic_role(self, semantic_role):
        self.info_dict['semantic_role'] = semantic_role

    def add_root_flag(self, root_flag):
        self.info_dict['root_flag'] = root_flag

    def add_is_subclass_of(self, is_subclass_of):
        self.info_dict['is_subclass_of'] = is_subclass_of

    def add_refer_to(self, refer_to):
        self.info_dict['refer_to'] = refer_to

    def add_ner(self, ner):
        self.info_dict['ner'] = ner

    def add_match_clue(self, match_clue):
        self.info_dict['match_clue'] = match_clue

    def add_merge_clue(self, merge_clue):
        self.info_dict['merge_clue'] = merge_clue

    def add_buddy(self, buddy):
        self.info_dict['buddy'] = buddy

    def add_start_index(self, start_index):
        self.info_dict['start_index'] = start_index

    def add_end_index(self, end_index):
        self.info_dict['end_index'] = end_index

    def add_children(self, children):
        self.children.append(children)

    def add_children_list(self, children_list):
        self.children = children_list

    def add_children_position_list(self, children_position_list):
        self.info_dict['children_position_list'] = children_position_list








class motion_event:
    def __init__(self,info_dict={}):
        self.info_dict = info_dict

    def get_action(self):
        if 'action' in self.info_dict:
            return self.info_dict['action']
        else:
            return None

    def get_relation(self):
        if 'relation' in self.info_dict:
            return self.info_dict['relation']
        else:
            return None

    def get_figure(self):
        if 'figure' in self.info_dict:
            return self.info_dict['figure']
        else:
            return None

    def get_ground(self):
        if 'ground' in self.info_dict:
            return self.info_dict['ground']
        else:
            return None

    def get_agent(self):
        if 'agent' in self.info_dict:
            return self.info_dict['agent']
        else:
            return None

    def get_recipient(self):
        if 'recipient' in self.info_dict:
            return self.info_dict['recipient']
        else:
            return None

    def get_source(self):
        if 'source' in self.info_dict:
            return self.info_dict['source']
        else:
            return None

    def get_path(self):
        if 'path' in self.info_dict:
            return self.info_dict['path']
        else:
            return None

    def get_goal(self):
        if 'goal' in self.info_dict:
            return self.info_dict['goal']
        else:
            return None

    def get_via(self):
        if 'via' in self.info_dict:
            return self.info_dict['via']
        else:
            return None

    def get_toward(self):
        if 'toward' in self.info_dict:
            return self.info_dict['toward']
        else:
            return None

    def get_away_from(self):
        if 'away from' in self.info_dict:
            return self.info_dict['away from']
        else:
            return None

    def get_manner(self):
        if 'manner' in self.info_dict:
            return self.info_dict['manner']
        else:
            return None

    def get_direction(self):
        if 'direction' in self.info_dict:
            return self.info_dict['direction']
        else:
            return None

    def get_speed(self):
        if 'speed' in self.info_dict:
            return self.info_dict['speed']
        else:
            return None

    def add_action(self, action):
        self.info_dict['action'] = action

    def add_relation(self, relation):
        self.info_dict['relation'] = relation

    def add_figure(self, figure):
        self.info_dict['figure'] = figure

    def add_ground(self, ground):
        self.info_dict['ground'] = ground

    def add_agent(self, agent):
        self.info_dict['agent'] = agent

    def add_recipient(self, recipient):
        self.info_dict['recipient'] = recipient

    def add_source(self, source):
        self.info_dict['source'] = source

    def add_path(self, path):
        self.info_dict['path'] = path

    def add_goal(self, goal):
        self.info_dict['goal'] = goal

    def add_via(self, via):
        self.info_dict['via'] = via

    def add_toward(self, toward):
        self.info_dict['toward'] = toward

    def add_away_from(self, away_from):
        self.info_dict['away from'] = away_from

    def add_manner(self, manner):
        self.info_dict['manner'] = manner

    def add_direction(self, direction):
        self.info_dict['direction'] = direction

    def add_speed(self, speed):
        self.info_dict['speed'] = speed

class locative:
    def __init__(self,info_dict={}):
        self.info_dict = info_dict

    def get_figure(self):
        if 'figure' in self.info_dict:
            return self.info_dict['figure']
        else:
            return None

    def get_ground(self):
        if 'ground' in self.info_dict:
            return self.info_dict['ground']
        else:
            return None

    def get_relation(self):
        if 'relation' in self.info_dict:
            return self.info_dict['relation']
        else:
            return None

    def add_figure(self, figure):
        self.info_dict['figure'] = figure

    def add_ground(self, ground):
        self.info_dict['ground'] = ground

    def add_relation(self, relation):
        self.info_dict['relation'] = relation
