from re import I


def gcd(a:int, b:int)-> int:
    """
    Method to count the greatest common divisor of two number.
    
    Parameters
    ----------
    a : int
        Number you want to count the gcd.
    b : int
        Number you want to count the gcd.
    """
    a = abs(a)
    b = abs(b)
    if (b == 0):
        return a
    return gcd(b, a % b)

def relativePrime(a:int, b:int)->bool:
    """
    Method to check relative prime of two number.

    Parameters
    ----------
    a : int
        Number you want to check relative prime.
    b : int
        Number you want to check relative prime.
    """
    return gcd(a, b) == 1

def modularInverse(a:int, b:int) -> int:
    """
    Method to find modular inverse of two number.

    Return the modular inverse of two number or 0 if modular inverse not exist.

    Parameters
    ----------
    a : int
        Number you want to check modular inverse.
    b : int
        Number you want to check modular inverse.
    """
    a = a % b
    for i in range (b):
        if ((i*a) % b == 1):
            return i
    return 0

# alphabets is a string that represent all Indonesia alphabet.
alphabets:str = "abcdefghijklmnopqrstuvwxyz"