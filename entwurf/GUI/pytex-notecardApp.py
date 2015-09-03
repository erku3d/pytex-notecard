#!/usr/bin/kivy

import kivy
kivy.require('1.8.0')



#from time import time
from kivy.app import App
from os.path import dirname, join, isfile, realpath, abspath,normpath, expanduser, lexists
from os import listdir, remove
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,ListProperty
#from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox

import os.path

#path to the sourcefiles
import sys
sys.path.append(sys.path[0]+'/data/src/')

from notecards import Notecards


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

                #self.curdir = dirname(__file__)
                self.curdir = dirname(realpath(__file__))
                
                                
                #add screens here
                self.available_screens['mainmenu'] =  join(self.curdir, 'data', 'screens', '{}.kv'.format('mainmenu'))
                self.available_screens['editmenu'] =  join(self.curdir, 'data', 'screens', '{}.kv'.format('editmenu'))
                self.available_screens['newcategory'] =  join(self.curdir, 'data', 'screens', '{}.kv'.format('newcategory'))
                

                #location oft the cards
                self.themesDirectories = []
                self.themesDirectories.append(join(self.curdir, 'data', 'cards'))
                #todo user can add more directories
                               
                               
               #load main menue
                self.load_screen('mainmenu','left')                
                self.updateThemeList()
                
                                
                

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
                                screen = Builder.load_file(self.available_screens[key])
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
                
                self.currentScreen = screen

        
        def updateThemeList(self):
            #get the Layout that contains the List of Themes
            tList = self.currentScreen.ids.tList 
            
            
            # when we add children to the grid layout, its size doesn't change at
            # all. we need to ensure that the height will be the minimum required to
            # contain all the childs. (otherwise, we'll child outside the bounding
            # box of the childs)
            
            tList.bind(minimum_height=tList.setter('height'))
            
            tList.clear_widgets()
            
            #generate the filenames and paths from the directories
                       
            files= []
                       
            for path in self.themesDirectories:         #for all paths
                       
                for f in listdir(path):                 #get all files and directories
                    if isfile(join(join(path,f))):      #use only files
                        if f.endswith('.xml'):          #that ends with '.xml'
                            name = f.split('.xml')         #split the '.xml'
                            
                            files.append([name[0],join(join(path,f))])      
            
            #generate ToggleButtons
            for t in files:                                                                       
                btn = ToggleButton(text=t[0],id='tbtn_'+t[1] ,group='theme', state = 'normal',size_hint_y=None, height='40dp')
                tList.add_widget(btn)
            
        def getPathFromToggleButton(self):
            """extracts the path from the id of the selected ToogleButton and returns it"""
            btns = ToggleButtonBehavior.get_widgets('theme')
            
            btn_pressed = False
            
            #get the button which is pressed
            for btn in btns:
                if(btn.state == 'down'):
                    btn_pressed = True
                    break
            
            if(not btn_pressed):
                self.showPopup("Fehler","Wähle eine Kategorie aus")
                return None
            
            #get the id of the btn -> path of the .xml file
                     
            
            tmp=btn.id.split('tbtn_')            
            
            return tmp[len(tmp)-1]
            
            
        
        def btnEditPressed(self,direction):
            """if edite btn is pressed, check which theme is selected and switch to the edit screen"""
            
            path = self.getPathFromToggleButton()
            
            self.editCards(path,direction)
        
        def btnNewCategoryPressed(self,direction):
            """create a new Theme with a .xml"""
            self.load_screen('newcategory',direction)
            
            self.currentScreen.ids.ti_name.text=''
            
            #~ fileChooser=self.currentScreen.ids.fileChooser
            #~ 
            #~ #fileChooser.path = dirname(realpath(__file__))
            #~ fileChooser.path = dirname(expanduser('~'))
            #~ 
            #~ self.updateFolderList()
            #~ 
        
        def btnDeleteCategoryPressed(self):            
            path = self.getPathFromToggleButton()
            
            if( path != None):
                self.deleteCategory(path)
        
        def updateFolderList(self):
            
            fl = self.currentScreen.ids.folderList
                        
            fl.bind(minimum_height=fl.setter('height'))
            
            fl.clear_widgets()
            
            fileChooser=self.currentScreen.ids.fileChooser
            
            def callback(instance,state):
                if(state):
                    if(instance.id == 'cb_new'):
                        return
                                       
                    path = instance.id.split('cb_')[1]
                    
                    if(lexists(path)):
                        fileChooser.path=path
                
            
            bl = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp') 
            cb = CheckBox(active = True, id = 'cb_new', group ='folder', size_hint_x=0.1)
            cb.bind(active=callback)
            la = Label(text='Neu')
            
            bl.add_widget(cb)
            bl.add_widget(la)
            
            
            fl.add_widget(bl)
            
            for d in self.themesDirectories:

                bl = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp') 
                cb = CheckBox(active = False, id = 'cb_'+d, group ='folder', size_hint_x=0.1)
                cb.bind(active=callback)               
                la = Label(text=self.shortenPath(d,30))
                
                bl.add_widget(cb)
                bl.add_widget(la)
                
                
                fl.add_widget(bl)
            
            
        def shortenPath(self,path, length):
            """shortens the given path"""
            if(len(path) < length):
                return path
            
            head = os.path.split(path)[0]
            tail = os.path.split(path)[1]
            
            p = tail
                     
            while(len(p)<length):
                               
                head = os.path.split(head)[0]
                tail = os.path.split(head)[1]
                
                p = join(tail, p)
                
                #print (p)
            
            return '... /'+p
        
        
        def saveNewCategory(self):
            name = self.currentScreen.ids.ti_name.text
            
            if(len(name)<1):
                self.showPopup("Fehler","Bitte gib einen Namen ein!")
                return
            
            
            path = self.themesDirectories[0]
            
            #todo check if file exsists already
            
            Notecards.createEmptyXML(None,join(path,name+'.xml'))
            
            #load main menue
            self.load_screen('mainmenu','down')
            self.updateThemeList()         
            

        def editCards(self,path,direction):
            """edit the cards of the theme"""

            self.load_screen('editmenu',direction)

            #load the notecards
            #todo catch FileNotFound Exception
                       
            self.notecards = Notecards(path)
            
            
            self.updateQuestionList()
            
            
        def updateQuestionList(self):
            
            
            #get the Layout that contains the List of Questions
            qList = self.currentScreen.ids.qList    
            
            # when we add children to the grid layout, its size doesn't change at
            # all. we need to ensure that the height will be the minimum required to
            # contain all the childs. (otherwise, we'll child outside the bounding
            # box of the childs)
            
            qList.bind(minimum_height=qList.setter('height'))
            
                
            #remove all quetions from the list and add the new ones
            qList.clear_widgets()
            
            questions = self.notecards.getQuestions()
            
            #set the right id for the new btn
            self.currentScreen.ids.tbtn_0.id='tbtn_0'
            self.currentScreen.ids.tbtn_0.state = 'down'
            
            #clear the Inputfields
            self.newCard()
            
            
            #callback for the btn            
            def callback(instance):
                
                #ids have the format *_id 
                tmp=instance.id.split('_')             
                                
                self.loadCard(tmp[len(tmp)-1])       
            
            
            #create a toggleButton for each question
            for q in questions:
                
                if len(q.text) > 30:
                    txt = q.text[0:30]+' ...'
                else:
                    txt = q.text                
                
                btn = ToggleButton(id='tbtn_'+q.id, text=txt, group='questions', state = 'normal',size_hint_y=None, height='40dp')                
                
                btn.bind(on_press=callback)                
                
                qList.add_widget(btn)
                
                #qList.ids["tbtn_"+q.id]=btn.proxy_ref
            
            #print(qList.ids)
            #print(screen.ids)
        
        def loadCard(self,id):             
            """loads the question and the answer from the selected (id) card """
                       
            card = self.notecards.getCard(id)   
                      
            self.currentScreen.ids.ti_question.text = card.getQuestion()
           
            answer=''
            
            for a in card.getAnswer():
                answer = answer + '(*) '+a+'\n'
                
            self.currentScreen.ids.ti_answer.text = answer
        
        def newCard(self):
            """deletes the TextInputs"""
            
            self.currentScreen.ids.ti_question.text = ''
            self.currentScreen.ids.ti_answer.text = ''
            
        
        def saveCard(self):
            """saves a new card or the edited card"""
            
            btns = ToggleButtonBehavior.get_widgets('questions')
            
            btn_pressed = False
            
            #get the button wiche is pressed
            for btn in btns:
                if(btn.state == 'down'):
                    btn_pressed = True
                    break
            
            if(not btn_pressed):
                self.showPopup("Fehler","Wähle eine Karte aus")
                return
            
            #get the card Id ('0'  if new card)
            tmp=btn.id.split('_')
            cardId=tmp[len(tmp)-1]
            
            #get the values of the TextInputs
            q=self.currentScreen.ids.ti_question.text.strip()
            a=self.currentScreen.ids.ti_answer.text.strip()
            
            #check it
            if(len(q)<2):
                self.showPopup("Fehler","Bitte gib eine Frage ein!")
                return
            
            if(len(a)<1):
                self.showPopup("Fehler","Bitte gib eine Antwort ein!")
                return
            
            
            answers = []
            
            tmp = a.split('(*)')
            
            for item in tmp:                 
                if(len(item.strip())>0):
                    answers.append(item.strip())
                      
                       
            #edits an existing card or creates a new one if id is '0'
            self.notecards.setCard(cardId,q,answers) 
            
            
            self.notecards.saveAsXML()
            
                            
            
            #if new Question -> delte Inputtext
            if(cardId == '0'):
                q=self.currentScreen.ids.ti_question.text=''
                a=self.currentScreen.ids.ti_answer.text=''
            
            self.updateQuestionList()
            
            
            
            self.showPopup("speichern","Deine Änderungen\nwurden gespeichert!\n\n          \(^_^)/")
         
        def deleteCard(self):
            """delets the selected card"""
            
            btns = ToggleButtonBehavior.get_widgets('questions')
            
            #get the button wiche is pressed
            for btn in btns:
                if(btn.state == 'down'):
                    break
            
            #get the card Id ('0'  if new card)
            tmp=btn.id.split('_')
            cardId=tmp[len(tmp)-1]
            
            if cardId == '0':
                return
            
            self.notecards.deleteCard(cardId)
            
            self.updateQuestionList()
        
        
        def deleteCategory(self, path):
            """Deletes the .xml file of the selected Category"""
                      
            filename = os.path.split(path)[1].split('.xml')[0]
                               
            
            content = BoxLayout(orientation='vertical')              
            popup = Popup(title='Kategorie Löschen',content=content, auto_dismiss=False, size_hint=(.7,.7) )
            
            delCat = 0
            
            def callback(instance):
                
                #print(path)
                
                #TODO   Exceptions
                os.remove(path)
            
                self.updateThemeList()
                
                popup.dismiss()
            
            
            q = 'Soll die Kategorie \n'+filename+'\nwirklich glöscht werden?'
            content.add_widget(Label(text=q, font_size='20sp', size_hint_y=None, markup=True))
            content.add_widget(Label())
            
            btnBox = BoxLayout(orientation='horizontal', size_hint_y = None)              
            
            btn_abr = Button(text='Abbrechen')
            # bind the on_press event of the button to the dismiss function
            btn_abr.bind(on_press=popup.dismiss)
            
            btn_lo = Button(text='Löschen')
            btn_lo.bind(on_press=callback)
            
            
            btnBox.add_widget(btn_abr)
            btnBox.add_widget(btn_lo)
                        
            content.add_widget(btnBox)
            

            

            # open the popup
            popup.open()
            
            
            
            
        
        
        
        def showPopup(self,title ,txt):
            """shows a Popup witha given titel and text"""
            
            content = BoxLayout(orientation='vertical')              
            
            content.add_widget(Label(text='[b]'+txt+'[b]', font_size='20sp', size_hint_y=None, markup=True))
            content.add_widget(Label())
            
            btn = Button(text='OK',size_hint_y=None)
                        
            content.add_widget(btn)
            popup = Popup(title=title,content=content, auto_dismiss=False, size_hint=(.5,.5) )

            # bind the on_press event of the button to the dismiss function
            btn.bind(on_press=popup.dismiss)

            # open the popup
            popup.open()
        
    
            

if __name__ == '__main__':
        pytex_notecardApp().run()



