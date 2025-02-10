# Portable bell management program

DISCLAIMER: Все действия в настоящей инструкции справедливы для Raspberry OS (на Raspberry Pi 3B+), Zorin OS 17 (на Acer Power 2000), подойдут ли они для других ОС и железа - автор не гарантирует

## Запуск и настройка
Главную папку (sggs) вместе с содержимым (программой) нужно положить в домашнюю директорию пользователя (НЕ root!)

Файл ringer.service нужно закинуть в папку /etc/systemd/system/ (sudo)

Прописать в терминале: 

`sudo systemctl enable ringer`

`sudo systemctl start ringer`

В файле "requirements" хранятся названия необходимых библиотек

Установка:
`pip install requirements.txt`

Если pip не хочет устанавливать библиотеки, можно руками перенести папку нужной библиотеки в /usr/lib/python3/dist-packages

В system-req указаны системные библиотеки для установки

Необходим python 3.11 или выше

Установка python:
`sudo apt install python3` 
(Если через репозитории установится старая версия python, переходим в раздел FAQ)

Расписание звонков по умолчанию берется с сервера. В файле config.py (строка 70) меняете адрес сервера, на котором должен лежать файл с актуальным расписанием. 
При необходимости сменить расписание, редактируете файл именно там.  
Программа может работать и автономно (без интернета), но при редактировании локального файла, он просто перезапишется файлом с сервера, когда подключение будет восстановлено

В файле "quiet" вводятся даты (dd.mm) через пробел, 1 строка - 1 неделя.
Летние каникулы уже добавлены в программу

Если количество уроков изменится (станет отличным от 7), то помимо редактирования расписания, также необходимо в файле ringer.py найти 127 строку, и:

В случае добавления урока: ПОСЛЕ неё добавить строки:
```
schedule.every().day.at(lesson[0]).do(audio)
schedule.every().day.at(tb[0]).do(audio)
schedule.every().day.at(pre[0]).do(audio)
```  
где 0 - (номер урока минус 1) (н-р для 7 урока: 7-1=6)
	
В случае уменьшения количества уроков: удалить строки с номером убранного из расписания урока минус 1

Удалять начиная С КОНЦА!

(н-р, если было 7 уроков, стало 5: удалить строки
```
schedule.every().day.at(lesson[6]).do(audio)
schedule.every().day.at(tb[6]).do(audio)
schedule.every().day.at(pre[6]).do(audio)
```
также и для `lesson[5]`, `tb[5]`, `pre[5]` (так как убираем уроки 7 и 6, 7-1=6, 6-1=5))

После этого перезагрузить устройство

Аудиозаписи для смены звонков скидывать в папку: wav/storage

Названия аудиофайлам даем, как в файле change.py

По мере ненадобности аудиофайлы удаляем

--------------------------------------------------------------------

## FAQ
Install python3.11:

1 вариант - через репозитории:

[python3.11](https://ubuntuhandbook.org/index.php/2022/10/python-3-11-released-how-install-ubuntu/)

[добавление репозиториев](ubunlog.com/ru/как-добавить-репозитории-ppa-в-debian-и-дистрибутивы-на-его-основе)

[add-apt-repository](https://xn----jtbnolen3a.xn--p1ai/%D0%BA%D0%B0%D0%BA-%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%B8%D1%82%D1%8C-ppa-%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B9-%D0%B2-debian)

репозиторий для Raspberry pi 3: [Jammy (22.04)](launchpad.net/~deadsnakes/+archive/ubuntu/ppa)

Спуститься к разделу Add the repository, раскрыть пункт Technical details about this PPA, выбрать подходящую версию Ubuntu (обычно это Jammy 22.04), скопировать репозитории и вставить в конец файла /etc/apt/sources.list

Скопировать Signing key (То, что после слеша) и в терминале выполнить:

`sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys скопированный_код`

`sudo apt update`

2 вариант - с официального сайта:

Скачать архив (tarball) с официального сайта python.org

--------------------------------------------------------------------
### Systemctl
Если journalctl не выдает конкретную причину ошибки, рекомендуется на время поиска проблемы запуска сервиса закомментировать в `/etc/systemd/system/ringer.service` строку `Restart=`

Если systemctl не хочет запускать скрипт, значит:

1) в скрипте есть строка, требующая прав администратора (root)

2) скрипт содержит строку, которая перезапускает systemctl быстрее, чем интервал ожидания по умолчанию (10 сек) (ошибка Failed: start-limit-hit)

3) systemctl перезапускается слишком часто или не может запуститься (ошибка Failed: exit-code)
    
Для 1 пункта: в конце файла /etc/sudoers (sudo visudo /etc/sudoers) прописать:
```
user     ALL=(ALL)       NOPASSWD: /home/user/sggs/ringer.py
user     ALL=(ALL)       NOPASSWD: /bin/systemctl
user     ALL=(ALL)       NOPASSWD: /usr/bin/service
user     ALL=(ALL)       NOPASSWD: /home/user/sggs/radio/radio-off.sh
```

Вместо /home/user подставить путь до папки приложения (sggs) на устройстве

Вместо user подставить имя пользователя, у которого лежит папка с программой

Для 2 пункта: изменить строку в коде, ответственную за перезапуск демона systemctl, чтобы не перезапускалось так быстро

Для 3 пункта: искать ошибку в коде (скрипте) посредством запуска файла в консоли напрямую

Если в консоли запускается, а в systemctl - нет, значит, вы что-то пропустили.
	
--------------------------------------------------------------------
Настройка вывода alsamixer:
https://wiki.gentoo.org/wiki/ALSA/ru

--------------------------------------------------------------------
Ошибка update-alternatives: error: cannot stat file '/usr/bin/python3.6': Too many levels of symbolic links
https://unix.stackexchange.com/questions/511510/python-symbolic-links-mixed-up

Ошибка update-alternatives: error: no alternatives for python3
https://askubuntu.com/questions/1403759/system-cannot-find-alternative-python3-versions-on-ubuntu-20-04

Ошибка ModuleNotFoundError: No module named 'distutils.util'
https://stackoverflow.com/questions/69919970/no-module-named-distutils-but-distutils-installed
```
sudo apt-get install python3.9-distutils
```

Ошибка со звуковыми библиотеками, невозможностью открыть gl, al модули и т.д.

Может помочь: 
`sudo apt-get install linux-generic-lts-wily xserver-xorg-lts-wily libgl1-mesa-glx-lts-wily libglapi-mesa-lts-wily libwayland-egl1-mesa-lts-wily libgl1-mesa-glx-lts-wily:i386 libglapi-mesa-lts-wily:i386`

--------------------------------------------------------------------
### Звуковой сервер
Если в системе стоит звуковой сервер PulseAudio, чтобы звук играл из-под sudo нужно в файле /etc/asound.conf прописать:
```
pcm.pulse {
  type pulse
}

ctl.pulse {
  type pulse
}

pcm.!default {
  type pulse
}
ctl.!default {
  type pulse
}
```

Если звуковой сервер PipeWire, то в том же файле (/etc/asound.conf) заменяем все, что внутри на:
```
ctl.!default {
  type hw
  card PCH
}

pcm.!default {
  type plug
  slave.pcm "dmix:PCH,0"
}
```
Вместо PCH нужно вставить название звуковой карты, как ее определила система (название можно посмотреть в файле /proc/asound/cards).
0 - номер устройства (подустройства) звуковой карты по порядку		(номер можно посмотреть командой aplay -l)
