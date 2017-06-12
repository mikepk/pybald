'''The constants helper module is to allow for creating 'safer' ini files for
values that will be injected into templates. The basic rationale is that there
are often values that you want non-technical people to control (phone numbers,
marketing claims, addresses) and similar values. Using constants allows these
individuals to use friendlier ini format but still have the values available
for page templates.'''
try:
    from ConfigParser import ConfigParser as configparser
except ImportError:
    from configparser import ConfigParser as configparser
from collections import namedtuple

# generate constants for templates
# this is a little squirrley looking, but all it does is use the config
# parser to read an INI file and then generates a two level set of named
# tuples to surface the data. Inside the template the section/data of the
# constants ini is dereferenced using constants.SECTION.KEY


def read(filename='constants.ini', constants_file=None):
    '''Read a constants ini file and return the constants helper object.

    When added to the page_options config, these constants can be used inside
    the templates where the section/data of the constants ini is dereferenced
    using constants.SECTION.KEY.
    '''
    config = configparser()
    if constants_file:
        config.readfp(constants_file)
    else:
        config.read(filename)
    constants = namedtuple("Constant", config.sections())._make([
        namedtuple('Field', dict(config.items(section)).keys()
            )._make(dict(config.items(section)).values())
                for section in config.sections() ])
    return constants
