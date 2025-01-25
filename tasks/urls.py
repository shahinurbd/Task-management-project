from django.urls import path
from tasks.views import admin_dashboard, user_dashboard, test,task_form
urlpatterns = [
    path('admin-dashboard/', admin_dashboard),
    path('user-dashboard/', user_dashboard),
    path('test/', test),
    path('task_form/', task_form)

]