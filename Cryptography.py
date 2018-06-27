import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from math import gcd
import random
import Math_Modules


class AESCipher:

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


class RSA:
    def __init__(self):
        self.p = 0
        self.q = 0
        self.N = 0
        self.e = 0
        self.d = 0

    def setRSA(self, p, q, N, e, d):
        self.p = p
        self.q = q
        self.N = N
        self.e = e
        self.d = d

    def setPublicKey(self, N, e):
        self.N = N
        self.e = e

    def setPrivateKey(self, p, q, d):
        self.p = p
        self.q = q
        self.d = d

    def generatePublic(self):
        # return 608304910142350396698363327001812754362885774565113507467145687232890587785014631394173069824500094829807307054273835218156320703304105285660931778433496412765294560162930708921682965665533072584084877545594795640400563105158139815
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


class DH:
    def __init__(self):
        self.p = 0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371
        self.g = 0xA4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5
        self.privatePower = self.generatePrivatePower()
        self.publicKey = self.generatePublicKey()

    def generatePrivatePower(self):
        return random.randrange(2, self.p - 1)

    def generatePublicKey(self):
        return Math_Modules.fast_power(self.g, self.privatePower, self.p)

    def generatePrivateKey(self, value):
        self.privateKey = Math_Modules.fast_power(value, self.privatePower, self.p)


def powerModulo(message, power, modulo):
    return Math_Modules.fast_power(message, power, modulo)

def hashMessageToInt(message):
    m = hashlib.sha256()
    m.update(message.encode())
    h = m.hexdigest()
    return int(h, 16)

def hashBytesToInt(bytes):
    m = hashlib.sha256()
    m.update(bytes)
    h = m.hexdigest()
    return int(h, 16)

def packMessage(bytes, signKey, modulo):
    from json import dumps
    hashedMessage = hashBytesToInt(bytes)
    signature = powerModulo(hashedMessage, signKey, modulo)
    packed = {
            'message': bytes.decode(),
            'signature': signature
           }
    # print(hashedMessage)
    return dumps(packed)

def verifySignature(signature, message, key, modulo):
    hashedMessage = hashMessageToInt(message)
    decryptedSignature = powerModulo(signature, key, modulo)
    return hashedMessage == decryptedSignature