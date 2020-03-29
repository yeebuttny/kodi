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


MURL							='https://www.animezone.pl'

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
	xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=animezonepl&action=serie",listitem=xbmcgui.ListItem("[COLOR orange]Anime serie[/COLOR]"),isFolder=True)
	xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=shindenpl&action=filmy",listitem=xbmcgui.ListItem("[COLOR orange]Anime filmy[/COLOR]"),isFolder=True)
	
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	xbmcplugin.endOfDirectory(common.addon_handle)


def serie(params):
	u=MURL+params.get('url','/anime/lista/')

	letters=['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	letter=letters[xbmcgui.Dialog().select('Wyswietl anime zaczynajace sie na',letters)]
	u+=letter
	
	l=common.solveCFP(u)
	if not l==None:
		try:
			rows=re.compile('<div class=\"well well-sm categories\">.*?<div class=\"image pull-left\">.*?<a href=\"(.*?)\">.*?<img src=\"(.*?)\".*?<i class=\"fa fa-star\"></i>(.*?)</span>.*?<div class=\"description pull-right\">.*?<a href=\".*?\">(.*?)</a>.*?<p>(.*?)</p>',re.DOTALL).findall(l.text.encode('utf-8'))
			for r in range(len(rows)):
				img=rows[r][1]
				title=rows[r][3]
				link=rows[r][0]
				ocena=rows[r][2]
				desc=rows[r][4]

				li=xbmcgui.ListItem(title,thumbnailImage=MURL+img)
				info={'rating':ocena,'plot':desc}
				li.setInfo( type="video", infoLabels = info )
				li.setProperty('IsPlayable', 'true')
				li.setProperty('fanart_image', MURL+img )

				u=common.sysaddon+"?mode=animezonepl&action=seria&url="+urllib.quote_plus(link)
				xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=True)
		except:
			xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=animezonepl&action=serie",listitem=xbmcgui.ListItem("[COLOR red]-- error --[/COLOR]"),isFolder=True)		
		
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	xbmcplugin.endOfDirectory(common.addon_handle)
	
def filmy(params):
	u=MURL+params.get('url','/anime/filmy/')

	letters=['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	letter=letters[xbmcgui.Dialog().select('Wyswietl anime zaczynajace sie na',letters)]
	u+=letter
	
	l=common.solveCFP(u)
	if not l==None:
		try:
			rows=re.compile('<div class=\"well well-sm categories\">.*?<div class=\"image pull-left\">.*?<a href=\"(.*?)\">.*?<img src=\"(.*?)\".*?<i class=\"fa fa-star\"></i>(.*?)</span>.*?<div class=\"description pull-right\">.*?<a href=\".*?\">(.*?)</a>.*?<p>(.*?)</p>',re.DOTALL).findall(l.text.encode('utf-8'))
			for r in range(len(rows)):
				img=rows[r][1]
				title=rows[r][3]
				link=rows[r][0]
				ocena=rows[r][2]
				desc=rows[r][4]

				li=xbmcgui.ListItem(title,thumbnailImage=MURL+img)
				info={'rating':ocena,'plot':desc}
				li.setInfo( type="video", infoLabels = info )
				li.setProperty('IsPlayable', 'true')
				li.setProperty('fanart_image', MURL+img )

				u=common.sysaddon+"?mode=animezonepl&action=seria&url="+urllib.quote_plus(link)
				xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=True)
		except:
			xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=animezonepl&action=serie",listitem=xbmcgui.ListItem("[COLOR red]-- error --[/COLOR]"),isFolder=True)		
		
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	xbmcplugin.endOfDirectory(common.addon_handle)

def seria(params):
	u=MURL+params.get('url','')	
	l=common.solveCFP(u)
	if not l==None:
		##getEpizodes(s,'playEpizod')
		
		rows=re.compile('<td class=\"text-center\"><strong>(.*?)</strong>.*?<td class=\"episode-title\">(.*?)</td>.*?<a href=\"\.\.(.*?)\"',re.DOTALL).findall(l.text.encode('utf-8'))
		
		img=re.compile('<div class=\"image pull-left\">.*?<img src=\"(.*?)\".*?class=\"img-responsive\">.*?</div>',re.DOTALL).findall(l.text.encode('utf-8'))[0]

		if rows:
			for r in range(len(rows)):
				title='('+rows[r][0]+')'+rows[r][1]
				link=rows[r][2]
				addLink(title,link,img,'animezonepl&action=playEpizod')
	xbmcplugin.setContent(common.addon_handle, 'episodes')		
	xbmcplugin.endOfDirectory(common.addon_handle)

def playEpizod(params):
	xbmcplugin.setContent(common.addon_handle, 'movie')
	u=MURL+params.get('url','')
	l=common.solveCFP(u)
	if not l==None:
		rows=re.compile('<tr>.*?<td>(.*?)</td>.*?<span class=\"sprites (.*?) lang\">.*?<button class=\".*?\" data-efl=\"(.*?)\">',re.DOTALL).findall(l.text.encode('utf-8'))
		players=[]
		selList=[]
		for r in range(len(rows)):
			pl=rows[r][0] or 0
			subs=rows[r][1] or 0
			id=rows[r][2] or 0
			players.append([pl,id])
			selList.append("%s [COLOR lime]%s[/COLOR]" % (pl,subs))
		playfrom=xbmcgui.Dialog().select('Wybor zrodla',selList)
		if playfrom>=0:
			player(players[playfrom],u)
	else:
		common.info("LINK FEATCHING FAILED","E404", time=5000)
	xbmcplugin.endOfDirectory(common.addon_handle)

def player(p,l):
	pl=p[0]
	id=p[1]
	rURL=l
	data={"data":id}
	common.log('id: '+id+ " key: "+key)
	s=common.get(rURL,data)
	if s:
		m=re.compile('<a href=\"(.*?)\"',re.DOTALL).findall(s.text.encode('utf-8'))
		common.log(s.text.encode('utf-8'))
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
	
def addLink(title,link,img,sendto):
	l=link
	li=xbmcgui.ListItem(title,thumbnailImage=MURL+img)
	
	li.setInfo( type="video", infoLabels = {} )
	li.setProperty('IsPlayable', 'true')
	u=common.sysaddon+"?mode="+str(sendto)+"&url="+urllib.quote_plus(l)
	ok=xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=False)##change to False
	return ok