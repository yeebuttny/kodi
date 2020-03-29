# -*- coding: utf-8 -*-
## imports

import re, os, urlparse, requests, time, sys
import xbmcplugin, xbmcgui, xbmcaddon, xbmc
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
		
# link to file with versions
# https://github.com/yeebuttny/plugs/raw/master/versions.txt


MURL							='http://alltube.pl'
aURL=common.sysaddon+"?mode=test"

def MainMenu(p):
	xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=aURL+"&action=update",listitem=xbmcgui.ListItem("[COLOR orange]show directory[/COLOR]"),isFolder=True)
	
	xbmcplugin.setContent(common.addon_handle, 'tvshows')
	xbmcplugin.endOfDirectory(common.addon_handle)
## -==================== END ====================- 
def update(p):
	# read local version file
	lpath = os.path.join(xbmc.translatePath('special://home'), 'addons', 'plugin.video.play', 'resources','lib','versions.txt')
	lvf=open(lpath)
	lv=lvf.read().rstrip('\n').split("\n")
	lvf.close()
	lvd=mdict(lv)

	s=get("https://github.com/yeebuttny/plugs/raw/master/versions.txt?raw=true")
	if not s==None:
		rv=s.text.encode('utf-8').rstrip('\n').split("\n")
		rvd=mdict(rv)
		for plug in rvd:
			if plug in lvd:
				common.log('remote: '+plug+'-'+rvd[plug]+' | local: '+lvd[plug])
				if rvd[plug]>lvd[plug]:
					common.log(plug+' new version found: '+rvd[plug])
					if updatelocal(plug):
						lvd[plug]=rvd[plug]
			else:
				common.log('remote: '+plug+'-'+rvd[plug]+' |')
				common.log(plug+' new version found: '+rvd[plug])
					if updatelocal(plug):
						lvd[plug]=rvd[plug]
		saveVersions(lvd)
	else:
		common.info('nie pobrano danych','getURL error')


def get(u,d=None,ref=None,h=None):
	if u:
		s=requests.Session()
		res=s.get(u,params=d, headers=h,timeout=10,stream=False)
		return res

def saveVersions(d):
	s=''
	for i in d:
		s+=i+' '+d[i]+'\n'
	s.rstrip('\n')
	lpath = os.path.join(xbmc.translatePath('special://home'), 'addons', 'plugin.video.play', 'resources','lib','versions.txt')
	lvf=open(lpath,"w")
	lvf.write(s)
	lvf.close()

def updatelocal(fname):
	rfn="https://github.com/yeebuttny/plugs/raw/master/lib/"+fname+".py?raw=true"
	lfn=os.path.join(xbmc.translatePath('special://home'), 'addons', 'plugin.video.play', 'resources','lib',fname+'.py')
	s=get(rfn)
	if not s==None:
		s=s.text.encode('utf-8')
		lf=open(lfn,"w")
		lf.write(s)
		lf.close()
		common.log(fname+" updated")
		return True
	else:
		common.info('nie pobrano danych','getURL error')
		return False

def mdict(s):
	d={}
	for i in s:
		ii=i.split(' ')
		d[ii[0]]=ii[1]
	return d

def dir(p):
	u=MURL+p.get('url','/')
	dir=xbmcaddon.Addon().getAddonInfo('path')
	path = os.path.join(xbmc.translatePath('special://home'), 'addons', 'plugin.video.play', 'resources','lib')
	out=open(path+os.sep+"test.txt","w")
	out.write(dir)
	out.close()
	xbmcgui.Dialog().textviewer('Opis',dir+'\n'+path)