from django.contrib.auth import authenticate


def check_user(request):
    un = request.COOKIES.get('un')
    if un:
        pw = request.COOKIES.get('pw')
        user = authenticate(username=un,password=pw)
    else:
        user = request.user
    if not user.is_authenticated:
        user = None
    return {'user':user}

