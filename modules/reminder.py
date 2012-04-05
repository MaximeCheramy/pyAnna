# -*- coding: utf-8 -*-
from module import Module
import time 
from time import strftime 
import datetime 
from datetime import date 
import threading

class Reminder(Module):
	_tab = []
	_tab_private = []
	_thread = None
	_continuer = True

	def __init__(self, room):
		self.room = room
		self._thread=threading.Thread(target=self.rappeler)
		self._thread.start()
	
	def __del__(self):
		_continuer = False
		self._thread.join()

	def ecrire_rappel(self, msg, to):
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

			if valide:
				# On créé un tps de rappel
				t_rappel = datetime.datetime(1,1,1, heure, minutes, 00)
				# On enregistre le message aussi
				m_rappel = msg[14:]
				# On ne met pas de rappel pour un message vide...
				if m_rappel != '':
					if to == '':
						# On mets les deux dans un tableau pour les rappels généraux
						self._tab.append((t_rappel, m_rappel))
						# On annonce que c'est OK
						self.room.send_message("Rappel enregistré pour "+str(heure)+"h"+str(minutes)+" , message : "+m_rappel)
					else:
						# On mets les deux dans un tableau pour les rappels private
						self._tab_private.append((t_rappel, m_rappel, to))
						# On annonce que c'est OK
						self.room.send_private_message("Rappel enregistré pour "+str(heure)+"h"+str(minutes)+" , message : "+m_rappel, to)
	
	def rappeler(self):
		while self._continuer:
			Current_Time = datetime.datetime(1,1,1,int(time.strftime("%H")), int(time.strftime("%M")),  int(time.strftime("%S")) )
			# On parcours le tableau "normal"
			for e in self._tab:
				if e[0] == Current_Time:
					self.room.send_message("RAPPEL ("+str(Current_Time)[11:]+") : "+e[1])
					self._tab.remove(e)
			# On parcours le tableau "spécial"
			for e in self._tab_private:
				if e[0] == Current_Time:
					self.room.send_private_message("RAPPEL ("+str(Current_Time)[11:]+") : "+e[1], e[2])
					self._tab_private.remove(e)
			time.sleep(1)

	def handle_message(self, msg):
		if msg['body'].lower() == "!help":
			time.sleep(0.5)
			self.room.send_message("- !rappel 20h17 Prendre ma brosse à dents : Vous affichera un rappel à 20h17 pour ne pas oublier ^^")
		elif msg['body'][:7] ==  "!rappel":
			self.ecrire_rappel(msg['body'], '')

	def handle_private_message(self, msg, to):
		if msg['body'][:7] == "!rappel":
			self.ecrire_rappel(msg['body'], to)
