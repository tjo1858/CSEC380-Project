import pytest
import requests
from bs4 import BeautifulSoup
from werkzeug import generate_password_hash, check_password_hash
import cgi



def Act3Test():
    data = {'username': 'admin', 'password': 'admin'}
    r = requests.post('http://127.0.0.1:5000/login', data=data)
    print ('TEST1 - correct login : admin:admin')
    assert 'SAMPLE HOMEPAGE SHOULD GO HERE......' in r.content.decode('UTF-8')

    data = {'username': 'admin', 'password': 'admin1'}
    r = requests.post('http://127.0.0.1:5000/login', data=data)
    print ('TEST2 - incorrect password : admin:admin1')
    assert 'wrong password' in r.content.decode('UTF-8')
    
    data = {'username': 'admin1', 'password': 'admin'}
    r = requests.post('http://127.0.0.1:5000/login', data=data)
    print ('TEST3 - incorrect username : admin1:admin')
    assert 'wrong username' in r.content.decode('UTF-8')



def Act2test():
    r = requests.get('http://localhost:8080')
    s = BeautifulSoup(r.text, 'html.parser')
    assert s.title.string == 'Hello World!'
    print(s.title.string)
    assert 'Hello World!' in r.text

Act3Test()
