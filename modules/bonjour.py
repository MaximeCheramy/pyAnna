from module import Module

class Bonjour(Module):
	def __init__(self, room):
		self.room = room

	def muc_online(self, presence):
			self.room.send_message("Salut, %s %s" % (presence['muc']['role'],
                          presence['muc']['nick']))
