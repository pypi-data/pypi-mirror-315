
class StubHash:
    def __init__(self, raw: str):
        self.__bit_size: int = 64
        self.__fixed_size: int = 0x123456789ABCDEF0
        self.__raw: str = raw
        self.__shift: int = 7

    def __right_rotate(self, value: int) -> int:
        result = ((value >> self.__shift) | (value << (self.__bit_size - self.__shift))) & ((1 << self.__bit_size) - 1)
        return result

    def __xor(self, char_value: int, hash_value: int) -> int:
        return hash_value ^ char_value

    def __hexdigest(self) -> str:
        hash_value = self.__fixed_size
        for char in self.__raw:
            char_value = ord(char)
            hash_value = self.__xor(char_value, hash_value)
            hash_value = self.__right_rotate(hash_value)
            hash_value = (hash_value + char_value) & 0xFFFFFFFFFFFFFFFF
        final_hash = f"{hash_value:018x}"
        return final_hash

    def __str__(self):
        return self.__hexdigest()

