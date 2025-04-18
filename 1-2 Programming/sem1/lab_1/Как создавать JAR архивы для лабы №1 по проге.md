> Специально для студентов ИТМО : )

(частично взято [отсюда](https://coderbook.ru/%D0%B0%D1%80%D1%85%D0%B8%D0%B2%D0%B0%D1%82%D0%BE%D1%80-jar/))

### Компилируем java в машинный код

Это делается командой `javac`:

```bash
javac Main.java
```

### Создание архива

Чтобы создать исполняемый jar архив, нужно прописать следующую команду:

```
jar {ctxu}[vfm0M] [jar-file] [manifest-file] [-C dir] files…_
```

```
jar -cvmf [jar-file] Main files…_
```

Где в `{}` действия с jar архивом:

```
c (create) -- создать новый архив
t (table of contents) -- вывести в стандартный вывод список содержимого архива
х (extract) — извлечь из архива один или несколько файлов
u (update) — обновить архив, заменив или добавив один или несколько файлов
```

Далее в `[]` обозначения аргументов:

```
v (verbose) — выводить сообщения о процессе работы с архивом в стандартный вывод
f (file) — записанный далее параметр jar-file показывает имя архивного файла
m (manifest) — записанный далее параметр manifest-file показывает имя файла описания
0 (нуль) — не сжимать файлы, записывая их в архив
M (manifest) — не создавать файл описания
```

В `jar-file` записывается имя архивного файла (можно с указанием пути, т.е. в моем случае если надо поместить файл в папку `builds`, то прописываем `builds/jar-filename.jar`)

За более подробной информацией пишите в консоль `man jar`!

### Индексация файлов архива

После создания `.jar` архива, можно его "оптимизировать" путем индексации всех существующих там файлов. Это делется путем команды:

```bash
jar -i Build.jar
```

После этого создается файл `INDEX.LIST`
### Примеры команд

```bash
jar cfv build/Build.jar Lab1.class
```

--> Создание `jar` архива Build.jar с классом `Lab1.class` в папке `build`.

Попробуем прочитать созданный нами архив:

```bash
cd build
java -jar Build.jar
```

--> И что мы видим????

![Image 1](https://github.com/ssnagin/ITMO_SPPO/blob/main/Programming/sem1/lab_1/assets/Pasted%20image%2020240928171418.png?raw=true)

Правильно, у нас нет входной точки в файле-манифесте, с которого бы стартовала программа

![Image 2](https://github.com/ssnagin/ITMO_SPPO/blob/main/Programming/sem1/lab_1/assets/dem_66f810313c83a.png?raw=true)



Мы, конечно, можем прописать всякие костыли (я не гарантирую их работоспособность):

```bash
cd ..
java -cp build/Build.jar Main.class
```

Или так:

```bash
jar cfe build/Build.jar Main Main.class
```

Но каждый раз вводить это такое себе. Поэтому мы будем прописывать главный файл в манифесе.

Открывем в созданом архиве MANIFEST.MF и прописываем входной файл:

![Image 3](https://github.com/ssnagin/ITMO_SPPO/blob/main/Programming/sem1/lab_1/assets/Pasted%20image%2020240928192911.png?raw=true)

![Image 4](https://github.com/ssnagin/ITMO_SPPO/blob/main/Programming/sem1/lab_1/assets/Pasted%20image%2020240928192929.png?raw=true)

Здесь нам нужно прописать атрибут:

```
Main-Class: Main
```

![Image 5](https://github.com/ssnagin/ITMO_SPPO/blob/main/Programming/sem1/lab_1/assets/Pasted%20image%2020240928194629.png?raw=true)

Закрываем этот архив и вуаля! Программа создана. Осталось только показать все эти этапы преподу и залить исходники на Gelios, поэтому лучше попрактиковаться в этом деле.

Запускать архив так:

```bash
java -jar Build.jar
```
### FAQ

> **В чем разница между .jar, .jav и .class?**

**Java** файлы это исходники, т.е. код, который потом будет преобразован в **.class** (байт-код, которые понимает JRE). Все сурсы хранятся в **.java** файлах.

**Jav** -- не очень распространенный формат, он нам нафиг сейчас не нужон. Забейте на него и используйте **.java**.
