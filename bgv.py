import numpy as np
import random
from typing import Tuple, Union

class BGV:
    def __init__(self, n: int = 1024, q: int = 2**15, t: int = 257):
        """
        Initialize the BGV encryption system.
        Args:
            n: Ring dimension (power of 2, e.g., 1024)
            q: Ciphertext modulus (large prime or power of 2)
            t: Plaintext modulus (should be prime)
        """
        self.n = n
        self.q = q
        self.t = t
        self.sk, self.pk = self._generate_keys()
        # For demo: evaluation key for relinearization (sk^2)
        self.ek = self.sk * self.sk % self.q

    def _generate_keys(self) -> Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Generate secret and public keys.
        Returns:
            Tuple of (secret_key, (a, b))
        """
        sk = np.random.randint(-1, 2, self.n)  # Small coefficients
        a = np.random.randint(0, self.q, self.n)
        e = np.random.randint(-4, 5, self.n)   # Small error
        b = (-a * sk + e) % self.q
        return sk, (a, b)

    def encode(self, message: int) -> np.ndarray:
        """
        Encode a message as a polynomial.
        """
        poly = np.zeros(self.n, dtype=np.int64)
        poly[0] = message % self.t
        return poly

    def decode(self, poly: np.ndarray) -> int:
        """
        Decode a polynomial to a message.
        """
        return int(np.round(poly[0]) % self.t)

    def encrypt(self, message: int) -> Tuple[np.ndarray, np.ndarray]:
        m = self.encode(message)
        a, b = self.pk
        v = np.random.randint(0, 2, self.n)
        e0 = np.random.randint(-1, 2, self.n)
        e1 = np.random.randint(-1, 2, self.n)
        scaled_m = (m * (self.q // self.t)) % self.q
        c0 = (scaled_m + e0 + b * v) % self.q
        c1 = (e1 + a * v) % self.q
        return c0, c1

    def decrypt(self, ct: Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, np.ndarray]]) -> int:
        if len(ct) == 2:
            c0, c1 = ct
            scaled_m = (c0 + c1 * self.sk) % self.q
        elif len(ct) == 3:
            c0, c1, c2 = ct
            scaled_m = (c0 + c1 * self.sk + c2 * (self.sk * self.sk % self.q)) % self.q
        else:
            raise ValueError("Ciphertext must have 2 or 3 components.")
        m = int(np.round((scaled_m[0] * self.t) / self.q)) % self.t
        return m

    def add(self, ct1, ct2):
        c0_1, c1_1 = ct1[:2]
        c0_2, c1_2 = ct2[:2]
        c0_sum = (c0_1 + c0_2) % self.q
        c1_sum = (c1_1 + c1_2) % self.q
        if len(ct1) == 3 or len(ct2) == 3:
            c2_1 = ct1[2] if len(ct1) == 3 else np.zeros(self.n, dtype=np.int64)
            c2_2 = ct2[2] if len(ct2) == 3 else np.zeros(self.n, dtype=np.int64)
            c2_sum = (c2_1 + c2_2) % self.q
            return c0_sum, c1_sum, c2_sum
        return c0_sum, c1_sum

    def poly_mul(self, a, b):
        # Schoolbook polynomial multiplication mod x^n+1
        res = np.zeros(2 * self.n - 1, dtype=np.int64)
        for i in range(self.n):
            for j in range(self.n):
                res[i + j] += a[i] * b[j]
        # Reduce mod x^n+1
        for i in range(self.n, 2 * self.n - 1):
            res[i - self.n] = (res[i - self.n] - res[i]) % self.q
        return res[:self.n] % self.q

    def multiply(self, ct1, ct2):
        c0_1, c1_1 = ct1
        c0_2, c1_2 = ct2
        c0 = self.poly_mul(c0_1, c0_2)
        c1 = (self.poly_mul(c0_1, c1_2) + self.poly_mul(c1_1, c0_2)) % self.q
        c2 = self.poly_mul(c1_1, c1_2)
        return c0, c1, c2

    def relinearize(self, ct):
        # For demo: just use sk^2 as evaluation key
        c0, c1, c2 = ct
        # Relinearize: c0' = c0 + c2 * ek, c1' = c1
        c0_new = (c0 + c2 * self.ek) % self.q
        c1_new = c1 % self.q
        return c0_new, c1_new 