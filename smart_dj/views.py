from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, 'smart_dj/about.html', {})

def layout(request):
    return render(request, 'smart_dj/layout.html', {})
