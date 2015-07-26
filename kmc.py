#!/usr/bin/env python
# -*- coding: utf-8 -*-

#TODO
# make it work on other computers
# don't have errors
# settings

import module_locator
import subprocess
import os

try:
	import kivy
except ImportError:
	print "Kivy not found!"
	installscript = subprocess.Popen(["./install_debian.sh"])
	installscript.wait()

from kivy.config import Config

Config.set('kivy', 'log_level', 'warning')

from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
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

"""
try:
	from kivy.uix.effectwidget import EffectWidget
except ImportError:
	EffectWidget = None
from kivy.uix.effectwidget import InvertEffect, HorizontalBlurEffect, VerticalBlurEffect
"""

import pickle
import re
import operator
import copy
#import tkSimpleDialog
#import tkMessageBox
#import Tkinter
import sys
import time
import urllib2
import urllib
import simplejson
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
#from tkFileDialog import askopenfilename

#Rename
#delete
#renamefolder
#newimage

def timeme(method):
	def wrapper(*args, **kw):
		startTime = int(round(time.time() * 1000))
		result = method(*args, **kw)
		endTime = int(round(time.time() * 1000))

		print(endTime - startTime,'ms')
		return result

	return wrapper

#root = Tkinter.Tk()
#root.withdraw()

buttoncolor=(0,0,0,0)
selectedcolor=(1,0,0.4,0.3)
errorcolor=(1,1,0,0.4)
textcolor=(0,0,0,1)#(1,1,1,1)
BACKOPACITY = 0.2
backgroundcolor=(1,1,1,BACKOPACITY)
backgroundinvisible=(1,1,1,0)

SORT_ALPHABETICAL = "Alpha"
SORT_WATCHED = "Watched"
SORT_CREATED = "Created"
SORT_SIZE = "Size"
SORTING = [SORT_ALPHABETICAL, SORT_WATCHED, SORT_CREATED, SORT_SIZE]

mainfont = "DejaVuSans"#'/usr/share/pyshared/kivy/data/fonts/DejaVuSans.ttf'

showupdown = False

popuphasfocus = False

useblur = False
#if EffectWidget == None:
#	useblur = False

def popupmessage(title, message, content=None, options=[["Dismiss", None]], arg=None, cleanup=None):
	vbox = BoxLayout(orientation="vertical")
	scroll = ScrollView()
	vbox.add_widget(scroll)
	vbox2 = BoxLayout(orientation="vertical")
	scroll.add_widget(vbox2)
	l = Label(text=message, size_hint=[1,None])
	vbox2.add_widget(l)
	if content != None:
		vbox2.add_widget(content)
	hbox = BoxLayout(orientation="horizontal", size_hint=(1, .2))
	vbox.add_widget(hbox)

	popup = Popup(title=title,
    	content=vbox,
    	size_hint=(.5, .5), auto_dismiss=False)
	for text, method in options:
		b = Button(text=text)
		b.bind(on_press=partial(popupmethod, popup, method, arg, cleanup))
		hbox.add_widget(b)
	popup.open()

	global popuphasfocus
	popuphasfocus = True

def popupmethod(popup, method, arg, cleanup, button):
	popup.dismiss()
	global popuphasfocus
	popuphasfocus = False
	if method != None:
		if arg != None:
			method(arg())
		else:
			method()
	if cleanup != None:
		cleanup()

def popupaskstring(title, message, method, default=""):
	content = TextInput(text=default)
	popupmessage(title, message, content=content, options=[["OK", method], ["Cancel", None]], arg=partial(finishaskstring, content), cleanup=partial(unfocustextinput, content))

def finishaskstring(content):
	return content.text

def unfocustextinput(*content):
	for c in content:
		c.focus = False
	app.getkeyboard()

def popupaskyesno(title, message, method):
	popupmessage(title, message, options=[["Yes", partial(method, True)], ["No", partial(method, False)]])

def popupaskconfirmation(title, message, method):
	popupmessage(title, message, options=[["Yes", method], ["No", None]])

def popupaskfile(title, message, method, folder="~"):
	filechooser = FileChooserListView(size_hint_y=1, path=folder)
	popupmessage(title, message, content=filechooser, options=[["OK", partial(finishaskfile, method, filechooser)], ["Cancel", None]])

def finishaskfile(method, filechooser):
	selection = filechooser.selection
	if len(selection) == 0:
		return
	else:
		path = selection[0]
		method(path)

class dictwithdefault(UserDict):
	def __init__(self, default=None):
		UserDict.__init__(self)
		self.default = default

	def __getitem__(self, key):
		if key in self.keys():
			return UserDict.__getitem__(self, key)
		else:
			if hasattr(self.default, "__call__"):
				value = self.default(key)
				if value != None:
					self[key] = value
				if key in self.keys():
					return UserDict.__getitem__(self, key)
				else:
					print "ERROR"
					return None
			else:
				return self.default

def getcreatedtime(f):
	return os.path.getctime(f)

class savedata(object):
	"""Class that is persistent (pickle)"""

	def makevars(self):
		v = {"showwatched":True,
			"watched":dictwithdefault(),
			"names":dictwithdefault(),
			"images":dictwithdefault(),
			"scrollstate":dictwithdefault(),
			"lastwatched":dictwithdefault(),
			"sort":SORT_ALPHABETICAL,
			"watchedset":set(),
			"created":dictwithdefault(),
			"allshows":allshowsclass(),
			"triedimage":set(),
			"usempv":True,
			"tracks":{}
#			"usebumblebee":False
			}

		for plugin in plugins:
			for newvar, default in plugin.getsavevars():
				v[newvar] = default

		for var in v:
			value = v[var]
			if not var in self.__dict__:
				print "MAKE", var
				setattr(self, var, value)
			value = getattr(self, var)

		self.watched.default = False
		self.names.default = renamefiles
		self.images.default = defaultimageloc
		self.created.default = getcreatedtime
		self.scrollstate.default = [0,0,None]
		self.lastwatched.default = dictwithdefault(time.gmtime(0))

	def setimage(self, tvpath, imgpath):
		if tvpath in self.images:
			currentimage = self.images[tvpath]
			if os.path.exists(currentimage) and os.path.normpath(imgpath) != os.path.normpath(currentimage):
				os.remove(currentimage)

		self.images[tvpath] = imgpath

def downloadtempimage(url):
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
	"""manages savedata"""

	def __init__(self):
		global saveclassinst
		saveclassinst = self
		self.savestatevar = savedata()

		self.allfolders = [tvfolder, kmcfolder, imagesfolder, pluginsfolder]
		self.allfiles = [savefile]

		self.makefolders()
		self.loadall()

	def dosave(self):
		print "SAVING"
		self.save(self.savestatevar, savefile)

	def makefolders(self):
		for folder in self.allfolders:
			if not os.path.exists(folder):
				os.makedirs(folder)

	def loadall(self):
		self.savestatevar = self.load(savefile, self.savestatevar)
		self.savestatevar.makevars()

	def load(self, loc, defaultdata):
		if os.path.exists(loc):
			f = open(loc, "rb")
			data = pickle.load(f)
		else:
			f = open(loc, "w")
			pickle.dump(defaultdata, f)
			data = defaultdata
		f.close()

		return data

	def save(self, data, loc):
		shutil.copyfile(loc, loc+".bak") # make backup

		f = open(loc, "w")
		pickle.dump(data, f)
		f.close()

class numpos(object):
	"""holds a number and its position in the string"""
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

def namedir(l, override=False):
	"""Looks for episode numbers"""
	print "naming dir"

	global torrenteps
	torrenteps = []

	files = l

	print "###"

	filenums = {}

	for f in files:
		filenums[f] = getnumbers(stripname(f.getpathname(), False))
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

	toremove += removeindexes

	for fnum in filenumcounter:
		times = filenumcounter[fnum]
		if times >= len(files)-1:
			toremove.append(fnum.strindex)
		elif float(fnum.num) > 100:
			toremove.append(fnum.strindex)

	for f in files:
		filenums[f] = [fnum for fnum in filenums[f] if not fnum.strindex in toremove]

	filenumsstrindex = [fnum.strindex for f in files for fnum in filenums[f]]
	epnumpos = None
	if len(filenumsstrindex) != 0:
		filenumsstrindex = Counter(filenumsstrindex)
		commonlist = filenumsstrindex.most_common()
		epnumpos = commonlist[0][0]
		print epnumpos

	names = copy.copy(l)
	eps = [None for f in l]

	for index, name in enumerate(names):
		path = l[index]
		changedname = files[index]
		newname = path.getpathname()
		if epnumpos != None:
			numpos = epnumpos
			numbers = filenums[changedname]
			number = [num for num in numbers if num.strindex == numpos]
			if number != []:
				number = number[0].num
				if "." in number:
					number = float(number)
				else:
					number = int(number)
				eps[index] = number
		names[index] = newname

	numbereps = sum([ep != None for ep in eps])
	if numbereps <= 1:
		eps = [None for ep in eps]

	for index, path in enumerate(l):
		if not path.getkey() in save.names or override:
			if isinstance(path, episode):
				name = names[index]
				epnumber = eps[index]
				path.setname([name, epnumber])

homefolder = os.path.expanduser("~")
tvfolder = os.path.join(homefolder, "Videos/tv")
kmcfolder = os.path.join(homefolder, ".kmc")
imagesfolder = os.path.join(kmcfolder, "images")
savefile = os.path.join(kmcfolder, "save")
deletedfile = os.path.join(homefolder, "Videos/deleted")
#startupscript = os.path.join(kmcfolder, "startup.sh")
pluginsfolder = os.path.join(kmcfolder, "plugins")

defaultimageloc = os.path.join(kmcfolder, "default.jpg")
if not os.path.exists(defaultimageloc):
	defaultimageloc = os.path.join(module_locator.module_path(), "default.jpg")

mpvinputconf = os.path.join(module_locator.module_path(), "input.conf")

checkmark = u"\u2713"

dogooglesearch = False
whitespaces = ["_"]
removestuff = ["DVD", "Ep", "Episodes", "+ OVA", "OVA", ".!qB", ".part"]
removestuffregex = ["[\[\(][^\]^\)]*[\]\)]", "v[0-9]"]
numberregex = "[0-9]+\s*[0-9]+"
ignorefiles = ["/"]
stripchars = [" ", "-"]

ignore = ["xbmc", "lost+found"]

subfolders = []

opedcounter = 1
othercounter = 1

plugins = []

class plugin(object):
	def __init__(self):
		plugins.append(self)

	def onstart(self):
		pass

	def getshows(self):
		return []

	def onclose(self):
		pass

	def onplayepisode(self, ep):
		pass

	def changecommand(self):
		return [[], [], []]

	def getsavevars(self):
		return []

	def getsettings(self):
		return []

	def getoptions(self):
		return []

if os.path.exists(pluginsfolder):
	for pluginfile in os.listdir(pluginsfolder):
		if pluginfile.endswith(".py"):
			pluginfile = os.path.join(pluginsfolder, pluginfile)
			execfile(pluginfile)

class googleimage():
	def __init__(self, url, previewurl, size, page):
		self.url, self.previewurl, self.size, self.page = url, previewurl, size, page

def imagesearch(searchTerm, page):
	"""Searches google images"""
	searchTerm = searchTerm.replace(' ','%20')

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

	print len(images)

	return images

def findimage(loc, page=0):
	searchterm = loc.getname()[0] + " wallpaper"#save.names[loc][0] + " wallpaper"
	images = imagesearch(searchterm, page)
	return images

def downloadimage(url, path):
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
	"""Names shows (not episodes)"""
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
		if newbasename == "":
			return
		if newbasename[0] in stripchars:
			newbasename = newbasename[1:]
		else:
			break
	while True:
		if newbasename == "":
			return
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

		if newbasenameending.endswith(".part"):
			newbasenameending = newbasenameending.replace(".part", "")
		newbasename = newbasenamebase + "." + newbasenameending
	if dosearch:
		newbasename = searchgoogle(newbasename)
	if newbasename == "":
		newbasename = basename
	return newbasename

class ShadowLabel(Label):
	tint = ListProperty([0, 0, 0, 0.1])

class ShadowButton(Button):
	tint = ListProperty([0, 0, 0, 0.1])

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

buttonactivatedtexture = Gradient.horizontal(selectedcolor, selectedcolor[:3] + (0,))
buttoninvisibletexture = Gradient.horizontal((0,0,0,0), (0, 0, 0, 0))
buttonnormaltexture = Gradient.horizontal(buttoncolor, buttoncolor[:3] + (0,))
buttonerrortexture = Gradient.horizontal(errorcolor, errorcolor[:3] + (0,))
rightbuttonnormaltexture = Gradient.horizontal(buttoncolor[:3] + (0,), buttoncolor)

class abutton(AnchorLayout):
	"""Buttons to the left"""

	def __init__(self, ep, app, name=None):
		AnchorLayout.__init__(self)#, size_hint=(.9, None), height='60dp')

		with self.canvas.before:
			self.rect = Rectangle(pos=self.pos, size=self.size)
			self.rect.texture = buttonactivatedtexture

		self.ep = ep
		self.app = app
		self.watched = False

		self.showfolder = ep.getparent()
		while True:
			if isinstance(self.showfolder, show) or self.showfolder == save.allshows:
				break
			self.showfolder = self.showfolder.getparent()

		if name == None:
			name = ep.getname()[0]
			if name == None:
				name = ep.getpathname()
		self.name = name

		self.font_size='40sp'
		self.progress = None
		self.selected = False

		self.epnum = None

		self.missingprevepisode = False

		self.unselect()

		self.layout = BoxLayout(size_hint=(1,1))
		self.add_widget(self.layout)

		self.checklabel = Label(halign="right", size_hint=[None,1], font_name=mainfont, color=textcolor)
		self.checklabel.text = ""
		self.checklabel.font_size = '40sp'
		self.layout.add_widget(self.checklabel)

		self.labellayout = ScrollView()
		self.labellayout.bar_color = [1,1,1,0]
		self.labellayout.do_scroll_y = False

		self.labellayout2 = AnchorLayout(anchor_x="left", anchor_y="center")
		self.labellayout.add_widget(self.labellayout2)

		self.label = Label(halign="left", size_hint=[None, None], font_name=mainfont, color=textcolor)
		self.label.bind(texture_size=self.label.setter('size'))
		self.labellayout2.add_widget(self.label)
		
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
			self.label.text = self.ep.getpathname()

	def pressed(self, *args):
		self.ep.pressed()

	def redrawsize(self, *args):
		pass

	def redrawpos(self, *args):
		pass

	def hover(self):
		pass

	def updatechecked(self):
		if self.ep.getwatched():
			self.check()
		else:
			self.uncheck()

	def togglechecked(self):
		if self.watched:
			self.uncheck()
		else:
			self.check()
		self.ep.setwatched(self.watched)

	def check(self):
		self.watched = True
		self.checklabel.text = checkmark

	def uncheck(self):
		self.watched = False
		self.checklabel.text = ""

	def unselect(self):
		self.selected = False

		self.rect.texture = buttonnormaltexture

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
		if self.ep.getpathname().endswith(".part") or self.ep.getpathname().endswith(".!qB"):
			has_error=True

		self.rect.texture = buttonactivatedtexture
		if has_error:
			self.rect.texture = buttonerrortexture


class gradientButton(Button):
	"""Buttons to the right"""

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
		self.button = gradientButton(text="hi", halign="center", size_hint=[1,1], font_name=mainfont, color=textcolor, font_size='70sp')
#		self.button.background_color = buttoncolor#[.5, .5, .5, buttonopacity]
		self.add_widget(self.button)

		Clock.schedule_interval(self.update, 1)

	def update(self, *args):
		self.button.text = time.strftime("%I:%M %p")


class pathobj(object):
	"""Base object for shows and episodes"""

	def __init__(self):
		pass

	def getkey(self):
		return self

	def getparent(self):
		return None

	def getchildren(self):
		return None

	def exists(self):
		return False

	def getname(self):
		if not self.getkey() in save.names.keys():
			save.names[self.getkey()] = self.defaultname()
		return save.names[self.getkey()]

	def defaultname(self):
		return None #override

	def setname(self, name):
		save.names[self.getkey()] = name

	def getwatched(self):
		if not self.getkey() in save.watched.keys():
			save.watched[self.getkey()] = self.defaultwatched()
		return save.watched[self.getkey()]

	def defaultwatched(self):
		return False

	def setwatched(self, watched):
		save.watched[self.getkey()] = watched

	def getcreated(self):
		if not self.getkey() in save.created.keys():
			save.created[self.getkey()] = self.defaultcreated()
		return save.created[self.getkey()]

	def defaultcreated(self):
		return time.time() # override

	def setcreated(self, created):
		save.created[self.getkey()] = created

	def getimage(self):
		if not self.getkey() in save.images.keys():
			return self.defaultimage()
		return save.images[self.getkey()]

	def defaultimage(self):
		if not self.gettriedimage():

			gimages = findimage(self)

			for gimage in gimages:
				result = app.doimagedownload(self, gimage)
				if result:
					break

			self.settriedimage()
		else:
			return defaultimageloc

	def deleteimage(self):
		if self.getkey() in save.images.keys():
			del save.images[self.getkey()]

	def hasimage(self):
		return self.getkey() in save.images.keys()

	def setimage(self, image):
		save.images[self.getkey()] = image

	def getscrollstate(self):
		if not self.getkey() in save.scrollstate.keys():
			return self.defaultscrollstate()
		return save.scrollstate[self.getkey()]

	def defaultscrollstate(self):
		return [0,0,None]

	def setscrollstate(self, scrollstate):
		save.scrollstate[self.getkey()] = scrollstate

	def getlastwatched(self):
		if not self.getkey() in save.lastwatched.keys():
			return self.defaultlastwatched()
		return save.lastwatched[self.getkey()]

	def defaultlastwatched(self):
		return time.gmtime(0)

	def setlastwatched(self, lastwatched):
		save.lastwatched[self.getkey()] = lastwatched

	def getpathname(self):
		return None # overwrite

	def getsize(self):
		size = 0
		for child in self.getchildren():
			size += child.getsize()
		return size

	def gettriedimage(self):
		return self.getkey() in save.triedimage

	def settriedimage(self):
		if not self.getkey() in save.triedimage:
			save.triedimage.add(self.getkey())

	def pressed(self):
		app.enterfolder(self)

	def getepnumber(self):
		if self.getname()[1] != None:
			return self.getname()[1]
		else:
			if self.getchildren() != None:
				thisep = None
				for child in self.getchildren():
					ep = child.getepnumber()
					if ep != None:
						if thisep == None:
							thisep = ep
						elif ep > thisep:
							if child.getwatched():
								thisep = ep
				return thisep
			return None

	def getshow(self):
		if self.getparent() == None:
			return None
		return self.getparent().getshow()
		
	def gettracks(self):
		if not self.getkey() in save.tracks.keys():
			return self.defaulttracks()
		return save.tracks[self.getkey()]

	def defaulttracks(self):
		return [None, None]
		
	def settracks(self, tracks):
		save.tracks[self.getkey()] = tracks

class allshowsclass(pathobj):
	"""Root for shows"""

	def __init__(self):
		self.shows = []

	def getchildren(self):
		allstrshoweps = []
		for show in self.shows:
			if isinstance(show, strshow):
				allstrshoweps += show.getchildren()

		# check for new shows
		for pathname in os.listdir(tvfolder):
			path = os.path.join(tvfolder, pathname)
			if os.path.isdir(path):
				foundpath = False
				for show in self.shows:
					if isinstance(show, foldershow):
						if os.path.normpath(show.path) == os.path.normpath(path):
							foundpath = True
							break
				if not foundpath:
					self.shows.append(foldershow(path))
			else:
				foundpath = False
				for ep in allstrshoweps:
					if os.path.normpath(ep.path) == os.path.normpath(path):
						foundpath = True
						break
				if not foundpath:
					newshow = newstrshowfromep(path)
					print newshow.showstr
					self.shows.append(newshow)
					allstrshoweps += newshow.getchildren()

		# check plugins' shows
		for plugin in plugins:
			newshows = plugin.getshows()
			for newshow in newshows:
				if not newshow in self.shows:
					self.shows.append(newshow)

		# check for deleted shows
		showstoremove = []
		for show in self.shows:
			if not show.exists():
				showstoremove.append(show)
		for show in showstoremove:
			self.shows.remove(show)

		return self.shows

	def getname(self):
		return ["TV Shows", None]

class show(pathobj):
	def __init__(self):
		pathobj.__init__(self)

	def getparent(self):
		return save.allshows

	def delete(self):
		with open(deletedfile, "a") as myfile:
			myfile.write(self.getname()[0] + "\n")

		for child in self.getchildren():
			child.delete()

	def getshow(self):
		return self

class foldershow(show):
	"""Shows which are an actual folder"""

	def __init__(self, path):
		show.__init__(self)
		self.path = path

	def getkey(self):
		return self.path

	def getchildren(self):
		children = []
		for pathname in os.listdir(self.path):
			if not pathname.startswith(".") and not pathname in ignore:
				path = os.path.join(self.path, pathname)
				if os.path.isdir(path):
					children.append(folder(path, self))
				else:
					children.append(episode(path, self))
		return children

	def exists(self):
		return os.path.exists(self.path)

	def getpathname(self):
		return os.path.basename(self.path)

	def defaultname(self):
		return [changename(self.getpathname(), takeoutnumbers=True, dosearch=dogooglesearch, title=True), None]

	def defaultcreated(self):
		return getcreatedtime(self.path)

	def delete(self):
		show.delete(self)
		os.rmdir(self.path)

def stripname(name, stripnums = True):
	"""Episode name -> string which is the same for all episodes in the same show"""
	for pattern in removestuffregex:
		name = re.sub(pattern, "", name)
	if stripnums:
		name = re.sub(numberregex, "", name)
	for pattern in removestuff:
		name = name.replace(pattern, "")
	return name

class strshow(show):
	"""Guesses which files belong to the same show"""

	def __init__(self, showstr):
		show.__init__(self)
		self.showstr = showstr

	def getchildren(self):
		children = []
		for pathname in os.listdir(tvfolder):
			path = os.path.join(tvfolder, pathname)
			showstr = stripname(self.showstr)
			if not os.path.isdir(path):
				if stripname(pathname) == showstr:
					children.append(episode(path, self))
		return children

	def defaultname(self):
		return [changename(self.getpathname(), takeoutnumbers=True, dosearch=dogooglesearch, title=True), None]

	def exists(self):
		if self.getchildren() == []:
			return False
		else:
			return True

	def getpathname(self):
		name = self.showstr
		if "." in name:
			name = name.rsplit(".", 1)[0]
		return name

def newstrshowfromep(ep_path):
	epname = os.path.basename(ep_path)
	return strshow(stripname(epname))

class filesyspath(pathobj):
	def __init__(self, path, up):
		pathobj.__init__(self)
		self.path = path
		self.up = up

	def getkey(self):
		return self.path

	def getparent(self):
		return self.up

	def exists(self):
		return os.path.exists(self.path)

	def getpathname(self):
		return os.path.basename(self.path)

	def defaultcreated(self):
		return getcreatedtime(self.path)

	def defaultname(self):
		namedir(self.up.getchildren())
		if not self.getkey() in save.names.keys():
			save.names[self.getkey()] = self.getpathname()
		return save.names[self.getkey()]

class episode(filesyspath):
	def __init__(self, path, up):
		filesyspath.__init__(self, path, up)

	def getsize(self):
		return os.path.getsize(self.path)

	def delete(self):
		print "DELETING:", self.path
		os.remove(self.path)

	def pressed(self):
		self.setwatched(True)
		self.getparent().setlastwatched(time.gmtime())
		app.select_down()
		app.refresh()
		path = self.path

		for plugin in plugins:
			plugin.onplayepisode(self)
			
		show = self.getshow()
		a, s = show.gettracks()

		if save.usempv:
			new_env = os.environ.copy()
#			new_env["VDPAU_DRIVER"] = "va_gl"
#			new_env["DRI_PRIME"] = "1"
			command = ["mpv", path, "--fullscreen", "--input-conf="+mpvinputconf] # "--display-fps=60",
#			if save.usebumblebee:
#				command = ["primusrun"] + command + ["--vo=opengl-hq:scale=ewa_lanczossharp"]
			if a != None:
				command += ["--aid="+a]
			if s != None:
				command += ["--sid="+s]
			for plugin in plugins:
				env, before, after = plugin.changecommand()
				for key, value in env:
					new_env[key] = value
				command = before + command + after
			print "Running:", command
			subprocess.Popen(command, env=new_env)
		else:
			subprocess.Popen(["smplayer", "-fullscreen", "-close-at-end", path])


class folder(filesyspath):
	"""Folders which aren't shows"""

	def __init__(self, path, up):
		filesyspath.__init__(self, path, up)

	def getchildren(self):
		children = []
		for pathname in os.listdir(self.path):
			path = os.path.join(self.path, pathname)
			if os.path.isdir(path):
				children.append(folder(path, self))
			else:
				children.append(episode(path, self))
		return children

	def defaultname(self):
		return [changename(self.getpathname(), takeoutnumbers=False, dosearch=False, title=True), None]

	def delete(self):
		for child in self.getchildren():
			child.delete()
		os.rmdir(self.path)

class KMCApp(App):
	"""Main Class"""
	def build(self):
		Window.clearcolor = (0,0,0,0)

		self.imagesloaders = {}

		self.sm = ScreenManager()

		""" Main Screen """

		self.defaultscreen = Screen(name="default")
		self.sm.add_widget(self.defaultscreen)

		self.sm.current = "default"

		fllayout = FloatLayout()

		self.downloadedinfo = {}

		self.defaultscreen.add_widget(fllayout)

		self.imageloader = None

		self.backgroundimage = Image(pos_hint={'center_x':.5, 'center_y':.5}, size_hint=[1,3], allow_stretch=True)
		fllayout.add_widget(self.backgroundimage)

		contentlayout = FloatLayout(pos_hint={'center_x':.5, 'center_y':.5}, size_hint=[1,1])
		fllayout.add_widget(contentlayout)

		leftsidelayout = FloatLayout(pos_hint={'center_x':.325, 'center_y':.5}, size_hint=(.65, 1))
		contentlayout.add_widget(leftsidelayout)

		sidebarlayout = FloatLayout(pos_hint={'center_x':.85, 'center_y':.5}, size_hint=[.3, 1])
		contentlayout.add_widget(sidebarlayout)
		
		if not useblur:
			rightback = GradientWidget(colors=(backgroundinvisible, backgroundcolor), pos_hint={'center_x':.5, 'center_y':.5}, size_hint=[1,1])
			sidebarlayout.add_widget(rightback)

		buttons = []

		self.clock = clock(pos_hint={'center_x':.5, 'center_y':.825}, size_hint=[1,.15])
		sidebarlayout.add_widget(self.clock)

		self.buttonspacing = 5

		if not useblur:
			leftback = GradientWidget(colors=(backgroundcolor, backgroundinvisible), pos_hint={'center_x':.5, 'center_y':.5}, size_hint=[1,1])
			leftsidelayout.add_widget(leftback)

		self.layout = BoxLayout(orientation="vertical", pos_hint={'center_x':.5, 'center_y':.5}, size_hint=(1, 1), spacing=self.buttonspacing)
		leftsidelayout.add_widget(self.layout)

		self.layoutheight = 15
		self.layouttop = 0

		self.titlelabel = gradientButton(text="hi", pos_hint={'center_x':.5, 'center_y':1-.05}, valign="top", size_hint=(1, .1), font_name=mainfont, color=textcolor, font_size="40sp")
		sidebarlayout.add_widget(self.titlelabel)

		self.buttons = []

		self.namedisplay = "name"

		self.infolder = None

		self.showwatched = True

		self.selectedindex = 0

		Window.bind(mouse_pos=self.mouse_pos)
		Window.bind(on_motion=self.on_motion)
		self.scrolltimer = 0
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)

		self.enterfolder(save.allshows)

		Clock.schedule_interval(self.lookfordownloadupdate, 60)

		optionlayout = BoxLayout(orientation="vertical", pos_hint={'center_x':.5, 'center_y':.35}, size_hint=[1,.7], spacing=self.buttonspacing)
		sidebarlayout.add_widget(optionlayout)

		if showupdown:
			updown = BoxLayout(orientation="horizontal", pos_hint={'center_x':.85, 'center_y':.5}, size_hint=[.3,1], spacing=0)
			optionlayout.add_widget(updown)

		self.options = {}

		options = []
		if showupdown:
			options += [[u"\u25b3", self.select_up, updown], [u"\u25bd", self.select_down, updown]]

		# buttons to the right
		options += [["Play", self.dobutton], ["Up", self.esc], ["Refresh", self.refresh],
			["Delete", self.delete], ["Folder Rename", self.folderrename], ["Rename", self.rename],
			["Change Image", self.imageselector], ["Change Tracks", self.changetracks], ["Settings", self.showsettings]]
		for plugin in plugins:
			options += plugin.getoptions()
		options += [["Toggle Watched", self.togglewatched], ["Show Full Names", self.togglenamedisplay],
			["Sort", self.togglesort], ["Show Watched", self.toggleshowwatched]]


		for opt in options:
			parent = optionlayout
			if len(opt) > 2:
				parent = opt[2]
			text, command = opt[0], opt[1]
			button = gradientButton()
			parent.add_widget(button)
			button.font_size='30sp'
			button.font_name = mainfont
			button.text = text
			button.color = textcolor
			button.bind(on_press=partial(self.runcommand, command))

			self.options[text] = button

		self.togglesort(toggle=False)

		""" Google Images image selector screen """

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
		self.nextimgpageb.bind(on_press=self.cancelimagedownload)
		self.imgwin.add_widget(self.nextimgpageb)

		self.localimgbutton = Button(text="From File", size_hint=[.15, .05], pos_hint={'center_x':.2, 'center_y':.1})
		self.localimgbutton.bind(on_press=self.localimageselector)
		self.imgwin.add_widget(self.localimgbutton)

		""" Settings Screen """

		self.settingsscreen = Screen(name="settings")
		self.sm.add_widget(self.settingsscreen)

		self.settingsscroll = ScrollView()
		self.settingsscreen.add_widget(self.settingsscroll)

		self.settingsgrid = GridLayout(cols=2, spacing=10, size_hint=[1, None])
		self.settingsscroll.add_widget(self.settingsgrid)

		def getcheckbox (checkbox):
			return checkbox.active
		def setcheckbox(checkbox, active):
			checkbox.active = active

		# label, widget, save variable, getter, setter

		self.settings = [
			["Use MPV", CheckBox(), "usempv", getcheckbox, setcheckbox]
#			["Use Bumblebee", CheckBox(), "usebumblebee", getcheckbox, setcheckbox]
			]

		for plugin in plugins:
			self.settings += plugin.getsettings()

		for labeltext, widget, savevar, getter, setter in self.settings:
			label = Label(text=labeltext)
			self.settingsgrid.add_widget(label)
			self.settingsgrid.add_widget(widget)
			if savevar != None:
				setter(widget, getattr(save, savevar))

		self.settingscancel = Button(text="Cancel")
		self.settingscancel.bind(on_press=partial(self.finishsettings, False))
		self.settingsgrid.add_widget(self.settingscancel)

		self.settingsok = Button(text="Done")
		self.settingsok.bind(on_press=partial(self.finishsettings, True))
		self.settingsgrid.add_widget(self.settingsok)

		""" End of building screens """

		for show in save.allshows.getchildren():
			name = show.getname()[0]
			save.watchedset.add(name)

		Clock.schedule_once(self.onstart)

		return self.sm

	def onstart(self, *args):
		for plugin in plugins:
			plugin.onstart()

	def runcommand(self, command, *args):
		command()

	def delete(self):
		popupaskconfirmation("Delete", "Delete?", method=self.finishdelete)
#		if tkMessageBox.askyesno("Delete", "Delete?", default="no"):

	def finishdelete(self):
		ep = self.buttons[self.selectedindex].ep
		ep.delete()

		self.refresh()

	def lookfordownloadupdate(self, *args):
		self.refresh()

	def enterfolder(self, folder, up=False):
		self.infolder = folder

		name, epnumber = self.infolder.getname()
		if name == None:
			name, epnumber = self.infolder.defaultname()

		self.titlelabel.text = name

		self.refresh()
		self.refreshimage()
		self.refreshdownloadedfrominfo()

	def refresh(self, *args):
		l = self.infolder.getchildren()

		if not save.showwatched and self.infolder == save.allshows:
			l = [child for child in l if not child.getwatched()]

		scrollstate = self.infolder.getscrollstate()
		if len(scrollstate) == 2:
			selectindex, top = scrollstate
			name=None
		else:
			selectindex, top, name = scrollstate

		self.populatebuttons(l)

		self.layouttop = top

		for index, button in enumerate(self.buttons):
			if button.name == name:
				selectindex = index
				break

		self.select(selectindex)

	def clearbuttons(self):
		self.layout.clear_widgets()

	def populatebuttons(self, l):
		self.buttons = []

		allfiles = [[] for f in l]

		for index, ep in enumerate(l):
			name, epnumber = ep.getname()
#			newname = ''.join([i if ord(i) < 128 else '?' for i in name])
#			if newname != name:
#				print newname
#				ep.setname([newname, None])
#				name = newname
			allfiles[index] = [ep, name, epnumber]

		allfiles.sort(key=lambda f : f[1])
		allfiles.sort(key=lambda f : f[2])

		if self.infolder == save.allshows:
			if save.sort == SORT_WATCHED:
				allfiles.sort(key=lambda f : f[0].getlastwatched(), reverse=True)
			elif save.sort == SORT_CREATED:
				allfiles.sort(key=lambda f : f[0].getcreated(), reverse=True)
			elif save.sort == SORT_SIZE:
				allfiles.sort(key=lambda f : f[0].getsize(), reverse=True)

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

		if len(self.buttons) == 0:
			if self.infolder == save.allshows:
				text = "There are no TV Shows in\n" + tvfolder
			else:
				if hasattr(self.infolder, "path"):
					text = "There are no files in\n" + self.infolder.path
				else:
					text = "There are no files here\n"
			text += "\nTry adding some!"
			b = abutton(notafile, self, text)
			self.buttons.append(b)

		self.select(0, True)

	def loadimage(self, imgpath):
		proxyimage = Loader.image(imgpath)
		self.imagesloaders[imgpath] = proxyimage

	def loadimages(self):
		dirs = [d for d in save.images.keys()]
		for d in dirs:
			print save.images[d]
			imgpath = save.images[d]
			self.loadimage(imgpath)

	def refreshimage(self):
		if self.infolder == save.allshows:
			path = self.buttons[self.selectedindex].ep
		else:
			path = self.buttons[self.selectedindex].showfolder

		imgpath = path.getimage()

		self.imageloader = Loader.image(imgpath)
		self.imageloader.bind(on_load=self.imageloaded)
		self.imageloaded()

	def imageloaded(self, *args):
		if self.imageloader.loaded:
			self.backgroundimage.texture = self.imageloader.image.texture

	def selectbutton(self, b):
		self.select(self.buttons.index(b))

	def select(self, newindex, override=False, noscroll=False):
		if newindex < 0 or newindex >= len(self.buttons):
			return

		try:
			self.buttons[self.selectedindex].unselect()
		except IndexError:
			pass
		self.selectedindex = newindex
		selectedbutton = self.buttons[newindex]
		selectedbutton.select()

		if self.infolder == save.allshows:
			self.refreshimage()

		self.clearbuttons()

		if self.selectedindex > self.layouttop+self.layoutheight-1:
			self.layouttop = self.selectedindex - self.layoutheight+1
		elif self.selectedindex < self.layouttop:
			self.layouttop = self.selectedindex

		for i in range(self.layouttop, self.layouttop+self.layoutheight):
			if i < len(self.buttons):
				b = self.buttons[i]
				self.layout.add_widget(b)

		self.infolder.setscrollstate([self.selectedindex, self.layouttop, self.buttons[self.selectedindex].name])

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
		if not popuphasfocus:
			if motionevent.button == "scrollup":
				self.scroll(direction=-1)
			elif motionevent.button == "scrolldown":
				self.scroll(direction=1)

	def mouse_pos(self, instance, value):
		x, y = value
		for b in self.buttons:
			if b.collide_point(x, y):
				b.hover()

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

	def select_down(self):
		if self.selectedindex != len(self.buttons) - 1:
			self.select(self.selectedindex + 1)

	def select_up(self):
		if self.selectedindex != 0:
			self.select(self.selectedindex - 1)


	def rename(self):
		loc = self.buttons[self.selectedindex].ep
		oldname = loc.getname()
		popupaskstring("Rename", loc.getpathname(), default=oldname[0], method=partial(self.finishrename, loc))
#		newname = tkSimpleDialog.askstring("Rename", loc.getpathname(), initialvalue=oldname[0], parent=root)

	def finishrename(self, loc, newname):
		if newname == "":
			del save.names[loc.getkey()]
		elif newname != None:
			if newname.isdigit():
				loc.setname([oldname[0], int(newname)])
			else:
				loc.setname([newname, None])
		self.refresh()

	def esc(self):
		saveclassinst.dosave()
		if self.infolder == save.allshows:
			EventLoop.close()
		else:
			if self.allwatched():
				self.infolder.setwatched(True)
			self.enterfolder(self.infolder.getparent())

	def dobutton(self):
		self.buttons[self.selectedindex].pressed()

	def folderrename(self):
		popupaskconfirmation("Rename", "Rename this directory?", method=self.finishfolderrename)
#		if tkMessageBox.askyesno("Rename", "Rename this directory?"):

	def finishfolderrename(self):
		print "rename"
		namedir(self.infolder.getchildren(), True)
		self.refresh()

	def imageselector(self):
		path = None
		if self.infolder == save.allshows:
			path = self.buttons[self.selectedindex].ep
		else:
			path = self.buttons[self.selectedindex].showfolder

		if path != None:
			self.pickimage(path)

	def localimageselector(self, *args):
		popupaskfile("Image", "Select new image file", folder=imagesfolder, method=self.finishlocalimageselector)
#		filename = askopenfilename(initialdir=imagesfolder)

	def finishlocalimageselector(self, filename):
		path = self.imageloc

		if filename != None:
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
		save.showwatched = not save.showwatched
		self.refresh()

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		if not popuphasfocus:
			key = keycode[1]
			if key == 'up':
				self.select_up()
			elif key == 'down':
				self.select_down()
			elif key == "escape":
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
					thebutton = None
					if "Progress: " in atorrent:
						progress = atorrent.split("Progress: ", 1)[1].split("%", 1)[0]
						self.downloadedinfo[name] = progress

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
		for f in self.downloadedinfo:
			progress = self.downloadedinfo[f]
			for b in self.buttons:
				if os.path.basename(b.path) == f:
					b.setprogress(progress)

	def pickimage(self, loc, page=0):
		self.imagepage = page
		self.imageloc = loc

		self.imgpage.text = "Page: " + str(self.imagepage+1)

		self.sm.current = "images"

		self.imgwinlist.clear_widgets()

		gimages = findimage(loc, page=page)

		for gimage in gimages:
			url = gimage.previewurl

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

			button.add_widget(img)
			self.imgwinlist.add_widget(button)

	def nextimgpage(self, *args):
		self.pickimage(self.imageloc, page=self.imagepage+1)

	def cancelimagedownload(self, *args):
		self.sm.current = "default"
		
	def changetracks(self):
		show = self.buttons[self.selectedindex].ep.getshow()
		at, st = show.gettracks()
		if at == None:
			at = ""
		if st == None:
			st = ""
		at, st = str(at), str(st)
		f = BoxLayout(orientation="vertical")
		al = Label(text="Audio:")
		f.add_widget(al)
		atext = TextInput(text=at)
		f.add_widget(atext)
		sl = Label(text="Subtitles:")
		f.add_widget(sl)
		stext = TextInput(text=st)
		f.add_widget(stext)
		popupmessage("Change tracks", "Enter track number\nor leave blank for default", content=f, options=[["OK", partial(self.finishchangetracks, show, atext, stext)], ["Cancel", None]], cleanup=partial(unfocustextinput, atext, stext))
		
	def finishchangetracks(self, show, atext, stext):
		a = atext.text
		s = stext.text
		if a == "":
			a = None
		
		if s == "":
			s = None
		
		show.settracks([a,s])

	def doimagedownload(self, loc, gimage, *args):
		result = None
		if gimage != None:
			url = gimage.url
			temp = downloadtempimage(url)
			result = self.setimage(loc, temp)
		self.sm.current="default"
		return result

	def setimage(self, tvpath, imgpath):
		if tvpath.hasimage():
			path = tvpath.getimage()
			basename = os.path.basename(path)
			number = basename.rsplit(".", 2)
			if len(number) == 3:
				number = int(number[1])
				number += 1
			else:
				number = 1
			if os.path.exists(path):
				os.remove(path)
		else:
			number = 1

		ending = "png"
		middle = "." + str(number)
		newimagename = tvpath.getpathname() + middle + "." + ending
		downloadfolder = imagesfolder
		newimagepath = os.path.join(downloadfolder, newimagename)

		try:
			img = Image(source=imgpath)
			img.texture.save(newimagepath)
			tvpath.setimage(newimagepath)
			self.loadimage(newimagepath)

			self.refreshimage()

			return True
		except Exception as e:
			print e
			print "Could not open file"

			return False

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
		elif save.sort == SORT_SIZE:
			button.text = "Sort: Size"

		self.refresh()

	def showsettings(self):
		self.sm.current = "settings"

	def finishaskstring(self, text):
		print text

	def finishsettings(self, dosave, widget):
		if dosave:
			for labeltext, widget, savevar, getter, setter in self.settings:
				if savevar != None:
					setattr(save, savevar, getter(widget))
		self.sm.current = "default"

	def getkeyboard(self):
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)

saveclassinst = saveclass()
save = saveclassinst.savestatevar

notafile = episode(os.path.join(tvfolder, "NOTAFILE"), save.allshows)
save.images[notafile.getkey()] = defaultimageloc

app = KMCApp()
subprocess.Popen("wmctrl -r \":ACTIVE:\" -b toggle,fullscreen", shell=True)
app.run()

for plugin in plugins:
	plugin.onclose()
#root.destroy()
