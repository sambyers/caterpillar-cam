from requests import get
from time import sleep

def url_alive(url, retries=0, seconds=0, ok=0):
    '''Simple function to check the liviness of a url.

    Args:
        url: the URL to be checked
        retries: Integer of times to retry the URL, if not receiving OK
        seconds: Integer of seconds to wait in between retries
        ok: Integer of OK messages to receive before considering the URL alive

    Returns:
        True if URL responds with OK message or False if URL responds with anything
        else.
    '''
    retrycount = 1
    okcount = 1
    while True:
        if okcount == ok:
            return True
        elif retrycount == retries:
            return False
        else:
            retrycount += 1
            response = get(url)
            if response.ok:
                okcount += 1
            sleep(seconds)

if __name__ == '__main__':
    if url_alive("https://google.com", retries=2, seconds=2, ok=2):
        print("Google.com is up.")
    else:
        print("Google.com is down.")
