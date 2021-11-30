import requests
import requests.auth
from bs4 import BeautifulSoup
import time
import random
import sqlite3
import json


db = sqlite3.connect('E:\z.db', timeout=10)
dbzubr = db.cursor()

dbi = sqlite3.connect('E:\item.db', timeout=10)
dbitem = dbi.cursor()

p = dict()
fileptr = open("E:\ips-zone1.txt","r");
n=0
for i in fileptr:  
    p[n] = i.strip()
    n += 1

HOST = 'https://maxmaster.ru'


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
zproxy = {'http':'socks5://lum-customer-hl_d354f9b0-zone-zone1-ip-93.113.52.5:sijkg7f1n39v@zproxy.lum-superproxy.io:22225','https': 'socks5://zproxy.lum-superproxy.io:22225'}
#proxies = {'http':'socks5://127.0.0.1:9150','https': 'socks5://127.0.0.1:9150'}
#proxies = {'http':'http://lum-customer-hl_d354f9b0-zone-zone1-ip-93.113.52.5:sijkg7f1n39v@zproxy.lum-superproxy.io:22225','https': 'https://lum-customer-hl_d354f9b0-zone-zone1-ip-93.113.52.5:sijkg7f1n39v@zproxy.lum-superproxy.io:22225'}
proxies = dict()



auth=False
allow_redirects = True

def plusarticul(url):
	prox = dict()
	number = random.randrange(19999)  # значение от 0 до 10
	pp = p[number].split(':')
	ppp =  pp[2] + ':' + pp[3] + '@' + pp[0] + ':' + pp[1]
	prox['http'] = 'http://' + ppp;
	prox['https'] = 'https://' + ppp;
	print(prox)
	
	sss=requests.get(url, headers=headers, proxies=prox, allow_redirects=allow_redirects)
	if sss.status_code == 200:
		print(sss.text)
	else:
		print('Error 3')

def mojet(st):
	params = {}
	params['is_ajax'] = 1
	params['security_hash'] = st.select('input[name="security_hash"]')[0]['value']
	get_join_products = st.select('ul.ty-tabs__list > li[data-b]')
	queue = {}
	#print(get_join_products)
	for getjoinproducts in get_join_products:
		params['block_id'] = getjoinproducts['data-b']
		params['join_id'] = getjoinproducts['data-j']
		params['product_id'] = getjoinproducts['data-p']
		ss=requests.post('https://maxmaster.ru/index.php?dispatch=ab__ia_joins.get_join_products',headers=headers, params=params, proxies=proxies, allow_redirects=allow_redirects)
		queue[getjoinproducts.span.text] = ''
		#print(queue)
		#print(ss)
		if ss.status_code == 200:
			#ssoup = BeautifulSoup(ss.text, 'lxml') #lxml
			#ssoup = ssoup.replace('&lt;','<')
			#ssoup = ssoup.replace('&gt;','>')
			#print(soup.prettify())
			prig = ss.text.split('"products_scroller":"')[1]
			prig = prig.replace('","notifications":[]}','')
			prig = prig.replace('\\n','')
			prig = prig.replace('\\t','')
			prig = prig.replace('\\r','')
			prig = prig.replace('\\"','"')
			prig = prig.replace('\\/','/')
			Psoup = BeautifulSoup(prig, 'html.parser')
			for dop in Psoup.select("a.product-title"):
				queue[getjoinproducts.span.text] = dop['href'].replace('https://maxmaster.ru','') + ' ' + queue[getjoinproducts.span.text]
				queue[getjoinproducts.span.text] = queue[getjoinproducts.span.text].strip()
				
		else:
			print('Error 2')
	return queue
		
def soups(so, url):
	soup = BeautifulSoup(so, 'html.parser')
	try:
		articul = soup.select("div.ty-control-group span.ty-control-group__item:not(.ty-qty-in-stock)")[0].text.strip()
		name = soup.select("h1.ut2-pb__title bdi")[0].text.strip()
		if articul and name:
			description = soup.select("div.ty-wysiwyg-content[data-ca-live-editor-object-id]")[0].text.strip()
			i = soup.select('a[data-ca-gallery-large-id] img')
			images = ''
			for image in i:
				images = image['src'] + ' ' + images
				images = images.strip()
			prop = soup.select('div.ty-product-feature')
			with open('E:\prop.txt', 'r') as file:
				response=file.read().replace('\n', '').replace('\r', '')
			prall = json.loads(response)
			print(prall)
			pr = {}
			for property in prop:
				pr[property.span.text[:-1]] = property.div.span.text
				prall[property.span.text[:-1]] = property.div.span.text
			with open("E:\prop.txt", "w", encoding="utf-8") as file:
				json.dump(prall, file)
			prjson = json.dumps(pr)
			mojetjson = json.dumps(mojet(soup))
			print(url, '|', articul, '|', name, '|', description, '|' , images , '|', prjson, '|', mojetjson)
			for row in dbitem.execute('SELECT count(*) FROM url WHERE url = "%s" ORDER BY url;' % url):
				count = row[0]
				if count==0:
					print(count)
					dbitem.execute('INSERT INTO url (url, articul, name, description, images, pr, mojet) VALUES (?, ?, ?, ?, ?, ?, ?);', (url, articul, name, description, images, prjson, mojetjson))
					dbi.commit()
	except Exception:
		print(Exception,'!!!!!!', url)
	dbzubr.execute('UPDATE link SET en=2 WHERE href = "%s";' % url)
	db.commit()
	imports()

def imports():
	number = random.randrange(19999)  # значение от 0 до 10
	pp = p[number].split(':')
	ppp =  pp[2] + ':' + pp[3] + '@' + pp[0] + ':' + pp[1]
	proxies['http'] = 'http://' + ppp;
	proxies['https'] = 'https://' + ppp;
	print(proxies)
	dbzubr.execute('SELECT * FROM link WHERE en = 0 ORDER BY href DESC limit 1 ;')
	result = dbzubr.fetchall()
	print(result)
	url = result[0][0]
	print(HOST+url)
	s=requests.get(HOST+url,headers=headers, proxies=proxies, allow_redirects=allow_redirects)
	if s.status_code == 200:
		soups(s.text, url)
	else:
		print('Error 1')
	
imports()
