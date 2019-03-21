git pull 
cd .. 
IF not exist Dependencies (git clone https://github.com/Artibot/Dependencies.git) 
cd Dependencies 
git fetch 
git checkout 33688260c36ea301aa85227276b1b376ab94d14f
cd .. 
cd Autonomous-Car-CHEBB 
