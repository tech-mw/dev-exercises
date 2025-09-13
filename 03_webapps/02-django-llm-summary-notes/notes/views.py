from django.http import HttpResponse


def IndexView(request):
    return HttpResponse('Hello, world. You are at the notes index.')
