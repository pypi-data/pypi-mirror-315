"""
Pure-Python implementation of the `Tonelli-Shanks algorithm \
<https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm>`__
for calculating a square root modulo a prime.
"""
from __future__ import annotations
from typing import Optional
import doctest

def _legendre(a: int, p: int) -> int:
    """
    Return the
    `Legendre symbol <https://en.wikipedia.org/wiki/Legendre_symbol>`__ for the
    two arguments.

    >>> _legendre(2, 7)
    1
    """
    return pow(a, (p - 1) // 2, p)

def tonellishanks(integer: int, prime: int) -> Optional[int]:
    """
    Return the least nonnegative residue modulo ``prime`` that is the square root
    of ``integer`` modulo ``prime`` (where ``prime`` is a prime number).

    >>> tonellishanks(4, 7)
    2
    >>> tonellishanks(2, 7)
    3
    >>> all(tonellishanks(n ** 2, 17) in (n, 17 - n) for n in range(1, 17))
    True

    Integer inputs are always interpreted as representing the corresponding
    least nonnegative residue modulo ``prime``.

    >>> tonellishanks(9, 7)
    3
    >>> tonellishanks(-5, 7)
    3
    >>> tonellishanks(-12, 7)
    3
    >>> tonellishanks(0, 7)
    0

    The result ``None`` is returned for inputs that are not a square modulo
    ``prime``.

    >>> tonellishanks(3, 7) is None
    True

    Any attempt to invoke this function with an argument that does not
    have the expected types (or does not fall within the supported range)
    raises an exception.

    >>> tonellishanks('abc', 19)
    Traceback (most recent call last):
      ...
    TypeError: 'str' object cannot be interpreted as an integer
    >>> tonellishanks(16, {})
    Traceback (most recent call last):
      ...
    TypeError: 'dict' object cannot be interpreted as an integer
    >>> tonellishanks(25, -1)
    Traceback (most recent call last):
      ...
    ValueError: prime modulus must be a positive integer

    This implementation has been adapted from the version presented at  
    `Tonelli-Shanks algorithm <https://rosettacode.org/wiki/Tonelli-Shanks_algorithm>`__
    on `Rosetta Code <https://rosettacode.org>`__.
    """
    if not isinstance(integer, int):
        raise TypeError(
            "'" + type(integer).__name__ + "'" + ' object cannot be interpreted as an integer'
        )

    if not isinstance(prime, int):
        raise TypeError(
            "'" + type(prime).__name__ + "'" + ' object cannot be interpreted as an integer'
        )

    if prime < 0:
        raise ValueError('prime modulus must be a positive integer')

    if integer == 0:
        return 0

    if _legendre(integer, prime) != 1:
        return None

    odd = prime - 1
    exponent = 0
    while odd % 2 == 0:
        odd >>= 1
        exponent += 1

    # Use the explicit formula.
    if exponent == 1:
        root = pow(integer, (prime + 1) // 4, prime)
        return min(root, prime - root)

    for z in range(2, prime):
        if prime - 1 == _legendre(z, prime):
            break

    c = pow(z, odd, prime)
    root = pow(integer, (odd + 1) // 2, prime)
    t = pow(integer, odd, prime)

    m = exponent
    t2 = 0
    while (t - 1) % prime != 0:
        t2 = (t * t) % prime
        for i in range(1, m):
            if (t2 - 1) % prime == 0:
                break
            t2 = (t2 * t2) % prime

        b = pow(c, 1 << (m - i - 1), prime)

        root = (root * b) % prime
        c = (b * b) % prime
        t = (t * c) % prime
        m = i

    return min(root, prime - root)

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
