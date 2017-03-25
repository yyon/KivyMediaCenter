#!/usr/bin/env python

from trackma.engine import Engine
from trackma.accounts import AccountManager

import trackma.messenger as messenger
import trackma.utils as utils

from kivy.uix.togglebutton import ToggleButton
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner


from subprocess import Popen

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

class trackmaplugin(plugin):
	shows = []
	auto = True
	showstoupdate = []

	def __init__(self):
		plugin.__init__(self)

		self.accountman = Trackma_accounts()
		self.account = self.accountman.select_account(False)

		print 'Initializing trackma engine...'
		self.engine = Engine(self.account, self.messagehandler)
#		self.engine.connect_signal('show_added', self._load_list)
#		self.engine.connect_signal('show_deleted', self._load_list)
#		self.engine.connect_signal('status_changed', self._load_list)
#		self.engine.connect_signal('episode_changed', self._load_list)
		self.engine.start()

#	def _load_list(self, *args):
#		self.showlist = self.engine.filter_list(1)

	def onstart(self):
#		for show in save.allshows:
		showstofind = []
		print "MALNAMES: ", save.malnames
		for show in save.allshows.shows:
			if not show.getkey() in save.malnames.keys():
				showstofind.append(show)

		self.searchshows(showstofind)

	def onplayepisode(self, ep):
		show = ep.getshow()
		if show != None:
			if not show in self.showstoupdate:
				self.showstoupdate.append(show)

	def updateallshows(self):
		for show in save.allshows.shows:
			self.update(show)

	def searchshows(self, shows, auto=True):
		self.auto = auto
		self.shows = shows
		self.nextshow()

	def nextshow(self):
		if self.shows != []:
			self.findshow(self.shows.pop())

	def search(self, name):
		try:
			return self.engine.search(name)
		except utils.TrackmaError, e:
			if str(e) == "No results.":
				return []
			else:
				print("Trackma error")
				return []
				#raise e

	def updateshowlist(self, showlist, textbox):
		self.buttons = {}

		name = textbox.text

		showlist.clear_widgets()

		if self.auto:
			entries = self.search(name)
			if entries == []:
				l = Label(text="No results.")
				showlist.add_widget(l)
				return

		self.spinner = Spinner(text = entries[0]["title"], values = [e["title"] for e in entries])
		showlist.add_widget(self.spinner)
		for i, entry in enumerate(entries):
			self.buttons[entry["title"]] = entry
		"""
			b = ToggleButton(text=entry["title"], group="showlist", size_hint=[None, 1], height=40)
			if i == 0:
				b.state = "down"
			showlist.add_widget(b)
#			print "%d: (%s) %s" % (i, entry['type'], entry['title'])
		"""


	def findshow(self, show):
		name = show.getname()[0]
		if type(name) == str:
			name = ''.join([i if ord(i) < 128 else '?' for i in name])

		entries = self.search(name)
		if len(entries) == 1:
			self.setshow(show, entries[0])
		else:
			vbox = BoxLayout(orientation="vertical", size_hint=[1,.8])
			textbox = TextInput(text=name, multiline=False, size_hint=[1, .2])
			vbox.add_widget(textbox)
			showlist = BoxLayout(orientation="vertical", size_hint=[1, .8])
			vbox.add_widget(showlist)

			textbox.bind(on_text_validate=partial(self.updateshowlist, showlist))
			self.updateshowlist(showlist, textbox)

			popupmessage("Select show", "Select show for\n" + name + "\n" + show.getpathname(), content=vbox, options=[["OK", partial(self.finishpopup, show, True)], ["Don't rename", partial(self.finishpopup, show, False)], ["Cancel", None]], cleanup=partial(unfocustextinput, textbox))

	def finishpopup(self, show, rename=True):
		entry = None
		selection = self.spinner.text
		if selection in self.buttons:
			entry = self.buttons[selection]
#		for b in self.buttons:
#			if b.state == "down":
#				entry = self.buttons[b]
#				break

		if entry != None:
			print "Setting show to", selection, entry["id"]
			self.setshow(show, entry)
			show.setname([selection, show.getname()[1]])
			app.refresh()

	def setshow(self, show, entry):
		try:
			self.engine.add_show(entry)
		except utils.TrackmaError, e:
			print(e)

		save.malnames[show.getkey()] = entry["id"]

		self.nextshow()

	def getsavevars(self):
		return [["malnames", {}], ["browsercommand", "xdg-open %U"]]

	def messagehandler(self, classname, msgtype, msg):
		try:
			if msgtype == messenger.TYPE_INFO:
				print "%s: %s" % (classname, msg)
			elif msgtype == messenger.TYPE_WARN:
				print "%s warning: %s" % (classname, msg)
		except UnicodeEncodeError:
			print "couldn't print due to unicode"
#		elif _DEBUG and msgtype == messenger.TYPE_DEBUG:
#			print "%s: %s" % (classname, msg)

	def update(self, show, ep=None):
		if ep == None:
			ep = show.getepnumber()
			if ep == None:
				print "show", show.getname(), "couldn't find episode number"
				return
			else:
				print "show", show.getname(), "episode", ep

		if show.getkey() in save.malnames.keys():
			id = save.malnames[show.getkey()]
			try:
				self.engine.set_episode(id, ep)
			except utils.EngineError, e:
				print e
		else:
			print "show", show.getname(), "doesn't have an id"

#	def getshowbyid(self, id):
#		for show in self.showlist:
#			if show["id"] == id:
#				return show

	def onclose(self):
		for show in self.showstoupdate:
			self.update(show)

		self.engine.unload()

	def getoptions(self):
		return [["Open MAL", self.openmal]]

	def openmal(self):
		loc = app.buttons[app.selectedindex].ep.getshow()
		if loc.getkey() in save.malnames.keys():
			id = save.malnames[loc.getkey()]
			show = self.engine.get_show_info(id)
			url = show["url"]
			cmd = save.browsercommand.replace("%U", url)
			print cmd
			Popen(cmd, shell=True)#["xdg-open", url], shell=True)

	def getsettings(self):
		ts = textsaver("MAL Browser", "Browser Command (%U is url):")
		return [["MAL Browser Command", ts.getbutton(), "browsercommand", ts.get, ts.set]]


class Trackma_accounts(AccountManager):
	def _get_id(self, index):
		if index < 1:
			raise IndexError

		return self.indexes[index-1]

	def select_account(self, bypass):
		if not bypass and self.get_default():
			return self.get_default()
		if self.get_default():
			self.set_default(None)

		while True:
			print '--- Accounts ---'
			self.list_accounts()
			key = raw_input("Input account number ([r#]emember, [a]dd, [c]ancel, [d]elete, [q]uit): ")

			if key.lower() == 'a':
				available_libs = ', '.join(sorted(utils.available_libs.iterkeys()))

				print "--- Add account ---"
				import getpass
				username = raw_input('Enter username: ')
				password = getpass.getpass('Enter password (no echo): ')
				api = raw_input('Enter API (%s): ' % available_libs)

				try:
					self.add_account(username, password, api)
					print 'Done.'
				except utils.AccountError, e:
					print 'Error: %s' % e.message
			elif key.lower() == 'd':
				print "--- Delete account ---"
				num = raw_input('Account number to delete: ')
				try:
					num = int(num)
					account_id = self._get_id(num)
					confirm = raw_input("Are you sure you want to delete account %d (%s)? [y/N] " % (num, self.get_account(account_id)['username']))
					if confirm.lower() == 'y':
						self.delete_account(account_id)
						print 'Account %d deleted.' % num
				except ValueError:
					print "Invalid value."
				except IndexError:
					print "Account doesn't exist."
			elif key.lower() == 'q':
				sys.exit(0)
			else:
				try:
					if key[0] == 'r':
						key = key[1:]
						remember = True
					else:
						remember = False

					num = int(key)
					account_id = self._get_id(num)
					if remember:
						self.set_default(account_id)

					return self.get_account(account_id)
				except ValueError:
					print "Invalid value."
				except IndexError:
					print "Account doesn't exist."

	def list_accounts(self):
		accounts = self.get_accounts()
		self.indexes = []

		print "Available accounts:"
		i = 0
		if accounts:
			for k, account in accounts:
				print "%i: %s (%s)" % (i+1, account['username'], account['api'])
				self.indexes.append(k)
				i += 1
		else:
			print "No accounts."

actualplugin = trackmaplugin()
