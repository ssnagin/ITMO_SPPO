ALLOWED_DIGITS = [{"0", "1"}, {"1", "0"}, {"1"}, {"0"}]
NAMES = ["r1", "r2", "i1", "r3", "i2", "i3", "i4"]


def intro() -> str:
    return "ssngn | Hamming code ver. 1.0\nINFO  | Запись делать след. образом: r1 r2 i1 r3 i2 i3 i4"


def regular_check(binary_number: str) -> bool:
    global ALLOWED_DIGITS
    if len(binary_number) != 7: return False

    for element in ALLOWED_DIGITS:
        if set(binary_number) == element:
            return True

    return False


def parse_bits(number: str) -> []:
    """
    output: [r1, r2, i1, r3, i2, i3, i4]
    """
    return [int(x) for x in number]


def parse_payload_bits(bits: []) -> []:
    """
    output: [i1, i2, i3, i4]
    """
    parsed = parse_bits(number)
    return [bits[2], bits[4], bits[5], bits[6]]


def hamming_7_4(number: str) -> str:

    global NAMES

    # Our response to the console:
    response = " ...  | \n"

    # Count syndromes:
    bits = parse_bits(number)


    syndromes = [
        bits[0] ^ bits[2] ^ bits[4] ^ bits[6],
        bits[1] ^ bits[2] ^ bits[5] ^ bits[6],
        bits[3] ^ bits[4] ^ bits[5] ^ bits[6],
    ]

    if syndromes == [0, 0, 0]:
        response = "      | " + str(bits[2]) + str(bits[4]) + str(bits[5]) + str(bits[6])
        return response

    # wrong_bit_place = int(str(syndromes[0]) + str(syndromes[1]) + str(syndromes[2]), 2)
    wrong_bit_place = (syndromes[2] << 2) | (syndromes[1] << 1) | syndromes[0]
    response += "ERROR | Wrong bit place: " + str(wrong_bit_place) + f" ({NAMES[wrong_bit_place - 1]})\n" +\
                "WAS   | Replaced with " + str(int(not bits[wrong_bit_place - 1])) + "\n"

    bits[wrong_bit_place - 1] = int(not bits[wrong_bit_place - 1])

    payload_bits = parse_payload_bits(bits)

    response += "FIXED | Payload is " + "".join(str(x) for x in payload_bits)

    return response


print(intro())

while True:

    number = input("Input | Binary number (7 bits): ")

    if not regular_check(number):
        print("Error | check if the number was written correctly.")
        continue

    print(hamming_7_4(number))
    break