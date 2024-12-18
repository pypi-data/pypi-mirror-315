from .byte import Byte
from .word import Word
from typing import List

class State:
    def __init__(self, words: List[Word]):
        self.state = [[0 for j in range(4)] for i in range(4)]
        for i in range(4):
            for j in range(4):
                self.state[i][j] = words[j].word[i]
    def __repr__(self):
        st = ""
        for i in range(4):
            for j in range(4):
                st+=str(hex(self.state[i][j].byte))+' '
            st+="\n"
        return st
    
    def to_word(self) -> Word:
        words = []
        for i in range(4):
            word = []
            for j in range(4):
                word.append(self.state[j][i])

            words.append(Word(word))
        return words
        
