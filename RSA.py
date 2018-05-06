from math import gcd
import random
import Math_Modules


class RSA:
    def __init__(self):
        self.p = 33478071698956898786044169848212690817704794983713768568912431388982883793878002287614711652531743087737814467999489
        self.q = 36746043666799590428244633799627952632279158164343087642676032283815739666511279233373417143396810270092798736308917
        self.N = self.p * self.q
        self.e = self.generatePublic()
        self.d = self.generatePrivate()

    def generatePublic(self):
        fiValue = self.fiFunction()
        checkedE = random.randrange(2, fiValue)
        while gcd(checkedE, fiValue) != 1:
            checkedE = random.randrange(2, fiValue)
        return checkedE

    def generatePrivate(self):
        return Math_Modules.modulo_multiplicative_inverse(self.e, self.fiFunction())

    def fiFunction(self):
        return (self.p - 1)*(self.q-1)

    def encryption(self, message):
        return Math_Modules.fast_power(message, self.e, self.N)

    def decryption(self, ciphertext):
        return Math_Modules.fast_power(ciphertext, self.d, self.N)





