# Конспект лекций по Лабораторной работе №3


## Организация программ в БЭВМ



### Команды вызова подпрограммы и результата




## Аргументы и возвращаемые значения подпрограммы



### Способы организации передачи аргументов и возвращаемых значений


## Организация стека

![](Pasted%20image%2020250408171918.png)

![](Pasted%20image%2020250408171938.png)


### Рекурсивный вызов подпрограмм

Для облегчения работы составим простую тестовую программу. По ней можно делать микротрассировку и разбирать каждую из комманд.

```
ORG 0x0
LD #FE
PUSH

CLA
LD &0
POP

CALL 0x00A
HLT
JUMP 0x000

ORG 0x00A
RET
```


## Описание команд



### Команда CALL

В цикле исполнения: нужно сохранить в стек прежний IP, взять новый из BR (DR) в IP, SP - 1.

```
exec:

DR -- Значение адреса, куда обращаться


DR -> BR            Cохряняем адрес куда обращаться 
IP -> DR            Нужно чтобы сохранить адрес возврата
BR -> IP            Записываем адрес куда надо будет перейти
~0 + SP -> SP, AR   Делает SP - 1 и передает значение сразу в SP (обновляет указатель) и AR (чтобы потом записать в ячейку по этому адресу)
DR -> MEM(AR)

```

### Команда RET

Через SP взять адрес возврата и записать его в IP. Стек уменьшить

```
exec:
- ADRLESS (это уже цикл исполнения лол)

Если у AL10XX, то это работа со стеком (RET и POP)

AL10XX | SP -> AR
	   | MEM(AR) -> DR
RET    | DR -> IP
INCSP  | SP + 1 -> SP
```

### Команда PUSH


Команда PUSH складывает значение AC в стек.

Цикл исполнения PUSH в микрокоде:

| код | команда           | комментарии                                                                                                             |
| --- | ----------------- | ----------------------------------------------------------------------------------------------------------------------- |
| B7  | AC -> DR          | передает значение из AC в DR для дальнейшей передачи в память                                                           |
| 51  | ~0 + SP -> SP, AR | Делает SP - 1 и передает значение сразу в SP (обновляет указатель) и AR (чтобы потом записать в ячейку по этому адресу) |
| 55  | DR -> MEM(AR)     | Запись значения из DR в память по адресу AR                                                                             |

### Команда POP



```
AL10XX | SP -> AR
	   | MEM(AR) -> DR
POP    | DR -> AC
INCSP  | SP + 1 -> SP
```

### Команда SWAP

### Команда JUMP

```
DR -> IP
```
