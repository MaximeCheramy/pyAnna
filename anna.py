#!/usr/bin/env python

import logging
import sleekxmpp
import room
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
		sleekxmpp.ClientXMPP.__init__(self, jid + "/" + resource, password)
		self._rooms = []

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

if __name__ == "__main__" :
	main()
