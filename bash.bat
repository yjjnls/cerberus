@echo OFF

REM
REM  THIS SHOULD BE COPIED TO CERBERUS ROOT
REM 
set __WD__=%CD%
set __rootdir__=%~dp0
set __bash__=C:\MinGW\msys\1.0\bin\bash.exe
if not exist %__bash__% (
   echo "Please install MinGW."
   pause
   exit 128
)

pushd %__rootdir__%
PATH=C:\MinGW\msys\1.0\bin;%PATH%
if "x%1" == "x" ( 
    %__bash__%  --init-file tools\windows-bash-init.sh 
) else (
    %__bash__%  tools\windows-bash-init.sh %1 %2 %3 %4 %5 %6 %7 %8
)
popd