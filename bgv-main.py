import numpy as np
from typing import Tuple, List
import random

class BGVEncryption:
    def __init__(self, n: int = 1024, q: int = 2**32, t: int = 2):
        """
        Initialize the BGV encryption system.
        Args:
            n: Ring dimension (power of 2)
            q: Modulus for ciphertext space
            t: Plaintext modulus
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
        # Generate secret key (binary)
        sk = np.random.randint(0, 2, self.n)
        
        # Generate public key
        a = np.random.randint(0, self.q, self.n)
        e = np.random.randint(-self.q//4, self.q//4, self.n)
        pk = (-np.polyval(a, sk) + e) % self.q
        
        return sk, pk
    
    def _encode(self, message: int) -> np.ndarray:
        """
        Encode a message into a polynomial.
        Args:
            message: Integer message to encode
        Returns:
            Encoded polynomial
        """
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
        # Take the constant term as the message
        return int(polynomial[0])
    
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
        
        # Generate random polynomial
        u = np.random.randint(0, 2, self.n)
        
        # Generate error polynomial
        e1 = np.random.randint(-self.q//4, self.q//4, self.n)
        e2 = np.random.randint(-self.q//4, self.q//4, self.n)
        
        # Compute ciphertext components
        c0 = (np.polyval(self.pk, u) + e1 + self.q//self.t * m) % self.q
        c1 = (np.polyval(self.pk, u) + e2) % self.q
        
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
        m = (c0 - np.polyval(c1, self.sk)) % self.q
        
        # Scale and round
        m = np.round(m * self.t / self.q) % self.t
        
        # Decode
        return self._decode(m)
    
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
        Multiply two ciphertexts.
        Args:
            ct1: First ciphertext
            ct2: Second ciphertext
        Returns:
            Product of the ciphertexts
        """
        c0_1, c1_1 = ct1
        c0_2, c1_2 = ct2
        
        # Compute product components
        c0_prod = (c0_1 * c0_2) % self.q
        c1_prod = (c0_1 * c1_2 + c1_1 * c0_2) % self.q
        c2_prod = (c1_1 * c1_2) % self.q
        
        # Relinearize (simplified version)
        c0_final = (c0_prod + self.pk * c2_prod) % self.q
        c1_final = (c1_prod + self.pk * c2_prod) % self.q
        
        return c0_final, c1_final

# Example usage
if __name__ == "__main__":
    # Create BGV instance with smaller parameters for better demonstration
    bgv = BGVEncryption(n=4, q=2**16, t=2)  # Using smaller parameters for demonstration
    
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