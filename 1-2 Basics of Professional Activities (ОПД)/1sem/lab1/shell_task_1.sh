#!/bin/sh

echo "TASK 1"

cd ~

mkdir lab0
cd lab0

# DIR lab0
# Creating internal data

mkdir bagon4
touch ducklett6
touch golem7
mkdir ninjask5
mkdir slugma2
touch togekiss5

# bagon4

mkdir bagon4/pidove
mkdir bagon4/voltorb
touch bagon4/timburr

# ninjask5

mkdir ninjask5/lickitung
mkdir ninjask5/huntail
touch ninjask5/zweilous
touch ninjask5/tangela

# slugma2

mkdir slugma2/magby
touch slugma2/persian
touch slugma2/ferroseed

echo "WRITING CONTENTS TO FILES..."

# timburr
cat > bagon4/timburr <<'EOF'
Возможности  Overland=6 Surface=4 Jump=4 Power=4
Intelligence=2
EOF

# ducklett6
cat > ducklett6 <<'EOF'
Способности  Water Gun Water Sport Defog
Wing Attack Water Pulse Aerial Ace Bubblebeam Featherdance Aqua Ring
Air Slash Roost Rain Dance Tailwind Brave Bird Hurricane
EOF

# golem7
cat > golem7 <<'EOF'
Тип
покемона  ROCK GROUND
EOF

# zweilous
cat > ninjask5/zweilous <<'EOF'
Способности  Focus Energy Bite
Headbutt Dragonbreath Roar Crunch Slam Dragon Pulse Work Up Dragon
Rush Body Slam Scary Face Hyper Voice Outrage
EOF

# tangela
cat > ninjask5/tangela <<'EOF'
Ходы
Ancientpower Bind Body Slam Bullet Seed Double-Edge Endeavor Giga
Drain Knock Off Pain Split Seed Bomb Shock Wave Sleep Talk Snore
Synthesis Worry Seed
EOF

# persian
cat > slugma2/persian <<'EOF'
Ходы  Body Slam Covet Dark Pulse Defense
Curl Double-Edge Fake Out Foul Play Gunk Shot Hyper Voice Icy Wind
Iron Tail Knock Off Last Resort Mud-Slap Pay Day Seed Bomb Shock Wave
Sleep Talk Snatch Snore Spite Swift Switcheroo  Uproar Water
Pulse
EOF

#ferroseed
cat > slugma2/ferroseed <<'EOF'
Живёт  Cave Mountain
EOF

#togekiss5
cat > togekiss5 <<'EOF'
Возможности
Overland=5 Surface=6 Sky=14 Jump=5 Power3=0 Intelligence=4 Aura=0
Guster=0
EOF


