echo off
where /q hugo
IF ERRORLEVEL 1 (
    ECHO hugo.exe not found. Ensure it is installed and placed in your PATH.
    EXIT /B
)
echo on
hugo
git add --all
git commit -m "buildme"
git push
git subtree push --prefix public origin gh-pages