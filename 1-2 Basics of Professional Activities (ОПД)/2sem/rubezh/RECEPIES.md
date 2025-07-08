Подпрограмма сложения 32-разрядных чисел
```

rl	6
rh	5
yl	4
yh	3
xl	2
xh	1
ret	0

sum32:
.pro:
.bdy:	LD &2
	ADD &4
	ST &6
	LD &1
	ADC &3
	ST &5
.epi:	SWAP
	ST &4
	SWAP
	SWAP
	POP
	SWAP
	POP
	SWAP
	POP
	SWAP
	POP
	RET

```

Подпрограмма инверсии знака 32-разрядного числа

```
    rl	4	8-6	10-6
rh	3	7-5	9-5
xl	2	6-4	8-4
xh	1	5-3	7-3
ret	0	4-2	6-2
---------------
rl*		3-1
rh*		2-0
xl*		1-X
xh*		0-X
---------------------
rl**			5-1			
rh**			4-0
yl**			3-X
yh**			2-X
xl**			1-X
xh**			0-X

neg32:
.pro:
.bdy:	
.not:	PUSH
	PUSH
	PUSH
	PUSH
	LD &6
	ST &1
	LD &5
	ST &0
	CALL neg32
	LD &1
	ST &6
	LD &0
	ST &5
	SWAP
	POP
	SWAP
	POP
.add:	PUSH
	PUSH
	PUSH
	PUSH
	PUSH
	PUSH
	LD &10
	ST &1
	LD &9
	ST &0
	CALL add32
	LD &1
	ST &6
	LD &0
	ST &5
	SWAP
	POP
	SWAP
	POP
.epi:	SWAP
	ST &2
	SWAP
	SWAP
	POP
	SWAP
	POP
	RET
```

Подпрограмма вычитания 32-разрядных чисел
```
rl	6	10-8	12-8
rh	5	9-7	11-7
yl	4	8-6	10-6
yh	3	7-5	9-5
xl	2	6-4	8-4
xh	1	5-3	7-3
ret	0	4-2	6-2
---------------
rl*		3-1
rh*		2-0
xl*		1-X
xh*		0-X
----------------------
rl**			5-1
rh**			4-0
yl**			3-X
yh**			2-X
xl**			1-X
xh**			0-X

sub32:
.pro:
.bdy:	
.neg:	PUSH
	PUSH
	PUSH
	PUSH
	LD &7
	ST &0
	LD &8
	ST &1
	CALL neg32
	LD &1
	ST &8
	LD &0
	ST &7
	SWAP
	POP
	SWAP
	POP
.add:	PUSH
	PUSH
	PUSH
	PUSH
	PUSH
	PUSH
	LD &12
	ST &3
	LD &11
	ST &2
	LD &8
	ST &1
	LD &7
	ST &0
	CALL add32
	LD &1
	ST &8
	LD &0
	ST &7
	SWAP
	POP
	SWAP
	POP
.epi:	SWAP
	ST &4
	SWAP
	SWAP
	POP
	SWAP
	POP
	SWAP
	POP
	SWAP
	POP
	RET
```

Подпрограмма расширения знака 16-разрядных чисел

```
rl	3
rh	2
x	1
ret	0

sxt16:
.pro:
.bdy:	LD &1
	ST &3
	BGE .els
.thn:   LD #0xFF
	ST &2
	JUMP .epi
.els:	CLA
	ST &2
.epi:	SWAP
	ST &1
	SWAP
	SWAP
	POP
	RET
```