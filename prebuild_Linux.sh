@echo off
@echo git pull > CheckoutRepo_linux.sh
@echo cd .. >> CheckoutRepo_linux.sh
@echo IF not exist Dependencies (git clone https://github.com/Artibot/Dependencies.git) >> CheckoutRepo_linux.sh
@echo cd Dependencies >> CheckoutRepo_linux.sh
@echo git fetch >> CheckoutRepo_linux.sh
@echo|set /p=" git checkout " >> CheckoutRepo_linux.sh
git rev-parse HEAD >> CheckoutRepo_linux.sh
@echo cd .. >> CheckoutRepo_linux.sh
@echo cd Autonomous-Car-CHEBB > CheckoutRepo_linux.sh