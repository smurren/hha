import glob, sys
import cPickle, shelve
import pygame
import math
import os, os.path


class Draw(object):
	
	def __init__(self, mainWindow, game, limit, seats, singleOutput, filter):
	
		self.button = self.generateCardDict()
		self.sb = self.generateCardDict()
		self.bb = self.generateCardDict()
		self.utg = self.generateCardDict()
		self.utg1 = self.generateCardDict()
		self.utg2 = self.generateCardDict()
		self.mp = self.generateCardDict()
		self.mp1 = self.generateCardDict()
		self.mp2 = self.generateCardDict()
		self.co = self.generateCardDict()
		self.all = self.generateCardDict()
		self.currentCoordinates = []
		self.HANDS = self.generateHands()
		
		self.generalHandsDict = {}
		
		self.gameType = game
		self.gameLimit = limit
		self.greatestProfit = 0.0
		self.seats = seats
		self.allSeats = []
		self.mainWindow = mainWindow
		self.singleOutput = singleOutput
		self.filter = filter
		self.totalHands = 0
		
		# creates a dictionary contain general hands as keys, 0.0 profit as values
		for i in self.HANDS:
			self.generalHandsDict[i] = 0.0
		
		# creates draw layer
		self.layer = pygame.Surface((mainWindow.get_width(), mainWindow.get_height()))
		self.layer.fill((255, 255, 255))
		self.layer.set_colorkey((255, 255, 255))
		
		# creates profits layer
		self.profitLayer = pygame.Surface((mainWindow.get_width(), mainWindow.get_height()))
		self.profitLayer.fill((255, 255, 255))
		self.profitLayer.set_colorkey((255, 255, 255))
		
		# creates profits individual line layer
		self.lineLayer = pygame.Surface((500, 6))
		self.lineLayer.fill((255, 255, 255))
		self.lineLayer.set_colorkey((255, 255, 255))
		self.lineLayer.set_alpha(255)
		

		
	def drawMainMethod(self):
		mainScreen = self.mainWindow
		seats = self.seats
		textSize = 50
		titleX = 10
		title2Y = 65
		title3Y = 125
		
		positionList = []
		positionName = ""
		pointsForSeats = []
		point = ()
		
		if seats not in self.allSeats:
			print "Error:  No hand histories for given players number"
			exit(0)
		

		if int(seats) == 10:
			positionList = ["BUTTON", "SB", "BB", "UTG", "UTG+1", "UTG+2", "MP", "MP+1", "MP+2", "CO"]
			pointsForSeats = [(7000, 1250), (9000, 2000), (9000, 4000), (7000, 4750), (5000, 4750), (3000, 4750), (1000, 4000),  (1000, 2000), (3000, 1250), (5000, 1250)]
		elif int(seats) == 9:
			positionList = ["BUTTON", "SB", "BB", "UTG", "UTG+1", "MP", "MP+1", "MP+2", "CO"]
			pointsForSeats = [(7000, 1250), (9000, 2000), (9000, 4000), (7000, 4750), (5000, 4750), (3000, 4750), (1000, 3000), (3000, 1250), (5000, 1250)]
		elif int(seats) == 8:
			positionList = ["BUTTON", "SB", "BB", "UTG", "UTG+1", "MP", "MP+1", "CO"]
			pointsForSeats = [(6000, 1250), (7000, 3000), (6000, 4750), (4000, 4750), (2000, 4750), (1000, 3000), (2000, 1250), (4000, 1250)]
		elif int(seats) == 7:
			positionList = ["BUTTON", "SB", "BB", "UTG", "MP", "MP+1", "CO"]
			pointsForSeats = [(6000, 1250), (7000, 3000), (5000, 4750), (3000, 4750), (1000, 3000), (2000, 1250), (4000, 1250)]
		elif int(seats) == 6:
			positionList = ["BUTTON", "SB", "BB", "UTG", "MP", "CO"]
			pointsForSeats = [(4000, 1175), (4800, 3000), (4000, 4825), (2000, 4825), (1300, 3000), (2000, 1175)]
		elif int(seats) == 5:
			positionList = ["BUTTON", "SB", "BB", "UTG", "MP"]
			pointsForSeats = [(4000, 1250), (4750, 3250), (3000, 4750), (1250, 3250), (2000, 1250)]
		elif int(seats) == 4:
			positionList = ["BUTTON", "SB", "BB", "MP"]
			pointsForSeats = [(3000, 1250), (4750, 3000), (3000, 4750), (1250, 3000)]
		elif int(seats) == 3:
			positionList = ["BUTTON", "SB", "BB"]
			pointsForSeats = [(2250, 1250), (3300, 3250), (1200, 3250)]
		elif int(seats) == 2:
			positionList = ["BUTTON", "BB"]
			pointsForSeats = [(1200, 1250), (3300, 1250)]
		else:
			print "Error:  Invalid number of seats given by user prompt."
			exit(0)	
	
		
		
		if self.singleOutput == False:
			for i in range(int(seats)):
				positionName = positionList.pop(0)
				point = pointsForSeats.pop(0)

				self.currentCoordinates = self.drawSeat(mainScreen, positionName, point[0], point[1])
				self.drawProfits(mainScreen, positionName, self.currentCoordinates, point[0], point[1])
		else:
			positionName = "OVERALL"
			point = (1000, 1000)
			
			self.currentCoordinates = self.drawSeat(mainScreen, positionName, point[0], point[1])
			self.drawProfits(mainScreen, positionName, self.currentCoordinates, point[0], point[1])
		
		
		# draws title text in top left of image (game, limit)
		if self.singleOutput == False:
			if 4 <= int(seats) <= 6:
				textSize = 88
				title2Y = 110
				title3Y = 210
			if int(seats) > 6:
				textSize = 100
				title2Y = 140
				title3Y = 245
		
		self.font = pygame.font.SysFont("Comic Sans MS", textSize)
		text = self.font.render(self.gameType, 1, (0,0,0))
		self.layer.blit(text, (titleX, 5))
		text = self.font.render(self.gameLimit, 1, (0,0,0))
		self.layer.blit(text, (titleX, title2Y))
		
		if self.filter != None:
			text = self.font.render(self.filter, 1, (0,0,0))
			self.layer.blit(text, (titleX, title3Y))

		
		# updates main window with profits and main draw layer
		mainScreen.blit(self.profitLayer, (0,0))
		mainScreen.blit(self.layer, (0,0))
		print "Total hands: ", self.totalHands
		
	
	def readAllHands(self, handLists):
		seats = self.seats
		save = True
		
		# record profits by position and cards
		for hand in handLists:
			if hand[5] == seats:
				save = True
				if self.filter != None:
					if hand[6][self.filter] == False:
						save = False
				
				if save == True:
					self.saveHandData(hand)
					self.totalHands += 1
	
	
	def generateHands(self):
		list = []
		RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
		RANKS.reverse()
		generalSuitedHand = ""
		generalOffsuitHand = ""
		pairHand = ""
		
		for rank1 in RANKS:
			for rank2 in RANKS:
				
				if rank1 != rank2:
					generalSuitedHand = rank1 + rank2 + "s"
					generalOffsuitHand = rank1 + rank2 + "o"
				else:
					pairHand = rank1+rank2
				
				if generalSuitedHand not in list:
					if generalSuitedHand != "":
						if (generalSuitedHand[1] + generalSuitedHand[0] + "s") not in list:
							list.append(generalSuitedHand)
				if generalOffsuitHand not in list:
					if generalOffsuitHand != "":
						if (generalOffsuitHand[1] + generalOffsuitHand[0] + "o") not in list:	
							list.append(generalOffsuitHand)
				if pairHand not in list:
					if pairHand != "":
						list.append(pairHand)

		return list	

	
	def generateCardDict(self):
		
		cardsList = []
		allCardCombos = {}
		hand = ""
		reverseHand = ""
		RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
		SUITS = ["c", "d", "h", "s"]
		
		# generates 52 cards in the deck in a list
		for rank in RANKS:
			for suit in SUITS:
				hand = rank + suit
				cardsList.append(hand)
				
		# generates all possible combinations of the 52 cards into a list
		for card in cardsList:
			for card2 in cardsList:
				if card != card2:
					hand = card + "," + card2
					if hand not in allCardCombos:
						allCardCombos[hand] = 0.0
					
		return allCardCombos
	
	
	def generateProfitsDict(self, positionDict, coordinates):
		newDict = self.generalHandsDict.copy()
		generalHands = self.HANDS[:]
		currentPositionDict = positionDict.copy()
		currentHand = ""	
		
		
		for coordinate in coordinates:
			currentHand = generalHands.pop()
			for key in currentPositionDict:
				if key[0] == key[3]:
					if (key[0] + key[3]) == currentHand:
						if currentPositionDict[key] != 0.0:
							newDict[key[0] + key[3]] += currentPositionDict[key]
							
							if abs(newDict[key[0] + key[3]]) > self.greatestProfit:
								self.greatestProfit = abs(newDict[key[0] + key[3]])
							
							currentPositionDict[key] = 0.0
						
				else:		
					if key[0] and key[3] in currentHand:
						if key[1] == key[4]:
							if "s" in currentHand:
								if currentPositionDict[key] != 0.0:
									try:
										newDict[key[0] + key[3] + "s"] += currentPositionDict[key]
										if abs(newDict[key[0] + key[3] + "s"]) > self.greatestProfit:
											self.greatestProfit = abs(newDict[key[0] + key[3] + "s"])
									except:
										newDict[key[3] + key[0] + "s"] += currentPositionDict[key]
										if abs(newDict[key[3] + key[0] + "s"]) > self.greatestProfit:
											self.greatestProfit = abs(newDict[key[3] + key[0] + "s"])
									
									currentPositionDict[key] = 0.0
								
									
						else:
							if "o" in currentHand:
								if currentPositionDict[key] != 0.0:
									try:
										newDict[key[0] + key[3] + "o"] += currentPositionDict[key]
										if abs(newDict[key[0] + key[3] + "o"]) > self.greatestProfit:
											self.greatestProfit = abs(newDict[key[0] + key[3] + "o"])
									except:
										newDict[key[3] + key[0] + "o"] += currentPositionDict[key]
										if abs(newDict[key[3] + key[0] + "o"]) > self.greatestProfit:
											self.greatestProfit = abs(newDict[key[3] + key[0] + "o"])
									
									currentPositionDict[key] = 0.0
							
		return newDict
		
	
	def saveHandData(self, list):
		
		# saves seats/players data
		if list[5] not in self.allSeats:
			self.allSeats.append(list[5])
		
		
		# only saves hands from game type and limit that user specified
		if list[3] == self.gameLimit:
			if list[4] == self.gameType:
				
				# saves the greatest amount of profit/loss to set draw scale
				#if abs(list[2]) > self.greatestProfit:
				#	self.greatestProfit = abs(list[2])
				
				if self.singleOutput == True:
					# adds everything to one position
					self.all[list[0]] += list[2]
				else:
					# records profit from each hand played by position
					if list[1] == "BUTTON":
						self.button[list[0]] += list[2]
					elif list[1] == "SB":
						self.sb[list[0]] += list[2]
					elif list[1] == "BB":
						self.bb[list[0]] += list[2]
					elif list[1] == "UTG":
						self.utg[list[0]] += list[2]
					elif list[1] == "UTG+1":
						self.utg1[list[0]] += list[2]
					elif list[1] == "UTG+2":
						self.utg2[list[0]] += list[2]
					elif list[1] == "MP":
						self.mp[list[0]] += list[2]
					elif list[1] == "MP+1":
						self.mp1[list[0]] += list[2]
					elif list[1] == "MP+2":
						self.mp2[list[0]] += list[2]
					elif list[1] == "CO":
						self.co[list[0]] += list[2]
					else:
						print "Error: Hand history contained incorrect position data during draw."
						print list
						exit(0)
		
			
	def drawSeat(self, mainScreen, position, x, y):
		pointsUsed = []
		
		# sets font for position title
		self.font = pygame.font.SysFont("Comic Sans MS", 58)
		
		text = self.font.render(position, 1, (0,0,0))
		
		if position == "BUTTON" or position == "OVERALL":
			self.layer.blit(text, (x- 350, y - 170))
		else:
			self.layer.blit(text, (x- 200, y - 170))
		

		pointsUsed = self.drawAllHands(mainScreen, x, y)
	
		return pointsUsed
		
	
	def drawAllHands(self, mainScreen, x, y):
		
		x -= 340
		y += 50
		newX = 0
		newY = 0
		angle = .335
		angleIncrement = 1.0
		angleIncrementChange = .9827
		radius = 30.0
		radiusIncrement = 1.01
		radiusIncrementChange = .9998
		points = []
		generalHandsList = self.HANDS[:]
		
		self.font = pygame.font.SysFont("Comic Sans MS", 12)
		
		
		for i in range(169):
			
			points.append((x, y))
			
			newX = int(radius * math.sin(angle))
			newY = int(radius * math.cos(angle))
			
			x += newX
			y += newY
			
			angle += .135 * angleIncrement
			angleIncrement *= angleIncrementChange
			angleIncrementChange *= 1.000121

		for point in points:
			text = self.font.render(generalHandsList.pop(), 0, (0,0,0))
			self.layer.blit(text, point)	
			
		
		return points
	

	def drawProfits(self, mainScreen, position, coordinates, x, y):
		
		x -= 100
		y -= 100
		
		angle = 0.0
		length = 0.0
		distance = 0.0
		alpha = 0
		
		posProfitsDict = {}
		generalHands = self.HANDS[:]
		
		if position == "BUTTON":
			posProfitsDict = self.generateProfitsDict(self.button, coordinates)
		elif position == "SB":
			posProfitsDict = self.generateProfitsDict(self.sb, coordinates)
		elif position == "BB":
			posProfitsDict = self.generateProfitsDict(self.bb, coordinates)
		elif position == "UTG":
			posProfitsDict = self.generateProfitsDict(self.utg, coordinates)
		elif position == "UTG+1":
			posProfitsDict = self.generateProfitsDict(self.utg1, coordinates)
		elif position == "UTG+2":
			posProfitsDict = self.generateProfitsDict(self.utg2, coordinates)
		elif position == "MP":
			posProfitsDict = self.generateProfitsDict(self.mp, coordinates)
		elif position == "MP+1":
			posProfitsDict = self.generateProfitsDict(self.mp1, coordinates)
		elif position == "MP+2":
			posProfitsDict = self.generateProfitsDict(self.mp2, coordinates)
		elif position == "CO":
			posProfitsDict = self.generateProfitsDict(self.co, coordinates)
		elif position == "OVERALL":
			posProfitsDict = self.generateProfitsDict(self.all, coordinates)
		else:
			print "Error:  Invalid position in hand during drawProfits()"
			print position
			
		
		for coordinate in coordinates:
			currentHand = generalHands.pop()
			for key in posProfitsDict:
				if key == currentHand:

					angle = math.atan2(-(y - coordinate[1] + 8), (x - coordinate[0] + 9))
					angle = math.degrees(angle)
					angle += 180						
					
					length = abs(225 * (posProfitsDict[key] / self.greatestProfit))
					
					alpha = int(length) + 55
					if alpha > 255:
						alpha = 255
					
					self.lineLayer.set_alpha(alpha)
					
					
					if posProfitsDict[key] > 0.0:
						pygame.draw.circle(self.profitLayer, (255 - alpha,255,255 - alpha), (coordinate[0] + 9, coordinate[1] + 8), 12, 0)
						pygame.draw.line(self.lineLayer, (0,255,0), (225, 2), (225 - length, 2), 6)
							
						line = pygame.transform.rotate(self.lineLayer, angle)						
						nrect = line.get_rect(center = (coordinate[0] + 9, coordinate[1] + 8))
						
						self.profitLayer.blit(line, nrect)
						
						self.lineLayer.fill((255, 255, 255))	
					
					
					if posProfitsDict[key] < 0.0:
						angle -= 180

						pygame.draw.circle(self.profitLayer, (255,255 - alpha,255 - alpha), (coordinate[0] + 9, coordinate[1] + 8), 12, 0)
						pygame.draw.line(self.lineLayer, (255,0,0), (225, 3), (225 - length, 3), 6)
						
						line = pygame.transform.rotate(self.lineLayer, angle)						
						nrect = line.get_rect(center = (coordinate[0] + 9, coordinate[1] + 8))
						
						self.profitLayer.blit(line, nrect)
						
						self.lineLayer.fill((255, 255, 255))

						
	

def screenshot(screen):
	file = ""
	fileNum = 1

	file = "screenshot" + str(fileNum) + ".png"
	pngFile = glob.glob('*.png')
	
	while file in pngFile:
		fileNum += 1
		file = "screenshot" + str(fileNum) + ".png"
	
	print "Saving " + file + "..."
	pygame.image.save(screen, file)
			
			
def process(file, handsList):
	
	player = -1
	totalPlayers = 0
	playerTotalBet = 0.0
	finalPots = []  # player, amount
	tempFinalPot = ["", ""] # player, amount
	totalWon = 0.0
	dealer = ""  # seat number
	activePlayers = []
	raisingPlayers = []
	tempSeats = ""
	tempDealtIn = ""
	allSeats = []
	positionList = []  # calculated at end of hand using positionList and totalPlayers
	actualPositionDic = {}
	tempPlayer = ""
	filters = {"3bet": False}  # player 3-bet pre-flop
	saveHand = ["", "", 0.0, "", "", "", filters]  # cards, position, profit, limit, game, total seats
	allBets = []
	tempBet = ["", ""]  # player, amount
	tempBetType = ""
	currentStreet = ""
	handLog = []
	pRaiseCount = 0
	count = 0
	
	
	for line in file:
		
		handLog.append(line)
		
		# saves game description
		if "<description type=" in line:
			for ch in range(len(line)):
				if line[ch] == "\"":
					count += 1	
				if (count == 1) and (line[ch] != "\""):
					saveHand[4] += line[ch]
				if (count == 3) and (line[ch] != "\""):
					saveHand[3] += line[ch]
			count = 0
		
		if "<game id=" in line:
			for ch in range(len(line)):
				if line[ch] == "\"":
					count += 1	
				if (count == 9) and (line[ch] != "\""):
					saveHand[5] += line[ch]
			count = 0
		
		if "<round id=" in line:
			currentStreet = ""
			for ch in range(len(line)):
				if line[ch] == "\"":
					count += 1	
				if (count == 1) and (line[ch] != "\""):
					currentStreet += line[ch]
			count = 0
				
		
		# saves dealer position
		if "<players dealer=" in line:
			for ch in range(len(line)):
				if line[ch] == "\"":
					count += 1	
				if (count == 1) and (line[ch] != "\""):
					dealer += line[ch]
			count = 0
		
		if "<player seat=" in line:
			tempSeats = ""
			tempDealtIn = ""
			for ch in range(len(line)):
				if line[ch] == "\"":
					count += 1	
				if (count == 1) and (line[ch] != "\""):
					tempSeats += line[ch]
				if (count == 7) and (line[ch] != "\""):
					tempDealtIn += line[ch]
			if tempDealtIn == "true":
				allSeats.append(int(tempSeats))
				totalPlayers += 1
			count = 0
		
		# saves bet info (Player and amount).  Also total players/ relative positions
		if "<event sequence=" in line:
			tempBetType = ""
			tempBet = ["", ""]
			for ch in range(len(line)):
				if line[ch] == "\"":
					count += 1	
				if (count == 3) and (line[ch] != "\""):
					tempBetType += line[ch]
				if (count == 7) and (line[ch] != "\""):
					tempBet[0] += line[ch]
				if (count == 9) and (line[ch] != "\""):
					tempBet[1] += line[ch]
			
			if tempBetType == "RAISE" and currentStreet == "PREFLOP":
				pRaiseCount += 1
				raisingPlayers.append(int(tempBet[0]))
			
			if "amount=" in line and tempBetType != "RETURN_BLIND":
				allBets.append(tempBet)
					
			
			if currentStreet == "PREFLOP":
				if "type=\"CHAT\"" not in line:
					if "type=\"SIT_IN\"" not in line:
						if "type=\"SIT_OUT\"" not in line:
							if int(tempBet[0]) not in activePlayers:
								activePlayers.append(int(tempBet[0]))
			count = 0
		
		# saves cards, player
		if "<cards type=\"HOLE\"" in line:
			if len(saveHand[0]) == 0:
				tempPlayer = ""
				for ch in range(len(line)):
					if line[ch] == "\"":
						count += 1	
					if (count == 3) and (line[ch] != "\""):
						saveHand[0] += line[ch]
					if (count == 5) and (line[ch] != "\""):
						tempPlayer += line[ch]
			
				player = int(tempPlayer)
				count = 0
		
		# saves final pot amounts
		if "<winner amount=" in line:
			tempFinalPot = ["", ""]
			for ch in range(len(line)):
				if line[ch] == "\"":
					count += 1	
				if (count == 1) and (line[ch] != "\""):
					tempFinalPot[1] += line[ch]
				if (count == 7) and (line[ch] != "\""):
					tempFinalPot[0] += line[ch]
			
			if player == int(tempFinalPot[0]):
				finalPots.append(tempFinalPot)
			count = 0
				
		
		if "</game>" in line:
			
			if (player != -1) and (totalPlayers > 1):
				
				if len(activePlayers) < len(allSeats):
					for i in range(totalPlayers):
						if allSeats[i] not in activePlayers:
							activePlayers.append(allSeats[i])
				
				# adds up total amount player has wagered
				for betList in allBets:
					if player == int(betList[0]):
						playerTotalBet += float(betList[1])
							
				# subtracts total amount wagered from total won in all pots at showdown to get profit.
				for pot in finalPots:
					totalWon += float(pot[1])
				saveHand[2] = round(totalWon - playerTotalBet, 2)
				
				
				for seat in activePlayers:
					actualPositionDic[str(seat)] = ""
				
				
				# creates actualPositionsList
				if totalPlayers == 10:
					positionList = ["UTG", "UTG+1", "UTG+2", "MP", "MP+1", "MP+2", "CO", "BUTTON", "SB", "BB"]
				elif totalPlayers == 9:
					positionList = ["UTG", "UTG+1", "MP", "MP+1", "MP+2", "CO", "BUTTON", "SB", "BB"]
				elif totalPlayers == 8:
					positionList = ["UTG", "UTG+1", "MP", "MP+1", "CO", "BUTTON", "SB", "BB"]
				elif totalPlayers == 7:
					positionList = ["UTG", "MP", "MP+1", "CO", "BUTTON", "SB", "BB"]
				elif totalPlayers == 6:
					positionList = ["UTG", "MP", "CO", "BUTTON", "SB", "BB"]
				elif totalPlayers == 5:
					positionList = ["UTG", "MP", "BUTTON", "SB", "BB"]
				elif totalPlayers == 4:
					positionList = ["MP", "BUTTON", "SB", "BB"]
				elif totalPlayers == 3:
					positionList = ["BUTTON", "SB", "BB"]
				elif totalPlayers == 2:
					positionList = ["BUTTON", "BB"]
				else:
					print "Error:  Invalid number of players in hand"
					exit(0)

				
				# matches up actualPositionDic keys with correct positions in hand
				for seat in activePlayers:
					actualPositionDic[str(seat)] = positionList.pop(0)
						
				# saves player position to saveHand list
				try:
					saveHand[1] = actualPositionDic[str(player)]
				except:
					for eachLine in handLog:
						print eachLine
					print "Error: Unable to save player position"
					print "player position: ", player
					print actualPositionDic
					print "total players: ", totalPlayers
					print "active players: ", activePlayers
					exit(0)
				
				# saves hand data to main hand list
				if len(saveHand[0]) > 5:
					for eachLine in handLog:
						print eachLine
					print "Error:  Incorrect hand data saved."
					print saveHand[0]
					exit(0)
				
				# ADDS FILTERS
				# -- 3bet preflop
				if player in raisingPlayers:
					if pRaiseCount == 2:
						saveHand[6]["3bet"] = True
					else:
						saveHand[6]["3bet"] = False
				else:
					saveHand[6]["3bet"] = False
				# --
				
				# SAVES HAND TO THE MAIN LIST
				handsList.append(saveHand)
			
			# reset method variables/lists
			filters = {"3bet": False}
			saveHand = ["", "", 0.0, saveHand[3], saveHand[4], "", filters]
			allBets = []
			finalPots = []
			dealer = ""
			player = -1
			totalPlayers = 0
			playerTotalBet = 0.0
			totalWon = 0.0
			tempPlayer = ""
			pRaiseCount = 0
			count = 0
			activePlayers = []
			raisingPlayers = []
			allSeats = []
			actualPositionDic = {}
			currentStreet = ""
			tempSeats = ""
			tempDealtIn = ""
			handLog = []
	
	return handsList
	

def main():
	# ----------------------------------------------------------------
	# Loads Merge hand histories, then sends the data to process()
	# saves all hands from 
	# ----------------------------------------------------------------
	fileList = []
	handsData = []
	pickleFile = open("saved_hands.dat", "w")
	count = 0
	
	#fileList = glob.glob('*.xml')
	
	for dirpath, dirnames, filenames in os.walk("."):
		for filename in [f for f in filenames if f.endswith(".xml")]:
			fileList.append(os.path.join(dirpath, filename))
	
	print "Loading hand histories"
	
	# saves file list length so program knows number of lists
	# to unpickle when opening the .dat file.
	cPickle.dump(len(fileList), pickleFile)
	
	for file in fileList:
		count += 1
		print "Opening file...", file
		newFile = open(file, "r")
		handsData = process(newFile, handsData)
		
		# saves handsData list in pickled form in a .dat file
		cPickle.dump(handsData, pickleFile)
		
		handsData = []  # clears handsData list
		newFile.close()  # closes the current xml file
	
	# closes pickle file
	pickleFile.close()
	
	print "Hands data saved.  ", count, " files loaded successfully."
	# ----------------------------------------------------------------
	
	
	raw_input("Press any key to draw data.")
	
	
	# ----------------------------------------------------------------
	# Object of Draw class is instantiated.  Draws an image based on 
	# pickled hand history data and user parameters.
	# ----------------------------------------------------------------
	
	
	# ***
	# ADD PROMPTS HERE FOR USER TO INPUT WHAT THEY WANT DRAWN
	# GAME TYPE AND LIMIT
	# ***
	totalSeats = "6"
	singleOutput = True
	filter = None    # options:  None, "3bet"
	
	# sets window size based on number of seats being draw
	width = 0
	height = 0
	
	if int(totalSeats) == 2:
		width = 4500
		height = 2500
	elif int(totalSeats) == 3:
		width = 4500
		height = 4500
	elif 4 <= int(totalSeats) <= 6:
		width = 6000
		height = 6000
	elif 7 <= int(totalSeats) <= 8:
		width = 8500
		height = 6500
	else:
		width = 10500
		height = 6500
		
	if singleOutput == True:
		width = 2000
		height = 2000
	
	
	# initializes pygame
	pygame.init()
	# opens main window, sets size
	window = pygame.display.set_mode((width, height))
	pygame.display.set_caption('Hand History Visualizer')
	window.fill((255, 255, 255))
	
	# Draw object instantiated
	# main window layer and unpickled hands data lists are arguments
	d = Draw(window, "Holdem", "No Limit ($0.02/$0.04)", totalSeats, singleOutput, filter)
	
	
	# loads data from .dat file
	pickleFile = open("saved_hands.dat", "r")
	count = cPickle.load(pickleFile)
	
	while count > 0:
		handsData = cPickle.load(pickleFile)
		d.readAllHands(handsData)
		handsData = []
		count -= 1

	d.drawMainMethod()
	
	pygame.display.flip()
	screenshot(window)  # saves screenshot of image drawn to main window
	
	# ----------------------------------------------------------------
	
	
	# closes pickle file
	pickleFile.close()
	# end of program


# start	of program
main()