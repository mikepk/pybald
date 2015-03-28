from ConfigParser import ConfigParser as configparser
from collections import namedtuple

# generate constants for templates
# this is a little squirrley looking, but all it does is use the config
# parser to read an INI file and then generates a two level set of named
# tuples to surface the data. Inside the template the section/data of the
# constants ini is dereferenced using constants.SECTION.KEY

def read(filename='constants.ini'):
    config = configparser()
    config.read(filename)
    constants = namedtuple("Constant", config.sections())._make([
        namedtuple('Field', dict(config.items(section)).keys()
            )._make(dict(config.items(section)).values())
                for section in config.sections() ])
    return constants
