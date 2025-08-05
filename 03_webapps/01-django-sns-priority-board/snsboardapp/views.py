from django.shortcuts import render


def signupfunc(request):
    """
    Render the signup page.
    """
    return render(request, 'signup.html', {})
