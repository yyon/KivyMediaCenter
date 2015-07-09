#!/usr/bin/env python

def getcheckbox (checkbox):
	return checkbox.active
def setcheckbox(checkbox, active):
	checkbox.active = active

class bumblebeeplugin(plugin):
	def changecommand(self):
		env = [["VDPAU_DRIVER", "va_gl"], ["DRI_PRIME", "1"]]
		if save.usebumblebee:
			before = ["primusrun"]
			after = ["--vo=opengl-hq:scale=ewa_lanczossharp"]
		else:
			before = []
			after = []
		return [env, before, after]

	def getsavevars(self):
		return [["usebumblebee", False]]

	def getsettings(self):
		return [["Use Bumblebee", CheckBox(), "usebumblebee", getcheckbox, setcheckbox]]

actualplugin = bumblebeeplugin()
