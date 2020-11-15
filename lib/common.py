# -*- coding: utf-8 -*-
## imports
import xbmcaddon,xbmcplugin, xbmcgui,xbmc,string
import re, os, urlparse, time, sys



##globals ## --------------------------------------------------------------------------
sysaddon                = sys.argv[0]
addon_handle            = int(sys.argv[1])
args                    = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))##urlparse.parse_qs(sys.argv[2][1:])
addon                = xbmcaddon.Addon()
addonId             = addon.getAddonInfo('id')
addonName           = addon.getAddonInfo('name')
## --------------------------------------------------------------------------
def addDirectoryItem(u,li,folder=True):
	return xbmcplugin.addDirectoryItem(handle=addon_handle,url=sysaddon+u,listitem=li,isFolder=folder)
## --------------------------------------------------------------------------

## loginfo ## ---------------------------------------------------------------
loginfo=addon.getSetting('loginfo')
## log ## -------------------------------------------------------------------
def log(msg):
	try:
		msg=str(msg)
	except:
		msg='can\'t convert to string'
	if loginfo:
		xbmc.log(addonName+" - "+msg,level=xbmc.LOGNOTICE)
## info ## ------------------------------------------------------------------
def info(msg=" ",title="Info",  time=5000):
	xbmc.executebuiltin("XBMC.Notification(%s,%s,%s)"%(title,msg,str(time)))
## --------------------------------------------------------------------------

## --------------------------------------------------------------------------
def Opcje():
	addon.openSettings()
## --------------------------------------------------------------------------