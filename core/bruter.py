import requests
import re

def check_response(request):

    response = requester(request)
    if type(response) != str and response.status_code in (400, 413, 418, 429, 503):
        return False
    if type(response) ==str:
        return False

    value='"dalaho'
    if value in response.text and re.search(r'[\'"\s]%s[\'"\s]' % value, response.text):
        return True

        
def requester(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1'
    }
    session = requests.Session()
    try:
        response = session.get(url,
            headers=headers,
            verify=False,
            allow_redirects=False,
            timeout=5
            )
        return response
    except Exception as e:
        return str(e)