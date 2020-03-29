# -*- coding: utf-8 -*-
## imports

import re, os, urlparse, requests, time, sys
import xbmcplugin, xbmcgui, xbmcaddon
import urllib, urllib2,  cookielib, ssl, zlib, base64
import string, json
import resolveurl as urlresolve

from resources.lib import helpers
from resources.lib import common

def route(p):
	action=p.get("action","MainMenu")
	if action:
		eval(action)(p)
	else:
		MainMenu(p)


MURL							='http://alltube.pl'


def MainMenu(p):
	xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=alltubepl&action=filmy",listitem=xbmcgui.ListItem("[COLOR orange]Filmy[/COLOR]"),isFolder=True)
	xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=alltubepl&action=seriale",listitem=xbmcgui.ListItem("[COLOR orange]Seriale[/COLOR]"),isFolder=True)
	xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=alltubepl&action=szukaj",listitem=xbmcgui.ListItem("[COLOR orange]Szukaj[/COLOR]"),isFolder=True)
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	xbmcplugin.endOfDirectory(common.addon_handle)
## -==================== END ====================- 
	
def filmy(p):
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	u=MURL+p.get('url','/filmy-online')
	page=int(p.get('page',1))
	u+='/strona['+str(page)+']+'
	l=common.solveCFP(u)
	if not l==None:
		try:
			rows=re.compile('<div class=\"item-block clearfix\">.*?<div class=\"row\">.*?(<a href=\".*?<\/a>).*?<\/div>.*?<\/div>',re.DOTALL).findall(l.text.encode('utf-8'))
			common.log(len(rows))
			for r in range(len(rows)):
				img=(re.compile('<img src=\"(.*?)\"',re.DOTALL).findall(rows[r])[0])#.replace("thumb","normal")
				title=helpers.PLchar(re.compile('<h3>(.*?)<\/h3>',re.DOTALL).findall(rows[r])[0])
				stitle=re.compile('<div class=\"second-title\">(.*?)<\/div>',re.DOTALL).findall(rows[r])[0]
				details=helpers.PLchar(re.compile('<i class=\"fa fa-microphone\".*?>.*?<\/i>(.*?)<i',re.DOTALL).findall(rows[r])[0])
				desc=helpers.PLchar(re.compile('<p .*?>(.*?)<\/p',re.DOTALL).findall(rows[r])[0])
				link=re.compile('<a href=\"(.*?)\">',re.DOTALL).findall(rows[r])[0]
				li=xbmcgui.ListItem(title+' - [COLOR lime]('+details+')[/COLOR]',thumbnailImage=img)
				info={'plotoutline':desc,'plot':desc}
				li.setInfo( type="video", infoLabels = info )
				li.setProperty('IsPlayable', 'true')
				li.setProperty('fanart_image', img.replace('thumb','normal') )
				u=common.sysaddon+"?mode=alltubepl&action=play&url="+urllib.quote_plus(link)
				xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=False)
			xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=alltubepl&action=filmy&page="+str(page+1),listitem=xbmcgui.ListItem("[COLOR gold]>>> DALEJ >>>[/COLOR]"),isFolder=True)
		except:
			xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=alltubepl&action=filmy",listitem=xbmcgui.ListItem("[COLOR red]-- error --[/COLOR]"),isFolder=True)		
	xbmcplugin.endOfDirectory(common.addon_handle)
## -==================== END ====================- 

def seriale(p):
	xbmcplugin.setContent(common.addon_handle, 'episodes')
	xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=alltubepl&action=nowelinki",listitem=xbmcgui.ListItem("[COLOR orange]Nowe linki[/COLOR]"),isFolder=True)
	xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=alltubepl&action=alfabetycznie",listitem=xbmcgui.ListItem("[COLOR orange]Alfabetycznie[/COLOR]"),isFolder=True)
	xbmcplugin.endOfDirectory(common.addon_handle)
## -==================== END ====================- 

def nowelinki(p):
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	u=MURL+p.get('url','/seriale-online')
	page=int(p.get('page',1))
	u+='/'+str(page)
	l=common.solveCFP(u)
	if not l==None:
		try:
			rows=re.compile('<div class=\"item-block clearfix\">.*?<div class=\"row\">.*?(<a href=\".*?<\/a>).*?<\/div>.*?<\/div>',re.DOTALL).findall(l.text.encode('utf-8'))
			common.log(len(rows))
			for r in range(len(rows)):
				img=(re.compile('<img src=\"(.*?)\"',re.DOTALL).findall(rows[r])[0]).replace("thumb","normal")
				title=helpers.PLchar(re.compile('<div class=\"top-belt\">(.*?)<\/div>',re.DOTALL).findall(rows[r])[0])
				desc=helpers.PLchar(re.compile('<div class=\"bottom-belt\">(.*?)<\/div>',re.DOTALL).findall(rows[r])[0])
				link=re.compile('<a href=\"(.*?)\">',re.DOTALL).findall(rows[r])[0]
				li=xbmcgui.ListItem(title+' - [COLOR lime]('+desc+')[/COLOR]',thumbnailImage=img)
				info={'plotoutline':title+" | "+desc,'plot':title+" | "+desc}
				li.setInfo( type="video", infoLabels = info )
				li.setProperty('IsPlayable', 'true')
				li.setProperty('fanart_image', img )
				u=common.sysaddon+"?mode=alltubepl&action=play&url="+urllib.quote_plus(link)
				xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=False)
			xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=alltubepl&action=nowelinki&page="+str(page+1),listitem=xbmcgui.ListItem("[COLOR gold]>>> DALEJ >>>[/COLOR]"),isFolder=True)
		except:
			xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=alltubepl&action=nowelinki",listitem=xbmcgui.ListItem("[COLOR red]-- error --[/COLOR]"),isFolder=True)		
	xbmcplugin.endOfDirectory(common.addon_handle)
## -==================== END ====================- 

def alfabetycznie(p):
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	u=MURL+p.get('url','/seriale-online/')
	l=common.solveCFP(u)
	if not l==None:
		try:
			lista=re.compile('<ul class=\"list-unstyled text-white term-list clearfix\">(.*?)<\/ul>',re.DOTALL).findall(l.text.encode('utf-8'))
			letters=re.compile('<li class=\"letter\">(.*?)<\/li>',re.DOTALL).findall(lista[0])
			for l in range(len(letters)):
				items=re.compile('<li data-letter=\"'+letters[l]+'\">(<a.*?<\/a>)<\/li>',re.DOTALL).findall(lista[0])
				li=xbmcgui.ListItem('[COLOR gold] ------------------------ '+letters[l]+' ------------------------ [/COLOR]')
				li.setProperty('IsPlayable', 'false')
				xbmcplugin.addDirectoryItem(handle=common.addon_handle,url='',listitem=li,isFolder=False)
				for i in range(len(items)):
					try:
						link=re.compile('<a href=\"(.*?)\">',re.DOTALL).findall(items[i])[0]
						title=helpers.PLchar(re.compile('<a href=.*?>(.*?)<\/a>',re.DOTALL).findall(items[i])[0])
						li=xbmcgui.ListItem(title)
						info={}
						li.setInfo( type="video", infoLabels = info )
						li.setProperty('IsPlayable', 'true')
						u=common.sysaddon+"?mode=alltubepl&action=serial&url="+urllib.quote_plus(link)
						xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=True)
					except:
						common.log('litera '+letter[l]+' - '+len(items)+' elementow | error')
		except:
			xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=alltubepl&action=alfabetycznie",listitem=xbmcgui.ListItem("[COLOR red]-- error --[/COLOR]"),isFolder=True)		
	xbmcplugin.endOfDirectory(common.addon_handle)
## -==================== END ====================-

def serial(p):
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	u=p.get('url','')
	l=common.solveCFP(u)
	if not l==None:
		try:
			title2=helpers.PLchar(re.compile('<div class=\"col-sm-9\">.*?<h3 class=\"headline\">(.*?)<\/h3>',re.DOTALL).findall(l.text.encode('utf-8'))[0])
			common.log(title2)
			img=re.compile('<div class=\"col-sm-9\">.*?<img src=\"(.*?)\" alt=\".*?\" class=\"img-responsive\"',re.DOTALL).findall(l.text.encode('utf-8'))[0]
			common.log(img)
			episodes=re.compile('<li class=\"episode\">(.*?)<\/li>',re.DOTALL).findall(l.text.encode('utf-8'))
			common.log(len(episodes))
			lista=[]
			for e in range(len(episodes)):
				try:
					lista.append([helpers.PLchar(re.compile('<a href=.*?>(.*?)<\/a>',re.DOTALL).findall(episodes[e])[0]),
					re.compile('<a href=\"(.*?)\">',re.DOTALL).findall(episodes[e])[0]])
				except:
					common.log('przygotowanie listy epizodow')
			lista.sort()
			
			for e in range(len(lista)):
				try:
					link=lista[e][1]#re.compile('<a href=\"(.*?)\">',re.DOTALL).findall(episodes[e])[0]
					title=lista[e][0]#helpers.PLchar(re.compile('<a href=.*?>(.*?)<\/a>',re.DOTALL).findall(episodes[e])[0])
					li=xbmcgui.ListItem(title,thumbnailImage=img)
					info={}
					li.setInfo( type="video", infoLabels = info )
					li.setProperty('IsPlayable', 'true')
					li.setProperty('fanart_image', img )
					u=common.sysaddon+"?mode=alltubepl&action=play&url="+urllib.quote_plus(link)
					xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=False)
				except:
					common.log('wyswietlenie listy epizodow')
		except:
			xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=alltubepl&action=serial",listitem=xbmcgui.ListItem("[COLOR red]-- error --[/COLOR]"),isFolder=True)	
	xbmcplugin.endOfDirectory(common.addon_handle)
## -==================== END ====================-

def szukaj(p):
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	u="http://alltube.pl/szukaj"
	s={'search':xbmcgui.Dialog().input('Wyszukaj..')}
	l=common.post(u,s)
	if not l==None:
		try:
			r=re.compile('<div class=\"container-fluid\">(.*)</div>',re.DOTALL).findall(l.text.encode('utf-8'))[0]
			r=re.compile('</div>\s<div class=\"container-fluid\">(.*)<div class=\"navbar navbar-fixed-bottom\">',re.DOTALL).findall(r)[0]
			r=re.compile('<div class=\"item-block clearfix\">\n<div class=\"row\">\n<a h(.*?)</p>\n</div>\n</a>',re.DOTALL).findall(r)
			for r1 in range(len(r)):
				item=re.compile('ref=\"(\S*)\".*?<img src=\"(\S*)\".*?<h3>(.*?)</h3>.*\">(.*)',re.DOTALL).findall(r[r1])[0]
				link=item[0]or""
				kind=re.compile('alltube.pl/(.*?)/',re.DOTALL).findall(link)[0]
				img=item[1]or""
				title=item[2]or""
				desc=item[3]or""
				li=xbmcgui.ListItem("[COLOR silver]["+kind+"][/COLOR] "+title,thumbnailImage=img)
				info={}
				li.setInfo( type="video", infoLabels = info )
				li.setProperty('IsPlayable', 'true')
				li.setProperty('fanart_image', img )
				if kind=="film":
					u=common.sysaddon+"?mode=alltubepl&action=play&url="+urllib.quote_plus(link)
					xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=False)
				else:
					u=common.sysaddon+"?mode=alltubepl&action=serial&url="+urllib.quote_plus(link)
					xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=True)
		except:
			xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+"?mode=alltubepl&action=serial",listitem=xbmcgui.ListItem("[COLOR red]-- error --[/COLOR]"),isFolder=True)	
	xbmcplugin.endOfDirectory(common.addon_handle)

def play(p):
	xbmcplugin.setContent(common.addon_handle, 'movie')
	u=p.get('url','')
	l=common.solveCFP(u)
	if not l==None:
		t=re.compile('<table class=\"table\">(.*?)<\/table>',re.DOTALL).findall(l.text.encode('utf-8'))[0]
		rows=re.compile('(<tr.*?)<\/tr>',re.DOTALL).findall(t)
		players=[]
		selList=[]
		for r1 in range(len(rows)):
			tds=re.compile('(<td.*?<\/td>)',re.DOTALL).findall(rows[r1])
			pl=re.compile('> (.*?)<\/td>',re.DOTALL).findall(tds[0])[0]
			link=re.compile('<a href=\"(.*?)\" ',re.DOTALL).findall(tds[1])[0]
			kind=re.compile('<td.*?>(.*?)<\/td>',re.DOTALL).findall(tds[3])[0]
			players.append([pl,link])
			selList.append("%s [COLOR lime]%s[/COLOR] | %s" % (pl,kind,link))
		playfrom=xbmcgui.Dialog().select('Wybor zrodla',selList)
		if playfrom>=0:
			common.log("Wybrano :"+players[playfrom][0]+" - link: "+players[playfrom][1])
			player(players[playfrom])
	else:
		common.info("LINK FEATCHING FAILED","E404", time=5000)
	xbmcplugin.endOfDirectory(common.addon_handle)
## -==================== END ====================-

def player(p):
	pl=p[0]
	link=p[1]
	l=common.solveCFP(link)
	stream_url=''
	if not l==None:
		try:
			iframesrc=re.compile('<iframe src=\"(.*?)\" ',re.DOTALL).findall(l.text.encode('utf-8'))[0]
			common.log(l.text.encode('utf-8'))
			if iframesrc.startswith('//'):
				iframesrc = 'http:' + iframesrc
			try:
				stream_url = urlresolve.resolve(iframesrc)
			except Exception,e:
				stream_url=''
				s = xbmcgui.Dialog().ok('[COLOR red]Problem[/COLOR]','Może inny stream_url będzie działał?','Urlresolver ERROR: [%s]'%str(e))
		except:
			common.log('no iframe found: '+link)
		if stream_url:
			xbmcplugin.setResolvedUrl(common.addon_handle, True, xbmcgui.ListItem(path=stream_url))
		else:
			return False
		xbmcplugin.endOfDirectory(common.addon_handle)
## -==================== END ====================-
	