REPLY=""
while [[ ! $REPLY =~ ^[YyNn]$ ]]
do
    read -p "Ali naj namestim vse potrebne pakete za pygame? (y/n) " -n 1 -r
    echo
done
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Namescam..."
    sudo apt-get install mercurial python3-dev libsdl-image1.2-dev libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python3-numpy subversion \
    libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev
fi


REPLY=""
while [[ ! $REPLY =~ ^[YyNn]$ ]]
do
    read -p "Ali naj prenesem pygame tukaj v mapo 'pygame'? (y/n) " -n 1 -r
    echo
done
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Prenasam..."
    hg clone https://bitbucket.org/pygame/pygame
fi


REPLY=""
while [[ ! $REPLY =~ ^[YyNn]$ ]]
do
    read -p "Ali naj preverim nastavitve 'pygame'? (y/n) " -n 1 -r
    echo
done
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Prenasam..."
    cd pygame
    python3 config.py
    cd ..
fi


REPLY=""
while [[ ! $REPLY =~ ^[YyNn]$ ]]
do
    read -p "Ali naj zgradim knjiznico pygame? (y/n) " -n 1 -r
    echo
done
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Gradim..."
    cd pygame
    python3 setup.py build
    cd ..
fi


REPLY=""
while [[ ! $REPLY =~ ^[YyNn]$ ]]
do
    read -p "Ali naj namestim knjiznico pygame na sistem? (y/n) " -n 1 -r
    echo
done
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Gradim..."
    cd pygame
    sudo python3 setup.py install
    cd ..
fi


REPLY=""
while [[ ! $REPLY =~ ^[YyNn]$ ]]
do
    read -p "Ali naj zazenem testni program za pygame? (y/n) " -n 1 -r
    echo
done
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Zaganjam..."
    python3 -c "import pygame.examples.aliens; pygame.examples.aliens.main()"
fi

