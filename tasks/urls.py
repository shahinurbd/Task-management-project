from django.urls import path
from tasks.views import showtask,show_task
urlpatterns = [
    path('show-task/', showtask),
    path('show_task/<int:id>/', show_task)


]