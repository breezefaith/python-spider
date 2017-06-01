@echo off  
start cmd /k "mongo.bat"
choice /t 2 /d y /n >nul
start cmd /k "python app.py"  