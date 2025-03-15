from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskModelForm,TaskDetailModelForm
from tasks.models import Task,Project
from datetime import date
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView,DetailView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


User = get_user_model()


def is_manager(user):
    return user.groups.filter(name='Manager').exists()


def is_employee(user):
    return user.groups.filter(name='User').exists()



class AdminDashboard(UserPassesTestMixin,View):

    login_url = 'no-permission'
    def test_func(self):
        return self.request.user.groups.filter(name="Admin").exists()

    def get(self,request,*args,**kwargs):

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



class EmployeeDashboard(UserPassesTestMixin,View):

    login_url = 'no-permission'
    def test_func(self):
        return self.request.user.groups.filter(name="User").exists()

    def get(self, request,*args, **kwargs):
        return render(request, "dashboard/user_dashboard.html")



class CreateTask(ContextMixin,LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin,View):
    login_url = 'sign-in'
    permission_required = 'tasks.add_task'
    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('no-permission')


    def get_context_data(self, **kwargs):
        Context = super().get_context_data(**kwargs)
        Context['task_form'] = kwargs.get('task_form', TaskModelForm())
        Context['task_detail_form'] = kwargs.get('task_detail_form', TaskDetailModelForm())
        return Context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request,'task_form.html',context)

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            task_form = TaskModelForm(request.POST)
            task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():
            """For Model form data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request,"Task created successfully")
            context = self.get_context_data(task_form=task_form,task_detail_form=task_detail_form)
            
            return render(request, 'task_form.html', context)
        


permission = [login_required,permission_required('tasks.change_task', login_url='no-permission')]
@method_decorator(permission, name='dispatch')
class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()
        # print(context)
        if hasattr(self.object, 'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(
                instance=self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)

        task_detail_form = TaskDetailModelForm(
            request.POST, request.FILES, instance=getattr(self.object, 'details', None))

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', self.object.id)
        return redirect('update-task', self.object.id)


    

delete_permission = [login_required,permission_required('tasks.delete_task', login_url='no-permission')]
@method_decorator(delete_permission, name='dispatch')
class DeleteTask(DeleteView):

    model = Task
    success_url = reverse_lazy('manager-dashboard')
    pk_url_kwarg = 'id'
    context_object_name = 'task_details.html'



view_project_permission = [login_required,permission_required('projects.view_project', login_url='no-permission')]

@method_decorator(view_project_permission, name='dispatch')
class ViewProject(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'show_task.html'

    def get_queryset(self):
        queryset = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
        return queryset


class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    template_name = 'task_details.html'
    content_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Task.STATUS_CHOICES
        return context
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)

@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('admin-dashboard')
    elif is_employee(request.user):
        return redirect('user-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    
    return redirect('no-permission')




    

