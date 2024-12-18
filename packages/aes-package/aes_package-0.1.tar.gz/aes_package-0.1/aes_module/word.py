from .byte import Byte

class Word:
    def __init__(self, bytes):
        assert len(bytes)==4
        self.word = [byte for byte in bytes]
    def matmul(self, other):
        b0, b1, b2, b3 = self.word
        a0, a1, a2, a3 = other.word
        d0 = (a0 * b0) + (a3 * b1) + (a2 * b2) + (a1 * b3)
        d1 = (a1 * b0) + (a0 * b1) + (a3 * b2) + (a2 * b3)
        d2 = (a2 * b0) + (a1 * b1) + (a0 * b2) + (a3 * b3)
        d3 = (a3 * b0) + (a2 * b1) + (a1 * b2) + (a0 * b3)
        return Word([d0, d1, d2, d3])
    def __add__(self, other):
        return Word([self.word[i] + other.word[i] for i in range(4)])
    
    def __repr__(self):
        return f"Word({self.word})"

    
