import argparse
from core.colors import green, end,back,red
import argparse
import threading
from art import text2art
import requests
import warnings
import core.config as mem
from core.exporter import exporter
from plugins.heuristic import heuristic
from core.utils import prepare_requests,create_query,update_request
from core.bruter import check_response

warnings.filterwarnings('ignore') 
parser = argparse.ArgumentParser() # defines the parser
# Arguments that can be supplied

result=[]
killed_Urls=[]



parser.add_argument('-o', help='Path for text output file.', dest='text_file')
parser.add_argument('-t', help='Number of concurrent threads. (default: 5)', dest='threads', type=int, default=5)
parser.add_argument('-i', help='Import target URLs from file.', dest='import_file', nargs='?', const=True)
parser.add_argument('-q', help='Quiet mode. No output.', dest='quiet', action='store_true')

args = parser.parse_args() # arguments to be parsed

if args.quiet:
    print = lambda _: None

a = text2art(f"Dalaho")
print(a)



mem.var = vars(args)


def narrower(request2):
   is_reflected= check_response(request2)
   if is_reflected:
       return True


def initialize(url):
    """
    handles parameter finding process for a single request object
    """

    response=requester(url)   
    if type(response) != str:
        found = heuristic(response)
        if found:
            query= create_query(found)

            if "?" in url:
                url2="".join([url,"&",query]) 
            else:
                url2="".join([url,"?",query]) 

        if "=" in url:
            request2=update_request(url)
            response = requester(request2)


def requester(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        response = requests.get(url,
            headers=headers,
            verify=False,
            allow_redirects=False,
            timeout=5
            )
        return response
    except Exception as e:
        return str(e)

def worker(url):
    # Wrapper function for threading, calls initialize
    try:
        initialize(url) 
    except Exception as e:
        global killed_Urls
        killed_Urls.append(url)


def worker_K(url):
    # Wrapper function for threading, calls initialize
    try:
        initialize(url) 
    except Exception as e:
        print(f"Error processing {url}:{e}")


def main():
    num_threads = mem.var['threads']
    thread_list = []
    while urls:
        for _ in range(num_threads):
            if urls:
                u = urls.pop(0) 
                thread = threading.Thread(target=worker, args=(u,))
                thread_list.append(thread)


        for thread in thread_list:
            thread.start()


        for thread in thread_list:
            thread.join()

        thread_list = []  # Clear the thread_list after joining threads

    if killed_Urls:
        if killed_Urls:
            u = killed_Urls.pop(0)  
            worker_K(u)


if __name__ == '__main__':
    urls = prepare_requests(args)
    if len(urls) == 0:
        print("import_file has no any url")
        exit()
    else:
        print(f"count of urls:{green}{len(urls)}")

    main()

    if len(result) !=0:
        exporter(result)