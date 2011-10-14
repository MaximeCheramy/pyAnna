#encoding:UTF-8
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

from module import Module
from random import choice
import threading
import time

class Bombe(threading.Thread):
	def __init__(self, attacker, room):
		threading.Thread.__init__(self)
		self.active = True
		self.room = room
		roster = self.room.get_roster()
		roster.remove(self.room.get_botname())
		self.victime = choice(roster)
		if self.victime == attacker:
			self.room.send_message(attacker + " a jeté une bombe sur ses propres pieds ! Mouahaha !")
		else:
			self.room.send_message(attacker + " a jeté une bombe sur les pieds de " + victime + ".")
		self.start()

	def run(self):
		time.sleep(10.0)
		if self.active:
			self.room.send_message("Boom! " + self.victime + " est mort !")

	def defuse(self):
		if self.active:
			self.room.send_message("Bombe désactivée à temps !")
			self.active = False

class War(Module):
	def __init__(self, room):
		self.room = room
		self.bombs = []

	def shoot(self, jid):
		pseudo_shooter = jid.resource
		roster = self.room.get_roster()
		roster.remove(self.room.get_botname())
		victim = choice(roster)
		if victim == pseudo_shooter:
			self.room.send_message(pseudo_shooter + " s'est tiré une balle dans le pied...")
		else:
			self.room.send_message(victim + " est mort.")

	def drop_bomb(self, jid):
		self.bombs.append(Bombe(jid.resource, self.room))

	def defuse_bomb(self, jid):
		for b in self.bombs:
			if b.victime == jid.resource:
				b.defuse()

	def handle_message(self, msg):
		if msg['body'] == '!shoot':
			self.shoot(msg['from'])
		elif msg['body'] == '!bomb':
			self.drop_bomb(msg['from'])
		elif msg['body'] == '!defuse':
			self.defuse_bomb(msg['from'])
