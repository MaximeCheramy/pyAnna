import time
class Module:
	def handle_message(self, msg):
		if msg['body'].lower() == '!help':
			time.sleep(0.5)
			self.room.send_message('============ Aide Generale ===========')
		else:
			pass

	def handle_private_message(self, msg, to):
		pass

	def muc_online(self, presence):
		pass

	def muc_offline(self, presence):
		pass    		

