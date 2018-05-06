import unittest
import RSA
import Math_Modules



class TestMath_Modules(unittest.TestCase):

    def testFastModulo(self):
        self.assertEqual(Math_Modules.fast_power(2, 37, 57), 2, "inversion doesnt work!")

    def testEuclid(self):
        self.assertEqual(Math_Modules.extended_euclid_gcd(6, 12)[0], 6, "gcd doesnt work")

    def testInversion(self):
        self.assertEqual(Math_Modules.modulo_multiplicative_inverse(2, 5), 3, "inversion doesnt work")


class TestRSA(unittest.TestCase):

    def testCoprime(self):
        self.myRSA = RSA.RSA()
        self.assertEqual(self.myRSA.e * self.myRSA.d % self.myRSA.fiFunction(), 1, "not coprime!")

    def testEncodingDecoding(self):
        self.myRSA = RSA.RSA()
        self.assertEqual(
            self.myRSA.decryption(self.myRSA.encryption(651651)), 651651, "RSA doesnt work"
        )





if __name__ == "__main__":
    unittest.main()