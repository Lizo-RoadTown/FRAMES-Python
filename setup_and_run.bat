@echo off
echo Installing notion-client...
cd /d "C:\Users\LizO5\FRAMES Python"
call venv\Scripts\activate.bat
pip install notion-client
echo.
echo Running workspace creation...
python scripts\create_notion_workspace.py 2b76b8ea578a8040b328c8527dedea93
echo.
echo Done!
pause
