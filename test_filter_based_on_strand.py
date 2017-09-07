import operator
from unittest import TestCase
from filter_based_on_strand import StrandFilter, LongReadIntersect, BndFilter

class TestStrandFilter(TestCase):
    def test_init(self):
        obj = StrandFilter([(1, 1), (1, 1)])
        self.assertEqual(obj.allowable_strands, set([(1, 1)]))

    def test_call(self):
        obj1 = StrandFilter([('+', '-')])
        self.assertTrue(obj1(None, None, '+', '-'))
        self.assertFalse(obj1(None, None, '-', '+'))
        self.assertFalse(obj1(None, None, None, None))

    def test_multiple(self):
        obj1 = StrandFilter([('+', '-'), ('+', '+')])
        self.assertTrue(obj1(None, None, '+', '-'))
        self.assertTrue(obj1(None, None, '+', '+'))
        self.assertFalse(obj1(None, None, '-', '+'))

class TestBndFilter(TestCase):
    def test_init(self):
        obj = BndFilter([])
        self.assertEqual(obj.allowable_strands, set())

    def test_call(self):
        obj1 = BndFilter([])
        self.assertTrue(obj1('+', '+', '+', '-'))
        self.assertTrue(obj1('-', '-', '+', '-'))
        self.assertFalse(obj1('-', '+', '+', '-'))
        self.assertFalse(obj1('+', '-', '+', '-'))

class TestLongReadIntersect(TestCase):
    def test_init(self):
        obj = LongReadIntersect()
        self.assertTrue(obj.filters['DEL'])
        self.assertRaises(KeyError, operator.getitem, obj.filters, 'LOL')

    def test_call(self):
        obj = LongReadIntersect()
        self.assertRaises(ValueError, obj, 'LOL', '-', '-', '-', '+')
        self.assertTrue(obj('DEL', '-', '-', '+', '-'))
        self.assertTrue(obj('INV', '-', '-', '-', '-'))
        self.assertTrue(obj('BND', '+', '-', '-', '-'))
        self.assertFalse(obj('DEL', '-', '-', '+', '+'))

