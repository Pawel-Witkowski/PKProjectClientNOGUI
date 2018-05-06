def extended_euclid_gcd(a, b):
    """
    Returns a list `result` of size 3 where:
    Referring to the equation ax + by = gcd(a, b)
        result[0] is gcd(a, b)
        result[1] is x
        result[2] is y
    """
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a

    while r != 0:
        quotient = old_r//r
        old_r, r = r, old_r - quotient*r
        old_s, s = s, old_s - quotient*s
        old_t, t = t, old_t - quotient*t

    return [old_r, old_s, old_t]

def modulo_multiplicative_inverse(A, M):
    """
    Assumes that A and M are co-prime
    Returns multiplicative modulo inverse of A under M
    """

    gcd, x, y = extended_euclid_gcd(A, M)
    if x < 0:
        x += M
    return x

def fast_power(base, power, MOD):
    result = 1
    while power > 0:
        if power % 2 == 1:
            result = (result * base) % MOD
        power = power // 2
        base = (base * base) % MOD
    return result