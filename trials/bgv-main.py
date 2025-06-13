import numpy as np
from typing import Tuple, List
import random

class BGVEncryption:
    def __init__(self, n: int = 8, q: int = 2**16, t: int = 257):
        """
        Initialize the BGV encryption system.
        Args:
            n: Ring dimension (power of 2)
            q: Modulus for ciphertext space
            t: Plaintext modulus (should be prime)
        """
        self.n = n
        self.q = q
        self.t = t
        self.sk, self.pk = self._generate_keys()
        
    def _generate_keys(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate secret and public keys.
        Returns:
            Tuple of (secret_key, public_key)
        """
        # Generate secret key with small coefficients
        sk = np.random.randint(-1, 2, self.n)
        
        # Generate public key
        a = np.random.randint(0, self.q, self.n)
        e = np.random.randint(-4, 4, self.n)  # Small error
        pk = (-(a * sk) + e) % self.q
        
        return sk, pk
    
    def _encode(self, message: int) -> np.ndarray:
        """
        Encode a message into a polynomial.
        Args:
            message: Integer message to encode
        Returns:
            Encoded polynomial
        """
        # Map message to the range [0, t)
        message = message % self.t
        # Create a polynomial with the message as the constant term
        poly = np.zeros(self.n, dtype=np.int64)
        poly[0] = message
        return poly
    
    def _decode(self, polynomial: np.ndarray) -> int:
        """
        Decode a polynomial back to a message.
        Args:
            polynomial: Encoded polynomial
        Returns:
            Decoded message
        """
        # Take the constant term mod t
        return int(polynomial[0] % self.t)
    
    def encrypt(self, message: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Encrypt a message.
        Args:
            message: Integer message to encrypt
        Returns:
            Tuple of (c0, c1) ciphertext components
        """
        # Encode message
        m = self._encode(message)
        
        # Generate very small random values
        v = np.random.randint(0, 2, self.n)
        e0 = np.random.randint(-1, 2, self.n)
        e1 = np.random.randint(-1, 2, self.n)
        
        # Scale message
        scaled_m = (m * (self.q // self.t)) % self.q
        
        # Compute ciphertext components
        c0 = (scaled_m + e0 + self.pk * v) % self.q
        c1 = (e1 + self.pk * v) % self.q
        
        return c0, c1
    
    def decrypt(self, ciphertext: Tuple[np.ndarray, np.ndarray]) -> int:
        """
        Decrypt a ciphertext.
        Args:
            ciphertext: Tuple of (c0, c1) ciphertext components
        Returns:
            Decrypted message
        """
        c0, c1 = ciphertext
        
        # Compute decryption
        scaled_m = (c0 + np.sum(c1 * self.sk)) % self.q
        
        # Use only the constant term for decryption
        m = int(round((scaled_m[0] * self.t) / self.q)) % self.t
        
        return m
    
    def add(self, ct1: Tuple[np.ndarray, np.ndarray], 
            ct2: Tuple[np.ndarray, np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Add two ciphertexts.
        Args:
            ct1: First ciphertext
            ct2: Second ciphertext
        Returns:
            Sum of the ciphertexts
        """
        c0_1, c1_1 = ct1
        c0_2, c1_2 = ct2
        
        # Add corresponding components
        c0_sum = (c0_1 + c0_2) % self.q
        c1_sum = (c1_1 + c1_2) % self.q
        
        return c0_sum, c1_sum
    
    def multiply(self, ct1: Tuple[np.ndarray, np.ndarray], 
                ct2: Tuple[np.ndarray, np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Multiply two ciphertexts (toy version: keep only first two coefficients).
        Args:
            ct1: First ciphertext
            ct2: Second ciphertext
        Returns:
            Product of the ciphertexts
        """
        c0_1, c1_1 = ct1
        c0_2, c1_2 = ct2

        # Scale down the result to prevent overflow
        scale_factor = self.q // (self.t * self.t)

        # Compute product components (polynomial multiplication, but keep only first two terms)
        c0_prod = ((c0_1[0] * c0_2[0]) * scale_factor) % self.q
        c1_prod = ((c0_1[0] * c1_2[0] + c1_1[0] * c0_2[0]) * scale_factor) % self.q

        # Return as polynomials with only the constant term set
        c0_final = np.zeros(self.n, dtype=np.int64)
        c1_final = np.zeros(self.n, dtype=np.int64)
        c0_final[0] = c0_prod
        c1_final[0] = c1_prod
        return c0_final, c1_final

# Example usage
if __name__ == "__main__":
    # Create BGV instance with carefully chosen parameters
    bgv = BGVEncryption(n=8, q=2**16, t=257)  # t is prime, q is much larger than t
    
    # Example values
    a = 5
    b = 3
    
    # Encrypt values
    ct_a = bgv.encrypt(a)
    ct_b = bgv.encrypt(b)
    
    print("Encrypted values:")
    print(f"Encrypted a: {ct_a}")
    print(f"Encrypted b: {ct_b}")
    
    # Perform homomorphic addition
    ct_sum = bgv.add(ct_a, ct_b)
    decrypted_sum = bgv.decrypt(ct_sum)
    print(f"Homomorphic addition: {a} + {b} = {decrypted_sum}")
    
    # Perform homomorphic multiplication
    ct_product = bgv.multiply(ct_a, ct_b)
    decrypted_product = bgv.decrypt(ct_product)
    print(f"Homomorphic multiplication: {a} * {b} = {decrypted_product}") 