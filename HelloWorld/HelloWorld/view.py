from django.shortcuts import render
def hello(request):
    context          = {}
    context['hello'] = 'Hel World!'
    return render(request, 'hello.html', context)