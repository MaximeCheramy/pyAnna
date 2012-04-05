# -*- coding: utf-8 -*-
import urllib, time
from module import Module

class Whois(Module):
	URL = 'https://www.etud.insa-toulouse.fr/modules/insannuaire/whois.php?login='

	def __init__(self, room):
		self.room = room

	def whois(self, send, msg, name):
		data = urllib.urlopen(Whois.URL + name, proxies={}).read().split("\n")
		if data[0] == 'ok=1':
			nom = data[1].split("=", 1)[1]
			prenom = data[2].split("=", 1)[1]
			send('Prenom : ' + prenom)
			send('Nom : ' + nom)
		else:
			send('Aucune information trouvee.')

	def whois_(self, send, msg):
		message = msg['body'].split(" ", 1)
		if len(message) == 2 and message[0] == "!whois":
			message[1] = message[1].strip()
			if message[1] == self.room.get_botname():
				send("C'est moi !!! :D")
			else:
				roster = self.room.get_roster()
				if message[1] in roster:
					jid = str(self.room.get_jid(message[1]))
					self.whois(send, msg, jid.split('@', 1)[0])
				else:
					self.whois(send, msg, message[1])
		
	def handle_message(self, msg):
		if msg['body'] == '!help':
			time.sleep(0.5)
			self.room.send_message("- !whois : Donne le nom et prénom du pseudo passé en paramètre")
		send = lambda m: self.room.send_message(m)
		self.whois_(send, msg)

	def handle_private_message(self, msg, to):
		send = lambda m: self.room.send_private_message(m, to)
		self.whois_(send, msg)
