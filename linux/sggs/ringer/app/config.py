import datetime
import time
import wave
import os
import shutil
import sys
import wget
import logging
import getpass


user = "/home/" + getpass.getuser()

logger2 = logging.getLogger(__name__)    #Используем имя модуля, чтобы знать откуда вывелся лог
logger2.setLevel(logging.INFO)    #минимальный уровень, на котором нужно начинать логирование (по умолчанию Warning)

#Настройка обработчика и форматировщика в соответствии с нашими нуждами
handler2 = logging.FileHandler(filename=f"sggs/ringer/logs/{__name__}.log", mode='a')
formatter2 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

#Добавление форматировщика к обработчику
handler2.setFormatter(formatter2)
#Добавление обработчика к логгеру
logger2.addHandler(handler2)

lines = []
def wd():
	weekday = datetime.datetime.now().strftime('%A')
	return weekday

def schedule_time(lines):
	pre = [lines[i -1] for i in range(1, len(lines) + 1) if (i + 3) % 4 == 0]
	lesson = [lines[i -1] for i in range(1, len(lines) + 1) if (i + 2) % 4 == 0]
	tb = [lines[i -1] for i in range(1, len(lines) + 1) if (i + 1) % 4 == 0]
	return lesson, tb, pre

def raspisanie():
	global lines
	inputFile = open(r"sggs/ringer/app/bells_time.txt", "r")  #w - перезаписать, a -  добавить, r - прочитать (default), x - создать эксклюзивный файл
	lines = inputFile.read().splitlines()
	inputFile.close()
	lesson, tb, pre = schedule_time(lines)
	return lesson, tb, pre
	
def kanikuly():
	global quiet
	quiet = []
	
	inputFile = open(r"sggs/ringer/app/quiet.txt", "r")
	weeks = inputFile.read().splitlines()
	inputFile.close()

	for i in range(len(weeks)):
		quiet += weeks[i].split(' ')

	for i in range(1, 30):	#июнь
		i += 1
		quiet.append(str(i) + ".06")    #преобразовать в строку и сложить со второй
	for i in range(1, 31):	#июль
		i += 1
		quiet.append(str(i + .07))      #сложить с десятичным числом и преобразовать в строку
	for i in range(1, 31):	#август
		i += 1
		quiet.append("{:d}.08".format(i))   #:d - форматировать как десятичное число

	return quiet
	
def clearLogs():
	shutil.rmtree(f"{user}/sggs/ringer/logs")
	os.mkdir(f"{user}/sggs/ringer/logs")
	
def update():
	url = "http://shkarenkov.ru/1212/bells_time.txt"
	try:
		os.system("mv sggs/ringer/app/bells_time.txt sggs/ringer/app/bells_time1.txt")
		wget.download(url, out=f"{user}sggs/ringer/app/")
		time.sleep(2)
		os.system("sudo systemctl restart ringer")
	except:
		os.system("mv sggs/ringer/app/bells_time1.txt sggs/ringer/app/bells_time.txt")
		logging.error(f"Function config.update")
		logging.error(f"Не получилось скачать расписание с сервера. Использую локальный файл")
	finally:
		if os.path.exists(f"sggs/ringer/app/bells_time1.txt"): os.remove(f"sggs/ringer/app/bells_time1.txt")
	#вернет True и для файла и для директории. os.path.isfile проверит именно на наличие файла

