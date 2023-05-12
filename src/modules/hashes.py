import hashlib


class HASH:
    def __init__(self, hash_name: str = 'base', value: str = None):
        self.hash_name: str = hash_name
        self.value: str = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f'HASH-{self.hash_name}({self.value})'

    def __eq__(self, other) -> bool:
        return self.value == other

    def __ne__(self, other) -> bool:
        return self.value != other


async def sha256(string: str) -> HASH:
    return HASH(
        hash_name='sha256',
        value=hashlib.sha3_256(string.encode()).hexdigest()
    )


async def sha512(string: str) -> HASH:
    return HASH(
        hash_name='sha512',
        value=hashlib.sha3_512(string.encode()).hexdigest()
    )
