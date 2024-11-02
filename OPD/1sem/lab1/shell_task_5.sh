#!/bin/sh

# Удалить файл golem7
rm ~/lab0/golem7

# Удалить файл lab0/slugma2/persian
rm -f ~/lab0/slugma2/persian

# удалить символические ссылки lab0/slugma2/persiantogeki*
rm ~/lab0/slugma2/persiantogeki*

# удалить жесткие ссылки lab0/bagon4/timburrtogeki*
rm -f ~/lab0/bagon4/timburrtogeki*

# Удалить директорию ninjask5
chmod -R u+rwx ~/lab0/ninjask5/
rm -rf ~/lab0/ninjask5/

# Удалить директорию lab0/ninjask5/lickitung
# Она уже была удалена, но всё же:
chmod -R u+rwx ~/lab0/ninjask5/lickitung
rm -rf ~/lab0/ninjask5/lickitung/
