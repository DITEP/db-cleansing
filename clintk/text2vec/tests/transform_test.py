"""
script to test functions in clintk.text2vec.fold
"""
import clintk.text2vec.tools
from nose.tools import assert_list_equal


class TestTransform(object):
    def setUp(self):
        pass

    def test_normalizer(self):
        s = 'alfred le chat de mon voisin était rose avec des tâches'

        res = clintk.text2vec.tools.text_normalize(s, ['chat'])

        expected = ['alfred', 'voisin', 'rose', 'tâches']

        assert_list_equal(expected, res)
