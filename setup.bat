@echo off

"%~dp0python-3.9.6-amd64.exe" /quiet InstallAllUsers=1 Prepend-Path=1

python "%~dp0get-pip.py"
python -m pip install -r requirements.txt
playwright install chromium

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\InstaTool_.lnk" >> %SCRIPT%
echo sLinkFile1 = "%AppData%\Microsoft\Windows\Start Menu\Programs\InstaTool.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo Set oLink1 = oWS.CreateShortcut(sLinkFile1) >> %SCRIPT%
echo oLink.TargetPath = "%~dp0launch.vbs" >> %SCRIPT%
echo oLink.IconLocation = "%~dp0instagram.ico" >> %SCRIPT%
echo oLink1.TargetPath = "%~dp0launch.vbs" >> %SCRIPT%
echo oLink1.IconLocation = "%~dp0instagram.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
echo oLink1.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%

cscript /nologo "%~dp0launch.vbs"