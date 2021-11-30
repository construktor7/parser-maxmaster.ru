
import requests
import requests.auth
from bs4 import BeautifulSoup
import time

import sqlite3
db = sqlite3.connect('E:\zubr.db', timeout=1)
dbzubr = db.cursor()


HOST = 'https://maxmaster.ru'

proxies = dict()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
zproxy = {'http':'socks5://lum-customer-hl_d354f9b0-zone-zone1-ip-93.113.52.5:sijkg7f1n39v@zproxy.lum-superproxy.io:22225','https': 'socks5://zproxy.lum-superproxy.io:22225'}
#proxies = {'http':'socks5://127.0.0.1:9150','https': 'socks5://127.0.0.1:9150'}
#proxies = {'http':'http://lum-customer-hl_d354f9b0-zone-zone1-ip-93.113.52.5:sijkg7f1n39v@zproxy.lum-superproxy.io:22225','https': 'https://lum-customer-hl_d354f9b0-zone-zone1-ip-93.113.52.5:sijkg7f1n39v@zproxy.lum-superproxy.io:22225'}
proxies['http'] = 'http://lum-customer-hl_d354f9b0-zone-zone1-ip-93.113.52.5:sijkg7f1n39v@zproxy.lum-superproxy.io:22225';
proxies['https'] = 'https://lum-customer-hl_d354f9b0-zone-zone1-ip-93.113.52.5:sijkg7f1n39v@zproxy.lum-superproxy.io:22225';

#auth = ('lum-customer-hl_d354f9b0-zone-zone1-ip-93.113.52.5','sijkg7f1n39v')
auth=False
allow_redirects = True

#session = requests.session()
#session.proxies = zproxy
#session.proxies['http'] = '://localhost:9051'
#session.proxies['https'] = 'socks5://localhost:9051'

#session.proxies['http'] = 'socks5://lum-customer-hl_d354f9b0-zone-zone1-ip-93.113.52.5:sijkg7f1n39v@zproxy.lum-superproxy.io:22225'
#session.proxies['https'] = 'socks5://lum-customer-hl_d354f9b0-zone-zone1-ip-93.113.52.5:sijkg7f1n39v@zproxy.lum-superproxy.io:22225'
#session.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}

def povtor():
	 dbzubr.execute('SELECT * FROM link WHERE en = 0 ORDER BY href DESC limit 1 ;')
	 result = dbzubr.fetchall()
	 r = result[0][0]
	 print(r)
	 dbzubr.execute('UPDATE link SET en=1 WHERE href = "%s";' % r)
	 db.commit()
	 linkins(result[0][0])

def forlink(a):
	for h in a:
           href = h.get('href');
           t = isinstance(href, str)
           if t:
               if (href[0] == '/' or href[0:21] == 'https://maxmaster.ru/') and href[21:27] != 'images':
                    if href[0:21] == 'https://maxmaster.ru/':
                       hr = href[20:]
                    else:
                        hr = href
                    
                    linkdb(hr)
	povtor()


def linkins(url):
    s=requests.get(HOST+url,headers=headers, allow_redirects=allow_redirects)
    print(HOST+url)
    if s.status_code == 200:
        soup = BeautifulSoup(s.text, 'html.parser')
       # html = soup.prettify()
        a = soup.find_all('a')
        forlink(a)                    
		
    else:
        print('Error 1')


def linkdb(l):
	for row in dbzubr.execute('SELECT count(*) FROM link WHERE href = "%s" ORDER BY href;' % l):
		#time.sleep(10)
		count = row[0]
		if count==0:
			 dbzubr.execute('INSERT INTO link  VALUES ("%s",0);' % l)
			# time.sleep(10)
			 print(count, '|', l)
	db.commit()
 
linkins('')





