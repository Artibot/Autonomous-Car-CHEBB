git pull 
cd .. 
if [ ! -d "$Dependencies" ]; then 
git clone https://github.com/Artibot/Dependencies.git 
cd Dependencies 
git fetch 
git checkout 564e3da9bae89fa03b0d4b902f83f846af81c0e0
cd .. 
cd Autonomous-Car-CHEBB 
