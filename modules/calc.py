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
from math import *

class Calc(Module):
	def __init__(self, room):
		self.room = room

	def calc(self, expression):
		try:
			#make a list of safe functions
			safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 
									'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
			#use the list to filter the local namespace
			safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])
			#add any needed builtins back in.
			safe_dict['abs'] = abs
			return eval(expression, {"__builtins__":None},safe_dict)
		except:
			return 'yé pas compris.'

	def handle_message(self, msg):
		if msg['body'].startswith("!calc "):
				msg['body'] = msg['body'].replace('"', '')
				msg['body'] = msg['body'].replace("'", '')
				self.room.send_message(str(self.calc(msg['body'][6:])))

	def handle_private_message(self, msg, to):
		if msg['body'].startswith("!calc "):
				msg['body'] = msg['body'].replace('"', '')
				msg['body'] = msg['body'].replace("'", '')
				self.room.send_private_message(str(self.calc(msg['body'][6:])), to)
