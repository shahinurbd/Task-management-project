from django.shortcuts import render
from django.http import HttpResponse
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




    

