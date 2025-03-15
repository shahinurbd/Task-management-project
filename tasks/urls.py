from django.urls import path
from tasks.views import dashboard,CreateTask,UpdateTask,ViewProject,TaskDetail,DeleteTask,EmployeeDashboard,AdminDashboard
urlpatterns = [
    path('manager-dashboard/', AdminDashboard.as_view(), name="manager-dashboard"),
    path('user-dashboard/', EmployeeDashboard.as_view(), name='user-dashboard'),
    #path('create-task/', create_task, name="create-task"),
    path('create-task/', CreateTask.as_view(), name="create-task"),
    # path('view_task/', view_task),
    path('view-task/', ViewProject.as_view(), name='view-task'),
    path('task/<int:task_id>/details/', TaskDetail.as_view(), name='task-details'),
    # path('update-task/<int:id>/',update_task, name='update-task'),
    path('update-task/<int:id>/',UpdateTask.as_view(), name='update-task'),
    # path('delete-task/<int:id>/',delete_task, name='delete-task'),
    path('delete-task/<int:id>/',DeleteTask.as_view(), name='delete-task'),
    path('dashboard/',dashboard, name='dashboard'),

]