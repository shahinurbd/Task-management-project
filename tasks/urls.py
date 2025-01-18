from django.urls import path
from tasks.views import showtask
urlpatterns = [
    path('show-task/', showtask)

]