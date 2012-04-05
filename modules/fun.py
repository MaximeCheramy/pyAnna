# coding: utf-8
import random, time
from module import Module

class Fun(Module):
	compteur = 0
	nLyric = 0
	lastmsg = ""

	def __init__(self, room):
		self.room = room
		  		
	def envoyer_salut(self, jid):
		envoyeur = jid.resource
		self.room.send_message("Salut " + envoyeur + " !") 

	def envoyer_bn(self, jid):
		envoyeur = jid.resource
		self.room.send_message("Bonne nuit " + envoyeur) 

	def envoyer_jtm(self, jid):
		envoyeur = jid.resource
		self.room.send_message("Moi aussi je t'aime " + envoyeur) 
	
	def handle_private_message(self, msg, to):
		if msg['body'].lower() == "!time":
			self.room.send_private_message(str(time.strftime('%d/%m/%y %H:%M',time.localtime())), to) 

	def handle_message(self, mesg):
		msg = mesg['body']
		bot = self.room.get_botname().lower()

		if msg.lower() == '!help':
			time.sleep(0.5)
			self.room.send_message("- fun : tout un tas de fonctions à decouvrir!")
		# A DEBUG
		elif (msg.lower() == ("salut " + bot) or msg.lower() == ("lu " + bot) or msg.lower() == ("alu " + bot) or msg.lower() == ("lut " + bot)):
			self.envoyer_salut(mesg['from'])
		# A DEBUG
		elif msg.lower() == ("bn " + bot):
			self.envoyer_bn(mesg['from'])
		elif msg.lower() == "!draco":
			self.room.send_message("Draconoob !") 
		elif msg.lower() == "!littlepea":
			self.room.send_message("Littlepea > Draco") 
		elif msg.lower() == "!smatcher":
			self.room.send_message("/me + Smatcher = <3") 
		elif msg.lower() == "!lolo":
			self.room.send_message("Ah ah ah ah ah") 
		elif msg.lower() == "!paul":
			self.room.send_message("Ce qui en soi est une forme d'echec") 
		elif msg.lower() == "!howler":
			self.room.send_message("Qui pour un cod4 ?") 
		elif msg.lower() == "!jerk":
			self.room.send_message("Jerk > Zwifi") 
		elif "pwned" in msg:
			self.room.send_message("stoi pwned !") 
		elif "emacs" in msg:
			self.room.send_message("vi > emacs") 
		elif msg.lower() == "!pizza":
			self.room.send_message("stoi pizza !") 
		# A DEBUG
		elif (len(msg) >= 4 and "où ?" in msg.lower()) or "où?" in msg.lower():
			self.room.send_message("dtc !") 
		elif msg.lower() == "je t'aime " + bot:
			self.envoyer_jtm(mesg['from'])
		elif msg == "!+1":
			self.compteur += 1 
			self.room.send_message(str(self.compteur)) 
		elif msg == "!-1":
			if(self.compteur > 0):
				self.compteur -= 1 
			self.room.send_message(str(self.compteur)) 
		elif msg == "!0":
			self.compteur = 0 
			self.room.send_message("Compteur remis à 0 !") 
		elif msg.lower() == "!anna":
			if(self.nLyric == 0):
				self.room.send_message("♫ Jag känner en bott, hon heter Anna, Anna heter hon ♫") 
			elif(self.nLyric == 1):
				self.room.send_message("♫ Och hon kan banna, banna dig så hårt ♫") 
			elif(self.nLyric == 2):
				self.room.send_message("♫ Hon röjer upp i våran kanal ♫") 
			else:
				self.room.send_message("♫ Jag vill berätta för dig, att jag känner en bott ♫") 
			self.nLyric = (self.nLyric + 1) % 4 
		elif msg.lower() == "!roll":
			self.room.send_message(str(random.randint(1,6))) 
		elif (msg.lower() == bot+"?") and (mesg['from'].resource == "Jerk"):
			self.room.send_message("Wi mon Jerk?") 
		elif msg.lower() == "!time":
			self.room.send_message(str(time.strftime('%d/%m/%y %H:%M',time.localtime()))) 
		elif self.lastmsg.lower() == msg:
			self.room.send_message(msg) 
			self.lastmsg = "" 
		else:
			self.lastmsg = msg
		

