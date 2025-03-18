echo "Volume is decreasing now"
amixer -q set Master 90%
sleep 0.4
amixer -q set Master 80%
sleep 0.4
amixer -q set Master 70%
sleep 0.4
amixer -q set Master 60%
sleep 0.4
amixer -q set Master 50%
sleep 0.4
amixer -q set Master 40%
sleep 0.4
amixer -q set Master 30%
sleep 0.4
amixer -q set Master 20%
sleep 0.4
amixer -q set Master 10%
sleep 0.4
amixer set Master 0%


killall mpg123
killall mpg123	#it doesn't always turn off the first time  #не всегда выключается с первого раза
sleep 2
echo "Radio stopped"
amixer -q set Master 100%
