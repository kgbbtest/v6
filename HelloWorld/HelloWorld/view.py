from django.shortcuts import render
def hello(request):
    context          = {}
    context['hello'] = 'He666 World!'
    return render(request, 'hello.html', context)