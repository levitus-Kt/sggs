amixer -q set Master 0%

echo "Enabling the radio"

#run in background: >/dev/null 2>&1 &
mpg123 http://ic7.101.ru:8000/v1_1 &	#NRJ (mp3)

echo "Volume is increasing now"
sleep 6

amixer -q set Master 10%
sleep 0.4
amixer -q set Master 20%
sleep 0.4
amixer -q set Master 30%
sleep 0.4
amixer -q set Master 40%
sleep 0.4
amixer -q set Master 50%
sleep 0.4
amixer -q set Master 60%
sleep 0.4
amixer -q set Master 70%
sleep 0.4
amixer -q set Master 80%
sleep 0.4
amixer -q set Master 90%
sleep 0.4
amixer set Master 100%
echo "Radio is playing"
