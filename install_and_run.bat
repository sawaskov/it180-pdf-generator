@echo off
echo Installing required packages...
python -m pip install Flask pandas pypdf reportlab openpyxl Werkzeug
echo.
echo Starting web server...
echo Open your browser and go to: http://localhost:5000
echo.
python app.py
pause
