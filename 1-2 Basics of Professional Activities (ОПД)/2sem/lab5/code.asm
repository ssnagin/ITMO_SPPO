
ORG 0xA00
START:
    PUSH
    PUSH
    CALL READ_VALUE
    SWAP ; Сначала состояние: пытаемся понять, последнее ли это значение, или нет
    POP
    HLT
    SWAP ; Потом результат: если состояние = 1, то 
    POP
    

    SWAP ; Потом то, что было в аккуме (просто отчистить)
    POP
    ;CALL STORE
    HLT
  
AWAIT_DATA: ; Ожидает команду готовности
    IN 7
    AND #0x40
    BEQ AWAIT_DATA
    RET
  
READ_VALUE: ; Возвращает результат чтения в AC

; ~return adr after call~ | 0
;   ITERATOR   | 1  Итератор для цикла
;    IS_STOP   | 2
;   TEMP_VAR   | 3
;     RESULT   | 4
    
    ST &3
    CLA
    CLC

    LD #0x0
    ST &2
    CLA
    CLC

        
    IN 6
    SWAP
    ST &4
    
    LD &1
    ADD #0x01
    ST &1       ; ПОДУМАТЬ И ПЕРЕДЕЛАТЬ ТУТ НЕ РАБОТАЕТ
    AND #0x01
    SWAP
    BEQ READ_VALUE_GENERAL
    
    ST &4
    LD &3 ; Возвращаем TEMP_VAR обратно, если там что-то было...
    RET

; Сделать бы процедуры для автоматического push'a и swap-pop'a по числу...

; Прочесть букву
; Записать букву
; Это стоп символ?

; ========================================================================

ORG 0x47B
FIRST_CHAR:
    CALL READ_CHAR

    CMP STOP_CHAR
    BNE SECOND_CHAR

    CALL STORE_INC
    JUMP EXIT
    
SECOND_CHAR:
    SWAB
    CALL READ_CHAR
    SWAB

    CALL STORE_INC
    
    AND MASK
    SWAB    

    CMP STOP_CHAR
    BEQ EXIT

    JUMP FIRST_CHAR

STORE_INC:
    ST (START_ADDR)+
    RET

READ_CHAR: ; returns AC 8 bit char segment
    
    CALL WAIT_DEVICE_READY
    IN 6

    RET
    
WAIT_DEVICE_READY:
    IN 7
    AND #0xFF40
    BEQ WAIT_DEVICE_READY
    RET

EXIT:
    HLT


STOP_CHAR: WORD 0x0001 ; Стоп-символ
START_ADDR: WORD 0x56A ; Адрес начала
MASK_FIRST: WORD 0x00FF ; маска
MASK_INPUT: WORD 0xFF40 ; маска для корректной обработки состояния

================

ORG 0x47B
START:
    LD START_ADDR
    ST CURRENT_ADDR

ODD_CHAR:
    CALL READ_CHAR
    CALL STORE_LOW
    CMP STOP_CHAR
    BEQ EXIT

EVEN_CHAR:
    CALL READ_CHAR
    CALL STORE_HIGH
    CMP STOP_CHAR
    BEQ EXIT
    CALL ADJUST_CURRENT_ADDR
    JUMP ODD_CHAR

EXIT:
    HLT

ADJUST_CURRENT_ADDR:
    LD (CURRENT_ADDR)+
    RET

STORE_HIGH: ; Сохранить верхнюю часть
    SWAB
    PUSH
    LD (CURRENT_ADDR)
    AND MASK_LOW
    OR &0
    ST (CURRENT_ADDR)
    POP
    RET

STORE_LOW: ; Сохранить нижнюю часть 
    PUSH
    LD (CURRENT_ADDR)
    AND MASK_HIGH
    OR &0
    ST (CURRENT_ADDR)
    POP
    RET

READ_CHAR: ; returns AC 8 bit char segment
    CALL WAIT_DEVICE_READY
    CLA
    IN 6
    RET

WAIT_DEVICE_READY: ; Ожидание готовности ву-3
    IN 7
    AND #0x40
    BEQ WAIT_DEVICE_READY
    RET


START_ADDR: WORD 0x56A ; Адрес начала
CURRENT_ADDR: WORD ? ; Адрес текущей ячейки
STOP_CHAR: WORD 0x0000 ; Стоп-символ
MASK_HIGH: WORD 0xFF00
MASK_LOW: WORD 0x00FF

==================================================

ORG 0x47B
START:
    LD START_ADDR
    ST CURRENT_ADDR

ODD_CHAR:
    CALL READ_CHAR
    CALL STORE_LOW
    CMP STOP_CHAR
    BEQ EXIT

EVEN_CHAR:
    CALL READ_CHAR
    CALL STORE_HIGH
    CMP STOP_CHAR
    BEQ EXIT
    CALL ADJUST_CURRENT_ADDR
    JUMP ODD_CHAR

EXIT:
    HLT

ADJUST_CURRENT_ADDR:
    LD (CURRENT_ADDR)+
    RET

STORE_HIGH: ; Сохранить верхнюю часть
    SWAB
    PUSH
    LD (CURRENT_ADDR)
    AND MASK_LOW
    OR &0
    ST (CURRENT_ADDR)
    POP
    RET

STORE_LOW: ; Сохранить нижнюю часть 
    PUSH
    LD (CURRENT_ADDR)
    AND MASK_HIGH
    OR &0
    ST (CURRENT_ADDR)
    POP
    RET

READ_CHAR: ; returns AC 8 bit char segment
    CALL WAIT_DEVICE_READY
    CLA
    IN 6
    RET

WAIT_DEVICE_READY: ; Ожидание готовности ву-3
    IN 7
    AND #0x40
    BEQ WAIT_DEVICE_READY
    RET


START_ADDR: WORD 0x56A ; Адрес начала
CURRENT_ADDR: WORD ? ; Адрес текущей ячейки
STOP_CHAR: WORD 0x0000 ; Стоп-символ
MASK_HIGH: WORD 0xFF00
MASK_LOW: WORD 0x00FF

======================

ORG 0x47B
START:
    LD START_ADDR
    ST CURRENT_ADDR

ODD_CHAR:
    CALL LOAD_LOW
    CALL WRITE_CHAR
    CMP STOP_CHAR
    BEQ EXIT

EVEN_CHAR:
    CALL LOAD_HIGH
    CALL WRITE_CHAR
    CMP STOP_CHAR
    BEQ EXIT
    CALL ADJUST_CURRENT_ADDR
    JUMP ODD_CHAR

EXIT:
    HLT

ADJUST_CURRENT_ADDR:
    LD CURRENT_ADDR
    INC
    ST CURRENT_ADDR
    RET

LOAD_HIGH:
    LD (CURRENT_ADDR)
    AND MASK_HIGH
    SWAB
    RET

LOAD_LOW:
    LD (CURRENT_ADDR)
    AND MASK_LOW
    RET

WRITE_CHAR:
    CALL WAIT_DEVICE_READY
    OUT 6
    RET

WAIT_DEVICE_READY:
    PUSH
NOT_READY:
    IN 7
    AND #0x40
    BEQ NOT_READY
    POP
    RET

START_ADDR: WORD 0x56A ; Адрес начала
CURRENT_ADDR: WORD ? ; Адрес текущей ячейки
STOP_CHAR: WORD 0x0000 ; Стоп-символ
MASK_HIGH: WORD 0xFF00
MASK_LOW: WORD 0x00FF

ORG 0x56A
DU: WORD 0xD5E4
BO: WORD 0xCFC2
KK: WORD 0x3ACB

STOP_SIGN: WORD 0x0000

