from django.shortcuts import render
def hello(request):
    context          = {}
    context['hello'] = 'He World!'
    return render(request, 'hello.html', context)