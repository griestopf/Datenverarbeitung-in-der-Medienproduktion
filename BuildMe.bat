echo off
where /q hugo
IF ERRORLEVEL 1 (
    ECHO hugo.exe not found. Ensure it is installed and placed in your PATH.
    EXIT /B
)
echo on
hugo
git subtree push --prefix public origin gh-pages