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

import random, string
from module import Module

class Talkative(Module):

	class Node:
		def __init__(self, w1, w2):
			self.w1 = w1
			self.w2 = w2
	
		def __cmp__(self, n2):
			if self.w1 == n2.w1 and self.w2 == n2.w2:
				return 0
			return (self.__hash__() - n2.__hash__()) % 2147483647
	
		def __hash__(self):
			return (self.w1.__hash__() + self.w2.__hash__()) % 2147483647
	
	class LString:

		class PString:
			def __init__(self, name):
				self._count = 1
				self._name = name
	
			def increment(self):
				self._count += 1
	
			def getCount(self):
				return self._count
	
			def getName(self):
				return self._name
	
		def __init__(self):
			self._size = 0
			self._r = []

		def put(self, word):
			for ps in self._r:
				if ps.getName() == word:
					ps.increment()
					self._size += 1
					break
			self._r.append(Talkative.LString.PString(word))
			self._size += 1

		def getRandom(self):
			ran = random.randint(0, self._size - 1)
			for ps in self._r:
				if ran < ps.getCount():
					return ps.getName()
				else:
					ran -= ps.getCount()
			return ""

	def __init__(self, room):
		self.words = dict()
		self.phrases = "phrases.txt"
		self.room = room
		self.load()
		self.output_file = open(self.phrases + "~", 'a')

	def load(self):
		for line in file(self.phrases):
			self.insertDB(line)

	def appendFile(self, message):
		self.output_file.write(message + "\n")

	def insertDB(self, message):
		if not message:
			return
		message = str(message)

		self.appendFile(message)
		message = message.translate(string.maketrans("",""), '!?.,').strip()
		prec = ""
		prec2 = ""
		for s in message.split(" "):
			if prec != "" and prec2 != "":
				n = Talkative.Node(prec2, prec)
				if n in self.words:
					ls = self.words[n]
					ls.put(s)
				else:
					ls = Talkative.LString()
					ls.put(s)
					self.words[n] = ls
			prec2 = prec
			prec = s
		if prec != "" and prec2 != "":
			ls = Talkative.LString()
			ls.put("")
			self.words[Talkative.Node(prec2, prec)] = ls

	def generate(self):
		result = ""
		while len(result) < 20 or len(result) > 100:
			result = ""
			c = self.words.keys()
			if len(c) == 0:
				return ""

			n = random.randint(0, len(c) - 1)
			s = c[n]

			str2 = s.w2
			result += s.w1 + " " + str2 + " "
			ls = self.words[s]
			str1 = ls.getRandom()
			while str1:
				result += str1 + " "
				try:
					ls = self.words[Talkative.Node(str2, str1)]
				except:
					break
				if not ls:
					break
				str2 = str1
				str1 = ls.getRandom()

		return result
	
	def handle_message(self, msg):
		self.insertDB(msg['body'])
		if self.room.get_botname() in msg['body']:
			self.room.send_message(self.generate())

if __name__ == "__main__":
	t = Talkative(None, "phrases.txt")
	print t.generate()
