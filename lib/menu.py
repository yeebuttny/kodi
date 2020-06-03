# -*- coding: utf-8 -*-
## imports

import re, os, urlparse, requests, time, sys
import xbmcplugin, xbmcgui, xbmcaddon
import urllib, urllib2,  cookielib, ssl, zlib, base64
import string, json
import resolveurl as urlresolve

from resources.lib import helpers
from resources.lib import common
# providers plugs
from resources.lib import alltubepl
from resources.lib import shindenpl
from resources.lib import selfupdate
from resources.lib import mysrc
from resources.lib import radio

def addDirectoryItem(u,li,folder=True):
	return xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+u,listitem=li,isFolder=folder)

def main():
	## MAIN LOOP ########################################################
	params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
	mode = params.get('mode', "menu")

	if params.get("mode"):
		eval(mode).route(params)
	else:
		common.addDirectoryItem("?mode=alltubepl",xbmcgui.ListItem("[COLOR azure]alltube.pl - [filmy | seriale][/COLOR]"),True)
		common.addDirectoryItem("?mode=shindenpl",xbmcgui.ListItem("[COLOR orange]shinden.pl - [anime][/COLOR]"),True)
		common.addDirectoryItem("?mode=mysrc",xbmcgui.ListItem("[COLOR skyblue]mysrc[/COLOR]"),True)
		common.addDirectoryItem("?mode=radio",xbmcgui.ListItem("[COLOR green]Radio[/COLOR]"),True)
		common.addDirectoryItem("?mode=selfupdate",xbmcgui.ListItem("[COLOR yellowgreen]Aktualizacja[/COLOR]"),False)
		xbmcplugin.setContent(common.addon_handle, 'tvshows')
		xbmcplugin.endOfDirectory(common.addon_handle)
	## END MAIN LOOP ####################################################