from suds.client import Client as SudsClient
from suds.sax.element import Element

"""
    default "UsernameToken" in suds produces "Password" element without a "Type" field
    https://fedorahosted.org/suds/ticket/402
    so need to build it manually, specifying namespaces
"""

wsse = ('wsse', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd')
security = Element('Security', ns=wsse)
usernametoken = Element('UsernameToken', ns=wsse)
uname = Element('Username', ns=wsse).setText('myusername')
passwd = Element('Password', ns=wsse).setText('mypassword')
passwd.set('Type', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText')

usernametoken.insert(uname)
usernametoken.insert(passwd)
security.insert(usernametoken)

url = 'http://127.0.0.1:5000/soap/someservice?wsdl'
client = SudsClient(url=url, cache=None)
client.set_options(soapheaders=security)

r = client.service.echo(str='hello world', cnt=3)

print(r)
