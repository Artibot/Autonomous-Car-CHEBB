@echo off
@echo git pull > CheckoutRepo_Windows.bat
@echo cd .. >> CheckoutRepo_Windows.bat
@echo IF not exist Dependencies (git clone https://github.com/Artibot/Dependencies.git) >> CheckoutRepo_Windows.bat
@echo cd Dependencies >> CheckoutRepo_Windows.bat
@echo git fetch >> CheckoutRepo_Windows.bat
@echo|set /p=" git checkout " >> CheckoutRepo_Windows.bat
git rev-parse HEAD >> CheckoutRepo_Windows.bat
@echo cd .. >> CheckoutRepo_Windows.bat
@echo cd Autonomous-Car-CHEBB >> CheckoutRepo_Windows.bat


@echo git pull > CheckoutRepo_Linux.sh
@echo cd .. >> CheckoutRepo_Linux.sh
@echo if [ ! -d "$Dependencies" ]; then >> CheckoutRepo_Linux.sh
@echo git clone https://github.com/Artibot/Dependencies.git >> CheckoutRepo_Linux.sh
@echo fi
@echo cd Dependencies >> CheckoutRepo_Linux.sh
@echo git fetch >> CheckoutRepo_Linux.sh
@echo|set /p=" git checkout " >> CheckoutRepo_Linux.sh
git rev-parse HEAD >> CheckoutRepo_Linux.sh
@echo cd .. >> CheckoutRepo_Linux.sh
@echo cd Autonomous-Car-CHEBB >> CheckoutRepo_Linux.sh