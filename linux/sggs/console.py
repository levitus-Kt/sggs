import os
import shutil


while 1:
	print("Вас приветствует программа управления школьными звонками v1.0")
	print(" 1 - Включить звонки")
	print(" 2 - Выключить звонки")
	print(" 3 - Сменить звонки")
	print(" 4 - Поменять расписание звонков (при отсутствии интернета)")
	print(" 5 - Добавить каникулы")
	print(" 6 - Воспроизвести звонок сейчас")
	print(" 7 - Очистить логи")
	print(" 8 - Выйти")
	
	try:
		inp = int(input("Введите номер: "))
		match inp:
			case 1: os.system("sudo systemctl start ringer"); print("Звонки включены!")
			case 2: os.system("sudo systemctl stop ringer"); print("Звонки выключены!")
			case 3: os.system("python ~/sggs/change.py"); os.system("sudo systemctl restart ringer")
			case 4: os.system("nano ~/sggs/bells_time.txt")
			case 5: os.system("nano ~/sggs/quiet.txt")
			case 6: os.system("bash ~/sggs/lesson.sh")
			case 7: 
				if input("Are you sure?") == "y": shutil.rmtree(r"~/sggs/logs"); os.makedirs(r"~/sggs/logs")
			case 8: break
			case _: print("Такой операции нет!")
	except ValueError:
		print("Это не номер!")
	
