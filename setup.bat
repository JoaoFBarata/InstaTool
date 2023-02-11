@echo off

echo A instalar... Pode demorar alguns momentos... Nao clique em nenhum lugar desta janela.

"%~dp0python-3.10.2-amd64.exe" /quiet InstallAllUsers=1 Prepend-Path=1 AssociateFiles=1

"%~dp0VC_redist.x64.exe"

FOR /F "tokens=* USEBACKQ" %%F IN (`%windir%\py.exe -3.10 -c "import sys; print(sys.executable[:-10])"`) DO (
SET pythonPath=%%F
)

"%pythonPath%python.exe" "%~dp0get-pip.py"
"%pythonPath%python.exe" -m pip install -r requirements.txt
set PLAYWRIGHT_BROWSERS_PATH=%pythonPath%Lib\site-packages\playwright\driver\package\.local-browsers\
"%pythonPath%python.exe" -m playwright install chromium

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\InstaTool.lnk" >> %SCRIPT%
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