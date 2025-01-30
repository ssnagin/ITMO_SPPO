#!/bin/sh

echo "TASK 2"

echo "SETTING PRIVLEGES..."

cd ~/lab0/

# DIR lab0
# Setting privledges to internal files/directories:

# bagon4:

chmod 571 bagon4/pidove
chmod a=rwx bagon4/voltorb
chmod 440 bagon4/timburr
chmod 775 bagon4

# ducklett6:

chmod 006 ducklett6

# golem7

chmod u=rw,g=w,o-rwx golem7

# ninjask5

chmod 330 ninjask5/lickitung
chmod u=rx,g=wx,o=rwx ninjask5/huntail
chmod 620 ninjask5/zweilous
chmod u=rw,go=w ninjask5/tangela
chmod 551 ninjask5

# slugma2

chmod 357 slugma2/magby
chmod 046 slugma2/persian
chmod 444 slugma2/ferroseed
chmod 700 slugma2

# togekiss5

chmod uo=,g=rw togekiss5
