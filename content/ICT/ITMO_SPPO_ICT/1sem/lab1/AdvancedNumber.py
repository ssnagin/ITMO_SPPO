class Symmetrical7CNumber:
    number: int
    number_converted: []
    number_converted_str: str

    DICTIONARY_7C = [-3, -2, -1, 0, 1, 2, 3]

    def __init__(self, number: int):
        self.assign(number)

    def assign(self, number: int):
        self.number = number

    def __str__(self):
        pass


def convert(num: int, base: int) -> str:

    res = ""
    while num > 0:
        remain = num % base - 3
        if remain < 0:
            remain = ("{"+str(num % base - 3)+"}").replace("-", "^")
        res = str(remain) + res
        num //= base
    return res

# Вывод чисел производить по принципу 33{^2}00
# input_number = Symmetrical7CNumber(input())
print(convert(-5, 7))


# -2 -1 0 1 2

# 7C

# -3,-2,-1,0,1,2,3

def make_combinations(n: int = 1) -> []:
    _res = []
    for i in range(1, n - 1):
        for j in range(-2,3):
            _res.append(j*5**i)
    return sorted(set(_res))


all_combinations = make_combinations(6)