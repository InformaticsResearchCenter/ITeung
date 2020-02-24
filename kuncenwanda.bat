@echo off
for /f %%i in ('tasklist /fi "imagename eq player.exe"') do set VAR=%%i
echo STATUS : %VAR%
echo Keterangan STATUS : jika berisi player.exe berarti masih jalan jika berisi INFO: berarti mati
IF %VAR%==INFO: taskkill /F /IM VBoxHeadless.exe && player --vm-name wanda
PING 8.8.8.8 -n 60 >NUL
cls
kuncenwanda.bat