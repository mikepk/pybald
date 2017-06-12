#!/usr/bin/env python
# encoding: utf-8
import unittest
from mako.template import Template
from pybald.util import text
import pybald
from pybald import context


class TestTemplate(unittest.TestCase):
    def setUp(self):
        pybald.configure(config_file="tests/sample_project/project.py")
        # from tests.sample_project.sample import app

    def tearDown(self):
        context._reset()

    def test_pluralize(self):
        '''Pluralize some words'''
        test_data = [('fox', 'foxes'),
                     ('quiz', 'quizzes'),
                     ('beach', 'beaches'),
                     ('test', 'tests'),
                     ('party', 'parties')]
        for singular, expected_plural in test_data:
            self.assertEqual(text.pluralize(singular), expected_plural)

    def test_ordinal_suffixes(self):
        '''Get the ordinal suffix for some numbers'''
        test_data = [(1, 'st'),
                     (2, 'nd'),
                     (17, 'th'),
                     (101, 'st'),
                     (33, 'rd'),
                     (-52, 'nd')]
        for number, expected_suffix in test_data:
            self.assertEqual(text.ordinal_suffix(number), expected_suffix)

    def test_camel_to_underscore(self):
        '''Convert camelcase to undesrscore separated'''
        test_data = [('TestOne', 'test_one'),
                     ('test123BigBang', 'test123_big_bang'),
                     ('HTMLTestOne', 'html_test_one'),
                     ('Justacap', 'justacap'),
                     ('PybaldIsTHEGreatest', 'pybald_is_the_greatest')]
        for camel, expected_underscore in test_data:
            self.assertEqual(text.camel_to_underscore(camel), expected_underscore)

    def test_underscore_to_camel(self):
        '''Convert underscore separated to camel case'''
        test_data = [('TestOne', 'test_one'),
                     ('Test123BigBang', 'test123_big_bang'),
                     ('HtmlTestOne', 'html_test_one'),
                     ('Justacap', 'justacap'),
                     ('PybaldIsTheGreatest', 'pybald_is_the_greatest')]
        for expected_camel, underscore in test_data:
            self.assertEqual(text.underscore_to_camel(underscore), expected_camel)

    def test_accent_stripping(self):
        '''Strip diacriticals and accents from words'''
        test_data = [(u'¡hosta cabrón!', u'¡hosta cabron!'),
                     (u'mötley crüe', u'motley crue'),
                     (b'bytes', u'bytes'),
                     (u'français', u'francais'),
                     (u'resumé', u'resume')]

        for accented, unaccented in test_data:
            self.assertEqual(text.strip_accents(accented), unaccented)
