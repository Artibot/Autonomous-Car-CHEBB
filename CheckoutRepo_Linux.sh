git pull
cd ..
if [ ! -d  ]; then
git clone https://github.com/Artibot/Dependencies.git
fi
cd Dependencies
git fetch
git checkout 7721b8642685315d315c69e3a83a1cdbfe5074c4
cd ..
cd Autonomous-Car-CHEBB
