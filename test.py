import pytest
import requests
from bs4 import BeautifulSoup

def test():
    r = requests.get('http://localhost:8080')
    s = BeautifulSoup(r.text, 'html.parser')
    print(s.title.string)
    assert s.title.string == 'Hello World!'
    assert 'Hello World!' in r.text

test()
