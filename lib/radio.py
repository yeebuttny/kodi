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
		ManiMenu(p)

_url=common.sysaddon+"?mode=radio"
_handle=common.addon_handle

def MainMenu(p):
	addLink("Radio BonTon","https://streaming.inten.pl:8020/bonton.mp3")
	
	xbmcplugin.endOfDirectory(common.addon_handle)


def playlink(params):
	u=params.get('url','')
	xbmcplugin.setResolvedUrl(common.addon_handle, True, xbmcgui.ListItem(path=u))
	

	
def addLink(title,link):
	l=link
	li=xbmcgui.ListItem(title)
	li.setInfo( type="music", infoLabels = {} )
	li.setProperty('IsPlayable', 'true')
	u=_url+"&action=playlink&url="+urllib.quote_plus(l)
	ok=xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=u,listitem=li,isFolder=False)##change to False
	return ok