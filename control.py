import re

class Control:
	def __init__(self, xmpp):
		self._xmpp = xmpp

	def handle_message(self, msg, to):
		send = lambda m: self.room.send_private_message(m, to)
		commands = re.compile("^(\\S+)\\s+(\\S+)\\s*(.*)$")
		fit = commands.match(msg['body'])
		if fit:
			if fit.groups()[0] == 'say':
				for room in self._xmpp._rooms:
					if room.get_roomname() == fit.groups()[1]:
						room.send_message(fit.groups()[2])
						break
			elif fit.groups()[0] == 'load':
				for room in self._xmpp._rooms:
					if room.get_roomname() == fit.groups()[1]:
						room.load_module(fit.groups()[2])
						break
