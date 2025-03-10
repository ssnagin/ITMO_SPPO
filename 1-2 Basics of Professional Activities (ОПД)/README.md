![](img/Data-2521677485.gif)

## Основы Професиональной Деятельности

На курсе студенты знакомятся с так называемой БЭВМ-2 - Базовой Электронно-Вычислительной Машиной. В деталях разбираются принципы работы процессора (АЛУ, Коммутатор, Микрокод), памяти, регистров, прерывания, стек, подпрограммы, синтез комманд и так далее. 

Многие преподователи склонны пугать студентов данным курсом (типа он сложный и всё очень плохо), так как чтобы освоить его, действительно, нужно приложить усилия, однако понимание основных принципов работы БЭВМ даст вам плацдарм для изучения её полностью.

Курс был доработан в 2019-20 годах, соответственно БЭВМ модернизировали и появилась 2 версия.

## Лабораторные работы


| номер | сложность | описание                                                                                                                                                           |
| ----- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1     | 🟨        | Основы команд на linux. Не знаю зачем это сюда впихнули, разве что поработать на гелиосе и сразу не пугать незадачливого студика (т.е. меня) всякими ассемблерами. |
| 2     | 🟥        | Большая. Новая. Сложная. Принималась у меня довольно долго. Если сделать её до допов по опд, то есть шанс, что за семестр вы получите зачет автоматом.             |
| 3     | 🟨        | Стек, работа с SP, массивы, виды адрессации. В целом, поменьше 2-ой.                                                                                               |
| 4     |           | Похожа на третюю, ничего по ней пока сказать не могу                                                                                                               |

## Немного про БЭВМ


Она тупая. БЭВМ это урезанный процессор, который, в силу своей архитектуры, поддерживает лишь однобайтовые команды. По этой причине, например, косвенная абсолютная адресация, недоступна.

### Почему 1 байт это 16 бит

Формулировка звучит некорректно и пародоксально, но в бэвм это так. Давайте взглянем на память в БЭВМ, она расположена справа:

![](img/Pasted%20image%2020250306174123.png)


Мы видим, что через команды мы можем обратиться к ячейке памяти, размер которой как раз 16 бит.

Теперь давайте посмотрим на дебаг какой-нибудь программы у наших привычных (32) 64-битных процессоров через тот же OllyDbg:

![](img/Pasted%20image%2020250306174825.png)

Видите разницу? Во-первых есть четкое разделение по памяти где находятся адреса программы, где стек и так далее, но не об этом сейчас 🙂. Во-вторых в ячейке команд хранятся байты (BYTE), а именно наборы из нескольких байт, к каждому из которых у процессора есть доступ для чтения. Напомню, что в БЭВМ мы можем читать только 16 бит (WORD) целиком.

В целом, команды в современных процессорах x86 многоадресные и состоят из нескольких байт, в отличие от той же архитектуры ARM.

### Сколько времени нужно для освоения БЭВМ?

За месяц интенсивного изучения вы в более-менее поймёте, как она работает. Если лекции Сергея Клименкова на ютубе, его презентации и целых 3 (2!!!) учебных пособия.

Читайте первым делом новую "синюю библию" (2011 год, не старая), так у вас будет большее понимание того, что вообще происходит. Новая методичка поможет только правильно организовать лабораторную работу и в целом понять специфику БЭВМ-2.

## Полезные источники

1. Инфа по курсу [здесь](https://se.ifmo.ru/courses/csbasics)
2. Полезная книжка, читать всем - [тык](https://books.ifmo.ru/file/pdf/761.pdf)
3. Менее полезная, но не менее важная методичка - [тут](Books/Методические указания к выполнению лабораторных работ и рубежного контроля БЭВМ 2019 bcomp-ng)