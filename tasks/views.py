from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Min,Max,Avg
# Create your views here.
def admin_dashboard(request):
    return render(request, "dashboard/admin_dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")

def test(request):
    names = ["shahin", "hasan", "zahid"]
    count = 0
    for name in names:
        count += 1

    context = {
        "names" : names,
        "age" : 25,
        "count" : count
    }
    return render(request, "test.html",context)

def task_form(request):
    # employee = Employee.objects.all()
    form = TaskModelForm()
    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():

            """For Model form data"""
            form.save()

            return render(request, 'task_form.html', {"form": form, "message": "task added successfully"})

            """for django form data"""
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')

            # task = Task.objects.create(title=title, description=description, due_date=due_date)

            # #assign employee to tasks
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            
            return HttpResponse("Task added succesfully!")


    context = {"form": form}
    return render(request,'task_form.html',context)


def view_task(request):
    #for retrive all data
    #tasks = Task.objects.all()

    #for retrive specefic data
    #task_3 = Task.objects.get(id=1)

    #get first data
    #first_task = Task.objects.first()

    # return render(request, 'show_task.html', {"tasks": tasks, "task3": task_3, "first_task": first_task})
    #show the tasks that are pending
    #tasks = Task.objects.filter(status="PENDING")
    #show the task wich due_date is today
    #tasks = Task.objects.filter(due_date=date.today())
    """show that task that are not Low"""
    #tasks = TaskDetail.objects.exclude(priority="L")
    """show the task which contain 'paper' AND status pending"""
    #tasks = Task.objects.filter(title__icontains='c', status="PENDING")

    """show the task which are pending or in progress"""
    #tasks = Task.objects.filter(Q(status="PENDING") | Q(status="IN_PROGRESS"))

    #tasks = Task.objects.filter(status="PENDING").exists()

    #Select_related (foreignKey, OneToOneField)
    #tasks = Task.objects.select_related('details').all()
    #tasks = TaskDetail.objects.select_related('task').all()
    #tasks = Task.objects.select_related('project').all()

    """prefetch_related (reverse foregnKey, ManyToMany)"""
    #tasks = Project.objects.prefetch_related('task_set').all()
    #tasks = Task.objects.prefetch_related('assigned_to').all()
    # tasks = Employee.objects.prefetch_related('tasks').all()
    # return render(request, "show_task.html", {"tasks": tasks})

    """aggrigate funtion"""
    #task_count = Task.objects.aggregate(num_cnt=Count('id'))

    projects = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
    return render(request, "show_task.html", {"projects": projects})



    

