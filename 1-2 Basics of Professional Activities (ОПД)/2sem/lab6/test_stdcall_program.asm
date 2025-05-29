ORG 0xA00

START:
    PUSH ; result_even
    PUSH ; result_odd
    PUSH ; data_even
    PUSH ; data_odd
    LD #2
    PUSH ; sum_even
    LD #3
    PUSH ; sum_odd

    CALL FUNCTION

    SWAP
    POP

    SWAP
    POP

    SWAP
    POP

    SWAP
    POP

FUNCTION:
    LD #4
    PUSH ; VAR_1
    LD #5
    PUSH ; VAR_2
    LD #6
    PUSH ; VAR_3
    
    CLA

    LD &7
    ADD &5
    ST &9

    LD &6
    ADC &4
    ST &8

    POP
    POP
    POP