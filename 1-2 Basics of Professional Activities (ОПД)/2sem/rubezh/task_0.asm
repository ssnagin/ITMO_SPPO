;Задание №1. Разработать программу для работы с элементами массива M, в которой:
;1. Массив имеет следующие характеристики:
;- адрес начала массива в памяти БЭВМ - 0x6df;
;- число измерений исходного массива - 1;
;- количество элементов исходного массива - 16;
;- каждый элемент является знаковым числом с разрядностью 9 бит;
;- нумерация элементов начинается с 1;
;- элементы хранятся в массиве по границам слов, нет необходимости в плотной упаковке;
;2. Для элементов массива необходимо вычислить 32-х битное значение функции:
;- формула функции F(Mi) = 11 * Mi + 175;
;- 32-битный результат необходимо поместить в другой массив по адресу 0x400
;- Результатом является массив 32-х разрядных чисел равным количеству элементов исходного массива.
; Примечание: все числа представлены в десятичной системе счисления, если явно не указано иное.

ORG 0x6df
    WORD 0x1234 ;
    WORD 0x6543
    WORD 0xBBBA ;
    WORD 0xBEBA
    WORD 0xFABA ;
    WORD 0x789A
    WORD 0xCACA ;
    WORD 0xAFAC
    WORD 0x1234 ;
    WORD 0x6543
    WORD 0xBBBA ;
    WORD 0xBEBA
    WORD 0xFABA ;
    WORD 0x789A
    WORD 0xCACA ;
    WORD 0xAFAC

; 0000.000X.0000.0000

ORG 0x400
    WORD ?
    WORD ?

ORG 0x100
START:
    LD ARRAY_LENGTH
    ST ARRAY_ITERATOR
    LD ARRAY_START_ADDR
    ST ARRAY_CURRENT_ADDR

MAIN_LOOP:
    LD (ARRAY_CURRENT_ADDR)+
    
    CALL MAIN

    LOOP ARRAY_ITERATOR
    JUMP MAIN_LOOP
    HLT

MAIN: 
        
    PUSH
    CALL LOAD_ARRAY_ELEMENT
    POP ; current_array_element
    
    PUSH ; current_array_element 6
    CLA
    PUSH ; result_little 5
    PUSH ; result_big 4
    CALL FUNCTION
    POP
    HLT
    POP
    HLT
    POP

    RET



; returns array_element (&1) - out
LOAD_ARRAY_ELEMENT:

    LD &1
    AND SIGN_MASK
    
    ; CMP SIGN_MASK ; избыточно, но я просто чтобы показать
    BEQ EXTEND_SIGN_POSITIVE
    
;    EXTEND_SIGN_NEGATIVE:
    LD &1
    OR EXTENSION_MASK_MINUS

    EXTEND_SIGN_POSITIVE:
        LD &1
        AND EXTENSION_MASK_PLUS
        JUMP LOAD_ARRAY_ELEMENT_CONTINUE_1

LOAD_ARRAY_ELEMENT_CONTINUE_1:

    ST &1
    RET


; 
FUNCTION:
    PUSH ; sub_result_little 2
    PUSH ; sub_result_big 1
    PUSH ; current_sign (0000 plus, ffff minus)

    LD &6
    ST &2

    AND SIGN_MASK_32
    BEQ EXTEND_32_SIGN_PLUS

    EXTEND_32_SIGN_MINUS:
        LD #0xFF
        ST &1
        ST &0
        JUMP FUNCTION_CONTINUE_1
        
    EXTEND_32_SIGN_PLUS:
        LD #0x00
        ST &1
        ST &0
        
FUNCTION_CONTINUE_1:

    FUNCTION_MULTIPLY:
        LD &2 ; load sub result little
        ADD &6 ; add to current_array_element
        ST &2
        
        LD &1 ; load sub_result_big
        ADC &0
        ST &1

        LOOP ADD_MULTIPLIER
        CALL FUNCTION_MULTIPLY

    LD &2
    ADD ADD_CONSTANT
    ST &5

    LD &4
    ADC #0
    ST &4

    POP
    POP
    POP

    RET
    
ARRAY_START_ADDR: WORD 0x6df
ARRAY_CURRENT_ADDR: WORD ?
ARRAY_ITERATOR: WORD ?
ARRAY_LENGTH: WORD 16

SIGN_MASK: WORD 0x0100
EXTENSION_MASK_MINUS: WORD 0xFF00
EXTENSION_MASK_PLUS: WORD 0x00FF

SIGN_MASK_32: WORD 0x8000

ADD_MULTIPLIER: WORD 10 ; (11 - 1)
ADD_CONSTANT: WORD 175

ORG 0x100