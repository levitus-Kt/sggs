#!/usr/bin/python3
import schedule
import time
import datetime
import sys
import os
import change
import config
import logging


logger = logging.getLogger(__name__)    #Используем имя модуля, чтобы знать откуда вывелся лог
logger.setLevel(logging.INFO)    #минимальный уровень, на котором нужно начинать логирование (по умолчанию Warning)

logging.basicConfig(level=logging.INFO, filename=f"~/sggs/logs/{__name__}.log", filemode="a",format="%(asctime)s %(levelname)s %(message)s \n")

#Настройка обработчика и форматировщика в соответствии с нашими нуждами
handler = logging.FileHandler(filename=f"~/sggs/logs/{__name__}.log", mode='a') 
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")


#Добавление форматировщика к обработчику
handler.setFormatter(formatter)
#Добавление обработчика к логгеру
logger.addHandler(handler)




lesson, tb, pre = config.raspisanie()

#Автоматическая смена звонков на Новый Год и отсчёт дней до праздника
def ny():
    try:
        change.new_year()
        result = str(time.localtime()).split(", ")
        year = result[0].split("=")
        day = result[7].split("=")
        if int(year[1]) % 4 == 0:
            ydays = lambda y: y - int(day[1])
            if ydays(366) <= 31:
                print(f"До нового года осталось {ydays(366)} дней")
            else:
                pass
        else:
            ydays = 365 - int(day[1])
            if ydays <= 31:
                print(f"До нового года осталось {ydays} дней")
            else:
                pass
        
        logging.info(f"Function new year {__name__}")
    except Exception:
        logging.error("Ошибка в функции ringer.ny", exc_info=True)


#Функция выбора аудиофайла в зависимости от текущего времени
def audio():
    
    config.kanikuly()

    true_time = str(datetime.datetime.now()).split()[1].split('.')  #Текущее время

    print("\n", time.ctime())
    print(datetime.datetime.now())
    
    
    date = datetime.datetime.now().strftime("%d.%m")    #Текущая дата
    
    #Если дата совпадает с датой в списке тишины, выполнение прерывается
    if date in config.quiet:
        print("Отдыхаем")
        logging.info(f"Отдыхаем (ringer)")
        return
        
    logging.info(f"Function kanikuly {__name__}")
    
    weekday = config.wd()       #Текущий день недели
    
    #Выбор аудио
    match weekday:
        case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":                #Не играть по выходным
            if true_time[0] in lesson: os.system("sh ~/sggs/lesson.sh")
            elif true_time[0] in tb: os.system("sh ~/sggs/timebreak.sh"); time.sleep(5.5); os.system("sh ~/sggs/radio/radio-on.sh")
            elif true_time[0] in pre: os.system("sh ~/sggs/radio/radio-off.sh"); time.sleep(5.5); os.system("sh ~/sggs/pre.sh")
        case _:
            print("Выходные!")
            pass
    
    logging.info(f"Function ringer.audio")


def sets():
	if datetime.datetime.now().strftime("%d.%m") == "31.12": config.clearLogs   #Очистка логов
	logging.info(f"-----------------")
	logging.info(f"Today is: {time.ctime()}")
	change.prazdniki()                                              #Смена звонков на праздники
	day = str(time.localtime()).split(", ")[7].split("=")           #Автоматическая смена на Новый Год
	if (int(366 - int(day[1]))) <= 21:
	    ny()
    logging.info(f"Function ringer.sets")



def sch():   
    logging.info(f"Function raspisanie {__name__}")
    
    def stop():
        os.system("bash ~/sggs/radio/radio-off.sh")
    
    
    schedule.every().day.at("15:30:00").do(stop)
    
    schedule.every().day.at(lesson[0]).do(audio)
    schedule.every().day.at(tb[0]).do(audio)
    schedule.every().day.at(lesson[1]).do(audio)
    schedule.every().day.at(tb[1]).do(audio)
    schedule.every().day.at(lesson[2]).do(audio)
    schedule.every().day.at(tb[2]).do(audio)
    schedule.every().day.at(lesson[3]).do(audio)
    schedule.every().day.at(tb[3]).do(audio)
    schedule.every().day.at(lesson[4]).do(audio)
    schedule.every().day.at(tb[4]).do(audio)
    schedule.every().day.at(lesson[5]).do(audio)
    schedule.every().day.at(tb[5]).do(audio)
    schedule.every().day.at(lesson[6]).do(audio)
    schedule.every().day.at(tb[6]).do(audio)
    
    schedule.every().day.at(pre[0]).do(audio)
    schedule.every().day.at(pre[1]).do(audio)
    schedule.every().day.at(pre[2]).do(audio)
    schedule.every().day.at(pre[3]).do(audio)
    schedule.every().day.at(pre[4]).do(audio)
    schedule.every().day.at(pre[5]).do(audio)
    schedule.every().day.at(pre[6]).do(audio)
    
    schedule.every().day.at("08:00").do(sets)		#Обновление мелодии и логов
    schedule.every(2).hours.do(config.update)		#Обновление расписания
    
    schedule.every(52).weeks.do(config.clearLogs)	#Очистка логов каждый год со дня запуска программы


    #Запуск schedule
    while 1:
        schedule.run_pending()
        time.sleep(1.01)



if __name__ == "__main__":
    sch()

