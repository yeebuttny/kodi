# -*- coding: utf-8 -*-
import re, string, xbmcaddon

def headers(m):
	if m:
		return eval(m)


alltubepl = {
				'authority': 'alltube.pl',
				'pragma': 'no-cache','cache-control': 'no-cache',
				'upgrade-insecure-requests': '1',
				'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.71',
				'dnt': '1',
				'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'accept-encoding': 'identity',
				'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
				}
				
shindenpl = {
				'authority': 'shinden.pl',
				'pragma': 'no-cache','cache-control': 'no-cache',
				'upgrade-insecure-requests': '1',
				'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.71',
				'dnt': '1',
				'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'accept-encoding': 'identity',
				'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
				}
				
animezonepl = {
				'authority': 'www.animezone.pl',
				'pragma': 'no-cache','cache-control': 'no-cache',
				'upgrade-insecure-requests': '1',
				'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.71',
				'dnt': '1',
				'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'accept-encoding': 'identity',
				'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
				}
							

def PLchar(txt):
	if type(txt) is not str:
		txt=txt.encode('utf-8')

	txt = txt.replace('''&nbsp;''','')
	txt = txt.replace('''&quot;''','"')
	txt = txt.replace('''&bdquo;''','\'')
	txt = txt.replace('''&rdquo;''','\'')
	txt = txt.replace('''&oacute;''','ó').replace('''&Oacute;''','Ó')
	s='26235c642b3b'
	t='265b5e3b5d3b'
	txt = re.sub(s.decode('hex'),'',txt)
	txt = re.sub(t.decode('hex'),'',txt)
	txt = txt.replace('''&amp;''','&')
	txt = txt.replace('\u0105','ą').replace('\u0104','Ą')
	txt = txt.replace('\u0107','ć').replace('\u0106','Ć')
	txt = txt.replace('\u0119','ę').replace('\u0118','Ę')
	txt = txt.replace('\u0142','ł').replace('\u0141','Ł')
	txt = txt.replace('\u0144','ń').replace('\u0144','Ń')
	txt = txt.replace('\u00f3','ó').replace('\u00d3','Ó')
	txt = txt.replace('\u015b','ś').replace('\u015a','Ś')
	txt = txt.replace('\u017a','ź').replace('\u0179','Ź')
	txt = txt.replace('\u017c','ż').replace('\u017b','Ż')
	return txt