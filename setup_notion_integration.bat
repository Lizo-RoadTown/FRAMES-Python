@echo off
REM Quick setup script for GitHub-Notion integration
echo.
echo ================================================================
echo   FRAMES GitHub-Notion Integration Setup
echo ================================================================
echo.
echo This will guide you through setting up automated sync between
echo GitHub and Notion for the FRAMES project.
echo.
echo Prerequisites:
echo   - Python 3.11+ installed
echo   - Notion API key configured in .env
echo   - Notion integration created and shared with a page
echo.
pause

cd /d "%~dp0"

echo.
echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install notion-client python-dotenv requests --quiet
if errorlevel 1 (
    echo WARNING: Some packages may have failed to install
)

echo.
echo Starting interactive setup wizard...
echo.
python scripts\setup_github_notion.py

echo.
echo ================================================================
echo   Setup script finished
echo ================================================================
echo.
pause
