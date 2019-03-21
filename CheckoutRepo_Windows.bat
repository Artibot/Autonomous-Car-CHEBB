git pull 
cd .. 
IF not exist Dependencies (git clone https://github.com/Artibot/Dependencies.git) 
cd Dependencies 
git fetch 
git checkout 2373d6eaf9d38a76742ea6432f6806e4a9b5fed5
cd .. 
cd Autonomous-Car-CHEBB 
