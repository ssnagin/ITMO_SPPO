"""

Regular Expressions v.1.0
by ssnagin

"""

import re

while True:
    print(""" ssngn | Regular Expressions ver. 1.0\n       | Select item:""")

    command = int(input())
    # (?i)\b{0,}[ёюаеоияыиу]{2}(\s|[^ёюаеоияыиу\s])\s