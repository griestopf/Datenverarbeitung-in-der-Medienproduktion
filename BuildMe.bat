echo off
where /q hugo
IF ERRORLEVEL 1 (
    ECHO hugo.exe not found. Ensure it is installed and placed in your PATH.
    EXIT /B
)
echo on
rd public /s/q
hugo --destination public/script --baseURL https://sftp.hs-furtwangen.de/~lochmann/computergrafik2019/script/
xcopy /i /s /y _site\*.* public

