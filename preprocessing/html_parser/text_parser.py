"""
This script contains the functions used to parse one report, ie
the functions to split the html text into a dictionnary of
sections.

Only main_parser is used in practice since all the other functions
are auxiliary (~private)

@author Valentin Charvet
@date 11/04/2018
"""


from bs4 import BeautifulSoup

from unidecode import unidecode
import re


def main_parser(text, name, remove=['h4', 'table', 'link', 'style'], headers='h3'):
    """ takes as input the string from the report and
    transforms splits it into sections

    Parameters
    ----------
    text : string
        report in html format
    name : string
        name of the current document (useful for debugging purpose)
    remove : list
        name of the tags to remove because contain useless information
    headers : string
        name of the tags that delimit the sections

    Returns
    -------
    dict
        keys are section names
        values are the content of the section

    """
    try:
        soup = BeautifulSoup(text, 'html.parser')
        soup = BeautifulSoup(soup.prettify())
        soup.name = name
    except TypeError:
        print('{} can not be parsed'.format(text))
        soup = BeautifulSoup('')

    clean_soup(soup, remove)

    return parse_soup(soup, False, headers)


def text_between_tags(tag1, tag2):
    """ This function fetches the text between tag 1 and tag 2
    The soup should already be cleansed from useless tags such as  span

    Parameters
    ----------
    tag1
    tag2

    Returns
    -------
    string
    all the text between tag1 and tag2

    """
    res = tag1.text
    next_tag = tag1.find_next()
    # iterates over tags to append text to res
    while next_tag != tag2:
        # print(res, cur_tag.text)
        res += next_tag.text + ' '
        next_tag = next_tag.find_next()
    return clean_string(res)


def last_tag_text(final_tag):
    """ Fetches text from last tag

    Parameters
    ----------
    final_tag

    Returns
    -------
    string
        content of the last section

    """
    res = ''
    cur_tag = final_tag.find_next()
    while cur_tag is not None:
        res += cur_tag.text + ' '
        cur_tag = cur_tag.find_next()
    return clean_string(res)


def parse_soup(soup, verbose=False, headers='h3'):
    """Splits the soup between headers and returns a dictionnary

    Parameters
    ----------
    soup : BeautifulSoup instance
    verbose: bool, (default=False)
        weather to print informaion about parsing
    headers : string
        delimiters of the sections

    Returns
    -------
    dict
        keys are section names
        values are section contents

    """

    res_dic = {}
    header_list = list(soup.find_all(headers))

    for index, header in enumerate(header_list[:-1]):
        try:
            new_text = text_between_tags(header.find_next(), header_list[index + 1])
            key = header.text
            res_dic[clean_string(key)] = new_text
            # print(index, new_text)
        except AttributeError as e:
            print('{} occurred at {}'.format(e, soup.name))
    try:
        final_text = last_tag_text(header_list[-1])
        final_key = header_list[-1].text
        res_dic[clean_string(final_key)] = final_text
    except IndexError as e:
        if verbose:
            print('{} current report {} is empty'.format(e, soup.name))
    if verbose:
        print('Document {} has been parsed'.format(soup.name))
    return res_dic


def clean_soup(soup, remove):
    """ Remove the tags indicated in remove parameter from the soup
    soup
    Transfo done inline

    Parameters
    ----------
    soup : BeautifulSoup instance
    remove : list
        name of the tags to remove from the soup

    Returns
    -------
    BeautifulSoup instance
    the same as input since inline transformation

    """
    # remove first span <span style= "color: red"> that indicates
    # color legend
    try:
        soup.find('span', attrs={'style': "color: red"}).extract()
    except AttributeError:
        print('No legend found')

    # remove tags indicated in input
    for tag in remove:
        cont = True
        while cont:
            try:
                soup.find(tag).extract()
            except AttributeError:
                print('No tag {} in the soup {}'.format(tag, soup.name))
                cont = False
    return


def clean_string(s):
    """ remove non alphanumeric caracters from string s
    returns the lowerCase string

    :param s:
    :return:
    """
    s_decoded = unidecode(s).replace('\n', '').replace('  ', ' ')
    pattern = re.compile('[\W_]+')
    return pattern.sub(' ', s_decoded).lower().strip()