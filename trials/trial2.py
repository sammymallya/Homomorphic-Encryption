import numpy as np
import random

# Parameters for BGV (toy example, not secure for real use)
N = 8  # Degree of the polynomial modulus (should be a power of 2)
q = 257  # Ciphertext modulus (should be a large prime)
t = 17   # Plaintext modulus

# Helper functions for polynomials

def poly_add(a, b):
    return [(x + y) % q for x, y in zip(a, b)]

def poly_sub(a, b):
    return [(x - y) % q for x, y in zip(a, b)]

def poly_mul(a, b):
    # Schoolbook multiplication, then reduce mod (x^N + 1)
    res = [0] * (2 * N - 1)
    for i in range(N):
        for j in range(N):
            res[i + j] += a[i] * b[j]
    # Reduce mod (x^N + 1)
    for i in range(N, 2 * N - 1):
        res[i - N] = (res[i - N] - res[i]) % q
    return [x % q for x in res[:N]]

def poly_scalar_mul(a, scalar):
    return [(x * scalar) % q for x in a]

def poly_mod(a, modulus):
    return [x % modulus for x in a]

def poly_round(a, modulus):
    return [int(round(x)) % modulus for x in a]

def sample_poly_small():
    # Sample from {-1, 0, 1}
    return [random.choice([-1, 0, 1]) for _ in range(N)]

def sample_poly_uniform():
    return [random.randint(0, q - 1) for _ in range(N)]

class BGV:
    def __init__(self):
        self.secret_key = sample_poly_small()
        self.public_key = self.keygen()

    def keygen(self):
        s = self.secret_key
        a = sample_poly_uniform()
        e = sample_poly_small()
        b = poly_sub(poly_scalar_mul(a, -1), poly_scalar_mul(e, 1))
        b = poly_add(b, poly_scalar_mul(s, 0))  # b = -a*s - e
        return (a, b)

    def encrypt(self, m):
        # m: integer in [0, t)
        m_poly = [m] + [0] * (N - 1)
        a, b = self.public_key
        u = sample_poly_small()
        e1 = sample_poly_small()
        e2 = sample_poly_small()
        ct0 = poly_add(poly_add(poly_scalar_mul(b, u[0]), e1), poly_scalar_mul(m_poly, q // t))
        ct1 = poly_add(poly_scalar_mul(a, u[0]), e2)
        return (ct0, ct1)

    def decrypt(self, ct):
        s = self.secret_key
        if len(ct) == 2:
            ct0, ct1 = ct
            prod = poly_mul(ct1, s)
            v = poly_add(ct0, prod)
        elif len(ct) == 3:
            ct0, ct1, ct2 = ct
            prod1 = poly_mul(ct1, s)
            prod2 = poly_mul(ct2, poly_mul(s, s))
            v = poly_add(poly_add(ct0, prod1), prod2)
        else:
            raise ValueError("Ciphertext must have 2 or 3 components.")
        scaled = [(x % q) * t / q for x in v]
        m = poly_round(scaled, t)
        return m[0]  # Only the constant term

    def add(self, ct1, ct2):
        ct0 = poly_add(ct1[0], ct2[0])
        ct1_ = poly_add(ct1[1], ct2[1])
        return (ct0, ct1_)

    def mul(self, ct1, ct2):
        # Naive multiplication (ciphertext size grows)
        c0 = poly_mul(ct1[0], ct2[0])
        c1 = poly_add(poly_mul(ct1[0], ct2[1]), poly_mul(ct1[1], ct2[0]))
        c2 = poly_mul(ct1[1], ct2[1])
        return (poly_mod(c0, q), poly_mod(c1, q), poly_mod(c2, q))

# Demo usage
if __name__ == "__main__":
    bgv = BGV()
    m1 = 5
    m2 = 7
    print(f"Original messages: m1={m1}, m2={m2}")
    ct1 = bgv.encrypt(m1)
    ct2 = bgv.encrypt(m2)
    # Homomorphic addition
    ct_add = bgv.add(ct1, ct2)
    dec_add = bgv.decrypt(ct_add)
    print(f"Decrypted (m1 + m2): {dec_add} (expected {(m1 + m2) % t})")
    # Homomorphic multiplication
    ct_mul = bgv.mul(ct1, ct2)
    dec_mul = bgv.decrypt(ct_mul)
    print(f"Decrypted (m1 * m2): {dec_mul} (expected {(m1 * m2) % t})") 