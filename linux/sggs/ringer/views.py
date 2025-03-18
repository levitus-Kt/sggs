from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.db.models import F
from django.urls import reverse, reverse_lazy, resolve
from django.views import View, generic
from django.views.generic.edit import UpdateView, FormView
from django.contrib import messages

from .forms import HolidaysForm, QuantityForm, UploadFileForm
from .models import LessonQuantity, Holidays

import time
import re
import os
import shutil
import getpass
from ringer.app import fileRevealer as fr

user = "/home/" + getpass.getuser()

def IndexView(request):
    """Домашняя страница"""
    template_name = "ringer/index.html"
    return render(
        request,
        "ringer/index.html")


def shell(request):
    return render(
        request,
        "ringer/shell.html")

class EnableRing(UpdateView):
    #Если метод post, обрабатываем данные
    def post(self, request, *args, **kwargs):
        if 'yes-but' in request.POST:
            if os.system("sudo systemctl start ringer") == 0:
                msg = "Звонки включены"
                messages.info(request, msg)
            else:
                msg = "Что-то пошло не так. Попробуйте ещё раз"
                messages.error(request, msg)
            return HttpResponseRedirect("enable")
        else:
            return HttpResponseRedirect("home")
        

    #Если метод get, то создаем пустую форму
    def get(self, request, *args, **kwargs):
        return render(request, "ringer/form-yes-no.html", {'label': 'Включить звонки?'})
    


class DisableRing(UpdateView):
    #Если метод post, обрабатываем данные
    def post(self, request, *args, **kwargs):
        if 'yes-but' in request.POST:
            if os.system("sudo systemctl stop ringer") == 0:
                msg = "Звонки выключены"
                messages.info(request, msg)
            else:
                msg = "Что-то пошло не так. Попробуйте ещё раз"
                messages.error(request, msg)
            return HttpResponseRedirect("disable")
        else:
            return HttpResponseRedirect("home")
        

    #Если метод get, то создаем пустую форму
    def get(self, request, *args, **kwargs):
        return render(request, "ringer/form-yes-no.html", {'label': 'Выключить звонки?'})



class Melony(FormView):
    #Если метод post, обрабатываем данные
    def post(self, request, *args, **kwargs):
        file_list = []
        form = UploadFileForm(request.POST, request.FILES)
        title = request.POST["title"]
        prewav = request.FILES.get("file_pre")
        inwav = request.FILES.get("file_in")
        outwav = request.FILES.get("file_out")
        file_list.append(prewav)
        file_list.append(inwav)
        file_list.append(outwav)

        for f in file_list:
            if not str(f).endswith("wav"):
                msg = "Допускаются только аудиофайлы в формате wav"
                messages.error(request, msg)
                return render(request, 
                              "ringer/change.html", 
                              {'form': form, 
                               'label': 'Укажите событие, к которому приурочен звонок ' \
                                        'и 3 аудиофайла с расширением .wav'})
        
        if form.is_valid():
            try:
                if fr.FileRevealer(title, file_list).matched() == 0:
                    msg = "Мелодии изменены"
                    messages.info(request, msg)
                    return HttpResponseRedirect("melody")
                else:
                    msg = "Что-то пошло не так"
                    messages.error(request, msg)
                    return render(request, 
                                "ringer/change.html", 
                                {'form': form, 
                                'label': 'Укажите событие, к которому приурочен звонок ' \
                                         'и 3 аудиофайла с расширением .wav'})
            except Exception as e:
                msg = f"Ошибка {e}. Попробуйте еще раз или загрузите другой файл"
                messages.error(request, msg)
        else:
            return render(request, 
                            "ringer/change.html", 
                            {'form': form, 
                            'label': 'Укажите событие, к которому приурочен звонок ' \
                                     'и 3 аудиофайла с расширением .wav'})
        

    #Если метод get, то создаем пустую форму
    def get(self, request, *args, **kwargs):
        form = UploadFileForm()   #Создаем экземпляр формы
        return render(request, 
                        "ringer/change.html", 
                        {'form': form, 
                        'label': 'Укажите событие, к которому приурочен звонок и 3 аудиофайла с расширением .wav'})


#Если вся страница - это форма, то можно ее представить как view:
class LessonQuantityView(UpdateView):
    #Если метод post, обрабатываем данные
    def post(self, request, *args, **kwargs):
        form = QuantityForm(request.POST)   #Получаем данные из формы
        thisless = int(request.POST.get('num'))  #Или request.POST['num']
        LessonQuantity.count_num = str(sum(1 for line in open(f'{user}/sggs/ringer/app/ringer.py', 'r') if "day.at(pre" in line))
        lesson_num = int(LessonQuantity.count_num)

        if form.is_valid() and thisless <= 11: #Проверяем данные формы на корректность
            form.save

            if thisless > lesson_num:
                for i in range(lesson_num, thisless):
                    with open(f"{user}/sggs/ringer/app/ringer.py", "r") as f:
                        original_data = f.read()
                    new_data = original_data.replace('#Higlighter', 
                                                     f"schedule.every().day.at(pre[{i}]).do(audio)\n" \
                                                     f"    schedule.every().day.at(lesson[{i}]).do(audio)\n" \
                                                     f"    schedule.every().day.at(tb[{i}]).do(audio)\n" \
                                                     "    #Higlighter")
                    i += 1
                    with open(f"{user}/sggs/ringer/app/ringer.py", "w") as f:
                        f.write(new_data)
                os.system("sudo systemctl restart ringer")
            elif thisless < lesson_num:
                while thisless < lesson_num:
                    with open(f"{user}/sggs/ringer/app/ringer.py", "r") as f:
                        original_data = f.read()
                    new_data = original_data.replace(f"    schedule.every().day.at(pre[{lesson_num - 1}]).do(audio)\n" \
                                                     f"    schedule.every().day.at(lesson[{lesson_num - 1}]).do(audio)\n" \
                                                     f"    schedule.every().day.at(tb[{lesson_num - 1}]).do(audio)\n",
                                                     "")
                                                     
                    lesson_num -= 1
                    with open(f"{user}/sggs/ringer/app/ringer.py", "w") as f:
                        f.write(new_data)
                os.system("sudo systemctl restart ringer")

            LessonQuantity.objects.all().delete()
            LessonQuantity.objects.create(num=thisless)
            #LessonQuantity.objects.update(num=thisless)
            return HttpResponseRedirect("lessons")
        else:
            messages.error(request, "Число не может быть больше 11")
            return render(request, "ringer/lessons.html", {'form': form, 'count_num': LessonQuantity.count_num,})

    #Если метод get, то создаем пустую форму
    def get(self, request, *args, **kwargs):
        form = QuantityForm()   #Создаем экземпляр формы
        LessonQuantity.count_num = str(sum(1 for line in open(f'{user}/sggs/ringer/app/ringer.py', 'r') if "day.at(pre" in line))
        return render(request, "ringer/lessons.html", {'form': form, 'count_num': LessonQuantity.count_num,}) #Передаем нашу форму в контексте


class ClearLogs(UpdateView):
    #Если метод post, обрабатываем данные
    def post(self, request, *args, **kwargs):
        if 'yes-but' in request.POST:
            if shutil.rmtree(r"sggs/ringer/logs") == 0 and os.makedirs(r"sggs/ringer/logs") == 0:
                msg = "Логи очищены. Что сделано, уже не вернуть..."
                messages.info(request, msg)
            else:
                msg = "Что-то пошло не так. Попробуйте ещё раз"
                messages.error(request, msg)
            return HttpResponseRedirect("clear")
        else:
            return HttpResponseRedirect("home")
        
    #Если метод get, то создаем пустую форму
    def get(self, request, *args, **kwargs):
        return render(request, "ringer/form-yes-no.html", {'label': 'Вы уверены?'})


class HolidaysView(UpdateView):
    #Если метод post, обрабатываем данные
    def post(self, request, *args, **kwargs):
        sign_list = [",", "?", "!", "/", "\\", ":", ";", "@", "#", "$", "%", "^", "&", 
                     "*", "(", ")", "\"", "'", "|", "[", "]", "{", "}", "-", "_", "+", 
                     "=", "`", "~"]
        form = HolidaysForm(request.POST)   #Получаем данные из формы
        thisless = request.POST['content']
        example = re.findall(r"([0-3][0-9]\.[0-1][0-9])", thisless)

        if re.search(r"([3][2-9]\.)|(\.[1][3-9])|(\.[2-9])", thisless):
            msg = "Введите корректную дату"
            messages.error(request, msg)
            return render(request, "ringer/holiday.html", {'form': form})

        for s in thisless:
            if s in sign_list:
                msg = "Не допускаются лишние знаки. Введите корректную дату в формате dd.mm"
                messages.error(request, msg)
                return render(request, "ringer/holiday.html", {'form': form})

        
        if form.is_valid() and example != []:     #Проверяем данные формы на корректность
            form.save
            if 'add-but' in request.POST:
                for i in example:
                    if not Holidays.objects.filter(content__icontains=f'{i}'):    #icontains - нечувствительный к регистру подпоиск
                        Holidays.objects.create(content=i)
                        file = open(f"{user}/sggs/ringer/app/quiet.txt", "a")
                        file.write(f"{i}\n")
                        file.close()
                        #if i == example[-1]:
                return HttpResponseRedirect("holiday")

                    
            elif 'del-but' in request.POST:
                for i in example:
                    Holidays.objects.filter(content__icontains=f'{i}').delete()
                    with open(f"{user}/sggs/ringer/app/quiet.txt", "r") as f:
                        old_data = f.read()
                    new_data = old_data.replace(f'{i}\n', '')
                    with open(f"{user}/sggs/ringer/app/quiet.txt", "w") as f:
                        f.write(new_data)
                    if i == example[-1]:
                        return HttpResponseRedirect("holiday")

        else:
            msg = "Даты вводятся через пробел без лишних знаков препинания"
            messages.error(request, msg)
            return render(request, "ringer/holiday.html", {'form': form})


    #Если метод get, то создаем пустую форму
    def get(self, request, *args, **kwargs):
        form = HolidaysForm()   #Создаем экземпляр формы
        return render(request, "ringer/holiday.html", {'form': form}) #Передаем нашу форму в контексте


class PlayNow(UpdateView):
    def post(self, request, *args, **kwargs):
        if 'yes-but' in request.POST:
            if os.system("sh sggs/ringer/app/lesson.sh &") == 0:
                msg = "Звонок играет"
                messages.info(request, msg)
            else:
                msg = "Что-то пошло не так. Попробуйте ещё раз"
                messages.error(request, msg)
            return HttpResponseRedirect("play-now")
        else:
            return HttpResponseRedirect("home")

    def get(self, request, *args, **kwargs):
        return render(request, "ringer/form-yes-no.html", {'label': 'Звонок проиграется 1 раз. Воспроизвести?'})


class EnableRadio(UpdateView):
    def post(self, request, *args, **kwargs):
        if 'yes-but' in request.POST:
            with open(f"{user}/sggs/ringer/radio/radio-on.sh", "r") as f:
                original_data = f.read()
            new_data = original_data.replace(f"#mpg123",
                                             "mpg123")
            with open(f"{user}/sggs/ringer/radio/radio-on.sh", "w") as f:
                f.write(new_data)
            
            msg = "Радио включено"
            messages.info(request, msg)
            return HttpResponseRedirect("radio-on")
        else:
            return HttpResponseRedirect("home")
        
    def get(self, request, *args, **kwargs):
        return render(request, "ringer/form-yes-no.html", {'label': "Радио будет включаться по расписанию.\n" \
                                                                    'Включить радио?'})
    

class DisableRadio(UpdateView):
    def post(self, request, *args, **kwargs):
        if 'yes-but' in request.POST:
            with open(f"{user}/sggs/ringer/radio/radio-on.sh", "r") as f:
                original_data = f.read()
            new_data = original_data.replace(f"mpg123 ",
                                             "#mpg123 ")
            with open(f"{user}/sggs/ringer/radio/radio-on.sh", "w") as f:
                f.write(new_data)
            
            msg = "Радио выключено"
            messages.info(request, msg)
            return HttpResponseRedirect("radio-off")
        else:
            return HttpResponseRedirect("home")
        
    def get(self, request, *args, **kwargs):
        return render(request, "ringer/form-yes-no.html", {'label': 'Радио будет выключено на всех переменах.\n' \
                                                                    'Выключить радио?'})