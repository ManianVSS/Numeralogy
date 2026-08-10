@echo off
setlocal
cd /d "%~dp0"

echo Building Windows executable...
set CGO_ENABLED=0
set GOOS=windows
set GOARCH=amd64
go build -o numerology_windows.exe
IF ERRORLEVEL 1 (
    echo Build failed.
    EXIT /B 1
)

echo Build complete: %~dp0numerology_windows.exe
endlocal
