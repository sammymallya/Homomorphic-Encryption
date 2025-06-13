import random
import math
from typing import Tuple

class PaillierEncryption:
    def __init__(self, key_length: int = 1024):
        """
        Initialize the Paillier encryption system with a given key length.
        Args:
            key_length: The bit length of the prime numbers used in key generation
        """
        self.key_length = key_length
        self.public_key, self.private_key = self._generate_keys()

    def _generate_keys(self) -> Tuple[Tuple[int, int], int]:
        """
        Generate public and private keys for the Paillier cryptosystem.
        Returns:
            Tuple containing (public_key, private_key)
            public_key is a tuple (n, g)
            private_key is lambda
        """
        # Generate two large prime numbers
        p = self._generate_prime(self.key_length // 2)
        q = self._generate_prime(self.key_length // 2)
        
        # Calculate n = p * q
        n = p * q
        
        # Calculate lambda = lcm(p-1, q-1)
        lambda_val = self._lcm(p - 1, q - 1)
        
        # Choose generator g
        g = n + 1
        
        # Calculate mu = (L(g^lambda mod n^2))^(-1) mod n
        mu = self._mod_inverse(self._L(pow(g, lambda_val, n * n), n), n)
        
        return (n, g), lambda_val

    def _generate_prime(self, bits: int) -> int:
        """Generate a random prime number of specified bit length."""
        while True:
            num = random.getrandbits(bits)
            if self._is_prime(num):
                return num

    def _is_prime(self, n: int) -> bool:
        """Check if a number is prime using Miller-Rabin primality test."""
        if n < 2:
            return False
        for _ in range(40):  # 40 iterations for high probability
            a = random.randint(2, n - 1)
            if self._miller_rabin(n, a):
                return False
        return True

    def _miller_rabin(self, n: int, a: int) -> bool:
        """Miller-Rabin primality test."""
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return False
        return True

    def _lcm(self, a: int, b: int) -> int:
        """Calculate Least Common Multiple of two numbers."""
        return abs(a * b) // math.gcd(a, b)

    def _L(self, x: int, n: int) -> int:
        """L function used in Paillier cryptosystem."""
        return (x - 1) // n

    def _mod_inverse(self, a: int, m: int) -> int:
        """Calculate modular multiplicative inverse."""
        def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y

        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        return (x % m + m) % m

    def encrypt(self, message: int) -> int:
        """
        Encrypt a message using the public key.
        Args:
            message: The plaintext message to encrypt
        Returns:
            The encrypted message
        """
        n, g = self.public_key
        r = random.randint(1, n - 1)
        n_squared = n * n
        return (pow(g, message, n_squared) * pow(r, n, n_squared)) % n_squared

    def decrypt(self, ciphertext: int) -> int:
        """
        Decrypt a ciphertext using the private key.
        Args:
            ciphertext: The encrypted message to decrypt
        Returns:
            The decrypted message
        """
        n, _ = self.public_key
        n_squared = n * n
        return (self._L(pow(ciphertext, self.private_key, n_squared), n) * 
                self._mod_inverse(self._L(pow(self.public_key[1], self.private_key, n_squared), n), n)) % n

    def add(self, ciphertext1: int, ciphertext2: int) -> int:
        """
        Add two encrypted values.
        Args:
            ciphertext1: First encrypted value
            ciphertext2: Second encrypted value
        Returns:
            Encrypted sum of the two values
        """
        n, _ = self.public_key
        n_squared = n * n
        return (ciphertext1 * ciphertext2) % n_squared

    def multiply(self, ciphertext: int, plaintext: int) -> int:
        """
        Multiply an encrypted value by a plaintext value.
        Args:
            ciphertext: Encrypted value
            plaintext: Plaintext value
        Returns:
            Encrypted product
        """
        n, _ = self.public_key
        n_squared = n * n
        return pow(ciphertext, plaintext, n_squared)

# Example usage
if __name__ == "__main__":
    # Create an instance of the encryption system
    paillier = PaillierEncryption(key_length=512)  # Using 512 bits for demonstration

    # Example values
    a = 5
    b = 3

    # Encrypt the values
    encrypted_a = paillier.encrypt(a)
    encrypted_b = paillier.encrypt(b)
    print("Encrypted values:")
    print(f"Encrypted a: {encrypted_a}")
    print(f"Encrypted b: {encrypted_b}")
    # Perform homomorphic addition
    encrypted_sum = paillier.add(encrypted_a, encrypted_b)
    decrypted_sum = paillier.decrypt(encrypted_sum)
    print(f"Homomorphic addition: {a} + {b} = {decrypted_sum}")

    # Perform homomorphic multiplication
    encrypted_product = paillier.multiply(encrypted_a, b)
    decrypted_product = paillier.decrypt(encrypted_product)
    print(f"Homomorphic multiplication: {a} * {b} = {decrypted_product}") 