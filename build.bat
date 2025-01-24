@echo off
REM Step 1: Copy default.swf into the flash_projector folder, overwriting if it exists
if not exist "flash_projector" mkdir "flash_projector"
copy /Y "default.swf" "flash_projector\default.swf"

REM Step 2: Change directory to the flash_projector folder
cd flash_projector

REM Step 3: Use Node.js to run the build_projector.js script
node build_projector.js
if %errorlevel% neq 0 (
    echo [ERROR] Failed to run build_projector.js
    pause
    exit /b %errorlevel%
)

REM Step 4: Move Flash.exe to the folder just above, overwriting if it exists
move /Y "Flash.exe" "..\Flash.exe"

REM Step 5: Return to the original folder
cd ..

echo [INFO] Process completed successfully.
pause
