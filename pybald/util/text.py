import re
import unicodedata

try:
    type(unicode)
except NameError:
    def unicode(txt, errors=None):
        return txt.decode('utf-8')

# first pass, anything before a CAPLower gets separated. i.e. CAP_Lower
#  123Lower -> 123_Lower
first_pass = re.compile(r'(.)([A-Z][a-z]+)')
# second pass, anything lowerCAP gets split then lowercased lower_cap
second_pass = re.compile(r'([a-z0-9])([A-Z])')


# technically this is PascalCase (or StudlyCaps)
def camel_to_underscore(text):
    '''Convert CamelCase text into underscore_separated text.'''
    return second_pass.sub(r'\1_\2', first_pass.sub(r'\1_\2', text)).lower()


def underscore_to_camel(text):
    '''Convert underscore_separated text into CamelCase text.'''
    return ''.join([token.capitalize() for token in text.split(r'_')])


ordinal_suffixes = {1: 'st', 2: 'nd', 3: 'rd'}


def ordinal_suffix(num):
    '''Returns the ordinal suffix of an interger (1st, 2nd, 3rd).'''
    if 10 <= abs(num) % 100 <= 20:
        return 'th'
    return ordinal_suffixes.get(abs(num) % 10, 'th')


plural_patterns = [(re.compile(pattern), re.compile(search), replace
                                        ) for pattern, search, replace in (
                         ('[^aeiouz]z$', '$', 's'),
                         ('[aeiou]z$', '$', 'zes'),
                         ('[sx]$', '$', 'es'),
                         ('[^aeioudgkprt]h$', '$', 'es'),
                         ('[^aeiou]y$', 'y$', 'ies'),
                         ('$', '$', 's'))]


def _build_plural_rule(input_pattern):
    pattern, search, replace = input_pattern
    return lambda word: pattern.search(word) and search.sub(replace, word)


plural_rules = list(map(_build_plural_rule, plural_patterns))


def pluralize(text):
    '''
    Returns a pluralized from of the input text following simple naive
    english language pluralization rules.

    Smart enough to turn fox into foxes and quiz into quizzes. Does not catch
    all pluralization rules, however.
    '''
    for rule in plural_rules:
        result = rule(text)
        if result:
            return result


def strip_accents(text):
    '''
    Strip diacriticals from characters. This will change the meaning of words
    but for places where unicode can't be used (or ASCII only) francais looks
    better than fran-ais or fran?ais.
    '''
    if isinstance(text, bytes):
        return unicode(text, errors='ignore')
    return ''.join((c for c in unicodedata.normalize('NFD', text) if
                                              unicodedata.category(c) != 'Mn'))

