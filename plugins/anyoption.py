#!/usr/bin/env python

class anyoptionplugin(plugin):
	def changecommand(self):
		args = self.getarg()
		return [[], [], args.split(" ")]

	def getsavevars(self):
		return [["anyoptions", {}]]
	
	def getoptions(self):
		return [["Mpv Arguments", self.changearg]]
	
	def changearg(self, *args):
		popupaskstring("Mpv Arguments", "Change command-line arguments to mpv", self.setarg, default=self.getarg())
	
	def getep(self):
		return app.buttons[app.selectedindex].ep
	def getkey(self):
		return self.getep().getshow().getkey()
	def getarg(self):
		if self.getkey() in save.anyoptions:
			return save.anyoptions[self.getkey()]
		return ""
	def setarg(self, arg):
		save.anyoptions[self.getkey()] = arg

theanyoptionplugin = anyoptionplugin()
