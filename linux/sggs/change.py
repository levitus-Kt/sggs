import datetime
import time
import sys
import os
import shutil
import logging
import getpass

user = "/home/" + getpass.getuser()


logger3 = logging.getLogger(__name__)    #Используем имя модуля, чтобы знать откуда вывелся лог
logger3.setLevel(logging.INFO)    #минимальный уровень, на котором нужно начинать логирование (по умолчанию Warning)

#Настройка обработчика и форматировщика в соответствии с нашими нуждами
handler3 = logging.FileHandler(filename=f"sggs/logs/{__name__}.log", mode='a')
formatter3 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

#Добавление форматировщика к обработчику
handler3.setFormatter(formatter3)
#Добавление обработчика к логгеру
logger3.addHandler(handler3)



def bells():
    try:
        print("1 - Классические")
        print("2 - Новогодние")
        print("3 - Специальные")
        user = input('Введите номер типа звонка: ')
        if user == '1':
            shutil.copy(f'{user}/sggs/wav/storage/default/bell-classic-in.wav', f'{user}/sggs/wav/bells/bell-in.wav')
            shutil.copy(f'{user}/sggs/wav/storage/default/bell-classic-out.wav', f'{user}/sggs/wav/bells/bell-out.wav')
            shutil.copy(f'{user}/sggs/wav/storage/default/bell-classic-pre.wav', f'{user}/sggs/wav/bells/bell-pre.wav')
        elif user == '2':
            #shutil.copy(f'{user}/sggs/wav/storage/default/bell-ny-in.wav', f'{user}/sggs/wav/bells/bell-in.wav')
            #shutil.copy(f'{user}/sggs/wav/storage/default/bell-ny-out.wav', f'{user}/sggs/wav/bells/bell-out.wav')
            #shutil.copy(f'{user}/sggs/wav/storage/default/bell-ny-pre.wav', f'{user}/sggs/wav/bells/bell-pre.wav')
            new_year()
        else:
            #Gui с выбором файлов
            print("В разработке")
        
        logging.info(f"Function bells __change__")
    except Exception:
        logging.error("Ошибка в функции bells (смена звонков) change.bells", exc_info=True)

def new_year():
    try:
        shutil.copy(f'{user}/sggs/wav/storage/default/bell-ny-in.wav', f'{user}/sggs/wav/bells/bell-in.wav')
        shutil.copy(f'{user}/sggs/wav/storage/default/bell-ny-out.wav', f'{user}/sggs/wav/bells/bell-out.wav')
        shutil.copy(f'{user}/sggs/wav/storage/default/bell-ny-pre.wav', f'{user}/sggs/wav/bells/bell-pre.wav')
        
        logging.info(f"Function new_year {__name__}")
    except Exception:
        logging.error("Ошибка в функции change.new_year", exc_info=True)


def feast(load):
    d, m = load.split(".")
    year = int(datetime.datetime.now().strftime("%Y"))
    isowd = datetime.datetime(year, int(m), int(d)).isoweekday()	#Вывод дня недели: 1 - пон, 7 - вос
    return isowd

def prazdniki():
    try:
        weekday = datetime.datetime.now().strftime('%A')
        today = datetime.datetime.now().strftime("%d.%m")
        match today:
            case "20.02" | "21.02" | "22.02":
                if feast("23.2") == (1 or 6 or 7) and weekday == "Friday" or today == "22.02":        
                    shutil.copy(f'{user}/sggs/wav/storage/23.02-in.wav', f'{user}/sggs/wav/bells/bell-in.wav')
                    shutil.copy(f'{user}/sggs/wav/storage/23.02-out.wav', f'{user}/sggs/wav/bells/bell-out.wav')
                    shutil.copy(f'{user}/sggs/wav/storage/23.02-pre.wav', f'{user}/sggs/wav/bells/bell-pre.wav')
            case "05.03" | "06.03" | "07.03":
                if feast("8.3") == (1 or 6 or 7) and weekday == "Friday" or today == "07.03":
                    shutil.copy(f'{user}/sggs/wav/storage/8.03-in.wav', f'{user}/sggs/ggs/bells/bell-in.wav')
                    shutil.copy(f'{user}/sggs/wav/storage/8.03-out.wav', f'{user}/sggs/wav/bells/bell-out.wav')
                    shutil.copy(f'{user}/sggs/wav/storage/8.03-pre.wav', f'{user}/sggs/wav/bells/bell-pre.wav')
            case "28.04" | "29.04" | "30.04":
                if feast("1.5") == (1 or 6 or 7) and weekday == "Friday" or today == "30.04":
                    shutil.copy(f'{user}/sggs/wav/storage/1.05-in.wav', f'{user}/sggs/wav/bells/bell-in.wav')
                    shutil.copy(f'{user}/sggs/wav/storage/1.05-out.wav', f'{user}/sggs/wav/bells/bell-out.wav')
                    shutil.copy(f'{user}/sggs/wav/storage/1.05-pre.wav', f'{user}/sggs/wav/bells/bell-pre.wav') 
            case "06.05" | "07.05" | "08.05":
                if feast("9.5") == (1 or 6 or 7) and weekday == "Friday" or today == "08.05":
                    shutil.copy(f'{user}/sggs/wav/storage/9.05-in.wav', f'{user}/sggs/wav/bells/bell-in.wav')
                    shutil.copy(f'{user}/sggs/wav/storage/9.05-out.wav', f'{user}/sggs/wav/bells/bell-out.wav')
                    shutil.copy(f'{user}/sggs/wav/storage/9.05-pre.wav', f'{user}/sggs/wav/bells/bell-pre.wav')
            case "01.11" | "02.11" | "03.11":
                if feast("4.11") == (1 or 6 or 7) and weekday == "Friday" or today == "03.11":
                    shutil.copy(f'{user}/sggs/wav/storage/gymn-in.wav', f'{user}/sggs/wav/bells/bell-in.wav')
                    shutil.copy(f'{user}/sggs/wav/storage/gymn-out.wav', f'{user}/sggs/wav/bells/bell-out.wav')
                    shutil.copy(f'{user}/sggs/wav/storage/gymn-pre.wav', f'{user}/sggs/wav/bells/bell-pre.wav')
            case _:
                if today < "20.01": new_year()
                else:
                    shutil.copy(f'{user}/sggs/wav/storage/default/bell-classic-in.wav', f'{user}/sggs/wav/bells/bell-in.wav')
                    shutil.copy(f'{user}/sggs/wav/storage/default/bell-classic-out.wav', f'{user}/sggs/wav/bells/bell-out.wav')
                    shutil.copy(f'{user}/sggs/wav/storage/default/bell-classic-pre.wav', f'{user}/sggs/wav/bells/bell-pre.wav')
                
        logging.info(f"Function prazdniki {__name__}")
    except Exception:
        logging.error("Ошибка в функции change.prazdniki", exc_info=True)   
    

if __name__ == '__main__':
    bells()
    now = str(datetime.datetime.now()).split()
    now1 = time.ctime()
    result = str(time.localtime()).split(", ")
    print(f"\n{now[0]}\n{now1}\n")
    print(result[7].split("="))
