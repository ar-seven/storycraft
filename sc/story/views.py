from django.shortcuts import render

# Create your views here.
def home(request):    
    context = {"loggedin": "false"}
    
    if request.user.is_authenticated:
        context.update({
            "loggedin": "true",
            "name": request.user.first_name,
            "username": request.user.username
        })
    print(context)    
    return render(request, 'index.html', context)

# Create your views here.
def generate(request):      
    return render(request, 'generate.html')
