import os

def change_proxy(proxy):
    os.environ['http_proxy'] = proxy #same IP
    os.environ['HTTP_PROXY'] = proxy #same IP
    os.environ['https_proxy'] = proxy #changes IP
    os.environ['HTTPS_PROXY'] = proxy #changes IP

if __name__ == '__main__':
    change_proxy('http://127.0.0.1:2802')