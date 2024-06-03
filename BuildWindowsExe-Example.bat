REM delete previous build
del "Drive:\File\To\Folder\xmas mayhem\build" /S /Q

REM Run new exe build
python setup.py build > buildWindowsLog.txt

@echo off
PAUSE
