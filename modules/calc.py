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

class Calc(Module):
	def __init__(self, room):
		self.room = room

	def handle_message(self, msg):
		if msg['body'].startswith("!calc "):
			try:
				self.room.send_message(str(eval(msg['body'][6:])))
			except:
				self.room.send_message('yé pas compris.')

	def handle_private_message(self, msg, to):
		if msg['body'].startswith("!calc "):
			try:
				self.room.send_private_message(str(eval(msg['body'][6:])), to)
			except:
				self.room.send_message_message('yé pas compris.')
