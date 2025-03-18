import os
import shutil
import getpass

user = "/home/" + getpass.getuser()


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
			case 3: os.system("python sggs/ringer/appchange.py"); os.system("sudo systemctl restart ringer")
			case 4: os.system("sudo nano sggs/ringer/app/bells_time.txt")
			case 5: os.system("nano sggs/ringer/app/quiet.txt")
			case 6: os.system("sh sggs/ringer/app/lesson.sh")
			case 7: 
				if input("Are you sure?") == "y": shutil.rmtree(f"{user}/sggs/ringer/logs"); os.makedirs(f"{user}/sggs/ringer/logs")
				else: print("Введите y (англ. строчная Y) для согласия")
			case 8: break
			case _: print("Такой операции нет!")
	except ValueError:
		print("Это не номер!")
	
