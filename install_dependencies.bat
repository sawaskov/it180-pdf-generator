@echo off
echo Installing required packages for IT180 PDF Generator Web App...
echo.
python -m pip install Flask pandas pypdf reportlab openpyxl Werkzeug
echo.
echo Installation complete!
echo.
echo To start the server, run: python app.py
echo Or use: install_and_run.bat
pause
