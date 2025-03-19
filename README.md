# Portable bell management program

DISCLAIMER: Все действия в настоящей инструкции справедливы для Raspberry OS (на Raspberry Pi 3B+), Zorin OS 17 (на Acer Power 2000), семейство Mint OS. Подойдут ли они для других ОС и железа - автор не гарантирует

## Запуск и настройка
Главную папку (sggs, которая внутри linux) вместе с содержимым (программой) нужно положить в домашнюю директорию пользователя (НЕ root!)

В файлах ringer.service и django-server.service в строке WorkingDirectory изменить ctc на имя пользователя, в папке которого лежит программа

Файл ringer.service и django-server.service нужно закинуть в папку /etc/systemd/system/ (sudo)

В настройках сети устройства измените IP на статический: 172.23.56.50. Если хотите установить другой IP, то помимо настроек устройства нужно поменять настройки django. В файле mysite/settings.py в строке ALLOWED_HOSTS измените IP 172.23.56.50 на свой

Прописать в терминале: 

`sudo systemctl enable django-server`

`sudo systemctl start django-server`

`sudo systemctl enable ringer`

`sudo systemctl start ringer`

--------------------------------------------------------------------

### Info

В файле "requirements" хранятся названия необходимых библиотек

Установка:
`pip3 install -r requirements.txt`

Если pip не хочет устанавливать библиотеки, можно руками перенести папку нужной библиотеки в /usr/lib/python3/dist-packages

В файле "system-req" указаны системные библиотеки для установки

Необходим python 3.11 или выше

Установка python:

Системы с deb-пакетами (Ubuntu/Debian/Raspberry): `sudo apt install python3` 

Системы с rpm-пакетами (Fedora/Rosa): `sudo dnf install python3`

(Если через репозитории установится старая версия python, переходим в раздел FAQ)

 

Расписание звонков по умолчанию берётся с сервера. В файле config.py (строка 73) меняете адрес сервера, на котором должен лежать файл с актуальным расписанием. 
При необходимости сменить расписание, редактируете файл именно там (на сервере).  
Программа может работать и автономно (без интернета), но при редактировании локального файла, он просто перезапишется файлом с сервера, когда подключение будет восстановлено

В файле "ringer/app/quiet" хранятся даты (dd.mm) дней, когда звонки не играют.
Летние каникулы уже добавлены в программу

Аудиозаписи для смены звонков хрантся в папке: ringer/wav/storage

Управление программой осуществляется через локальный сервер (устройство с программой и устройство, с которого заходите на сервер, должны быть в одной подсети). Вбиваете в адресную строку браузера IP, который вы делали статическим (по умолчанию 172.23.56.50) с 8000 портом (н-р 172.23.56.50:8000)

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
