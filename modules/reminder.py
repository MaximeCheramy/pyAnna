# -*- coding: utf-8 -*-
from module import Module
import time 
from time import strftime 
import datetime 
from datetime import date 
import threading

class Reminder(Module):
	_dico = {}
	_dico_private = {}
	_thread = None
	_continuer = True

	def __init__(self, room):
		self.room = room
		self._thread=threading.Thread(target=self.rappeler)
		self._thread.start()
	
	def __del__(self):
		_continuer = False
		self._thread.join()

	def ecrire_rappel(self, msg, to=None):
		# On splitte le message
		heure = msg[8:10]
		minutes = msg[11:13]
		# On vérifie : 
		if heure != '' and minutes != '':
			# On essaye de les mettre en int (si s'en est pas => exception)
			valide = True
			try:
				heure = int(heure)
				minutes = int(minutes)
			except ValueError:
				valide = False
			# On vérifie qu'il n'y ait pas de gros lourd qui tente de faire crasher Anna
			if heure >= 24 or heure < 0 or minutes >= 60 or minutes < 0:
				valide = False
			
			if valide:
				# On créé un tps de rappel
				t_rappel = datetime.datetime(1,1,1, heure, minutes, 00)
				# On enregistre le message aussi
				m_rappel = msg[14:]
				# On ne met pas de rappel pour un message vide...
				if m_rappel != '':
					if not to:
						# On mets les deux dans un dico pour les rappels généraux
						if t_rappel in self._dico:
							self._dico[t_rappel].append(m_rappel)
						else:
							self._dico[t_rappel] = [m_rappel]
						# On annonce que c'est OK
						self.room.send_message("Rappel enregistré pour "+str(heure)+"h"+str(minutes)+" , message : "+m_rappel)
					else:
						# On mets les deux dans un tableau pour les rappels private
						if t_rappel in self._dico_private:
							self._dico_private[t_rappel].append((m_rappel, to))
						else:
							self._dico_private[t_rappel] = [(m_rappel, to)]
						# On annonce que c'est OK
						self.room.send_private_message("Rappel enregistré pour "+str(heure)+"h"+str(minutes)+" , message : "+m_rappel, to)
	
	def rappeler(self):
		while self._continuer:
			Current_Time = datetime.datetime(1,1,1,int(time.strftime("%H")), int(time.strftime("%M")),  int(time.strftime("%S")) )
			# On regarde si l'évènement est dans le dictionnaire "normal"
			if Current_Time in self._dico:
				for e in self._dico[Current_Time]:
					self.room.send_message("RAPPEL ("+str(Current_Time)[11:]+") : "+e)
					self._dico[Current_Time].remove(e)

			# On regarde si l'évènement est dans le dictionnaire "private"
			if Current_Time in self._dico_private:
				for e in self._dico_private[Current_Time]:
					self.room.send_private_message("RAPPEL ("+str(Current_Time)[11:]+") : "+e[0], e[1])
					self._dico_private[Current_Time].remove(e)
			time.sleep(1)

	def handle_message(self, msg):
		if msg['body'].lower() == "!help":
			time.sleep(0.5)
			self.room.send_message("- !rappel 20h17 Prendre ma brosse à dents : Vous affichera un rappel à 20h17 pour ne pas oublier ^^")
		elif msg['body'][:7] ==  "!rappel":
			self.ecrire_rappel(msg['body'])

	def handle_private_message(self, msg, to):
		if msg['body'][:7] == "!rappel":
			self.ecrire_rappel(msg['body'], to)
