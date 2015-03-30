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
from kivy.uix.label import Label

#path to the sourcefiles
import sys
sys.path.append(sys.path[0]+'/data/src/')

from karteikarte import Notecards


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

                self.curdir = dirname(__file__)

                #add screens here
                self.available_screens['mainmenu'] =  join(self.curdir, 'data', 'screens', '{}.kv'.format('mainmenu'))
                self.available_screens['addmenu'] =  join(self.curdir, 'data', 'screens', '{}.kv'.format('addmenu'))

            #load the notecards
           # self.notecards = Notecards( join(curdir, 'data', 'cards', '{}.xml'.format('test')))

               #load main menue
                self.load_screen('mainmenu','left')

                #screen = self.screens['addmenu']
                #status=screen.ids.status
                #status.text='geht'




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
                return screen

        def btnEditPressed(self,direction):
            """if edite btn is pressed, check which theme is selected and switch to the edit scree"""
            #todo read checkboxes

            self.editCards('test',direction)


        def editCards(self,name,direction):
            """edit the cards of the theme"""

            screen=self.load_screen('addmenu',direction)

            #get the Layout that contains the List of Questions
            qList = screen.ids.qList

            #load the notecards
            #todo catch FileNotFound Exception
            self.notecards = Notecards( join(self.curdir, 'data', 'cards', '{}.xml'.format(name)))

            questions = self.notecards.getQuestions()

            #for q in questions:
            for i in range(25):
                l = Label(text ='* '+ str(i), size_hint_y=1)
                qList.add_widget(l)
            qList.add_widget(Label(size_hint_y=2))

if __name__ == '__main__':
        pytex_notecardApp().run()
        #addCard.addCard().run()



