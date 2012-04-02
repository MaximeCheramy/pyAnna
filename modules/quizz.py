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

import threading
import time
from module import Module
from random import choice
from random import randint
import re

class Question:
	def __init__(self, q, a):
		self.question = q
		self.answer = a

	def getQuestion(self):
		return self.question

	def getAnswer(self):
		return self.answer

	def getIndice(self, n):
		pattern = re.compile('[\xe9-\xF8\w]')
		indice = pattern.sub('_', self.answer)
		nblettres = n*len(self.answer)/4
		r = randint(0, len(self.answer)-1)
		while nblettres > 0:
			if indice[r] == '_' and indice[r] != ' ':
				indice = indice[:r] + self.answer[r] + indice[r+1:]
				r = (r * 2) % len(self.answer)
				nblettres -= 1
			else:
				r = (r + 1) % len(self.answer)

		return indice

	def getExpected(self):
		pattern = re.compile('[\xe9-\xF8\w]')
		return pattern.sub(' _ ', self.answer)

	def isAnswer(self, a):
		return self.answer == a

class Questions:
	def __init__(self, base):
		file_questions = open(base)
		self.questions = []
		for qa in file_questions:
			q,a = qa.split("\\")
			self.questions.append(Question(q.strip(), a.strip()))
		file_questions.close()

	def randomQuestion(self):
		return choice(self.questions)

	def size(self):
		return len(self.questions)

class Quizz(Module,threading.Thread):
	def __init__(self, room):
		threading.Thread.__init__(self)
		self.room = room
		self.questions = Questions("database.txt")
		self.questionAsked = False
		self.nextTimer = 0
		self.started = False
		self.fin = False
		self.firstStart = True

	def readQuestion(self):
		self.questionTimer = 0
		self.questionAsked = True
		self.currentQuestion = self.questions.randomQuestion();
		self.room.send_message(self.currentQuestion.getQuestion() + "\n" + self.currentQuestion.getExpected())

	def nextQuestion(self):
		self.questionAsked = False
		self.nextTimer = 0
		self.room.send_message("Prochaine question dans 15 secondes ! Préparez-vous !")

	def startQuizz(self):
		if self.firstStart:
			self.start()
			self.firstStart = True
		self.started = True
		self.nextQuestion()

	def stopQuizz(self):
		self.started = False

	def run(self):
		self.room.send_message("..::: QuizzBot :::..")
		time.sleep(1)
		self.room.send_message("La base contient " + str(self.questions.size()) + " questions.")
		time.sleep(1)

		while not self.fin:
			if self.started:
				if self.questionAsked:
					if self.questionTimer == 15:
						self.room.send_message("Un indice : " + self.currentQuestion.getIndice(1))
					elif self.questionTimer == 30:
						self.room.send_message("Un indice : " + self.currentQuestion.getIndice(2))
					elif self.questionTimer == 45:
						self.room.send_message("Aucun gagnant ! La réponse était : " + self.currentQuestion.getAnswer())
						self.nextQuestion()
					self.questionTimer += 1
				else:
					if self.nextTimer == 15:
						self.readQuestion()
					self.nextTimer += 1
			time.sleep(1)

	def stop(self):
		self.fin = True

	def handle_message(self, msg):
		message = msg['body'].strip()
		nickname = msg['from'].resource
		if message == '!start' and not self.started:
			self.room.send_message(nickname + " a lancé le quizz !!!")
			self.startQuizz()
		elif message == '!stop':
			self.room.send_message(nickname + " a stoppé le quizz !")
			self.stopQuizz()
		elif self.questionAsked:
			if self.currentQuestion.isAnswer(message):
				self.room.sendMessage(nickname + " a trouvé la bonne réponse !")
		elif msg['body'] == '!help':
			time.sleep(0.5)
			self.room.send_message('- !start : lance le quizz')
			self.room.send_message('- !stop : arrête le quizz')

