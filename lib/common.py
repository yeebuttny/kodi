# -*- coding: utf-8 -*-
## imports
import xbmcaddon,xbmcplugin, xbmcgui,xbmc,string
import re, os, urlparse, requests, time, sys

import urllib, urllib2,  cookielib, ssl, zlib, base64
import json
import resolveurl as urlresolve
from resources.lib import helpers

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
def get(u,d=None,ref=None,h=None):
	if u:
		log('geturl - '+u)
		h=h or helpers.headers(args.get("mode"))
		h['referer']=ref or u
		s=requests.Session()
		res=s.get(u,params=d, headers=h,timeout=10,stream=False)
		log('status:' +str(res.status_code))
		log('headers: ')
		log(res.headers)
		log('end geturl')
		return res
## --------------------------------------------------------------------------
def post(u,d=None,ref=None,h=None):
	if u:
		log('posturl - '+u)
		h=h or helpers.headers(args.get("mode"))
		h['referer']=ref or u
		s=requests.Session()
		res=s.post(u,data=d, headers=h,timeout=10)
		log('status:' +str(res.status_code))
		log('headers: ')
		log(res.headers)
		log(res.text)
		log('end posturl')
		return res
## --------------------------------------------------------------------------
def isCFP(r):
	# if 503 CF protection 
	if  r==None:
		log('CFP check failed - no data to check')
		return None
	return r.status_code==503 and r.headers.get('server','')=='cloudflare'
## --------------------------------------------------------------------------
def solveCFP(l,h=None):
	log('CFP')
	tries=1
	res=None
	while tries<4:
		log('CFP tries: '+str(tries))
		r=get(l,h=h)
		if not isCFP(r):
			log('no CFP')
			return r
		if r==None:
			log('no link opened')
			break
		log(r.text.encode('utf-8'))
		form=re.compile('<form id=\"challenge-form\"(.*?)<\/form>',re.DOTALL).findall(r.text.encode('utf-8'))[0]
		formAction=re.compile('action=\"(.*?)\"',re.DOTALL).findall(form)[0]
		formvc=re.compile('<input type=\"hidden\" name=\"jschl_vc\" value=\"(.*?)\"').findall(form)[0]
		formPass=re.compile('<input type=\"hidden\" name=\"pass\" value=\"(.*?)\"').findall(form)[0]
		equation=re.compile('\[CDATA\[(.*?)\/\/\]\]>',re.DOTALL).findall(r.text)[0]
		bv=re.compile('\s*?var.*?:(.*?)};').findall(equation)[0]
		bv=bv.replace('!+[]', '1').replace('!![]','1').replace('[]', '0').replace('(','str(')
		bv=bv.split('/')
		bv=float(eval(bv[0].lstrip('+')))/float(eval(bv[1].lstrip('+')))
		eqs=re.compile('\s*?;(.*?);a\.value').findall(equation)[0]
		eqs=eqs.replace('!+[]', '1').replace('!![]','1').replace('[]', '0')
		eqs=eqs.split(';')
		for i in range(len(eqs)):
			eqs[i]=re.compile('(\w*?\.\w*?)([-+*/]?\=)(.*)').findall(eqs[i])[0]
			ee=eqs[i][2].replace('(','str(').split('/')
			aa=float(eval(ee[0].lstrip('+')))/float(eval(ee[1].lstrip('+')))
			if eqs[i][1]=='-=':
				bv-=aa
			elif eqs[i][1]=='+=':
				bv+=aa
			elif eqs[i][1]=='*=':
				bv*=aa
			elif eqs[i][1]=='/=':
				bv/=aa
			log(bv)
		# 'seriale.co' len = 10 
		log(bv)
		protocol=l.split("//")[0]
		domain=l.split("//")[1].split("/")[0]
		bv=round(bv,10)+len(domain)
		
		formData={'jschl_vc':formvc,'pass':formPass,'jschl-answer':bv}
		newURL=protocol+"//"+domain+"/"
		l2=newURL+formAction+'?jschl_vc=%s&pass=%s&jschl_answer=%s'%(formvc,formPass,bv)
		time.sleep(5)
		res=get(l2,ref=l,h=h)
		if res.status_code==200:
			log('CFP solved at '+str(tries)+' time')
			tries=4
		else:
			if tries==3:
				res=None
				log('CFP failed finding solution')
			tries+=1
			log(r.text)
	return res
## --------------------------------------------------------------------------
def Opcje():
	addon.openSettings()
## --------------------------------------------------------------------------