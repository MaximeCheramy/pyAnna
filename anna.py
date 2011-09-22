#!/usr/bin/env python
#
# Copyright (C) 2011 - pyAnna
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details at
# http://www.gnu.org/copyleft/gpl.html
# 
# You should have received a copy of the GNU General Public License 
# along with this program; if not, see <http://www.gnu.org/licenses>.
#

import logging
import sleekxmpp
import room
from control import Control
from ConfigParser import ConfigParser

# Uncomment the following line to turn on debugging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(message)s")

def main() :
	bot = Anna()
	bot.register_plugin('xep_0030')
	bot.register_plugin('xep_0045')
	bot.register_plugin('xep_0199')
	if bot.connect():
		bot.process(threaded=False)


class Anna(sleekxmpp.ClientXMPP):
	def __init__(self):
		config = ConfigParser()
		config.read("config.ini")
		jid = config.get("general", "jid")
		resource = config.get("general", "resource")
		password = config.get("general", "password")
		self.owner = config.get("general", "owner")
		sleekxmpp.ClientXMPP.__init__(self, jid + "/" + resource, password)
		self._rooms = []
		self._control = Control(self)

		self.add_event_handler("session_start", self.handle_XMPP_connected)
		self.add_event_handler("message", self.handle_incoming_message)

		for r in config.get("general", "rooms").split(","):
			self._rooms.append(room.Room(self, config.get(r, "room"), config.get(r, "modules").split(','), config.get(r, "botname")))

	def handle_XMPP_connected(self, event):
		self.sendPresence(pstatus = "<3")
		self.getRoster()
		for room in self._rooms:
			room.connect()

	def handle_incoming_message(self, message):
		if message['type'] == 'chat':
			for room in self._rooms:
				if room.get_roomname() == message['from'].bare and message['from'].resource in room.get_roster():
					room.handle_private_message(message, message['from'])
					break
			if message['from'].bare == self.owner:
				self._control.handle_message(message, message['from'])

if __name__ == "__main__" :
	main()
