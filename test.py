import pytest
import requests
from bs4 import BeautifulSoup
from werkzeug import generate_password_hash, check_password_hash
import cgi



def test_act3():
    data = {'username': 'admin', 'password': 'admin'}
    r = requests.post('http://localhost:5000/login', data=data)
    print ('TEST1 - correct login : admin:admin')
    assert 'SAMPLE HOMEPAGE SHOULD GO HERE......' in r.content.decode('UTF-8')

    data = {'username': 'admin', 'password': 'admin1'}
    r = requests.post('http://localhost:5000/login', data=data)
    print ('TEST2 - incorrect password : admin:admin1')
    assert 'You inputted the wrong password' in r.content.decode('UTF-8')
    
    data = {'username': 'admin1', 'password': 'admin'}
    r = requests.post('http://localhost:5000/login', data=data)
    print ('TEST3 - incorrect username : admin1:admin')
    assert 'That username does not exist.' in r.content.decode('UTF-8')



def Act2test():
    r = requests.get('http://localhost:8080')
    s = BeautifulSoup(r.text, 'html.parser')
    assert s.title.string == 'Hello World!'
    print(s.title.string)
    assert 'Hello World!' in r.text
    
def test_act4():
    data = {'username': 'admin', 'password': 'admin'}
    r = requests.post('http://localhost:5000/login', data=data)
    assert 'RITube Video System' in r.text
    t = requests.post("http://localhost:5000/homepage", {"file": "Activity\ 4/SampleVideo_1280x720_2mb.mp4"})
    assert 'SampleVideo_1280x720_2mb.mp4' in t.text
    
test_act4()
