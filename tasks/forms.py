from django import forms
from tasks.models import Task,TaskDetail

#django form
class TaskForm(forms.Form):
    title = forms.CharField(max_length=250,label="Task title")
    description = forms.CharField(widget=forms.Textarea,label="Task Description")
    due_date = forms.DateField(widget=forms.SelectDateWidget,label="Due Date")
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],label="Assigned To")

    def __init__(self, *args, **kwargs):
        #print(args,kwargs)
        employee = kwargs.pop("employees", [])
        print(employee)
        super().__init__(*args,**kwargs)
        self.fields['assigned_to'].choices = [
            (emp.id, emp.name) for emp in employee
        ]


class StyleFormMixin:
    """Mixinig to apply style to form field"""

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_style_widgets()


    default_class = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 mt-2"

    def apply_style_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                'class': self.default_class,
                'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                'class': self.default_class,
                'placeholder': f"Enter {field.label.lower()}",
                'row': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                'class': "border-2 border-gray-300 p-2 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 mt-2"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
               field.widget.attrs.update({
                'class': ""
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_class
                })


#django model form
class TaskModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Task

        fields = ['title','description','due_date','assigned_to']

        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple,
        }

        


class TaskDetailModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority','notes', 'asset']

    




