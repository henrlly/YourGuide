import os

proxy = 'http://127.0.0.1:2802' #computer's current proxy server

os.environ['http_proxy'] = proxy #same IP
os.environ['HTTP_PROXY'] = proxy #same IP
os.environ['https_proxy'] = proxy #changes IP
os.environ['HTTPS_PROXY'] = proxy #changes IP