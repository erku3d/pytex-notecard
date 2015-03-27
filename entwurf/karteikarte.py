#!/user/bin/env Python3
# -*- coding: utf-8 -*-

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element

import xml.etree.ElementTree as ET

class Card(object):
    """a card contains a question and answers"""
    def __init__(self, question, answer):
        self._question = question
        self._answer = answer

    def getQuestion(self):
        """returns the Question"""
        return self._question

    def getAnswer(self):
        """returns the list of answeritems"""
        return self._answer



class Notecards(object):
    """parses the given xml file to create a data structure"""

    def __init__(self, file_name):
        #todo Exceptions
        self._file = file_name
        self._tree = ET.parse(self._file)
        self._root = self._tree.getroot()

        self._notecards = []

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

            self._notecards.append(Card(q.text,answer))

    def getNotecards(self):
        """returns the list of cards"""
        return self._notecards


