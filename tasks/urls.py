from django.urls import path
from tasks.views import admin_dashboard, user_dashboard, test,create_task, view_task, update_task,delete_task
urlpatterns = [
    path('admin-dashboard/', admin_dashboard, name="admin-dashboard"),
    path('user-dashboard/', user_dashboard),
    path('test/', test),
    path('create-task/', create_task, name="create-task"),
    path('view_task/', view_task),
    path('update-task/<int:id>/',update_task, name='update-task'),
    path('delete-task/<int:id>/',delete_task, name='delete-task'),

]