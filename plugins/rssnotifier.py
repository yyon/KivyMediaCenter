#!/usr/bin/env python

import feedparser

class textsaver(object):
	vartext = ""

	def __init__(self, title, text):
		self.title = title
		self.text = text

	def getbutton(self):
		b = Button(text="Click to change")
		b.bind(on_press=self.onbutton)
		return b

	def onbutton(self, *args):
		popupaskstring(self.title, self.text, method=self.onpopup, default=self.vartext)

	def onpopup(self, newtext):
		self.vartext = newtext

	def set(self, button, newtext):
		self.vartext = newtext

	def get(self, button):
		return self.vartext

class rssplugin(plugin):
	def onstart(self):
		read_list = save.rssreadlist
		rssloc = save.rssloc
		if rssloc != "":
			d = feedparser.parse(rssloc)

			newnames = []

			for e in d.entries:
				name = e.summary_detail.value
				name = name.encode("ascii", "ignore")
				if not name in read_list:
					read_list.append(name)
					newnames.append(name)

			if newnames != []:
				popupmessage("New RSS Entry", "New RSS entries:\n\n" + "\n".join(newnames))

			save.rssreadlist = read_list
		else:
			print "Warning: no RSS feed location"

	def getsavevars(self):
		return [["rssreadlist", []], ["rssloc", ""]]

	def getsettings(self):
		ts = textsaver("RSS", "RSS feed location:")
		return [["Rss feed location", ts.getbutton(), "rssloc", ts.get, ts.set]]

actualplugin = rssplugin()
