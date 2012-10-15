#!/usr/bin/env python
# encoding: utf-8

from pprint import pprint as pp
from pyparsing import *

# Define the grammar for a bundle parser in a mako HEAD section
# ====================================================================
bundleStart, bundleEnd = makeXMLTags("bundle")
scriptStart, scriptEnd = makeXMLTags("script")
linkStart, linkEnd = makeXMLTags("link")
num_sign = Literal("#")
comment = num_sign + num_sign + Optional( restOfLine )

# XML tag bundle parser
# is this any better than using lxml? Such small specific bits, I'd have
# to believe more specific is better (although lxml is C so it could be 
# generally faster even though the code is more heavyweight)
bundle = Forward()
link = linkStart + SkipTo(linkEnd) + linkEnd.suppress() | linkStart
script = scriptStart + SkipTo(scriptEnd) + scriptEnd.suppress()
bundle_value = Group(bundle | link | script)
bundle_children = delimitedList(ZeroOrMore(bundle_value)).setResultsName("children")
bundle << bundleStart + bundle_children + bundleEnd.suppress()
bundle.ignore(comment)
bundle.ignore(htmlComment)


# HTML / tag block to be used in Mako using custom parser
# This idea of this code is to allow the script and css lines to be written
# mostly 'normally' but then create container 'bundle' tags that invoke
# the webassets package
# The mako block will have a filter called 'asset_bundler' that will pass the
# entire block through the parser before outputting URL's. (Verify that
# this is the) behavior we'll get with a block-level filter.
# <%block name="javascript" filter="asset_bundler">
defText = '''
<bundle name="empty_js" filters="rjsmin" output="js/test.js"></bundle>
<bundle name="all_js" filters="rjsmin" output="js/smarterer_min.js">
	<script src="js/test1.js"></script>
    <script src="js/test2.js"></script>
	<bundle name="all_coffee" filters="coffescript" output="js/coffee.js">
		<script type="text/coffeescript" src="coffee/test.coffee"></script>
	</bundle>
</bundle>
<bundle name="all_css" filter="css_min" output="css/smarterer_css.css">
    <link type="text/css" href="/css/960.css" media="screen" rel="stylesheet" />
    <link type="text/css" href="/css/961.css" media="screen" rel="stylesheet" />
    <link type="text/css" href="/css/jquery-ui.css" media="screen" rel="stylesheet" />
    <link type="text/css" href="/css/reset.css" media="screen" rel="stylesheet" />
    <link type="text/css" href="/css/mobile.css" media="screen" rel="stylesheet" />
    <link type="text/css" href="/css/styles.css" media="screen" rel="stylesheet" />
    <link type="text/css" href="/css/skillsets.css" media="screen" rel="stylesheet" />
</bundle>
'''

# Alternatively it could just be written as python code, bypassing the bundler
# parser altogether.
# # mako embedded python syntax
# ${bundle(name="all_css" filter="css_min" output="css/smarterer.css", input=(
#     {href:"/css/960.css"},
#     {href:"/css/961.css", media:"handheld"},
#     {href:"/css/jquery-ui.css"},
#     )
# )}
# % for url in env['all_css']:
# ${url}
# % endfor


# Tests and experiments with bundler behavior.

bundle_list = [tokens for tokens, start, end in bundle.scanString(defText)]

from webassets.env import Environment
from webassets import Bundle

env = Environment('/usr/share/smarterer/quiz_site/public/', '')

def print_tokens(tokens, idt='', bundle=None):
    for token in tokens:
        if token.tag == 'bundle':
            if bundle is None:
                bundle = Bundle(filters=token.filters, output=token.output)
                env.register(token.name, bundle)
            print idt+token.name, token.filters, token.output
            if isinstance(token, ParseResults) and len(token.children) > 0:
                print_tokens(token.children, idt+'\t', bundle)
        elif token.tag == 'script':
            bundle.contents = bundle.contents + (token.src,)
            print idt, token.src, token.type
        elif token.tag == 'link':
            bundle.contents = bundle.contents + (token.href,)
            # bundle.contents.append(token.href)
            print idt, token.href, token.media

print_tokens(bundle_list)
