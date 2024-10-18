"""

Regular Expressions v.1.0
by ssnagin

ISU: 467525 ( [</ )

467525 % 6 = 5 [
467525 % 4 = 1 <
467525 % 8 = 5 /

"""
import re
import random
import sys

UNIT_TESTS_FIRST_TASK = [
    "Как же похорошела Москва при [</! Никаких []>\\ или )<O=- -- вот инвалиды! Только два добротных [</!",
    "Я помню чудное [</: Передо мной явилась [</, Как [</[</ ми[</моле[</[</тное виде[</нье, Как ге[</й чистой [</кр[</ас[</[</ты",
    "А вы [</ знали,[</ что вышел альбом у Coldplay? [<</ Называется Moon Music !![</!! Пока делал лабу, сидел и [</.",
    "В этой фразе содержится сокральный смысл, ведь она без лиц!",
    "На самом деле  357**_([</&)%([[[[</</</</)0[[</</YH*[</^NZuo регулярки не такие уж и сложные, в них можно разобраться за пару [[</<[</[<//[</......"
]
PATTERN_FIRST_TASK = r"\[\<\/"

UNIT_TESTS_SECOND_TASK = [
    "Пришлось потратить часа 3 и проштудировать всю методичку по регуляркам, чтобы сделать это (!) пятое задание (просто мрак). И даже кривошеее существо, (!)3 которое гуляет по парку, вам не поможет!"
    "Я че вспомнил, надо холодильник в общагу купить, а то без него совсем как-то грустно... :(",
    "Администрация города во Владимирской области попросила местных жителей подарить ей елку на Новый год.",
    "Аеоловые ыи, уюдовые жуи, и другие приключения Васи-алкоголика!",
    "Нуу пожалуйста-пожалуйста-пожалуйста, можно соотку за эту лабораторку? :_("
]
PATTERN_SECOND_TASK = r"(?i)\b\w*[ёюаеоияыиу][ёюаеоияыиу]\w*\b(?=\s\b(?!([бвгджзйклмнпрстфхцчшщьъ][^бвгджзйклмнпрстфхцчшщьъ\s]*){4,})\b)"

def log(right_space: str, left_space: str = "       "):
    """
    Shows something in console

    :param kwargs:
    :return: a string
    """

    left_space = str(left_space)
    right_space = str(right_space)

    right_space = " " + right_space

    if len(left_space) > 7:

        left_space = left_space[:7]
    if len(left_space) != 7:
        left_space = '{: ^7}'.format(left_space)

    print(str(left_space) + "|" + str(right_space))

def show_menu():
    MENU_ITEMS = [
        ["ssngn", "Regular Expressions ver. 1.0"],
        ["0", "Exit."],
        ["1", "Generate module test based on random generation"],
        ["2", "Show tests and answers (part 1)"],
        ["3", "Bonus task (part 2)"],
        ["4", "Bonus-bonus task (part 3)"],
    ]
    for i in range(len(MENU_ITEMS)):
        log(MENU_ITEMS[i][1], MENU_ITEMS[i][0])
    return

def generate_random_pseudo_word(characters_amount: int = 4) -> str:
    """
    Generates pseudo word (A-z + А-я + whitespace)

    :param characters_amount:
    :return:
    """
    result = ""

    LAT_DICTIONARY = [character for character in "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzАаБбВвГгДдЕеЁёЖжЗзИиКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"]
    result = "".join([random.choice(LAT_DICTIONARY) for i in range(characters_amount)])

    return result + " "

def generate_test_string(characters_amount: int = 1024, autotest=True) -> str:
    """
    Get a string for unit testing

    (0) -- add [</ in a result
    (1) e -- pick an eye
    (2) n -- pick a nose
    (3) m -- pick a mouth
    (4) w -- pick a random english word

    :param characters_amount:
    :return: row of characters (and faces) by given length
    """
    EYE = ["8", ";", "X", ":", "=", "]"]
    NOSE = ["-", "<", "-{", "<{"]
    MOUTH = ["(", ")", "P", "|", "\\", "/", "O", "="]

    result = ""
    faces_amount = 0

    while len(result) <= characters_amount:

        decision = random.randint(0, 4)

        if decision == 0:
            result += "[</"
        if decision == 1:
            result += random.choice(EYE)
        if decision == 2:
            result += random.choice(NOSE)
        if decision == 3:
            result += random.choice(MOUTH)
        if decision == 4:
            result += generate_random_pseudo_word(random.randint(1,10))

    result = result[:characters_amount]
    faces_amount = len(re.findall(PATTERN_FIRST_TASK, result))

    if autotest: result = f"({faces_amount} found) --> " + result

    return result

def first_unittest():
    for row in UNIT_TESTS_FIRST_TASK:
        amount = len(re.findall(PATTERN_FIRST_TASK, row))
        log(row, amount)

def second_unittest():
    for row in UNIT_TESTS_SECOND_TASK:
        amount = len(re.findall(PATTERN_SECOND_TASK, row))
        log(row, amount)


def third_unittest():
    pass

while True:

    show_menu()

    try:
        command = int(input("       | "))

        if command == 0:
            sys.exit()
        if command == 1:
            log(generate_test_string(20), "DONE!")
        if command == 2:
            first_unittest()
        if command == 3:
            second_unittest()
        if command == 4:
            third_unittest()

    except ValueError as e:
        log("Value Error: Invalid number", "ERR")