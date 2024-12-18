from .byte import Byte
from .word import Word
from .state import State
from .operations import shiftRows, add_roundkey, subbytes, mixcolumns, rotword, subword, inv_shiftRows, inv_subbytes, inv_mixcolumns

def CIPHER(inp, Nr, w):
    state = inp
    
    state = add_roundkey(state, w[0 : 4])
    for round in range(1, Nr):
        state = subbytes(state)
        state = shiftRows(state)
        state = mixcolumns(state)
        state = add_roundkey(state, w[4 * round: 4 * round + 4])
    state = subbytes(state)
    state = shiftRows(state)
    state = add_roundkey(state, w[4 * Nr: 4 * Nr + 4])
    return state

def KEYEXPANSION(key, Nk, Nr):
    i = 0
    w = [-1]*(4*Nr + 4)

    Rcon = [
        Word([Byte(0x01), Byte(00), Byte(00), Byte(00)]),
        Word([Byte(0x02), Byte(00), Byte(00), Byte(00)]),
        Word([Byte(0x04), Byte(00), Byte(00), Byte(00)]),
        Word([Byte(0x08), Byte(00), Byte(00), Byte(00)]),
        Word([Byte(0x10), Byte(00), Byte(00), Byte(00)]),
        Word([Byte(0x20), Byte(00), Byte(00), Byte(00)]),
        Word([Byte(0x40), Byte(00), Byte(00), Byte(00)]),
        Word([Byte(0x80), Byte(00), Byte(00), Byte(00)]),
        Word([Byte(0x1b), Byte(00), Byte(00), Byte(00)]),
        Word([Byte(0x36), Byte(00), Byte(00), Byte(00)]),
    ]
    
    while i <= Nk-1:
        w[i] = Word(key[4 * i: 4 * i + 4])
        i = i + 1
    while i <= 4 * Nr + 3:
        temp = w[i - 1]
        if i % Nk == 0:
            temp = subword(rotword(temp)) + Rcon[i//Nk-1]
        elif Nk > 6 and i % Nk == 4:
            temp = subword(temp)
        w[i] = w[i - Nk] + temp
        i = i + 1
    return w


def INVCIPHER(inp, Nr, w):
    state = inp 
    state = add_roundkey(state, w[4 * Nr:4 * Nr + 4])
    for round in range(Nr - 1, 0, -1):
        state = inv_shiftRows(state)
        state = inv_subbytes(state)
        state = add_roundkey(state, w[4 * round:4 * round + 4])
        state = inv_mixcolumns(state)
    state = inv_shiftRows(state)
    state = inv_subbytes(state)
    state = add_roundkey(state, w[0:4])
    return state


if __name__ == "__main__":
    key = [
        Byte(0x54), Byte(0x68), Byte(0x61), Byte(0x74), Byte(0x73), Byte(0x20), 
        Byte(0x6D), Byte(0x79), Byte(0x20), Byte(0x4B), Byte(0x75), Byte(0x6E), 
        Byte(0x67), Byte(0x20), Byte(0x46), Byte(0x75)
    ]


    message = State([
        Word([Byte(0x54), Byte(0x77), Byte(0x6f), Byte(0x20)]),
        Word([Byte(0x4F), Byte(0x6E), Byte(0x65), Byte(0x20)]),
        Word([Byte(0x4E), Byte(0x69), Byte(0x6E), Byte(0x65)]),
        Word([Byte(0x20), Byte(0x54), Byte(0x77), Byte(0x6F)]),
    ])

    expanded_key = (KEYEXPANSION(key, 4, 10))
    encrypted = CIPHER(message, 10, expanded_key)
    for wor in encrypted.to_word():
        for byte in wor.word:
            print(hex(byte.byte), end = " ")
    print()
    print()
    decrypted = INVCIPHER(encrypted, 10, expanded_key)
    print(decrypted)
    print(message)

