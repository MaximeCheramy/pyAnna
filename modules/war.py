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

class War(Module):
	def __init__(self, room):
		self.room = room

	def shoot(self, jid):
		pseudo_shooter = jid.resource
		roster = self.room.get_roster()
		roster.remove(self.room.get_botname())
		victim = choice(roster)
		if victim == pseudo_shooter:
			self.room.send_message(pseudo_shooter + " s'est tiré une balle dans le pied...")
		else:
			self.room.send_message(victim + " est mort.")

	def handle_message(self, msg):
		if msg['body'] == '!shoot':
			self.shoot(msg['from'])					
