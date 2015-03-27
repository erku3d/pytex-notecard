#!/usr/bin/kivy

import kivy
kivy.require('1.8.0')

#from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,ListProperty
#from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen

class NotecardsScreen(Screen):
	fullscreen = BooleanProperty(False)

	def add_widget(self, *args):
		if 'content' in self.ids:
			return self.ids.content.add_widget(*args)
		return super(NotecardsScreen, self).add_widget(*args)




class pytex_notecardApp(App):

	#index = NumericProperty(-1)
	#current_title = StringProperty()
	#time = NumericProperty(0)
	#show_sourcecode = BooleanProperty(False)
	#sourcecode = StringProperty()
	#screen_names = ListProperty([])
	#higherarchy = ListProperty([])

	def build(self):
		self.title = 'pytex - NotecardApp' #Window  titel
		
		#mapping of the screen name and the widget created by the Builder
		self.screens = {}		
		
		#mapping of screen names (key) with the location of the *.kv file
		self.available_screens = {}		
		
		curdir = dirname(__file__)
		
		#add screens here
		self.available_screens['mainmenu'] =  join(curdir, 'data', 'screens', '{}.kv'.format('mainmenu'))
		self.available_screens['addmenu'] =  join(curdir, 'data', 'screens', '{}.kv'.format('addmenu'))
		
		
		#load main menue
		self.load_screen('mainmenu','left')
		
		
	def testbtn(self,key):
		print(self,key)
			
		
	def load_screen(self,key,direction):
		
		"""switch to the screen 'key' from the available screens, move in 'direction'"""
		
		#stop the app
		if key == 'stop':		
				self.stop()
				return
		
		
		#if the screen was already build 
		if key in self.screens:
			
			screen = self.screens[key]
		
		else:
			
			if key in self.available_screens:
				
				screen = Builder.load_file(self.available_screens[key].lower())
				self.screens[key] = screen
			
			else:
				print("Error! ",key," is not a Screen!") 
				return
		
		#get the ScreenManager
		#->'sm' is the id of the ScreenManager in pytex_notecard.kv
		sm = self.root.ids.sm  
		
		#check the 'direction'
		if not (direction in ['left', 'right', 'up', 'down']):
			direction = 'left'
		      
		sm.switch_to(screen, direction=direction)


if __name__ == '__main__':
	pytex_notecardApp().run()
	#addCard.addCard().run()



