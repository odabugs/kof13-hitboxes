@echo off
set PYTHON_DIR=%CD%\python
set SECOND_BATCH=start_real.bat
"%PYTHON_DIR%\%SECOND_BATCH%" %* < Nul
