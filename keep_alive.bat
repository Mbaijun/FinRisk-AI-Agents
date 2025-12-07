@echo off
:start
echo Connecting to serveo.net...
ssh -R 80:localhost:7860 serveo.net
echo Connection lost, reconnecting in 5 seconds...
timeout /t 5
goto start