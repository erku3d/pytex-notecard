#!/user/bin/env Python3
# -*- coding: utf-8 -*-

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment

import xml.etree.ElementTree as ET

from xml.dom import minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    
    return reparsed.toprettyxml(indent="  ")

class TextObj(object):
    """contains a text and an id as string"""
    def __init__(self, text, id):
        self.text = text        
        self.id = str(id)
    
#    def __str__(self):
#       """overloading the standard str method"""
#       return self.text
    
     


class Card(object):
    """a card contains a question, a answers and an id as string"""
    def __init__(self, question, answer, id):
        self._question = question
        self._answer = answer
        self._id = str(id)
        
    def getQuestion(self):
        """returns the Question"""
        return self._question
    
    def setQuestion(self,question):
        """sets a qiven question"""
        self._question = question

    def getAnswer(self):
        """returns the list of answeritems"""
        return self._answer
        
    def setAnswer(self,answer):
        """sets a qiven answer"""
        self._answer = answer
    
    def getId(self):
        """returns the id of the card"""
        return self._id
    
    def setCard(self, question, answer):
        """sets the question and the answer of the card """
        self._question = question
        self._answer = answer
        #todo rais Exception if the id isn't set!



class Notecards(object):
    """parses the given xml file to create a data structure"""

    def __init__(self, file_name):
			
        #todo Exceptions
        self._file = file_name
        self._tree = ET.parse(self._file)
        self._root = self._tree.getroot()

        self._notecards = []
        
        self._currentId = 0

        self._getNotecardsFromTree()
        
        
        
        

    def _getNotecardsFromTree(self):
        """creats a list of cards from the tree"""

        #todo exceptions
        #todo bilder in anworten (evtl. auch in fragen)
              

        for card in self._root:
            q = card.find('question')

            items = card.find('answer').findall('item')

            answer = []

            for a in items:
                answer.append(a.text)

            self._notecards.append(Card(q.text,answer,self._getNextId()))
                     
    
    def _getNextId(self):
        """returns the next id"""
        
        self._currentId = self._currentId + 1
        
        return str(self._currentId)
       
    def _getLastId(self):
        return str(self._currentId)    

    def getNotecards(self):
        """returns the list of cards"""
        return self._notecards

    def getQuestions(self):
        """returns a list of questions"""
        q=[]

        for card in self._notecards:
            q.append(TextObj(card.getQuestion(),card.getId()))

        return q
        
    def getCard(self,id):
        """returns the card with the given id"""
        for c in self._notecards:
                        
            if(id == c.getId()):
                return c
                
    def setCard(self, id, question, answer):
            """sets the Card with the id or creates a new one if id='0'"""
            
            if(id == '0'):
                self._notecards.append(Card(question,answer,self._getNextId()))
            
            else:
                for c in self._notecards:
                     
                    if(id == c.getId()):                        
                        c.setCard(question,answer)
                        
    def deleteCard(self,id):
        """deletes the card with the given id"""
                
        for c in self._notecards:                                
                    if(id == c.getId()):                        
                        self._notecards.remove(c)
                        return
    
    def saveAsXML(self):
        root = Element('notecards')
        
        for c in self._notecards:
            
            card = SubElement(root,'card')
            
            question = SubElement(card, 'question')
            question.text = c.getQuestion()
            
            answer = SubElement(card,'answer')
            
            for a in c.getAnswer():
                item = SubElement(answer,'item')
                item.text = a
        
        #todo Exceptions
                
        file = open(self._file,'w')
                
        file.write( prettify(root))
        file.close()
                              
            
        #print(prettify(root))   
        
    def createEmptyXML(self,filename):
        """creates an empty xml file for a new card deck"""
        
        root = Element('notecards')
                        
        #todo Exceptions
                
        file = open(filename,'w')
                
        file.write( prettify(root))
        file.close()
        
                
            
                        
            
        













