#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.config import Config

#Config.set('graphics', 'width', 1000)
#Config.set('graphics', 'height', 1000)
#Config.set('graphics', 'fullscreen', 'fake')
Config.set('kivy', 'log_level', 'warning')

from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.base import EventLoop
from kivy.loader import Loader
from kivy.clock import Clock
from kivy.loader import Loader
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest
from kivy.graphics.instructions import Canvas
from kivy.graphics import Color, Rectangle
from kivy.cache import Cache
from kivy.animation import Animation
from kivy.metrics import sp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.graphics import *
from kivy.graphics.texture import Texture
#from effectwidget.EffectBase import HorizontalBlurEffect, VerticalBlurEffect

#from kivy.clock import Clock
#Clock.max_iteration = 50

import pickle
import os
import subprocess
#import dogtail.rawinput
import re
import operator
import copy
import tkSimpleDialog
import tkMessageBox
import Tkinter
import sys
import time
#from urllib import FancyURLopener
import urllib2
import urllib
import simplejson
import random
import io
import base64
import tempfile
import imghdr
import shutil
import threading
from UserDict import UserDict
from functools import partial
from collections import OrderedDict, Counter
from urllib2 import urlopen
from tkFileDialog import askopenfilename
#import fcntl

import module_locator

try:
	from send2trash import send2trash
except ImportError:
	send2trash = None

#TODO
# make it work on other computers
# don't have errors
# settings

def timeme(method):
	def wrapper(*args, **kw):
		startTime = int(round(time.time() * 1000))
		result = method(*args, **kw)
		endTime = int(round(time.time() * 1000))

		print(endTime - startTime,'ms')
		return result

	return wrapper

root = Tkinter.Tk()
root.withdraw()

buttoncolor=(0,0,0,0)
selectedcolor=(0,0,1,0.3)
errorcolor=(1,0,0,0.4)
textcolor=(1,1,1,1)
BACKOPACITY = 0.2

SORT_ALPHABETICAL = "Alpha"
SORT_WATCHED = "Watched"
SORT_CREATED = "Created"
SORTING = [SORT_ALPHABETICAL, SORT_WATCHED, SORT_CREATED]

useoutlines = False

class dictwithdefault(UserDict):
	def __init__(self, default=None):
		UserDict.__init__(self)
#		self.value = {}
		self.default = default
#	def __set__(self, instance, value):
#		self.value = value
#	def __iter__(self):
#		return self.value.__iter__()

	def __getitem__(self, key):
		if key in self.keys():
			return UserDict.__getitem__(self, key)
		else:
			if hasattr(self.default, "__call__"):
				self.default(key)
				if key in self.keys():
					return UserDict.__getitem__(self, key)
				else:
					return None
			else:
				return self.default

#	def __setitem__(self, key, value):
#		self.value.__setitem__(key, value)

class savedata(object):
	def makevars(self):
		v = {"infolder":tvfolder,
			"showwatched":True,
			"watched":dictwithdefault(),
			"names":dictwithdefault(),
			"images":dictwithdefault(),
			"scrollstate":dictwithdefault(),
			"lastwatched":dictwithdefault(),
			"sort":SORT_ALPHABETICAL}
		
		for var in v:
			value = v[var]
			if not var in self.__dict__:
				print "MAKE", var
				setattr(self, var, value)
			value = getattr(self, var)
		
		self.watched.default = False
		self.names.default = renamefiles
		self.images.default = defaultimageloc
		self.scrollstate.default = [0,0,None]
		self.lastwatched.default = dictwithdefault(time.gmtime(0))
		
#			print var, value
			
#			if isinstance(value, dictwithdefault):
#				setattr(self, var, value.value)
#		saveclassinst.dosave()
#			if isinstance(value, dict):
#				print var, value
#				for key in value:
#					val = value[key]
#					v[var][key] = val
#				setattr(self, var, v[var])
#			saveclassinst.dosave()

#		for showname in self.images.keys():
#			if self.images[showname] == "default.jpg":
#				del self.images[showname]
	
	def setimage(self, tvpath, imgpath):
		if tvpath in self.images:
			currentimage = self.images[tvpath]
			if os.path.exists(currentimage) and os.path.normpath(imgpath) != os.path.normpath(currentimage):
				os.remove(currentimage)
		
		self.images[tvpath] = imgpath
	
def downloadtempimage(url):
	"""
	temp = tempfile.mktemp()
	downloadimage(url, temp)
	imgtype = imghdr.what(temp)
	ending = ""
	if imgtype != None:
		ending = "." +imgtype
	while True:
		filename = str(random.randrange(0, 10000))
		imagepath = os.path.join(imagesfolder, filename + ending)
		if not os.path.exists(imagepath):
			 break
	
	shutil.move(temp, imagepath)
	
	print "saved to", imagepath
	
	self["images"][loc] = imagepath
	"""
	temp = tempfile.mktemp()
	print url, temp
	downloadimage(url, temp)
	ending = imghdr.what(temp)
	if ending == None:
		urlending = url.rsplit(".", 1)[1]
		if len(urlending) == 3:
			ending = urlending
	if ending != None:
		newtemp = temp + "." + ending
		shutil.move(temp, newtemp)
		temp = newtemp
	return temp

def renamefiles(loc):
	namedir(os.path.dirname(loc))

class saveclass():
	def __init__(self):
		global saveclassinst
		saveclassinst = self
		self.savestatevar = savedata()#{"infolder":self.tvfolder, "showwatched":True, "watched":{}, "names":{}, "images":{}, "scrollstate":{}}
		
		self.allfolders = [tvfolder, kmcfolder, imagesfolder]
		self.allfiles = [savefile]
		
		self.makefolders()
		self.loadall()
		
	def dosave(self):
		self.save(self.savestatevar, savefile)
		
	def makefolders(self):
		for folder in self.allfolders:
			if not os.path.exists(folder):
				os.makedirs(folder)
	
	def loadall(self):
		self.savestatevar = self.load(savefile, self.savestatevar)
		self.savestatevar.makevars()
#		for index in newsavestatevar:
#			self.savestatevar[index] = newsavestatevar[index]
#		self.watched = self.load(self.watchedfile, self.watched)
#		self.names = self.load(self.namesfile, self.names)
#		self.images = self.load(self.imagesfile, self.images)
	
	"""
	def __iter__(self):
		return self.savestatevar.__iter__()
		
	def __getitem__(self, key):
		return self.savestatevar.__getitem__(key)
	"""
	
	def load(self, loc, defaultdata):
		if os.path.exists(loc):
			f = open(loc)
			data = pickle.load(f)
		else:
			f = open(loc, "w")
			pickle.dump(defaultdata, f)
			data = defaultdata
		f.close()
		
		return data
	
	"""
	def savestate(self, name, value):
		self.savestatevar[name] = value
		
	def dosave(self):
		self.save(self.savestatevar, self.savefile)
		
	def loadstate(self, name):
		if name in self.savestatevar:
			return self.savestatevar[name]
	"""
	
#	def getwatched(self, loc):
#		if loc in self["watched"]:
#			return self["watched"][loc]
#		else:
#			self.setwatched(loc, False)
#			return False
		
	"""
	def nextimage(self, loc):
		imagepath, imageurls, imagenum, page = self["images"][loc]
		if imagepath != None:
			os.remove(os.path.join(self.imagesfolder, imagepath))
		imagenum += 1
		if imagenum >= len(imageurls):
			page += 1
			imageurls = findimage(loc, page)
			imagenum = 0
		while True:
			fileending = imageurls[imagenum].rsplit(".", 1)[1][:5]
			filename = str(random.randrange(0, 10000)) + "." + fileending
			filename = filename.replace("/", "")
			imagepath = os.path.join(save.imagesfolder, filename)
			if not os.path.exists(imagepath):
				break
		downloadimage(imageurls[imagenum], imagepath)
		self["images"][loc] = [imagepath, imageurls, imagenum, page]
#		self.save(self.images, self.imagesfile)u
		self["images"][loc] = [imagepath, imageurls]
		
	def resetimageindex(self, loc):
#		images = findimage(loc)
#		self["images"][loc] = [None, images, -1, 0]
#		self.nextimage(loc)

		pickimage(loc)

#		imagepath = images[0]
	"""
	
	"""
	def getimage(self, loc):
		if not (loc in self["images"]) or not os.path.exists(self["images"][loc][0]):
			return self.defaultimageloc#self["images"][loc] = [self.defaultimageloc]
#			self.resetimageindex(loc)
		return self["images"][loc][0]
		
	def getname(self, loc):
		if loc in self["names"] and self["names"][loc] != None:
			return self["names"][loc]
		else:
			namedir(os.path.dirname(loc))
#			self.setwatched(loc, False)
			return self.getname(loc)
		
	def setwatched(self, loc, watched):
		self["watched"][loc] = watched
#		self.save(self.watched, self.watchedfile)
#		self.savestatevar()
	
	def setname(self, loc, name):
		self["names"][loc] = name
	"""
	
	def save(self, data, loc):
		f = open(loc, "w")
		pickle.dump(data, f)
		f.close()

class numpos(object):
	def __init__(self, numindex, strindex, num):
		self.numindex, self.strindex, self.num = numindex, strindex, num
	
	def __eq__(self, obj):
		if isinstance(obj, numpos):
			if self.numindex == obj.numindex and self.strindex == obj.strindex and self.num == obj.num:
				return True
		return False
	
	def __str__(self):
		return str(self.strindex)
		
	def __repr__(self):
		return str(self.strindex) + ":" + str(self.num)
		
	def __hash__(self):
		return int(self.numindex) + int(self.strindex)*100 + float(self.num)*10000

def getnumbers(string):
	num = ""
	nums = []
	for index, char in enumerate(string):
		if char.isdigit() or char == ".":
			num += char
		else:
			if num.endswith("."):
				num = num[:-1]
			if num.startswith("."):
				num = num[1:]
			if num != "" and num != ".":
				print num
				nums.append(numpos(len(nums), index - len(num), num))
				num = ""
	return nums

def namedir(folder, override=False): 
	print "naming dir"
	
	global torrenteps
	torrenteps = []
	
	l = os.listdir(folder)
	l = [os.path.join(folder, path) for path in l]
	l.sort()
	
	files = [os.path.basename(f).replace(",", ".") for f in l]
	for f in files:
		print f
	print "###"
#	filenumpos = [[] for f in files]
	
	filenums = {}
	
	for f in files:
		filenums[f] = getnumbers(f)
		print f, filenums[f]
	
	allfilenums = [fnum for f in files for fnum in filenums[f]]
	print allfilenums
	filenumcounter={}
	for fnum in allfilenums:
		if fnum in filenumcounter:
			filenumcounter[fnum] += 1
		else:
			filenumcounter[fnum] = 1
	
	print filenumcounter
	
	toremove = []
	
	indexes = [fnum.strindex for f in files for fnum in filenums[f]]
	removeindexes = set(indexes)
	indexnums = {}
	for f in files:
		for fnum in filenums[f]:
			if fnum.strindex in indexnums:
				if indexnums[fnum.strindex] != fnum.num:
					if fnum.strindex in removeindexes:
						removeindexes.remove(fnum.strindex)
			else:
				indexnums[fnum.strindex] = fnum.num
	
#	print "REMOVEINDEX", removeindexes
	toremove += removeindexes
#	for f in files:
#		for fnum in filenums[f]:
#			if fnum.strindex in removeindexes:
#				toremove.append(fnum)
	
	for fnum in filenumcounter:
		times = filenumcounter[fnum]
		if times >= len(files)-1:
			toremove.append(fnum.strindex)
		elif float(fnum.num) > 100:
			toremove.append(fnum.strindex)
	
#	for f in files:
#		for filenumpos in filenums[f]:
#			for otherf in files:
#				if f != otherf:
#					for otherfilenumpos in filenums[otherf]:
#						if filenumpos == otherfilenumpos:
#							strindex = filenumpos.strindex
#							if not strindex in toremove:
#								toremove.append(strindex)
	for f in files:
		filenums[f] = [fnum for fnum in filenums[f] if not fnum.strindex in toremove]
		print f, filenums[f]
	
	filenumsstrindex = [fnum.strindex for f in files for fnum in filenums[f]]
	epnumpos = None
	if len(filenumsstrindex) != 0:
		filenumsstrindex = Counter(filenumsstrindex)
		commonlist = filenumsstrindex.most_common()
#		mostcommoncount = commonlist[0][1]
#		commoncount = []
#		for commonepnum, count in commonlist:
#			if count == mostcommoncount:
#				commoncount.append(commonepnum)
#		commoncount.sort()
		epnumpos = commonlist[0][0]
		print epnumpos
	
#	for index, f in enumerate(files):
#		numstart = None
#		numlen = 0
#		basename = f#os.path.basename(f)
#		for loc in range(len(basename)):
#			num = getnumber(basename, loc)
#			if num != "" and num != ".":
#				filenumpos[index].append([loc])
	
#		for charpos, char in enumerate(os.path.basename(f)):
#			if char.isdigit():
#				if numstart == None:
#					numstart = charpos
#				numlen += 1
#			else:
#				if numstart != None:
#					filenumpos[index].append([numstart])#, numlen])
#					numstart = None
#					numlen = 0
	
	names = copy.copy(l)
	eps = [None for f in l]
	
#	numposs = []
#	for filenums in filenumpos:
#		numposs += filenums
	#remove all same nums
#	toremove = []
#	for filenums in numposs:
#		numpos = filenums[0]
#		if not loc in toremove:
#			locnum = None
#			removeloc = False
#			for index, f in enumerate(files):
#				basename = f#os.path.basename(f)
#				print basename[loc:]
#				newlocnum = getnumber(basename, loc)
#				if locnum == newlocnum:
#					removeloc = True
#				locnum = newlocnum
#			if removeloc:
#				toremove.append(loc)
#				print "remove", locnum
#	numposs = [filenums for filenums in numposs if not filenums in toremove]
	
#	fnumstrindexes = [fnum.strindex for fnum in filenums]
#	numpossamts = OrderedDict()
#	for fnumstrindex in fnumstrindexes:
#		numpossamts.append([numpos, numposs.count(numpos)])
#		if not fnumstrindex in numpossamts:
#			numpossamts[fnum.strindex] = fnumstrindexes.count(fnumstrindex)
#	if numpossamts != []:
#		epnums = max(numpossamts.keys(), key = lambda x : numpossamts[x])
#		numpossamts = [numpos for numpos in numpossamts if numpossamts[numpos]==numpossamts[epnums]]
#		epnums = min(numpossamts.keys(), key = lambda x : x[0][0])
#		for epnum in epnums:
#			allsame = True
#			oldnumber = None
#			for index, name in enumerate(names):
#				changedname = files[index]
#				print changedname
#				number = changedname[epnum[0]:epnum[0]+2]
#				if oldnumber != None and oldnumber == number:
#					allsame = False
#				oldnumber = number
#			if allsame:
#				epnums.remove(epnum)
		
		
#		epnumpos = epnums[0]
#	else:
#		epnumpos = None
	
	for index, name in enumerate(names):
		path = l[index]
		changedname = files[index]
		newname = os.path.basename(path)
		if os.path.isdir(path):
			newname = changename(newname, takeoutnumbers=True, dosearch=dogooglesearch, title=True)
		else:
			if epnumpos != None:
				numpos = epnumpos#[0]
#				numbers = getnumbers(changedname)#changedname[epnumpos[0]:epnumpos[0]+2]#+epnumpos[1]]
				numbers = filenums[changedname]
				number = [num for num in numbers if num.strindex == numpos]
				if number != []:
					number = number[0].num
					if "." in number:
						number = float(number)
					else:
						number = int(number)
#				number = number.strip()
#				number = filter(lambda x : x.isdigit(), number)
#				if number.isdigit() and number != "":
#					number = int(number)
#					afternumber = changedname[epnumpos[0]:epnumpos[0]+4]
#					if afternumber.endswith(".5"):
#						number = number + .5
					eps[index] = number#newname = "Episode " + number + " " + newname
		names[index] = newname
	
	numbereps = sum([ep != None for ep in eps])
	if numbereps <= 2:
		eps = [None for ep in eps]
	
	for index, path in enumerate(l):
		if not path in save.names or override:
			name = names[index]
			epnumber = eps[index]
			save.names[path] = [name, epnumber]


homefolder = os.path.expanduser("~")#os.environ['HOME']
tvfolder = os.path.join(homefolder, "Videos/tv")
kmcfolder = os.path.join(homefolder, ".kmc")
imagesfolder = os.path.join(kmcfolder, "images")
savefile = os.path.join(kmcfolder, "save")
deletedfile = os.path.join(homefolder, "Videos/deleted")

defaultimageloc = os.path.join(kmcfolder, "default.jpg")
if not os.path.exists(defaultimageloc):
	defaultimageloc = os.path.join(module_locator.module_path(), "default.jpg")

saveclassinst = saveclass()
save = saveclassinst.savestatevar

checkmark = u"\u2713"

dogooglesearch = False
whitespaces = ["_"]
removestuff = ["DVD", "Ep", "Episodes", "+ OVA", "OVA"]
removestuffregex = ["[\[\(][^\]^\)]*[\]\)]", "v[0-9]"]
numberregex = "[0-9]+\s*[0-9]+"
ignorefiles = ["/"]
stripchars = [" ", "-"]

ignore = ["xbmc", "lost+found"]

subfolders = []

opedcounter = 1
othercounter = 1

#class MyOpener(FancyURLopener): 
#	version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

class googleimage():
	def __init__(self, url, previewurl, size, page):
		self.url, self.previewurl, self.size, self.page = url, previewurl, size, page

def imagesearch(searchTerm, page):
	searchTerm = searchTerm.replace(' ','%20')
	
#	myopener = MyOpener()
	count= 0
	
	images = []
	
	# Notice that the start changes for each iteration in order to request a new set of images for each loop
	url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(page*4)+'&userip=MyIP' + "&imgsz=huge")
	request = urllib2.Request(url, None, {'Referer': 'testing'})
	response = urllib2.urlopen(request)
	
	# Get results using JSON
	results = simplejson.load(response)
	data = results['responseData']
	dataInfo = data['results']
	
	# Iterate for each result and get unescaped url
	for myUrl in dataInfo:
		count = count + 1
		previewurl = myUrl['tbUrl'].replace("\u003d", "=")
#		previewimages.append(previewurl)
		result = myUrl['unescapedUrl']
		size = [int(myUrl['width']), int(myUrl['height'])]
		images.append(googleimage(result, previewurl, size, page))
#		myopener.retrieve(myUrl['unescapedUrl'],str(count)+'.jpg')

	# Sleep for one second to prevent IP blocking from Google
#	time.sleep(1)
	
	print len(images)
	
	return images

def findimage(loc, page=0):
	searchterm = save.names[loc][0] + " wallpaper"
	images = imagesearch(searchterm, page)
	return images
	
def downloadimage(url, path):
#	filepath = os.path.join(save.imagesfolder, path)#os.path.basename(loc)) + "." + images[0].rsplit(".", 1)[1]
	print "downloading", url
	urllib.urlretrieve(url, path)
	print "done downloading"

def stringbetween(string, s, e):
	start, middleend = string.split(s, 1)
	middle, end = middleend.split(e, 1)
	return middle

def searchgoogle(string):
	g = pygoogle(string)
	g.pages = 1
	try:
		newname = g.search().keys()[0]
		if " - " in newname:
			newname = newname.split(" - ")[0]
		if " (" in newname:
			newname = newname.split(" (")[0]
		return newname
	except IndexError:
		return string

def removeregex(string, regex):
		matches = re.findall(regex, string)
		for match in matches:
			string = string.replace(match, "")
		return string

def changename(basename, toremove=None, number=False, takeoutnumbers=False, dosearch=False, title=False):
	global opedcounter, torrenteps, othercounter
	newbasename = basename
	for whitespace in whitespaces:
		newbasename = newbasename.replace(whitespace, " ")
	for thing in removestuff:
		newbasename = newbasename.replace(thing, "")
	for thing in removestuffregex:
		newbasename = removeregex(newbasename, thing)
	if takeoutnumbers:
		newbasename = removeregex(newbasename, numberregex)
	if toremove != None:
		newbasename = newbasename.replace(toremove, "")
	while True:
		if newbasename[0] in stripchars:
			newbasename = newbasename[1:]
		else:
			break
	while True:
		if newbasename[-1] in stripchars:
			newbasename = newbasename[:-1]
		else:
			break
	if title:
		if not newbasename.endswith("."):
			newbasename = newbasename.replace(".", " ")
	if "." in newbasename:
		newbasenamebase, newbasenameending = newbasename.rsplit(".", 1)
		newbasenamebase = newbasenamebase.strip()
		"""
		if number:
			for ignore in ignorefiles:
				if ignore in newbasenamebase:
					return ""
			if "OP" in newbasenamebase.upper() or "ED" in newbasenamebase.upper():
				newbasenamebase = toremove + "_S00E" + str(100 + opedcounter)
				opedcounter += 1
			else:
				if newbasenamebase.isdigit():
					thenumber = int(newbasenamebase)
					torrenteps.append(thenumber)
					thenumber = "Episode " + str(thenumber)
				else:
					thenumber = re.search(r'\d+', newbasenamebase)
					if thenumber == None:
						return basename
					else:
						thenumber = thenumber.group()
						thenumber = int(thenumber)
						if thenumber in torrenteps:
							thenumber = "_S00E" + str(0 + othercounter)
							print "special: " + str(othercounter)
							othercounter += 1
						else:
							torrenteps.append(thenumber)
							thenumber = "Episode " + str(thenumber)
				newbasenamebase = thenumber
		"""
		if newbasenameending.endswith(".part"):
			newbasenameending = newbasenameending.replace(".part", "")
		newbasename = newbasenamebase + "." + newbasenameending
	if dosearch:
		newbasename = searchgoogle(newbasename)
	return newbasename

class ShadowLabel(Label):
	tint = ListProperty([0, 0, 0, 0.1])

class ShadowButton(Button):
	tint = ListProperty([0, 0, 0, 0.1])

"""	def __init__(self, *args, **kwargs):
		Label.__init__(self, *args, **kwargs)
		
		with self.canvas.before:
			Color(self.tint)
			
			Rectangle(pos = self.pos, #[int(self.center_x - self.texture_size[0] / 2.) + self.decal[0],\
				size=self.texture_size)#int(self.center_y - self.texture_size[1] / 2.) + self.decal[1]], size=self.texture_size)
#			x.texture = self.texture
			Color([1,1,1,1])
"""


rectanglestring = """
		Rectangle:
			pos:
				int(self.center_x - self.texture_size[0] / 2.) + SHIFTX,\
				int(self.center_y - self.texture_size[1] / 2.) + SHIFTY
			size: root.texture_size
			texture: root.texture
"""

shadowlabelstring = """
<ShadowLabel>:
	canvas.before:
		Color:
			rgba: root.tint
		
RECTANGLES
		Color:
			rgba: 1, 1, 1, 1 
"""

fullrectanglestring = ""

rad = 8
circlepoints = []
for x in range(-rad, rad+1):
	for y in range(-rad, rad+1):
		if (x**2 + y**2 < rad):
			circlepoints.append([x,y])

toremove = []
for point in circlepoints:
	x, y = point
	if [x+1, y] in circlepoints and [x, y+1] in circlepoints and [x-1, y] in circlepoints and [x, y-1] in circlepoints:
		toremove.append(circlepoints)

for SHIFTX, SHIFTY in circlepoints:
	if not [SHIFTX, SHIFTY] in toremove:
		newrectanglestring = rectanglestring.replace("SHIFTX", str(SHIFTX)).replace("SHIFTY", str(SHIFTY))
		fullrectanglestring += newrectanglestring

shadowlabelstring = shadowlabelstring.replace("RECTANGLES", fullrectanglestring)

if useoutlines:
	Builder.load_string(shadowlabelstring)
	Builder.load_string(shadowlabelstring.replace("ShadowLabel", "ShadowButton"))

	Button = ShadowButton
	Label = ShadowLabel

#global Button

#Button = type('Button', (ShadowLabel,), dict(Button.__dict__)) 



class Gradient(object):
	@staticmethod
	def horizontal(rgba_left, rgba_right):
		texture = Texture.create(size=(2, 1), colorfmt="rgba")
		pixels =rgba_left + rgba_right
		pixels = [chr(int(v * 255)) for v in pixels]
		buf = ''.join(pixels)
		texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
		return texture

	@staticmethod
	def vertical(rgba_top, rgba_bottom):
		texture = Texture.create(size=(1, 2), colorfmt="rgba")
		pixels = rgba_bottom + rgba_top
		pixels = [chr(int(v * 255)) for v in pixels]
		buf = ''.join(pixels)
		texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
		return texture

class GradientWidget(Widget):
	def __init__(self, *args, **kwargs):
		colors = kwargs["colors"]
		del kwargs["colors"]
		
		Widget.__init__(self, *args, **kwargs)
		
		with self.canvas.before:
			self.rect = Rectangle(pos=self.pos, size=self.size)
			self.rect.texture = Gradient.horizontal(*colors)
		
		self.bind(pos=self.redraw)
		self.bind(size=self.redraw)
		
	def redraw(self, *args):
		self.rect.pos = self.pos
		self.rect.size = self.size

class AFLabel(Label):
	# AutoFont Label.
	#   resize the fontsize to make it fit best in allowed space

	def __init__(self, **kwargs):
		self.bind(height = self._resize)
		super(AFLabel, self).__init__(**kwargs)

	def _resize(self,instance, height):    
		# start with simple case of calculating scalefactor from height
		self.font_size = '%dsp' % sp(height)

buttonactivatedtexture = Gradient.horizontal(selectedcolor, (0, 0, 1, 0))
buttoninvisibletexture = Gradient.horizontal((0,0,0,0), (0, 0, 0, 0))
buttonnormaltexture = Gradient.horizontal(buttoncolor, (0, 0, 0, 0))
buttonerrortexture = Gradient.horizontal(errorcolor, (0, 0, 0, 0))
rightbuttonnormaltexture = Gradient.horizontal((0,0,0,0), buttoncolor)

class abutton(AnchorLayout):
	def __init__(self, path, app, name=None):
		AnchorLayout.__init__(self)#, size_hint=(.9, None), height='60dp')
		
		with self.canvas.before:
			self.rect = Rectangle(pos=self.pos, size=self.size)
			self.rect.texture = buttonactivatedtexture
			
#		self.button = Button(size_hint=(1,1), background_color=(0,0,0,0))
#		self.add_widget(self.button)
		
		self.path = path
		self.app = app
		self.watched = False
		
		self.showfolder = self.path
		while True:
			if os.path.samefile(os.path.normpath(os.path.join(self.showfolder, "..")), tvfolder):
				break
			self.showfolder = os.path.normpath(os.path.join(self.showfolder, ".."))
		
		if name == None:
			name = os.path.basename(self.path)
		self.name = name
		
		self.font_size='40sp'
		self.progress = None
		self.selected = False
		
		self.epnum = None
		
		self.missingprevepisode = False
		
		self.unselect()
		
		self.layout = BoxLayout(size_hint=(1,1))
		self.add_widget(self.layout)
		
		self.checklabel = Label(halign="right", size_hint=[None,1], font_name='/usr/share/pyshared/kivy/data/fonts/DejaVuSans.ttf', color=textcolor)
		self.checklabel.text = ""
		self.checklabel.font_size = '40sp'
		self.layout.add_widget(self.checklabel)
		
		self.labellayout = ScrollView()
		self.labellayout.bar_color = [1,1,1,0]
		self.labellayout.do_scroll_y = False
		
		self.labellayout2 = AnchorLayout(anchor_x="left", anchor_y="center")
		self.labellayout.add_widget(self.labellayout2)
		
		self.label = Label(halign="left", size_hint=[None, None], font_name='/usr/share/pyshared/kivy/data/fonts/DejaVuSans.ttf', color=textcolor)
#		self.label.text_size = (2000, None)
#		self.label.size = self.label.text_size
#		self.label.size[1] = self.label.texture_size[1]#self.label.text_size
		self.label.bind(texture_size=self.label.setter('size'))
		self.labellayout2.add_widget(self.label)
#		self.label.bind(texture_size=self.updatelabelsize)
		
		self.label.font_size = '30sp'
		
		self.labellayout.scroll_x = 0
		self.layout.add_widget(self.labellayout)
		
		self.downloadlabel = Label(text="", halign="right", size_hint=[None, 1], color=textcolor)
		self.downloadlabel.font_size='20sp'
		self.layout.add_widget(self.downloadlabel)
		
		self.actualbutton = Button(background_color=[0,0,0,0], text="", pos_hint=[0.5,0.5], size_hint=[1,1])
		self.add_widget(self.actualbutton)
		self.actualbutton.bind(on_press=self.buttonpressed)
		
		self.updatename()
		self.updatechecked()
		
		self.bind(pos=self.redraw)
		self.bind(size=self.redraw)
		
		self.bind(on_press=self.pressed)
		

		
	def redraw(self, *args):
		self.rect.pos = self.pos
		self.rect.size = self.size
	"""
	def updatelabelsize(self, *args):
		self.label.size = self.label.texture_size#max(self.label.texture_size[0], self.labellayout.size[0])
#		pass
		
#		self.label.size[1] = self.labellayout.size[1]h
	"""
		
	def setprogress(self, progress):
		self.progress = float(progress)
		self.downloadlabel.text = str(self.progress) + "%"
		if not self.selected:
			self.unselect()
		
	def updatename(self):
		namedisplay = app.namedisplay
		if namedisplay == "name":
			self.label.text = self.name
		elif namedisplay == "file":
			self.label.text = os.path.basename(self.path)
		
	def pressed(self, *args):
		if os.path.isdir(self.path):
			self.app.enterfolder(self.path)
		else:
#			dogtail.rawinput.click(0,0)
			save.watched[self.path] = True
			self.check()
			save.lastwatched[self.showfolder] = time.gmtime()
			self.app.select_down()
#			optirunflag = ""
#			if optirun:
#				optirunflag = "optirun "
#			if vlc:
#				subprocess.Popen(optirunflag + "vlc --fullscreen \"" + self.path + "\"", shell=True)#"vlc \"" + self.path + "\" --play-and-exit --video-on-top --fullscreen", shell=True)
#			else:
			path = self.path
#			path = path.replace("`", "\\`")
			subprocess.Popen(["smplayer", "-fullscreen", "-close-at-end", path])#, shell=True)#"vlc \"" + self.path + "\" --play-and-exit --video-on-top --fullscreen", shell=True)
	
	def redrawsize(self, *args):
		pass
#		Button.redraw(args)
#		self.layout.size = self.size
#		self.label.text_size = [self.labellayout.size[0]*.9, self.labellayout.size[1]*.9]#[self.size[0]*.95, None]
	
	def redrawpos(self, *args):
		pass
#		self.layout.pos = self.pos
#		self.text_size = self.size
	
	def hover(self):
		pass
#		print "hover"

	def updatechecked(self):
		if save.watched[self.path]:
			self.check()
		else:
			self.uncheck()
			
	def togglechecked(self):
		if self.watched:
			self.uncheck()
		else:
			self.check()
		save.watched[self.path] = self.watched
		
	def check(self):
		self.watched = True
		self.checklabel.text = checkmark
				
	def uncheck(self):
		self.watched = False
		self.checklabel.text = ""
		
	def unselect(self):
		self.selected = False
		
#		color = buttoncolor#self.unselected_color
		self.rect.texture = buttonnormaltexture
#		self.button.background_color = color
#		self.canvas.ask_update()
#		pass
		
	def buttonpressed(self, *args):
		if self.selected:
			self.pressed()
		else:
			app.selectbutton(self)
		
	def select(self):
		self.selected = True
		
		has_error = False
		if not (self.progress == None or self.progress == 100):
			has_error=True
		if self.missingprevepisode:
			has_error=True
		if self.path.endswith(".part") or self.path.endswith(".!qB"):
			has_error=True
		
#		color = selectedcolor
		self.rect.texture = buttonactivatedtexture
		if has_error:
#			color = errorcolor#self.error_color
			self.rect.texture = buttonerrortexture
			
#		self.button.background_color = color#self.selected_color
#		self.canvas.ask_update()
#		print "select"

#Builder.load_string( \
"""
<abutton>:
	canvas.before:
		Rectangle:
			size: self.size
			pos: self.pos
			texture: Gradient.horizontal((0, 0, 0, 1), (1, 1, 1, 1))
"""#)

class gradientButton(Button):
	def __init__(self, *args, **kwargs):
		kwargs["halign"]="right"
		if not "valign" in kwargs:
			kwargs["valign"]="middle"
		Button.__init__(self, *args, **kwargs)
		
		with self.canvas.before:
			self.rect = Rectangle(pos=self.pos, size=self.size)
			self.rect.texture = rightbuttonnormaltexture
			
		self.background_color = (0,0,0,0)
		
		self.bind(pos=self.redraw)
		self.bind(size=self.redraw)
		
		self.original_font_size = None
		if "font_size" in kwargs:
			self.original_font_size = kwargs["font_size"]
		
		
	def redraw(self, *args):
		self.rect.pos = self.pos
		self.rect.size = self.size
		
		self.text_size = [self.size[0]-50, self.size[1]]
		if self.text_size[0] < 300:
			if self.original_font_size == None:
				self.original_font_size = self.font_size
			self.font_size = '20sp'
		else:
			if self.original_font_size != None:
				self.font_size = self.original_font_size
		

class clock(AnchorLayout):
	def __init__(self, size_hint=None, pos_hint=None):
		AnchorLayout.__init__(self, size_hint=size_hint, pos_hint=pos_hint)
		self.button = gradientButton(text="hi", halign="center", size_hint=[1,1], font_name='/usr/share/pyshared/kivy/data/fonts/DejaVuSans.ttf', color=textcolor, font_size='70sp')
#		self.button.background_color = buttoncolor#[.5, .5, .5, buttonopacity]
		self.add_widget(self.button)
		
		Clock.schedule_interval(self.update, 1)
		
	def update(self, *args):
		self.button.text = time.strftime("%I:%M %p")


class KMCApp(App):
	def build(self):
		Window.clearcolor = (0,0,0,0)
		
		self.imagesloaders = {}
		
#		self.selectedfolder = save.loadstate("infolder")

#		save.setname(save.tvfolder, ["TV", None])
		
#		self.baseimagepath = os.path.join("/home/yyon/Pictures/wallpapers", random.choice(os.listdir("/home/yyon/Pictures/wallpapers")))
#		
		self.sm = ScreenManager()
		self.defaultscreen = Screen(name="default")
		self.sm.add_widget(self.defaultscreen)
		
		#self.sm.switch_to(self.defaultscreen)
		self.sm.current = "default"
		
		fllayout = FloatLayout()
		
		self.downloadedinfo = {}
		
		self.defaultscreen.add_widget(fllayout)
		
		self.imageloader = None
		
		self.backgroundimage = Image(pos_hint={'center_x':.5, 'center_y':.5}, size_hint=[1,3], allow_stretch=True)
		fllayout.add_widget(self.backgroundimage)
		
#		global BACKOPACITY
#		back = GradientWidget(colors=((0,0,0,BACKOPACITY), (0, 0, 0, BACKOPACITY)), pos_hint={'center_x':.5, 'center_y':.5}, size_hint=[1,1])
#		fllayout.add_widget(back)
#		BACKOPACITY=0
		
#		self.darkener = Button(background_color=[0,0,0,0])
#		fllayout.add_widget(self.darkener)
		
		contentlayout = FloatLayout(pos_hint={'center_x':.5, 'center_y':.5}, size_hint=[1,1])#(.95, .95))
		fllayout.add_widget(contentlayout)
		
		sidebarlayout = FloatLayout(pos_hint={'center_x':.85, 'center_y':.5}, size_hint=[.3, 1])
		contentlayout.add_widget(sidebarlayout)
		
		rightback = GradientWidget(colors=((0,0,0,0), (0, 0, 0, BACKOPACITY)), pos_hint={'center_x':.5, 'center_y':.5}, size_hint=[1,1])
		sidebarlayout.add_widget(rightback)
		
		"""
		layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
		self.layout = layout
		#Make sure the height is such that there is something to scroll.
		layout.bind(minimum_height=layout.setter('height'))
		"""
		
		buttons = []
		
		self.clock = clock(pos_hint={'center_x':.5, 'center_y':.825}, size_hint=[1,.15])
		sidebarlayout.add_widget(self.clock)
		
		self.buttonspacing = 5
		
		leftsidelayout = FloatLayout(pos_hint={'center_x':.325, 'center_y':.5}, size_hint=(.65, 1))
		contentlayout.add_widget(leftsidelayout)
		
		leftback = GradientWidget(colors=((0,0,0,BACKOPACITY), (0, 0, 0, 0)), pos_hint={'center_x':.5, 'center_y':.5}, size_hint=[1,1])
		leftsidelayout.add_widget(leftback)
		
		self.layout = BoxLayout(orientation="vertical", pos_hint={'center_x':.5, 'center_y':.5}, size_hint=(1, 1), spacing=self.buttonspacing)
		leftsidelayout.add_widget(self.layout)
		
		self.layoutheight = 15
		self.layouttop = 0
		
		
		"""
		self.boxes = []
		
		for i in range(15):
			box = FloatLayout()
			self.boxes.append(box)
			self.layout.add_widget(box)
		"""
		
		"""
		self.scroll = ScrollView(pos_hint={'center_x':.325, 'center_y':.5}, size_hint=(.65, 1))#pos_hint={'center_x':.35, 'center_y':.5}, size_hint=(.65, .9))
		contentlayout.add_widget(self.scroll)
		self.scroll.do_scroll_x = False
		self.scroll.bar_margin = -5
		self.scroll.bar_width=5
		self.scroll.add_widget(layout)
		"""
		
#		self.titlelayout = FloatLayout(pos_hint={'center_x':.5, 'center_y':.975}, size_hint=(.5, .06))
#		self.titleback = gradientButton(background_color=buttoncolor, pos_hint={'center_x':.5, 'center_y':.5},size_hint=[1,1])
#		self.titlelayout.add_widget(self.titleback)
		self.titlelabel = gradientButton(text="hi", pos_hint={'center_x':.5, 'center_y':1-.05}, valign="top", size_hint=(1, .1), font_name='/usr/share/pyshared/kivy/data/fonts/DejaVuSans.ttf', color=textcolor, font_size="40sp")
		sidebarlayout.add_widget(self.titlelabel)
#		self.titlelayout.add_widget(self.titlelabel)
		
#		self.previewimage = AsyncImage(pos_hint={'center_x':.85, 'center_y':.2}, size_hint=[.25,1])
#		self.previewimage.source = 
		
#		fllayout.add_widget(self.previewimage)
		
		self.buttons = []
		self.up = None
		self.namedisplay = "name"
		
		self.infolder = None
#		self.scrollstate = save.scrollstate#{}
		
		self.showwatched = True
		
		self.selectedindex = 0
		
		Window.bind(mouse_pos=self.mouse_pos)
		Window.bind(on_motion=self.on_motion)
		self.scrolltimer = 0
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
		
		#self.populatebuttons(["a", "b", "c"])
		self.enterfolder(tvfolder)
		
		Clock.schedule_interval(self.lookfordownloadupdate, 60)
#		Clock.schedule_once(self.on_start, 1)
#		Clock.schedule_interval(self.refresh, 30)
		
		options = [["Play", self.dobutton], ["Up", self.esc], ["Refresh", self.refresh], ["Delete", self.delete], ["Folder Rename", self.folderrename], ["Rename", self.rename], 
			["Change Image", self.imageselector], ["Toggle Watched", self.togglewatched], ["Show Full Names", self.togglenamedisplay], 
			["Sort", self.togglesort], ["Show Watched", self.toggleshowwatched]]
		
		optionlayout = BoxLayout(orientation="vertical", pos_hint={'center_x':.5, 'center_y':.35}, size_hint=[1,.7], spacing=self.buttonspacing)
		sidebarlayout.add_widget(optionlayout)
		
		self.options = {}
		
		for opt in options:
			text, command = opt
			button = gradientButton()
			optionlayout.add_widget(button)
			button.font_size='30sp'
			button.font_name = '/usr/share/pyshared/kivy/data/fonts/DejaVuSans.ttf'
			button.text = text
			button.color = textcolor
#			button.background_color=buttoncolor#[.5, .5, .5, buttonopacity]
			button.bind(on_press=partial(self.runcommand, command)) 
			
			self.options[text] = button
			
		self.togglesort(toggle=False)
		
		self.imgwin = Screen(name="images")
		self.sm.add_widget(self.imgwin)
		
		back = Button()
		back.background_color=[0,1,1,1]
		self.imgwin.add_widget(back)
		
		self.imgwinlist = GridLayout(cols=1, spacing=10, pos_hint={'center_x':.5, 'center_y':.6}, size_hint=[.9,.7])
		self.imgwin.add_widget(self.imgwinlist)
		
		self.nextimgpageb = Button(text="Next Page", size_hint=[.15, .05], pos_hint={'center_x':.8, 'center_y':.1})
		self.nextimgpageb.bind(on_press=self.nextimgpage)
		self.imgwin.add_widget(self.nextimgpageb)
		
		self.imgpage = Label(size_hint=[.15, .05], pos_hint={'center_x':.6, 'center_y':.1})
		self.imgwin.add_widget(self.imgpage)
		
		self.nextimgpageb = Button(text="Cancel", size_hint=[.15, .05], pos_hint={'center_x':.4, 'center_y':.1})
		self.nextimgpageb.bind(on_press=partial(self.setimage, None, None))
		self.imgwin.add_widget(self.nextimgpageb)
		
		self.localimgbutton = Button(text="From File", size_hint=[.15, .05], pos_hint={'center_x':.2, 'center_y':.1})
		self.localimgbutton.bind(on_press=self.localimageselector)
		self.imgwin.add_widget(self.localimgbutton)
		
#		imageloader = threading.Thread(target=self.loadimages)
#		imageloader.start()
		
#		Cache._categories['kv.loader']['timeout'] = None
#		self.loadimages()
		
		return self.sm#fllayout
		
#	def on_start(self, *args):
#		for index, button in enumerate(self.buttons):
#			if button.path == self.selectedfolder:
#				self.select(index, True)
##		self.refresh()
	
	def runcommand(self, command, *args):
		command()
		
	def delete(self):
		if tkMessageBox.askyesno("Delete", "Delete?", default="no"):
			path = self.buttons[self.selectedindex].path
			name = self.buttons[self.selectedindex].name
			if send2trash != None:
				with open(deletedfile, "a") as myfile:
					myfile.write(name + "\n")
					
				send2trash(path)
			else:
				tkMessageBox.showerror("No trash library", "install Send2Trash library (sudo pip install Send2Trash)")
		self.refresh()
		
	def lookfordownloadupdate(self, *args):
#		self.updatedownloaded()
		files = os.listdir(self.infolder)
		for f in files:
			foundbutton = False
			for b in self.buttons:
				bname = os.path.basename(b.path)
				if f == bname:
					foundbutton = True
					break
			if foundbutton == False:
				self.refresh()
				break
		
	def enterfolder(self, folder, up=False):
		self.infolder = os.path.normpath(folder)
		if self.infolder == tvfolder:
			self.up = None
		else:
			self.up = os.path.normpath(os.path.join(folder, ".."))
		name, epnumber = save.names[self.infolder]
		self.titlelabel.text = name
#		if up == False:
#			if self.up != []:
#				self.up[-1][1] = self.selectedindex
#				self.up[-1][2] = self.scroll.scroll_y
#			self.up.append([folder, 0, 0])
		self.refresh()
		self.refreshimage()
		self.refreshdownloadedfrominfo()
#		if up:
#			self.select(self.up[-1][1])
#			self.scroll.scroll_y = self.up[-1][2]
#			self.scroll.update_from_scroll()
	
	def refresh(self, *args):
		folder = self.infolder
		l = os.listdir(folder)
		l = [os.path.join(folder, path) for path in l]
		l.sort()
		if not save.showwatched and folder == tvfolder:
			l = [path for path in l if not save.watched[path]]
		
		if len(save.scrollstate[folder]) == 2:
			selectindex, top = save.scrollstate[folder]
			name=None
		else:
			selectindex, top, name = save.scrollstate[folder]
		
		self.populatebuttons(l)
		
		self.layouttop = top
		
		for index, button in enumerate(self.buttons):
			if button.name == name:
				selectindex = index
				break
		
		self.select(selectindex)
		
		"""
		if folder in self.scrollstate:
			newselect = self.scrollstate[folder][0]
			if len(self.buttons) > newselect:
				self.select(newselect, True, True)
				self.scroll.scroll_y = self.scrollstate[folder][1]
				self.scroll.update_from_scroll()
		"""
		
	def clearbuttons(self):
#		for box in self.boxes:
		self.layout.clear_widgets()
		
	def populatebuttons(self, l):
##		self.layout.clear_widgets()
		self.buttons = []
#		updir = os.path.normpath(os.path.join(self.infolder, ".."))#self.up[-1][0]
		if self.up == None:
			updirname = "TV Shows"
		else:
			updir = os.path.basename(self.up)
			updirname = changename(updir, takeoutnumbers=True, dosearch=dogooglesearch, title=True)
		
		allfiles = [[] for f in l]
		
		for index, path in enumerate(l):
			name, epnumber = save.names[path]
			allfiles[index] = [path, name, epnumber]
		
		allfiles.sort(key=lambda f : f[1]) # name
		allfiles.sort(key=lambda f : f[2]) # number
		
		if self.up == None:
			if save.sort == SORT_WATCHED:
				allfiles.sort(key=lambda f : save.lastwatched[f[0]], reverse=True)
			elif save.sort == SORT_CREATED:
				allfiles.sort(key=lambda f : os.path.getctime(f[0]), reverse=True)
		
		
		episodes = [f[2] for f in allfiles if f[2] != None]
		
		for path, name, epnumber in allfiles:
			missingprevepisode = False
			if epnumber != None:
				name = "Episode " + str(epnumber)
				missingprevepisode = True
				epnumber = float(epnumber)
				if epnumber == 1:
					missingprevepisode = False
				else:
					for ep in episodes:
						ep = float(ep)
						if epnumber > ep and epnumber - 1 <= ep:
							missingprevepisode = False
			else:
				name = name
			b = abutton(path, self, name)
			if epnumber != None:
				b.epnum = epnumber
			if missingprevepisode:
				b.missingprevepisode = True
				b.unselect()
			self.buttons.append(b)
#			self.layout.add_widget(b)
		
		if len(self.buttons) == 0:
			if self.up == None:
				text = "There are no TV Shows in\n"
			else:
				text = "There are no files in\n"
			text += self.infolder+"\nTry adding some!"
			b = abutton(os.path.join(self.infolder, "NOTAFILE"), self, text)
			self.buttons.append(b)
		
#		self.updatedownloaded()
#		if not self.infolder in self.scrollstate:
		self.select(0, True)
	
#	def loadimage(self, loader):
#		if loader.image.texture:
#			self.backgroundimage.texture = loader.texture
#			self.backgroundimage.canvas.ask_update()
	
	def loadimage(self, imgpath):
		proxyimage = Loader.image(imgpath)
		self.imagesloaders[imgpath] = proxyimage
	
	def loadimages(self):
#		dirs = os.listdir(save.tvfolder)
#		dirs = [os.path.join(save.tvfolder, d) for d in dirs]
		dirs = [d for d in save.images.keys() if os.path.exists(d)]
		for d in dirs:
			print save.images[d]
			imgpath = save.images[d]
			self.loadimage(imgpath)
	
	def refreshimage(self):
		if self.up == None:
			path = self.buttons[self.selectedindex].path
		else:
			path = self.buttons[self.selectedindex].showfolder
		
#		if len(self.up) == 1:
#		if self.infolder == save.tvfolder:
#		print "refreshing image"
		
#		try:
#			Loader.loading_image = self.backgroundimage.source
#		except:
#			pass
		
#			try:
#				self.backgroundimage.source = save.defaultimage
#		loader = Loader.image(save.getimage(path)

#		if self.up == None:
#			imgpath = self.baseimagepath
#		else:
		imgpath = save.images[path]
		
#		if imgpath in self.imagesloaders and self.imagesloaders[imgpath].loaded:
#			self.backgroundimage.texture = self.imagesloaders[imgpath].image.texture
#		else:
		
#		if self.imageloader != None:
#			self.imageloader.stop()
		self.imageloader = Loader.image(imgpath)
		self.imageloader.bind(on_load=self.imageloaded)
		self.imageloaded()
#		self.backgroundimage.source = imgpath
#			self.loadimage(imgpath)
#		loader.bind(on_load=self.loadimage)
#			except:
#				save.nextimage(path)

	def imageloaded(self, *args):
		if self.imageloader.loaded:#.image.texture:
			self.backgroundimage.texture = self.imageloader.image.texture
#		if proxyImage.image.texture:
#			self.backgroundimage.texture = proxyImage.image.texture
	
	def selectbutton(self, b):
		self.select(self.buttons.index(b))
	
	def select(self, newindex, override=False, noscroll=False):
#		if self.selectedindex != newindex or override:
		if newindex < 0 or newindex >= len(self.buttons):
			return
		
		try:
			self.buttons[self.selectedindex].unselect()
		except IndexError:
			pass
		self.selectedindex = newindex
		selectedbutton = self.buttons[newindex]
		selectedbutton.select()
		
		if self.up == None:
			self.refreshimage()
			
			save.infolder = selectedbutton.path
		
		self.clearbuttons()
		
		if self.selectedindex > self.layouttop+self.layoutheight-1:
			self.layouttop = self.selectedindex - self.layoutheight+1
		elif self.selectedindex < self.layouttop:
			self.layouttop = self.selectedindex
		
		for i in range(self.layouttop, self.layouttop+self.layoutheight):
			if i < len(self.buttons):
				b = self.buttons[i]
				self.layout.add_widget(b)
		
		save.scrollstate[self.infolder] = [self.selectedindex, self.layouttop, self.buttons[self.selectedindex].name]
		
		"""
			if not noscroll:
				totalheight = self.layout.size[1]
				
				viewheight = self.scroll.size[1]
				
				scrollheight = self.scroll.size[1]
				scrollpos = 1 - self.scroll.scroll_y
				scrolltop = (totalheight - scrollheight) * scrollpos
				scrollbottom = scrolltop + scrollheight
				
				bheight = selectedbutton.height
				bpadding = (totalheight) / len(self.buttons) - selectedbutton.height + 1
				buttonsabove = self.selectedindex
				btop = (bheight + bpadding) * buttonsabove
	#			print "####", selectedbutton.to_parent(*selectedbutton.pos)[1]#, self.scroll.size[1]-selectedbutton.pos[1], self.scroll.viewport_size[1]
				btop = (viewheight - (selectedbutton.to_parent(*selectedbutton.pos)[1] + bpadding)) + scrolltop
				bbottom = btop + bheight
				
				if bpadding > 0:
					newscrolly = None
					print "dscroll", self.scroll.scroll_y
					if totalheight - scrollheight != 0:
						if btop < scrolltop:
							newscrolly = 1 - btop / float(totalheight - scrollheight)
							self.scroll.scroll_y = newscrolly
							self.scroll.update_from_scroll()
						elif bbottom > scrollbottom:
							print "bottom"
							newscrolly = 1 - (bbottom - scrollheight) / float(totalheight - scrollheight)
							self.scroll.scroll_y = newscrolly
							self.scroll.update_from_scroll()
						
	#					newscrolly = 1 - float(self.selectedindex) / (len(self.buttons)-1)
						
	#					if newscrolly != None:
	#						anim = Animation(scroll_y=newscrolly, d=.1, transition="in_out_quad")
	#						anim.start(self.scroll)
					
					if self.infolder != None:
						print "cscroll", self.scroll.scroll_y
						self.scrollstate[self.infolder] = [self.selectedindex, self.scroll.scroll_y]
						save.scrollstate = self.scrollstate
			"""
	
	def scroll(self, direction):
		self.scrolltimer += 1
		if self.scrolltimer >= 5:
			self.scrolltimer = 0
			if direction == 1:
				if self.selectedindex != 0:
					self.select(self.selectedindex - 1)
			elif direction == -1:
				self.select_down()
			
	
	def on_motion(self, window, etype, motionevent):
#		if motionevent != []:
		if motionevent.button == "scrollup":
			self.scroll(direction=-1)
		elif motionevent.button == "scrolldown":
			self.scroll(direction=1)
	
	def mouse_pos(self, instance, value):
		x, y = value
		for b in self.buttons:
			if b.collide_point(x, y):
				b.hover()
		if x > 5 and x < self.root.width-5:
			if y < 2:
				self.scroll(direction=-1)
			elif y > self.root.height-2:
				self.scroll(direction=1)
#				self.select(self.buttons.index(b))
	
	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None
	
	def select_down(self):
		if self.selectedindex != len(self.buttons) - 1:
			self.select(self.selectedindex + 1)
	
	def rename(self):
		loc = self.buttons[self.selectedindex].path
		oldname = save.names[loc]
		newname = tkSimpleDialog.askstring("Rename", loc, initialvalue=oldname[0], parent=root)
		if newname == "":
			del save.names[loc]
		elif newname != None:
			if newname.isdigit():
				save.names[loc] = [oldname[0], int(newname)]
			else:
				save.names[loc] = [newname, None]
		self.refresh()
	
	def esc(self):
		saveclassinst.dosave()
		if self.up == None:
			EventLoop.close()
		else:
			if self.allwatched():
				save.watched[self.infolder] = True
			self.enterfolder(self.up)#os.path.normpath(os.path.join(self.infolder, "..")), up=True)
			
	def dobutton(self):
		self.buttons[self.selectedindex].pressed()
		
	def folderrename(self):
		if tkMessageBox.askyesno("Rename", "Rename this directory?"):
			print "rename"
			namedir(self.infolder, True)
		self.refresh()
		
	def imageselector(self):
		path = None
		if self.up == None:
			path = self.buttons[self.selectedindex].path
		else:
			path = self.buttons[self.selectedindex].showfolder
		
		if path != None:
#			self.backgroundimage.source = defaultimageloc
			self.pickimage(path)
	
	def localimageselector(self, *args):
		path = self.imageloc
		
		filename = askopenfilename(initialdir=imagesfolder)
#		dlg = wx.FileDialog(wxframe, "Choose a file", imagesfolder, "", "*.*", wx.OPEN)
		if filename != None:
#			filename = dlg.GetFilename()
#			dirname = dlg.GetDirectory()
#			filename = os.path.join(dirname, filename)
			print filename
			self.setimage(path, filename)
			self.sm.current="default"
			
	def togglenamedisplay(self):
		if self.namedisplay == "name":
			self.namedisplay = "file"
		elif self.namedisplay == "file":
			self.namedisplay = "name"
		for b in self.buttons:
			b.updatename()
	
	def togglewatched(self):
		self.buttons[self.selectedindex].togglechecked()
		
	def toggleshowwatched(self):
		selectedpath = self.buttons[self.selectedindex].path
		save.showwatched = not save.showwatched
		self.refresh()
		
#		selectbutton = None
#		for index, b in enumerate(self.buttons):
#			if b.path == selectedpath:
#				selectbutton = index
#				break
#		if selectbutton == None:
#			self.select(0)
#		else:
#			self.select(selectbutton)
		
	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		key = keycode[1]
#		print key
#		print key, modifiers
		if key == 'up':
			if self.selectedindex != 0:
				self.select(self.selectedindex - 1)
		elif key == 'down':
			self.select_down()
		elif key == "escape":
#			curdir = self.up.pop()
			self.esc()
		elif key == "enter" or key == "spacebar":
			self.dobutton()
		else:
			if modifiers == []:
				if key.isalpha() and len(key) == 1:
					for index, b in enumerate(self.buttons):
						if b.name.lower().startswith(key):
							self.select(index)
							break
		"""
		elif key == "o":
			self.buttons[self.selectedindex].pressed(optirun=True)
		elif key == "v":
			self.buttons[self.selectedindex].pressed(vlc=True)
		elif key == "w":
			self.togglewatched()
		elif key == "n":
			self.togglenamedisplay()
		elif key == "r":
			if tkMessageBox.askyesno("Rename", "Rename this directory?"):
				print "rename"
				namedir(self.infolder, True)
			self.refresh()
#			pass
		elif key == "s":
			self.rename()
		elif key == "i":
			self.imageselector()
		elif key == "h":
			self.toggleshowwatched()
		"""
			
		return True
	
	def allwatched(self):
		allwatched = False
		for b in self.buttons:
			if b.epnum != None:
				allwatched = True
		for b in self.buttons:
			if b.epnum != None:
				if not b.watched:
					allwatched = False
		return allwatched
	
	def checkdownloadedout(self, *args):
		if self.downloadedcmd == None:
			return
		
		done = False
		
		try:
			self.downloadout += self.downloadedcmd.stdout.read()
		except IOError:
			pass
		

		if self.downloadout.endswith("DONE\n"):
			done = True
			self.downloadedcmd.stdout.close()
		
		if done == False:
			Clock.schedule_once(self.checkdownloadedout, .1)
		else:
			text = self.downloadout
			self.downloadedcmd = None
			
			if "Name: " in text:
				for atorrent in text.split("\n \n"):
					name = atorrent.split("Name: ", 1)[1].split("\n", 1)[0]
		#			print name
		#			subfolder = os.path.join(videosfolder, name)#torrentname)
					thebutton = None
					if "Progress: " in atorrent:
						progress = atorrent.split("Progress: ", 1)[1].split("%", 1)[0]
						self.downloadedinfo[name] = progress
						"""
						for b in self.buttons:
							if os.path.basename(b.path) == name:
								self.downloadedinfo[f] = progress
								b.setprogress(progress)
						"""
		#					print "found"
		#			if thebutton == None:
		#				continue
					
					files = None
					if thebutton == None:
						if "::Files" in atorrent:
							files = atorrent.split("::Files\n", 1)[1].split("\n  ::Peers", 1)[0]
							files = files.split("\n")
							files = [f.strip() for f in files]
							progress = [f.split("Progress: ", 1)[1].split("%", 1)[0] for f in files]
							files = [f.rsplit("/", 1)[1] for f in files if "/" in f]
							files = [f.rsplit(" (", 1)[0] for f in files]
							
							for index, f in enumerate(files):
								self.downloadedinfo[f] = progress[index]
			self.refreshdownloadedfrominfo()
			
	
	def refreshdownloadedfrominfo(self):
#		if self.downloadedinfo == {}:
#			print "no info yet"
		for f in self.downloadedinfo:
			progress = self.downloadedinfo[f]
			for b in self.buttons:
				if os.path.basename(b.path) == f:
					b.setprogress(progress)
					#b.downloadlabel.text = fprogress
						
		#			thebutton.downloadlabel.text = "found"
	
	"""
	def updatedownloaded(self):
#		return
#		command = ["deluge-console", "info -v"]
		self.downloadedcmd = subprocess.Popen("deluge-console \"info -v\"; echo DONE", shell=True, stdout=subprocess.PIPE)
		self.downloadout = ""
		fcntl.fcntl(self.downloadedcmd.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
		self.checkdownloadedout()
#		text = p.stdout.read()
#		retcode = p.wait()
#		print text
	"""
	
	def pickimage(self, loc, page=0):
		self.imagepage = page
		self.imageloc = loc
		
		self.imgpage.text = "Page: " + str(self.imagepage+1)
		
		self.sm.current = "images"
		
		self.imgwinlist.clear_widgets()
		
		gimages = findimage(loc, page=page)
		
		for gimage in gimages:
			url = gimage.previewurl#.url#previewurl
#			url = "http://t2.gstatic.com/images?q=tbn:ANd9GcSUcpN4Qt05kh8aGW6e0qI0T98oSKutM4cbh-aREJvupUyqg5wDUbg_pjc".encode("utf-8")
#			print url
			
			button = AnchorLayout()
			layout = FloatLayout()
			button.add_widget(layout)
			
			b = Button(pos_hint={'center_x':.5, 'center_y':.5}, size_hint=[1,1])
			width, height = gimage.size
			
			print width, height
			if width < 1920 or height < 1080:
				print "too small"
				b.background_color=[0,0,0,1]
			
			ending = gimage.url.rsplit(".", 1)[1]
			print gimage.url
			if len(ending) > 3:
				b.background_color = [1, 0, 0, 1]
			
			
			b.bind(on_press=partial(self.doimagedownload, loc, gimage))
			layout.add_widget(b)
			img = Image(allow_stretch=True)
			
			layout.add_widget(Label(text=str(width) + "x" + str(height), pos_hint={'center_x':.9, 'center_y':.5}))
			
			temp = downloadtempimage(url)
			img.source=temp
#			UrlRequest(url, partial(self.showimg, img=img))
#			img.source = url#urllib.quote_plus("""http://t2.gstatic.com/images?q=tbn:ANd9GcSUcpN4Qt05kh8aGW6e0qI0T98oSKutM4cbh-aREJvupUyqg5wDUbg_pjc""")#url
			
			button.add_widget(img)
			self.imgwinlist.add_widget(button)
	
	def nextimgpage(self, *args):
		self.pickimage(self.imageloc, page=self.imagepage+1)
	
	def doimagedownload(self, loc, gimage, *args):
		if gimage != None:
			url = gimage.url
			temp = downloadtempimage(url)
			self.setimage(loc, temp)
			#save.downloadimage(loc, url)
		self.sm.current="default"
	
	def setimage(self, tvpath, imgpath):
		ending = "png"
		newimagename = os.path.basename(tvpath) + "." + ending
		downloadfolder = imagesfolder
		newimagepath = os.path.join(downloadfolder, newimagename)
		if os.path.exists(newimagepath):
			os.remove(newimagepath)
		
		img = Image(source=imgpath)
		img.texture.save(newimagepath)
		save.setimage(tvpath, newimagepath)
		
		self.loadimage(newimagepath)
#		self.imagesloaders[newimagepath].image = img
		
		self.refreshimage()
		
	def togglesort(self, toggle=True):
		if toggle:
			newindex = SORTING.index(save.sort)+1
			if newindex == len(SORTING):
				newindex = 0
			newsort = SORTING[newindex]
			save.sort = newsort
		
		button = self.options["Sort"]
		
		if save.sort == SORT_ALPHABETICAL:
			button.text = "Sort: A-z"
		elif save.sort == SORT_WATCHED:
			button.text = "Sort: Watched"
		elif save.sort == SORT_CREATED:
			button.text = "Sort: Created"
		
#		selectedpath = self.buttons[self.selectedindex].path
#		
#		save.sortlastwatched = not save.sortlastwatched
		self.refresh()
#		
#		selectbutton = None
#		for index, b in enumerate(self.buttons):
#			if b.path == selectedpath:
#				selectbutton = index
#				break
#		if selectbutton == None:
#			self.select(0)
#		else:
#			self.select(selectbutton)

app = KMCApp()
subprocess.Popen("wmctrl -r \":ACTIVE:\" -b toggle,fullscreen", shell=True)
app.run()
root.destroy()
