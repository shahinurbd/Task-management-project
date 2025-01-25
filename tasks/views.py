from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee,Task
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



    

