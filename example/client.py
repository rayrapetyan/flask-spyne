from suds.client import Client as SudsClient
import requests

url = 'http://127.0.0.1:5000/soap/someservice?wsdl'
client = SudsClient(url=url, cache=None)
r = client.service.echo(str='hello world', cnt=3)
print r

r = client.service.answer(str='some question')
print r

url = 'http://127.0.0.1:5000/json/anotherservice/echo'
params = {'str': 'hello world', 'cnt': 3}
r = requests.get(url=url, params=params)
print r.text

url = 'http://127.0.0.1:5000/json/anotherservice/answer'
params = {'str': 'some question'}
r = requests.get(url=url, params=params)
print r.text
