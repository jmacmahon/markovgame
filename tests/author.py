from __future__ import absolute_import

from pytest import mark
from itertools import product

from markovgame.markov import Author

def test_init_no_arguments():
    a = Author()
    assert a.words_map is None
    assert a.name is None

empty_words_map = {}
words_maps = [
    {'followed': [1, {'by': 1}]},
    {'quietly': [2, {'smoking': 1, 'into': 1}]},
    {'public': [8, {'support': 1}, {'domain': 7}]},
    {'livery,': [1, {'with': 1}], 'beginning': [4, {'to': 3, 'of': 1}]}
]

names = ['Lewis Caroll', 'Noam Chomsky', 'John Searle']

@mark.parametrize('name', names)
def test_init_name(name):
    a = Author(name=name)
    assert a.name == name

@mark.parametrize('words_map', words_maps)
def test_init_words_map(words_map):
    a = Author(words_map=words_map)
    assert a.words_map == words_map

@mark.parametrize('name,words_map', product(names, words_maps))
def test_init_order(name, words_map):
    a = Author(name, words_map)
    assert a.name == name
    assert a.words_map == words_map
