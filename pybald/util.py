
import re
# first pass, anything before a CAPLower gets separated. i.e. CAP_Lower
#  123Lower -> 123_Lower
first_pass = re.compile(r'(.)([A-Z][a-z]+)')
# second pass, anything lowerCAP gets split then lowercased lower_cap
second_pass = re.compile(r'([a-z0-9])([A-Z])')

def camel_to_underscore(text):
    '''Convert CamelCase text into underscore_separated text.'''
    return second_pass.sub( r'\1_\2', first_pass.sub(r'\1_\2', text)).lower()

def underscore_to_camel(text):
    '''Convert underscore_separated text into CamelCase text.'''
    return ''.join([token.capitalize() for token in text.split(r'_') ])

def buildRule((pattern, search, replace)):
    return lambda word: pattern.search(word) and search.sub(replace, word)

class Plural(object):
    '''Simple Pluralizer object. Stores naive rules for word pluralization.'''


    def __init__(self):
        '''Init pluralizer'''
        #Build regex patterns to do a quick and dirty pluralization.
        self.patterns = [ (re.compile(pattern), re.compile(search), replace
                                        ) for pattern, search, replace in (
                         ('[^aeiouz]z$', '$', 's'),
                         ('[aeiou]z$', '$', 'zes'),
                         ('[sx]$', '$', 'es'),
                         ('[^aeioudgkprt]h$', '$', 'es'),
                         ('[^aeiou]y$', 'y$', 'ies'),
                         ('$', '$', 's')) ]
        self.rules = map(buildRule, self.patterns)

    def __call__(self, text):
        '''Pluralize a noun using some simple rules.'''
        for rule in self.rules:
            result = rule(text)
            if result: return result

pluralize = Plural()