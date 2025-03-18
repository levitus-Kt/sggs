from django.urls import path

from . import views

app_name = "ringer"
urlpatterns = [
    # ex: /ringer/  # Домашняя страница
    path("", views.IndexView, name="index"),
    # ex: /ringer/lessons
    path("lessons", views.LessonQuantityView.as_view(), name="lessons"),
    path("holiday", views.HolidaysView.as_view(), name="holiday"),
    path("shell", views.shell, name="shell"),
    path("enable", views.EnableRing.as_view(), name="enable-ring"),
    path("disable", views.DisableRing.as_view(), name="disable-ring"),
    path("clear-logs", views.ClearLogs.as_view(), name="clear-logs"),
    path("melody", views.Melony.as_view(), name="Melony"),
    path("play-now", views.PlayNow.as_view(), name="play-now"),
    path("radio-on", views.EnableRadio.as_view(), name="enable-radio"),
    path("radio-off", views.DisableRadio.as_view(), name="disable-radio"),
    path("home", views.IndexView, name="empty"),
]
