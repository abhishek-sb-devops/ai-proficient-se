import string


class Base62Encoder:
    """High-performance Base62 encoder for numeric identifier conversion."""

    BASE62_ALPHABET: str = string.digits + string.ascii_letters
    BASE: int = len(BASE62_ALPHABET)

    @classmethod
    def encode(cls, num: int) -> str:
        if not isinstance(num, int):
            raise TypeError("Number to encode must be an integer.")
        if num < 0:
            raise ValueError("Number to encode must be non-negative.")
        if num == 0:
            return cls.BASE62_ALPHABET[0]

        digits = []
        while num:
            num, rem = divmod(num, cls.BASE)
            digits.append(cls.BASE62_ALPHABET[rem])

        digits.reverse()
        return "".join(digits)
