@echo off
cd /d "C:\Users\LizO5\FRAMES Python"
call venv\Scripts\activate.bat
python scripts\get_notion_db_ids.py > notion_db_ids.txt 2>&1
type notion_db_ids.txt
