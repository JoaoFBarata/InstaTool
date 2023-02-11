FOR /F "tokens=* USEBACKQ" %%F IN (`%windir%\py.exe -3.10 -c "import sys; print(sys.executable[:-10])"`) DO (
SET pythonPath=%%F
)
cd "%~dp0"
"%pythonPath%python.exe" "%~dp0InstaTool.py"