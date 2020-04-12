# -*- coding: utf-8 -*-
## imports

import re, os, urlparse, requests, time, sys
import xbmcplugin, xbmcgui, xbmcaddon
import urllib, urllib2,  cookielib, ssl, zlib, base64
import string, json
import resolveurl as urlresolve

from resources.lib import helpers
from resources.lib import common

rot13 = string.maketrans(
    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
    "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

def route(p):
	action=p.get("action","MainMenu")
	if action:
		eval(action)(p)
	else:
		ManiMenu(p)


MURL							='https://shinden.pl'

standardListOptions={'type': 'contains','search':'','genres': '','genres-type': 'all','year_from':'','year_to':'',
'start_date_precision': '3',
'series_status[0]': 'Currently Airing','series_status[1]': 'Finished Airing',
'series_length[2]': 'less_7','series_length[3]': '7_to_18','series_length[4]': '19_to_27','series_length[5]': '28_to_48','series_length[6]': 'over_48',
'series_number[0]': 'only_1','series_number[1]': '2_to_14','series_number[2]': '15_to_28','series_number[3]': '29_to_100','series_number[4]': 'over_100',
'series_number_from':'','series_number_to':'' ,'one_online': 'true',
'sort_by': 'ranking-rate','sort_order': 'desc',
'series_type[0]':'TV',
'series_type[1]':'OVA',
'series_type[2]':'Movie',
'series_type[3]':'ONA',
'series_type[4]':'Special'
}




def MainMenu(p):
	xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=shindenpl&action=nowe",listitem=xbmcgui.ListItem("[COLOR orange]Nowości[/COLOR]"),isFolder=True)
	xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=shindenpl&action=lista",listitem=xbmcgui.ListItem("[COLOR orange]Lista[/COLOR]"),isFolder=True)
	xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=shindenpl&action=lista&search=1",listitem=xbmcgui.ListItem("[COLOR orange]Szukaj[/COLOR]"),isFolder=True)
	xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=shindenpl&action=login",listitem=xbmcgui.ListItem("[COLOR orange]zaloguj[/COLOR]"),isFolder=True)
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	xbmcplugin.endOfDirectory(common.addon_handle)


def lista(params):
	u=MURL+params.get('url','/titles')
	search=params.get('search',None)
	letter=params.get('letter',None)
	if search=='1':
		p=standardListOptions
		p['search']=xbmcgui.Dialog().input('Wyszukaj..')
		common.log(p['search'])
	else:
		p=standardListOptions
		p['page']=int(params.get('page',1))
		if letter==None:
			letters=['-','1','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
			letter=letters[xbmcgui.Dialog().select('Wybor zrodla',letters)]
		p['letter']='' if letter=='-' else letter
	u+='?'+urllib.urlencode(p)	
	l=common.solveCFP(u)
	if not l==None:
		try:
			m=re.compile('<section class=\"title-table\">.*?<article>(.*?)<\/article>',re.DOTALL).findall(l.text.encode('utf-8'))
			rows=re.compile('<ul class=\"div-row\">(.*?<li class=\"rate-top\" title=\"Ocena TOP\">.*?<\/li>.*?)<\/ul>',re.DOTALL).findall(m[0])
			for r in range(len(rows)):
				img=re.compile('<li class=\"cover-col\">.*?<a href=\"(.*?)\"',re.DOTALL).findall(rows[r])[0]
				title=re.compile('<h3>.*?>(.*?)<\/a>',re.DOTALL).findall(rows[r])[0]
				link=re.compile('<h3>.*?<a href=\"(.*?)\">',re.DOTALL).findall(rows[r])[0]
				tags=string.join(re.compile('<li.*?<a data-tag-id.*?>(.*?)<\/a>',re.DOTALL).findall(rows[r]),',')
				try:
					nEE=re.compile('<li class=\"episodes-col\" title=\"(.*?)\">',re.DOTALL).findall(rows[r])[0]
				except:
					nEE='0 x 0min'
				nE=[re.compile('<li class=\"episodes-col\".*?>(.*?)<',re.DOTALL).findall(rows[r])[0],nEE]
				kind=re.compile('<li class=\"title-kind-col\">(.*?)<',re.DOTALL).findall(rows[r])[0]
				ocena=re.compile('<li class=\"rate-top\".*?>(.*?)<',re.DOTALL).findall(rows[r])[0]
				##addFolder(title,link,img,tags,nE,kind,ocena,sendto)
				## add item
				cm=[]
				cm.append(('Wyświetl opis', 'RunPlugin(%s?mode=shindenpl&action=opis&url=%s)' % (common.sysaddon,urllib.quote_plus(link))))
				
				link+='/all-episodes'
				noe=int(nE[0])
				try:
					dur=int(re.compile('x(.*?)min').findall(nE[1])[0])*60
				except:
					dur=0
				li=xbmcgui.ListItem('[COLOR silver]('+kind+')[/COLOR] '+title+' - [COLOR lime]('+(nE[1] if nE[1] else nE[0])+')[/COLOR]',label2='test',thumbnailImage=MURL+img)
				info={'rating':ocena,'genre':tags,'episode':noe,'duration':dur}
				li.setInfo( type="video", infoLabels = info )
				li.setProperty('IsPlayable', 'true')
				li.setProperty('fanart_image', MURL+img )
				## dodaje menu kontekstowe
				li.addContextMenuItems(cm)
				u=common.sysaddon+"?mode=shindenpl&action=seria&url="+urllib.quote_plus(link)
				xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=True)
			xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=shindenpl&action=lista&page="+str(p['page']+1)+"&letter="+letter,listitem=xbmcgui.ListItem("[COLOR gold]>>> DALEJ >>>[/COLOR]"),isFolder=True)
			xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=shindenpl",listitem=xbmcgui.ListItem("[COLOR gold]>>> MENU <<<[/COLOR]"),isFolder=True)
		except:
			xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=shindenpl&action=lista",listitem=xbmcgui.ListItem("[COLOR red]-- error --[/COLOR]"),isFolder=True)		
		
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	xbmcplugin.endOfDirectory(common.addon_handle)
def opis(params):
	u=MURL+params.get('url','')
	l=common.solveCFP(u)
	if not l==None:
		try:
			m=re.compile('<section class=\"info-top\">(.*?)<\/section>',re.DOTALL).findall(l.text.encode('utf-8'))[0]
			opis=re.compile('<div.*?>(.*?)<\/div>',re.DOTALL).findall(m)[0]
			xbmcgui.Dialog().textviewer('Opis',opis)
		except:
			common.log("brak informacji o serii")
			common.info("Problem z pobraniem opisu","BRAK OPISU", time=5000)   
def morelinks(params):
	u=MURL+params.get('url','')
	l=common.solveCFP(u)
	if not l==None:
		try:
			m=re.compile('<li class=\"relation_t2t\">.*?<a href=\"(.*?)\" title=\"(.*?)\".*?class=\"figure-type\">(.*?)</.*?<img src=\"(.*?)\".*?class=\"figure-type\">(.*?)</',re.DOTALL).findall(l.text.encode('utf-8'))
			for r in range(len(m)):
				title="[%s] %s (%s)"%(m[r][2][0],m[r][1],m[r][4])
				link=m[r][0]+'/all-episodes'
				img=m[r][3].replace("/100x100/","/genuine/")
				li=xbmcgui.ListItem(title,thumbnailImage=MURL+img)
				li.setInfo( type="video", infoLabels = {} )
				li.setProperty('IsPlayable', 'true')
				li.setProperty('fanart_image', MURL+img )
				cm=[]
				cm.append(('Wyświetl opis', 'RunPlugin(%s?mode=shindenpl&action=opis&url=%s)' % (common.sysaddon,urllib.quote_plus(link))))
				## dodaje menu kontekstowe
				li.addContextMenuItems(cm)
				u=common.sysaddon+"?mode=shindenpl&action=seria&url="+urllib.quote_plus(link)
				xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=True) 
		except:
			common.log("brak dodatkowych informacji")
			common.info("Problem z pobraniem dodatkowych linków","BŁĄD", time=5000)
		try:
			m=re.compile('<ul class=\"media-list box-scrollable\">(.*)<\/ul>',re.DOTALL).findall(l.text.encode('utf-8'))[0]
			m=re.compile('<li class=\"media media-item\">.*?<img class=\"img media-title-cover\" src=\"(.*?)\".*?<a href=\"(.*?)\">(.*?)</a>.*?<\/li>',re.DOTALL).findall(m)
			for r in range(len(m)):
				title=m[r][2]
				link=m[r][1]+'/all-episodes'
				img=m[r][0].replace("/100x100/","/genuine/")
				li=xbmcgui.ListItem(title,thumbnailImage=MURL+img)
				li.setInfo( type="video", infoLabels = {} )
				li.setProperty('IsPlayable', 'true')
				li.setProperty('fanart_image', MURL+img )
				cm=[]
				cm.append(('Wyświetl opis', 'RunPlugin(%s?mode=shindenpl&action=opis&url=%s)' % (common.sysaddon,urllib.quote_plus(link))))
				## dodaje menu kontekstowe
				li.addContextMenuItems(cm)
				u=common.sysaddon+"?mode=shindenpl&action=seria&url="+urllib.quote_plus(link)
				xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=True)
		except:
			common.log("brak dodatkowych informacji")
			common.info("Problem z pobraniem dodatkowych linków","BŁĄD", time=5000)       
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	xbmcplugin.endOfDirectory(common.addon_handle)

def seria(params):
	u=MURL+params.get('url','')	
	l=common.solveCFP(u)
	if not l==None:
		##getEpizodes(s,'playEpizod')
		m=re.compile('<tbody class=\"list-episode-checkboxes\">(.*?)<\/tbody>',re.DOTALL).findall(l.text.encode('utf-8'))
		img=re.compile('<img class=\"info-aside-img\" src=\"(.*?)\"',re.DOTALL).findall(l.text.encode('utf-8'))[0]
		mtitle=re.compile('<h1 class=\"page-title\">Anime: (.*?)<\/h1>').findall(l.text.encode('utf-8'))[0]
		if m:
			rows=re.compile('<tr>(.*?)<\/tr>',re.DOTALL).findall(m[0])
		if rows:
			for r in range(len(rows)):
				nE=re.compile('<td>(\d*?)<\/td>',re.DOTALL).findall(rows[r])[0]
				title=re.compile('<td class=\"ep-title\">(.*?)<\/td>',re.DOTALL).findall(rows[r])[0]
				title2=' | ' if title else ''
				title=mtitle+title2+title
				isOnline=re.compile('<i class=\"fa fa-fw fa-(\w*?)\">',re.DOTALL).findall(rows[r])[0]
				data=re.compile('\"ep-date\">(.*?)<\/td>',re.DOTALL).findall(rows[r])[0]
				link=re.compile('<a href=\"(.*?)\"',re.DOTALL).findall(rows[r])[0]
				addLink(title,nE,link,img,data,'shindenpl&action=playEpizod',isOnline)
	link=params.get('url','').replace("/all-episodes","")				
	u=common.sysaddon+"?mode=shindenpl&action=morelinks&url="+urllib.quote_plus(link)
	xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=xbmcgui.ListItem("[COLOR gold]>>> WIĘCEJ <<<[/COLOR]"),isFolder=True)
	xbmcplugin.setContent(common.addon_handle, 'episodes')		
	xbmcplugin.endOfDirectory(common.addon_handle)

def playEpizod(params):
	xbmcplugin.setContent(common.addon_handle, 'movie')
	u=MURL+params.get('url','')
	l=common.solveCFP(u)
	if not l==None:
		m=re.compile('<table class=\"data-view-table-strips data-view-table-big data-view-hover\">(.*?)<\/table>',re.DOTALL).findall(l.text.encode('utf-8'))[0]
		m1=re.compile('<tbody>(.*?)<\/tbody>',re.DOTALL).findall(m)
		rows=re.compile('<tr>(.*?)<\/tr>',re.DOTALL).findall(m1[0])
		KEY=re.compile("_Storage\.basic =  '(.*?)';",re.DOTALL).findall(l.text.encode('utf-8'))[0]
		XHR=re.compile("_Storage\.XHRService = '\/\/(.*?)';",re.DOTALL).findall(l.text.encode('utf-8'))[0]
		players=[]
		selList=[]
		for r in range(len(rows)):
			pl=re.compile('<td class=\"ep-pl-name\">.*?([\w\s\d]*?)<\/td>',re.DOTALL).findall(rows[r])[0] or 0
			audio=re.compile('<td class=\"ep-pl-alang\">.*?<span class=\"mobile-hidden\">(.*?)<\/span>',re.DOTALL).findall(rows[r])[0] or 0
			subs=re.compile('<td class=\"ep-pl-slang\">.*?<span class=\"mobile-hidden\">(.*?)<\/span>',re.DOTALL).findall(rows[r])[0] or 0
			res=re.compile('<td class=\"ep-pl-res\">.*?<\/span>(.*?)<\/td>',re.DOTALL).findall(rows[r])[0] or 0
			id=re.compile('\"online_id\":\"(.*?)\"',re.DOTALL).findall(rows[r])[0] or 0
			players.append([pl,id])
			selList.append("%s [COLOR blue]%s[/COLOR] A:%s N:%s" % (pl,res,audio,subs))
		playfrom=xbmcgui.Dialog().select('Wybor zrodla',selList)
		if playfrom>=0:
			player(players[playfrom],KEY,XHR)
	else:
		common.info("LINK FEATCHING FAILED","E404", time=5000)
	xbmcplugin.endOfDirectory(common.addon_handle)

def player(p,k,x):
	pl=p[0]
	id=p[1]
	key=k
	XHR=x
	rURL="https://"+XHR+"/"+id+"/"
	data={"auth":key}
	common.log('id: '+id+ " key: "+key)
	s=request(rURL,data)
	if s:
		m=re.compile('<iframe.*?src=\".*?\/\/(.*?)\"',re.DOTALL).findall(s)
		if len(m)>1:
			playfrom=xbmcgui.Dialog().select('Wybor zrodla',m)
			common.log('resolving: '+m[playfrom])
		else:
			playfrom=0
		m=m[playfrom]
		if 'cda' in m:
			resolveCDA(m)
		elif 'openload' in m:
			resolveOPENLOAD(m)
		elif 'facebook' in m:
			resolveFB(m)
		else:
			resolveOTHER(m)
			#info('Player nie jest obslugiwany','PLAYER ERROR',200)
	else:
		info("Brak odpowiedzi XHR, wiecej w log-u.","Upss...")

def request(l,d):
	s=requests.Session()
	head = {'authority': 'shinden.pl','user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.71','X-Requested-With': 'XMLHttpRequest','Host': 'shinden.pl','contentType': 'application/x-www-form-urlencoded; charset=UTF-8','Referer': 'https://shinden.pl',	
				'pragma': 'no-cache','cache-control': 'no-cache',
				'upgrade-insecure-requests': '1',				
				'dnt': '1',
				'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'accept-encoding': 'identity',
				'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'}
	#try:
	r=s.get(l+"player_load", params=d)#, headers=head,timeout=10)
	r.close()
	common.info('Pobieram dane playera','')
	time.sleep(int(r.text))
	d['width']="800"
	r=s.get(l+"player_show", params=d)#, headers=head,timeout=10)
	r.close()
	text=r.text.encode('utf-8')
	#except:
	#	log('nieudane request')
	#	text=''
	return text

def request2(l,d=None):
	s=requests.Session()
	head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36','X-Requested-With': 'XMLHttpRequest','Host': 'openload.co','contentType': 'application/x-www-form-urlencoded; charset=UTF-8','Referer': 'https://openload.co'}
	r=None
	try:
		r=s.get(l, params=d, headers=head,timeout=10)
	except:
		common.log('nieudane request OPENLOAD')
	return r
def decodeCDA(videofile): ##podziekowania dla mbebe za decoder
	a = videofile
	cc =len(a)
	linkvid=''
	for e in range(cc):
		f = ord(a[e])
		if f >=33 or f <=126:
			b=chr(33 + (f + 14) % 94)
		else:
			b=chr(f)
		linkvid+=b
	
	linkvid = linkvid.replace("adc.mp4", ".mp4")
	linkvid = linkvid.replace(".cda.mp4", "")
	linkvid = linkvid.replace(".2cda.pl", ".cda.pl")
	linkvid = linkvid.replace(".3cda.pl", ".cda.pl")
	linkvid = linkvid.replace(".3cda.pl", ".cda.pl")
	linkvid = linkvid.replace("0)sss.mp4", ".mp4")
	linkvid = linkvid.replace("0r)s.mp4", ".mp4")
	linkvid = linkvid[:linkvid.index('0"')]
	if not linkvid.startswith('http'):
		linkvid = 'https://'+linkvid
	if not linkvid.endswith('.mp4'):
		linkvid += '.mp4'
	return linkvid

def resolveCDA(l):
	s=common.get("https://"+l)
	if not s==None:
		m=re.compile('<div id=\".*?\" player_data=\'(.*?)\' tabindex').findall(s.text.encode('utf-8'))[0]
		if m:
			vl=re.compile('\"file\":\"(.*?)\"').findall(m)[0]
			vl=vl.replace('\\','')
			
			if re.match('uggc',vl):
				vl=string.translate(vl, rot13)
				vl=vl[:-7] + vl[-4:]
			else:
				vl=decodeCDA(urllib.unquote(vl))
				
			xbmcplugin.setResolvedUrl(common.addon_handle, True, xbmcgui.ListItem(path=vl))
	else:
		return False
	xbmcplugin.endOfDirectory(common.addon_handle)

def resolveFB(l):
	#if len(l)>1:
	#	playfrom=xbmcgui.Dialog().select('Wybor zrodla',l)
	#l=l[playfrom]
	s=common.get("https://"+l)
	if not s==None:
		#log(s)
		m=re.compile('\"hd_src\"\:"(.*?)\"').findall(s.text.encode('utf-8'))[0]
		if m:
			##vl=re.compile('\"file\":\"(.*?)\"').findall(m)[0]
			vl=m.replace('\\','')
			#log(m)
			xbmcplugin.setResolvedUrl(common.addon_handle, True, xbmcgui.ListItem(path=vl))
	else:
		return False
	xbmcplugin.endOfDirectory(common.addon_handle)

def resolveOTHER(l):
	link=''
	try:
		link=urlresolve.resolve("https://"+l)
	except:
		common.info('cos wiecej w logu','Blad resolveurl')
	if link:
		xbmcplugin.setResolvedUrl(common.addon_handle, True, xbmcgui.ListItem(path=link))
	

def resolveOPENLOAD(l):
	mediaid=l.split("/")
	#//openload.co/embed/T46sXRDbTos/
	mediaid=mediaid[len(mediaid)-2]
	status=requests.get('https://api.openload.co/1/file/info?file='+mediaid)
	if status:
		if status.json().get('status')==200:
			status=requests.get('https://api.openload.co/1/streaming/get?file='+mediaid)
			if status:
				if status.json().get('status')==200:
					link=status.json().get('result').get('url')
					if link:
						xbmcplugin.setResolvedUrl(common.addon_handle, True, xbmcgui.ListItem(path=link))
					else:
						common.info('OPENLOAD - link not found','',200)
				else:
					common.info(status.json().get('msg'))
			else:
				common.info('openload - request error','',200)
		else:
			common.info(status.json().get('msg'))
	else:
		common.info('openload - request error','',200)
	return 0
	
def addLink(title,nE,link,img,data,sendto,isOnline):
	l=link
	li=xbmcgui.ListItem('[COLOR gray]#'+str(nE)+'('+str(data)+') [/COLOR] [COLOR %s]'%('' if isOnline=='check' else 'red')+title+'[/COLOR]',thumbnailImage=MURL+img)
	
	info={'plotoutline':'data emisji: '+data,'plot':'data emisji: '+data,'year':int(nE),'episode':int(nE)}
	li.setInfo( type="video", infoLabels = info )
	li.setProperty('IsPlayable', 'true')
	u=common.sysaddon+"?mode="+str(sendto)+"&url="+urllib.quote_plus(l)
	ok=xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=False)##change to False
	return ok


def nowe(params):
	u=MURL#+params.get('url','')	
	l=common.solveCFP(u)
	sezon=None
	if not l==None:
		m=re.compile('<section class=\".*box-new-series\">.*?<ul class=\"seasons-list\">(.*?)<\/ul>',re.DOTALL).findall(l.text.encode('utf-8'))
		if m:
			sezony=re.compile('<a href=\"(.*?)\">(.*?)<\/a>',re.DOTALL).findall(m[0])
		if sezony:
			# przetestowac
			slinks=[]
			snames=[]
			for s in sezony:
				slinks.append(s[0])
				snames.append(s[1])
			sezon=slinks[xbmcgui.Dialog().select('Wybor zrodla',snames)]
			common.log(sezon)
		else:
			sezon="/series/season/current"
	l=None
	l=common.solveCFP(u+sezon)
	if not l==None:
		rows=re.compile('<li class=\"title anime\".*?<section>.*?<a href=\"(.*?)\" class=\"img  media-title-cover\".*?<img src=\"(.*?)\" alt=\"(.*?)\".*?<div class=\"title-desc box-scrollable\">(.*?)<\/div>',re.DOTALL).findall(l.text.encode('utf-8'))
		if rows:
			for r in range(len(rows)):
				title=rows[r][2]
				link=rows[r][0]
				img=rows[r][1]
				desc=rows[r][3]
				l=link+"/all-episodes"
				li=xbmcgui.ListItem(title,thumbnailImage=MURL+img)
				
				info={'plotoutline':desc,'plot':desc}
				li.setInfo( type="video", infoLabels = info )
				u=common.sysaddon+"?mode=shindenpl&action=seria&url="+urllib.quote_plus(l)
				xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=True)
				
				
				
	xbmcplugin.setContent(common.addon_handle, 'episodes')		
	xbmcplugin.endOfDirectory(common.addon_handle)
