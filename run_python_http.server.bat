REM LAC serveur (c)PCo2021
@echo off

REM obtient les paramètres
FOR /F "tokens=1* delims==" %%i in ('type config.ini') do (
 SET %%i=%%~j
)

REM actualise index.html
REM contenant la liste des VMs et le script bash
cd vmslinux
python _index-regenerer.py
cd ..

REM lance le serveur Web
echo *************************************************************
echo serveur WEB local Python pour LAC (Linux Auto Configuration)
echo *************************************************************
echo  1. obtenir le script : "wget %IP%:%PORT%/vmslinux"
echo  2. puis lancer le script  : "bash vmslinux"
echo *************************************************************

python -m http.server --bind 0.0.0.0 %PORT%