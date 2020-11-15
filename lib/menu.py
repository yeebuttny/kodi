# -*- coding: utf-8 -*-
## imports

import re, os, urlparse, requests, time, sys
import xbmcplugin, xbmcgui, xbmcaddon
import urllib, urllib2
import string, json
import resolveurl as urlresolve

from resources.lib import common
# providers plugs
from resources.lib import selfupdate
from resources.lib import mysrc


def addDirectoryItem(u,li,folder=True):
	return xbmcplugin.addDirectoryItem(handle=common.addon_handle,url=common.sysaddon+u,listitem=li,isFolder=folder)

def main():
	## MAIN LOOP ########################################################
	params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
	mode = params.get('mode', "menu")

	if params.get("mode"):
		eval(mode).route(params)
	else:
		common.addDirectoryItem("?mode=mysrc",xbmcgui.ListItem("[COLOR skyblue]mysrc[/COLOR]"),True)
		common.addDirectoryItem("?mode=selfupdate",xbmcgui.ListItem("[COLOR yellowgreen]Aktualizacja[/COLOR]"),False)
		xbmcplugin.setContent(common.addon_handle, 'tvshows')
		xbmcplugin.endOfDirectory(common.addon_handle)
	## END MAIN LOOP ####################################################