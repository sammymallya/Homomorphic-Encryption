import random

class ToyBGV:
    def __init__(self, q=4096, t=17):
        self.q = q
        self.t = t
        self.sk = random.randint(1, self.q-1)
        self.pk = random.randint(1, self.q-1)
    def encrypt(self, m):
        return (m * (self.q // self.t)) % self.q
    def decrypt(self, c):
        return int(round((c * self.t) / self.q)) % self.t
    def add(self, c1, c2):
        return (c1 + c2) % self.q

bgv = ToyBGV()
a, b = 5, 3
ct_a = bgv.encrypt(a)
ct_b = bgv.encrypt(b)
ct_sum = bgv.add(ct_a, ct_b)
print('Decrypted sum:', bgv.decrypt(ct_sum))  # Should print 8