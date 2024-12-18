class Byte:
    def __init__(self, n: int):
        self.byte = n
    
    def __add__(self, other):
        return Byte(self.byte ^ other.byte)
    
    def xTimes(self):
        if self.byte & 1<<7:
            return Byte(((self.byte<<1)^1<<8)^27)
        else:
            return Byte(self.byte<<1)
    
    def raise_to_2(self, n: int):
        if n==0:
            return self
        a = self.xTimes()
        for _ in range(n-1):
            a = a.xTimes()
        return a
    def __mul__(self,other):
        ans = Byte(0)
        for i in range(8):
            if 1<<i & other.byte:
                ans += self.raise_to_2(i)
        return ans
    
    def inverse(self):
        a = Byte(1)
        for _ in range(254):
            a = a * self
        return a
    
    def get_bit(self, index: int):
        return (self.byte >> index) & 1
    
    def set_bit(self, index: int, bit:int):
        self.byte = self.byte | (bit << index)

    
    def __repr__(self):
        return f"Byte(byte={hex(self.byte)})"

if __name__ == "__main__":
    byte1 = Byte(5*16+7)
    byte2 = Byte(8*16)