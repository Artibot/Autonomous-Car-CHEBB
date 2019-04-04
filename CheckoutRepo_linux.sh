git pull 
cd .. 
if [ ! -d "$Dependencies" ]; then 
git clone https://github.com/Artibot/Dependencies.git 
cd Dependencies 
git fetch 
git checkout 53a7ed6d1782c22f18d0e3d387a01b909f2d2971
cd .. 
cd Autonomous-Car-CHEBB 
