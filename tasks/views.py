from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm,TaskDetailModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Min,Max,Avg
from django.contrib import messages
# Create your views here.
def admin_dashboard(request):
   

    #getting task count
    # total_task = tasks.count()
    # pending_task = Task.objects.filter(status='PENDING').count()
    # in_progress_task = Task.objects.filter(status='IN_PROGRESS').count()
    # completed_task = Task.objects.filter(status='COMPLETED').count()

    type = request.GET.get('type', 'all')


    counts = Task.objects.aggregate(

        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING'))
    )

    

    #retriving task data

    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')

    if type=='completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type=='in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    if type=='pending':
        tasks = base_query.filter(status='PENDING')
    if type=='all':
        tasks = base_query.all()
        

    context = {
        "tasks": tasks,
        "counts": counts
    }
    return render(request, "dashboard/admin_dashboard.html", context)

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

def create_task(request):
    # employee = Employee.objects.all()
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()
    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)

        if task_form.is_valid() and task_detail_form.is_valid():

            """For Model form data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request,"Task created successfully")
            return redirect("create-task")
            
            return HttpResponse("Task added succesfully!")

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request,'task_form.html',context)


def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)
    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.details)

        if task_form.is_valid() and task_detail_form.is_valid():

            """For Model form data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', id)

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request,'task_form.html',context)

def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('admin-dashboard')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('admin-dashboard')
        


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



    

