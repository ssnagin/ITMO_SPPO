функции и соглашения о вызывах

CALL

RET

когда люди писали на asm, всё хорошо: проблема когда люди придумали библиотеки,
там надо в правильном порядке вызвать функции. Из-за этого пошли несостыковки.

пример: `int pow (int base, int exp)`

проблема что кто-то привык передавать аргументы справа-налево, а кто-то наоборот

`int pow (int exp, int base)`

поэтому возник calling convention

Calling Convention регламентирует:

1. Порядок аргументов
	1. Место размещения аргументов
2. Место результата
	1. Возврат составных типов (агрегатов)
3. CLEANUP, отчистка стека

```java
int pow (int base, int exp) {
	int result = 1;
	for (int i = 0;  i < exp; i++) {
		result += base;
	}
	return result;
}
```

Идея polling convention в том, чтобы были кубики, которые мы могли бы вызывать. Мы не знаем и нам не интересно что внутри. Мы знаем с какими параметрами её вызвать, тк у нас есть прототип.

### Виды calling conventions

Их великое множество. Это зависит от архитектуры (регистров). Polling convention могут быть похожи формально, но отличаться в реализации. Наиболее частые:

- `stdcall` (MSVC, Microsoft)
- `cdecall` (стандартный вызов для языка C) (Unix в основном)
- `fastcall` (fast потому что пытается использовать только регистры) (internal functions)
- `thiscall` (для вызова методов класса, C++ methods) 
- `vectorcall` (SIMD, для передачи векторов в функцию)

**Причем здесь бэвм?** Стоит разобраться, как писать такие штуки для написания их на рубежке. В данном случае мы будем рассматривать `cdecall` и `fastcall`. 

Основное отличиие `thiscall` от `cdecall` -- передача `this` в регистр.

```c
int pow (int base, int exp) {
	int result = 1;
	for (int i = 0;  i < exp; i++) {
		result += base;
	}
	return result;
}
```

### ctdcall

- Аргументы в стек в ***обратном** порядке*. Сначала `exp`, потом `base`.

```c
int printf(char* format, ...)
```

На вершине стека сначала format, потом всё остальное. В vararge справа налево.

- Результат в регистр
- Отчищает вызывающая функция. Отчистка стека перед вызовом следующей функции, очистка аргументов. 

спросить про зарисовки

### stdcall

- Аргументы стека тоже в ***обратном** порядке*. Так сложилось :/
- Результат в регистр. В 99% соглашений это так.
- Очистка аргументов: вызываемая функция.

Отличие только тем, кто чистит аргументы. Прочитать.

#### Что-то важное

как писать код на бэвм на asm чтобы не думать головой? Допустим написать pow

```c
int pow (int base, int exp) {          |
	int result = 1;                    |
	for (int i = 0;  i < exp; i++) {   |
		result += base;                |
	}                                  |
	return result;                    \|/
}
```

CDECL: exp base

```asm
FPOW: 
```

стек: пишем все переменные в функции, нумеруем сверху снизу вверх (стек же так растёт, верно?)

```
EXP    3 ^
base   2 |
RET    1 |
RESULT 0 |
```

Цифры помогают не думать головой чтобы вписывать `&{сюда}`


я забыл про i внутри цикла. Ничего страшного, просто всё сдвигаем:
 
 ```
EXP    3 ^
base   2 |
RET    1 |
RESULT 0 |
i     -1 |
```

 ```
EXP    4 ^
base   3 |
RET    2 |
RESULT 1 |
i      0 |
```

Пишем код:

```assembly
FPOW: 
	PUSH ; | ПРОГЛОГ
	PUSH ; | т.к. RET смещён, мы смещаем это (?) тоже
	
	LD #1
	ST &1
	CLA
	ST &0
LO:
	LD &0
	CMP &4
	BGE L_EXIT

; нам нужно написать тело цикла
```

Допустим, вместо `base` у нас некоторая другая функция (штука).

```c
int mul(int a, int b)
```

Используйте AC как супер временная штука

 ```
EXP    4 ^
base   3 |
RET    2 |
RESULT 1 |
i      0 |
---------|
b'       |
a'       |
```

Сдвигаем стековый фрейм

```assembly
FPOW: 
	PUSH ; | ПРОГЛОГ
	PUSH ; | т.к. RET смещён, мы смещаем это (?) тоже
	
	LD #1
	ST &1
	CLA
	ST &0
LO:
	LD &0
	CMP &4
	BGE L_EXIT

	PUSH
	PUSH
```

 ```
EXP pow4 ^ 6 mul
base   3 | 5
RET    2 | 4
RESULT 1 | 3
i      0 | 2
---------|  
b'       | 1
a'       | 0
```

(В БЭВМ LOOP это цикл с постусловием.)

```assembly
FPOW: 
	PUSH ; | ПРОГЛОГ
	PUSH ; | т.к. RET смещён, мы смещаем это (?) тоже
	
	LD #1
	ST &1
	CLA
	ST &0
LO:
	LD &0
	CMP &4
	BGE L_EXIT

	PUSH
	PUSH
	
	LD &5
	ST &1
	LD &3
	ST &0
	CALL MULL
```

**1 КУБИК**
`SWAP-POP` -- снимает 1 значение со стека, не ломая AC

```assembly
FPOW: 
	PUSH ; | ПРОГЛОГ
	PUSH ; | т.к. RET смещён, мы смещаем это (?) тоже
	
	LD #1
	ST &1
	CLA
	ST &0
LO:
	LD &0
	CMP &4
	BGE L_EXIT

	PUSH
	PUSH
	
	LD &5
	ST &1
	LD &3
	ST &0
	CALL MULL

	SWAP
	POP
	SWAP
	POP
```


 ```
EXP  pow 4 ^
base     3 |
RET      2 |
RESULT   1 |
i        0 |
```

```assembly
FPOW: 
	PUSH ; | ПРОГЛОГ
	PUSH ; | т.к. RET смещён, мы смещаем это (?) тоже
	
	LD #1
	ST &1
	CLA
	ST &0
LO:
	LD &0
	CMP &4
	BGE L_EXIT

	PUSH
	PUSH
	
	LD &5
	ST &1
	LD &3
	ST &0
	CALL MULL

	SWAP
	POP
	SWAP
	POP
	ST &1
	LD &0
	INC
	ST &0

	JUMP LO ; Всё вернулось на круги своя
```

```assembly
FPOW: 
	PUSH ; | ПРОГЛОГ
	PUSH ; | т.к. RET смещён, мы смещаем это (?) тоже
	
	LD #1
	ST &1
	CLA
	ST &0
LO:
	LD &0
	CMP &4
	BGE L_EXIT

	PUSH
	PUSH
	
	LD &5
	ST &1
	LD &3
	ST &0
	CALL MULL

	SWAP
	POP
	SWAP
	POP
	ST &1
	LD &0
	INC
	ST &0

	JUMP LO ; Всё вернулось на круги своя

L_EXIT:
	LD &1
	; Тело функции закончилось

```

Локальные переменные ВСЕГДА ЧИСТИТ САМА ФУНКЦИЯ!!!

Пишем 2 раза swap-pop:

```assembly
FPOW: 
	PUSH ; | ПРОГЛОГ
	PUSH ; | т.к. RET смещён, мы смещаем это (?) тоже
	
	LD #1
	ST &1
	CLA
	ST &0
LO:
	LD &0
	CMP &4
	BGE L_EXIT

	PUSH
	PUSH
	
	LD &5
	ST &1
	LD &3
	ST &0
	CALL MULL

	SWAP
	POP
	SWAP
	POP
	ST &1
	LD &0
	INC
	ST &0

	JUMP LO ; Всё вернулось на круги своя

L_EXIT:
	LD &1
	; Тело функции закончилось
	
	SWAP
	POP
	SWAP
	POP

	RET
```

Теперь перепишем это на ***stdcall***:

```assembly
FPOW: 
	PUSH ; | ПРОГЛОГ
	PUSH ; | т.к. RET смещён, мы смещаем это (?) тоже
	
	LD #1
	ST &1
	CLA
	ST &0
LO:
	LD &0
	CMP &4
	BGE L_EXIT

	PUSH
	PUSH
	
	LD &5
	ST &1
	LD &3
	ST &0
	CALL MULL

	ST &1
	LD &0
	INC
	ST &0

	JUMP LO ; Всё вернулось на круги своя

L_EXIT:
	LD &1
	; Тело функции закончилось
	
	SWAP |
	POP  |
	SWAP | 
	POP  |
	SWAP  ||
	ST &2 ||| ЭПИЛОГ (Всё остальное тело)
	SWAP  ||
	SWAP |
	POP  |
	SWAP |
	POP  |
```

**2 КУБИК**

`SWAP-ST &?-SWAP` - 

? -- здесь пишем количество слов. Оперируем мы словами а не аргументами.

При соблюдении строгой структуры ***calling convention*** тело функции не меняется

### Проблемы:

* 32 битное число на рубежке. Просто выделяем две ячейки (слова) вместо одного