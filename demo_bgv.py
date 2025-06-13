from bgv import BGV

if __name__ == "__main__":
    bgv = BGV(n=1024, q=2**15, t=257)
    m1 = int(input("Enter first number :"))
    m2 = int(input("Enter second number: "))
    print(f"Original messages: m1={m1}, m2={m2}")
    ct1 = bgv.encrypt(m1)
    ct2 = bgv.encrypt(m2)
    # Homomorphic addition
    ct_add = bgv.add(ct1, ct2)
    dec_add = bgv.decrypt(ct_add)
    print(f"Decrypted (m1 + m2): {dec_add} (expected {(m1 + m2) % bgv.t})")
    # Homomorphic multiplication
    ct_mul = bgv.multiply(ct1, ct2)
    ct_mul_relin = bgv.relinearize(ct_mul)
    dec_mul = bgv.decrypt(ct_mul_relin)
    print(f"Decrypted (m1 * m2): {dec_mul} (expected {(m1 * m2) % bgv.t})") 