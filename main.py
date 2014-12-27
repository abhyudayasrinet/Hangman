
from Tkinter import *
import random
from string import *
from wordnik import *

#api stuff for wordnik
apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'your API here' #get it here http://developer.wordnik.com/
client = None
wordApi = None


words = []
attempts = 0
corrects = 0
root = None

class MainWindow(Frame):
	
	def __init__(self, parent):

		Frame.__init__(self, parent)   
		self.parent = parent
		self.init()

	def init(self):
		global words
		global attempts
		global corrects
		attempts = 0
		corrects = 0

		#menu bar frame 
		self.MenuBarFrame = Frame(self.parent)
		self.MenuBarFrame.pack()

		#new game button
		self.NewGameButton = Button(self.MenuBarFrame,text="New Game",command = lambda: NewGame())
		self.NewGameButton.pack()

		#creating canvas
		self.canvas = Canvas(self.parent,bg="white",bd=10)
		self.canvas.pack()

		#get guess word from dictionary
		self.GuessWord = random.choice(words).upper()
		print('Guess word is : *** '+self.GuessWord+' *** ')

		
		#create guess word label
		self.GuessWordFrame = Frame(self.parent)
		self.GuessWordFrame.pack()
		self.GuessAlphabets = []
		i = 0
		for x in self.GuessWord :
			if(x in ascii_uppercase):
				self.GuessAlphabets.append(Label(self.GuessWordFrame,text = "__",padx=5))
				self.GuessAlphabets[i].grid(row = 0,column = i)
			else:
				self.GuessAlphabets.append(Label(self.GuessWordFrame,text = x,padx=5))
				self.GuessAlphabets[i].grid(row = 0,column = i)
			i+=1

		# Alphabet Grid ---
		self.AlphabetsGrid = Frame(self.parent)
		self.AlphabetsGrid.pack()
		self.Alphabets = []
		i = 0
		index = 0
		row_no = 0
		for c in ascii_uppercase:
			self.Alphabets.append( Button(self.AlphabetsGrid,text=c,command = lambda character = c: self.alphabetselect(character)) )
			if(ascii_uppercase.index(c) > 12 and row_no == 0) :
				row_no = 1
				i = 0
			self.Alphabets[index].grid(row=row_no,column=i)
			i+=1
			index+=1


	#check if alphabet exists in guess word
	#gray out the button of the selected alphabet
	def alphabetselect(self,character):

		global corrects

		fail = True
		i = 0

		for x in self.GuessWord:
			if(x == character):
				corrects += 1
				self.GuessAlphabets[i]['text'] = character
				fail = False
			i+=1

		self.Alphabets[ascii_uppercase.index(character)]['state'] = DISABLED

		if(corrects == len(self.GuessWord)):
			Label(self.parent,text="You Win!").pack()
			for i in range(0,26):
				self.Alphabets[i]['state'] = DISABLED
		
		#draw
		if(fail):
			self.HangHim()
			

		print(str(corrects)+' '+str(attempts))



	def HangHim(self):
		global attempts,wordApi
		attempts += 1

		if(attempts == 1):
			self.canvas.create_line(80,250,120,250)
			self.canvas.create_line(100,20,100,250)
			self.canvas.create_line(100,20,250,20)
			self.canvas.create_line(250,20,250,60)

		if(attempts == 2):
			self.canvas.create_oval(230,60,270,100)

		if(attempts == 3):
			self.canvas.create_line(250,100,250,160)
	
		if(attempts == 4):
			self.canvas.create_line(250,120,230,130)	
		
		if(attempts == 5):			
			self.canvas.create_line(250,120,270,130)
			definition = wordApi.getDefinitions(self.GuessWord.lower(),sourceDictionaries='wiktionary',limit = 1)
			Label(self.parent,text = definition[0].text,wraplength=1000,justify=LEFT).pack()

		if(attempts == 6):
			self.canvas.create_line(250,160,230,170)

		if(attempts == 7):
			self.canvas.create_line(250,160,270,170)
			Label(self.parent,text="You Lost!").pack()
			Label(self.parent,text="The word was "+self.GuessWord).pack()
			for i in range(0,26):
				self.Alphabets[i]['state'] = DISABLED


def NewGame():

	global root
	root.destroy()
	root = Tk()
	root.geometry('500x500+200+200')

	root.resizable(width=FALSE,height=FALSE)

	game = MainWindow(root)
	game.master.title("Hangman")	
	root.mainloop()

def main():

	

	#load words
	global words,root,client,wordApi

	client = swagger.ApiClient(apiKey, apiUrl)
	wordApi = WordApi.WordApi(client)	

	words = open('dictionary.txt').read().splitlines()

	root = Tk()
	root.geometry('500x500+200+200')

	root.resizable(width=FALSE,height=FALSE)

	game = MainWindow(root)
	game.master.title("Hangman")
	root.mainloop()


if __name__ == '__main__':
	main()
