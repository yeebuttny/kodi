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

_url=common.sysaddon+"?mode=mysrc"
_handle=common.addon_handle

def MainMenu(p):
	xbmcplugin.addDirectoryItem(handle=_handle,url=_url+"&action=linki",listitem=xbmcgui.ListItem("[COLOR orange]Linki[/COLOR]"),isFolder=True)

	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	xbmcplugin.endOfDirectory(common.addon_handle)



def linki(params):

	s=get("https://github.com/yeebuttny/plugs/raw/master/links.txt?raw=true")
	if not s==None:
		rv=s.text.encode('utf-8').replace('\r','').rstrip('\n').split("\n")
		rvd=mdict(rv)
		for item in rvd:
			li=xbmcgui.ListItem(item)
			li.setInfo( type="video", infoLabels = {} )
			li.setProperty('IsPlayable', 'true')
			u=_url+"&action=playlink&url="+urllib.quote_plus(rvd[item])
			xbmcplugin.addDirectoryItem(handle=_handle,url=u,listitem=li,isFolder=False)
	
		
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	xbmcplugin.endOfDirectory(common.addon_handle)

def get(u,d=None,ref=None,h=None):
	if u:
		s=requests.Session()
		res=s.get(u,params=d, headers={'pragma': 'no-cache','cache-control': 'no-cache'},timeout=10,stream=False)
		return res	

def mdict(s):
	d={}
	for i in s:
		ii=i.split(';')
		d[ii[0]]=ii[1]
	return d




def playlink(params):
	u=params.get('url','')
	link=''
	try:
		link=urlresolve.resolve(u)
		common.info(link,'resolved link')
		common.log(link)
	except:
		common.info('cos wiecej w logu','Blad resolveurl')
	if link:
		xbmcplugin.setResolvedUrl(common.addon_handle, True, xbmcgui.ListItem(path=link))
	

	
def addLink(title,link,img,sendto):
	l=link
	li=xbmcgui.ListItem(title,thumbnailImage=MURL+img)
	
	li.setInfo( type="video", infoLabels = {} )
	li.setProperty('IsPlayable', 'true')
	u=common.sysaddon+"?mode="+str(sendto)+"&url="+urllib.quote_plus(l)
	ok=xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=False)##change to False
	return ok