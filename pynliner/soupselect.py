"""
# Included with pynliner since it isn't on PyPI #

soupselect.py

CSS selector support for BeautifulSoup.

soup = BeautifulSoup('<html>...')
select(soup, 'div')
    - returns a list of div elements

select(soup, 'div#main ul a')
    - returns a list of links inside a ul inside div#main

patched to support multiple class selectors here http://code.google.com/p/soupselect/issues/detail?id=4#c0
"""
import re
import operator as operator_
from functools import partial

import bs4

ATTRIBUTE_PATTERN = re.compile(r'\[(?P<attribute>[^\s\]=~\|\^\$\*]+)(?P<operator>[=~\|\^\$\*]?)=?["\']?(?P<value>[^\]"]*)["\']?\]')
PSEUDO_CLASS_PATTERN = re.compile(u':(([^:.#(*\\[]|\\([^)]+\\))+)')
SELECTOR_TOKEN_PATTERN = re.compile(r'([_0-9a-zA-Z-#.:*]+|\[[^\]]+\])$')


def get_attribute_checker(operator, attribute, value=''):
    """
    Takes an operator, attribute and optional value; returns a function that
    will return True for elements that match that combination.
    """
    return {
        '=': lambda el: el.get(attribute) == value,
        # attribute includes value as one of a set of space separated tokens
        '~': lambda el: value in el.get(attribute, '').split(),
        # attribute starts with value
        '^': lambda el: el.get(attribute, '').startswith(value),
        # attribute ends with value
        '$': lambda el: el.get(attribute, '').endswith(value),
        # attribute contains value
        '*': lambda el: value in el.get(attribute, ''),
        # attribute is either exactly value or starts with value-
        '|': lambda el: el.get(attribute, '') == value \
            or el.get(attribute, '').startswith('%s-' % value),
    }.get(operator, lambda el: el.has_attr(attribute))


def is_white_space(el):
    if isinstance(el, bs4.NavigableString) and str(el).strip() == '':
        return True
    if isinstance(el, bs4.Comment):
        return True
    return False


def is_last_content_node(el):
    result = False
    if el is None:
        result = True
    elif is_white_space(el):
        result = is_last_content_node(el.nextSibling)
    return result


def is_first_content_node(el):
    result = False
    if el is None:
        result = True
    if is_white_space(el):
        result = is_first_content_node(el.previousSibling)
    return result


def get_pseudo_class_checker(psuedo_class):
    """
    Takes a psuedo_class, like "first-child" or "last-child"
    and returns a function that will check if the element satisfies
    that psuedo class
    """
    return {
        'first-child': lambda el: is_first_content_node(getattr(el, 'previousSibling', None)),
        'last-child': lambda el: is_last_content_node(getattr(el, 'nextSibling', None))
    }.get(psuedo_class, lambda el: False)


def contains_all_classes_checker(required_classes, el):
    if not el:
        return False
    actual_classes = el.get('class', [])
    test_has_class = partial(operator_.contains, actual_classes)
    return all(map(test_has_class, required_classes))


def get_checker(functions):
    def checker(el):
        for func in functions:
            if not func(el):
                return False
        return el
    return checker


def select(soup, selector):
    """
    soup should be a BeautifulSoup instance; selector is a CSS selector 
    specifying the elements you want to retrieve.
    """
    handle_token = True
    current_context = [(soup, [])]
    operator = None
    while selector:
        if handle_token:
            # Get the rightmost token
            handle_token = False
            match = SELECTOR_TOKEN_PATTERN.search(selector)
            if not match:
                raise Exception("No match was found. We're done or something is broken")
            token = match.groups(1)[0]

            # remove this token from the selector
            selector = selector.rsplit(token, 1)[0].rstrip()
            
            checker_functions = []
            #
            # Get attribute selectors from token
            #
            matches = ATTRIBUTE_PATTERN.findall(token)
            for match in matches:
                checker_functions.append(get_attribute_checker(match[1], match[0], match[2]))

            #
            # Get pseudo classes from token
            #
            for match in PSEUDO_CLASS_PATTERN.finditer(token):
                checker_functions.append(get_pseudo_class_checker(match.groups(1)[0]))

            checker = get_checker(checker_functions)
            #
            # Get tag
            #
            tag = re.findall('^([a-zA-Z0-9]+)', token)
            if len(tag) == 0:
                tag = True
            elif len(tag) == 1:
                tag = tag[0]
            else:
                raise Exception("Multiple tags found (invalid CSS)")

            #
            # Get ID
            #
            ids = re.findall('#([a-zA-Z0-9_-]+)', token)
            if len(ids) > 1:
                raise Exception("Only single # OK")
            #
            # Get classes
            #
            classes = re.findall('\.([a-zA-Z0-9_-]+)', token)
            checker_functions.append(partial(contains_all_classes_checker, classes))

            #
            # Search contexts for matches
            #
            found = []
            find_dict = {}
            if ids:
                find_dict['id'] = ids
            if classes:
                find_dict['class'] = partial(operator_.contains, classes)
            if operator is None:
                # This is the first token: simply find all matches
                for context in current_context:
                    context_matches = [el for el in context[0].find_all(tag, find_dict) if checker(el)]
                    for context_match in context_matches:
                        found.append(
                            (context_match, [context_match]),
                        )
            elif operator == ' ':
                # for each context in current_context, ensure there
                # exists an element somewhere above that element that
                # matches the provided token
                # ("descendant" selector)
                for context in current_context:
                    context_matches = []
                    for el in context[1]:
                        if checker(el.findParent(tag, find_dict)):
                            context_matches.append(el)
                    if context_matches:
                        found.append(
                            (context[0], context_matches),
                        )
            elif operator == '>':
                # for each context in current_context,
                # check if the parent satisfies the provided
                # arguments.
                for context in current_context:
                    context_matches = []
                    for el in context[1]:
                        if checker(el.findParent(tag, find_dict)) == el.parent:
                            context_matches.append(el.parent)
                    if context_matches:
                        found.append(
                            (context[0], context_matches),
                        )
            elif operator == '~':
                # for each context in current_context
                # check 
                raise NotImplementedError("~ operator is not implemented. Sad face :(")
            elif operator == '+':
                # for each context in current_context
                # check if the preceding sibling satisfies the
                # provided arguments
                for context in current_context:
                    context_matches = []
                    for el in context[1]:
                        if checker(el.findPreviousSibling(tag, find_dict)) == el.previousSibling:
                            context_matches.append(el.previousSibling)
                    if context_matches:
                        found.append(
                            (context[0], context_matches)
                        )
            current_context = found
        else:
            # Get the next operator (whitespace, >, ~, +)
            handle_token = True
            match = re.search('([>~+]+)$', selector)
            if match:
                operator = match.groups(1)[0]
                selector = selector.rsplit(operator, 1)[0].rstrip()
            else:
                operator = ' '
    return [entry[0] for entry in current_context]


def monkeypatch(BeautifulSoupClass=None):
    """
    If you don't explicitly state the class to patch, defaults to the most 
    common import location for BeautifulSoup.
    """
    if not BeautifulSoupClass:
        from bs4 import BeautifulSoup as BeautifulSoupClass
    BeautifulSoupClass.findSelect = select


def unmonkeypatch(BeautifulSoupClass=None):
    if not BeautifulSoupClass:
        from bs4 import BeautifulSoup as BeautifulSoupClass
    delattr(BeautifulSoupClass, 'findSelect')
