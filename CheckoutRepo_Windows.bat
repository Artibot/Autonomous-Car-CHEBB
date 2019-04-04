git pull 
cd .. 
IF not exist Dependencies (git clone https://github.com/Artibot/Dependencies.git) 
cd Dependencies 
git fetch 
git checkout 4abc6d807d59150fff2446dfc4da8535683f8c37
cd .. 
cd Autonomous-Car-CHEBB 
