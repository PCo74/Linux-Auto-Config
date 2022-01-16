@echo off
echo %1

IF [%1]==[] (
    echo parametre manquant
) ELSE ( 
    python .\_vmlinux-vue-html.py %1
)

timeout 5 > NUL