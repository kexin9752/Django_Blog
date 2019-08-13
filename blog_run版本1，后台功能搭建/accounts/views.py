from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from accounts.forms import RegisterForm, LoginForm, UserProfileForm
from accounts.models import User, UserProfile, UserIntegral
from utils.verify import VerifyCode


def user_login(request):
    form = LoginForm(request)
    if request.method == 'POST':
        form = LoginForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                response = redirect('index')
                if request.META.get('HTTP_X_FORWARDED_FOR'):
                    ip = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    ip = request.META['REMOTE_ADDR']
                u = User.objects.get(username=username)
                u.ip_save(ip)
                if request.POST.get('remember') == 'on':
                    response.set_cookie('un', username,max_age=1296000)
                    response.set_cookie('pw', password,max_age=1296000)
                return response
    return render(request,'login/login.html',{
        'form':form
    })

def user_logout(request):
    logout(request)
    response = redirect('index')
    for i in request.COOKIES:
        response.delete_cookie(i)
    return response

def user_register(request):

    if request.method == 'POST':
        form = RegisterForm(request=request,data=request.POST)
        params = request.POST.get('params')
        if form.is_valid():
            form.register()
            return redirect('index')
        else:
            if params in ['password','repassword']:
                    error = form.non_field_errors()
            else:
                    error = form.errors.get(params)
            rest = {'data':error}
            return JsonResponse(rest)
    form = RegisterForm(request)
    return render(request,'login/register.html',{
        'form':form
    })


def verify_code(request):
    client = VerifyCode(request)
    return client.gen_code()


@login_required
def user_center_index(request):
    return render(request,'user_manage/user_center_index.html')


def user_center_proinfo(request):
    user = request.user
    user_profile = UserProfile.objects.filter(user=user).first()
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        print(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            real_name = data.get('real_name')
            age = data.get('age')
            qq = data.get('qq')
            address = data.get('address')
            phone_no = data.get('phone_no')
            gender = data.get('gender')
            province = data.get('province')
            city = data.get('city')
            area = data.get('area')
            email = data.get('email')
            nickname = data.get('nickname')
            up = UserProfile.objects.filter(user=user).first()
            if not up:
                up.user = user
            up.real_name = real_name
            up.age = age
            up.qq = qq
            up.address = address
            up.phone_no = phone_no
            up.gender = gender
            up.area = area
            up.province = province
            up.city = city
            up.save()
            user.email = email
            user.nickname = nickname
            user.save()
            return JsonResponse({'status':200})

        else:
            # params = request.POST.get('params')
            # print(form.non_field_errors())

            error = form.non_field_errors()
            rest = {'data':error,'age':''}
            age = request.POST.get('age')
            if isinstance(age, str):
                age_error = '日期格式不正确'
                rest['age'] = age_error
            print(1111)
            return JsonResponse(rest)
    form = UserProfileForm()
    return render(request,'user_manage/user_center_proinfo.html',{
        'form':form,
        'user_profile':user_profile
    })


def user_center_password(request):
    user = request.user
    rest = {'params':'','data':''}
    if request.method == 'POST':
        old_passwd = request.POST.get('old_passwd')
        u = authenticate(username=user.username,password=old_passwd)
        if u:
            new_passwd = request.POST.get('new_passwd')
            new_repasswd = request.POST.get('new_repasswd')
            if len(new_passwd) > 20 or len(new_passwd) < 7:
                rest['params'] = 'new_passwd'
                rest['data'] = '密码长度在7-20之间'
                return JsonResponse(rest)
            elif new_passwd != new_repasswd:
                rest['params'] = 'diff'
                rest['data'] = '两次输入密码不一致'
                return JsonResponse(rest)
            else:
                user.set_password(new_passwd)
                user.save()

        else:
            rest['params'] = 'old_passwd'
            rest['data'] = '原密码不正确'
            return JsonResponse(rest)

    return render(request,'user_manage/user_center_password.html')


def user_point_convert(request):
    user = request.user
    # integral = user.user_integral.first().integral
    be_integral = 10 * int(user.balance)
    print(be_integral)
    if request.method == 'POST':
        balance = request.POST.get('balance')
        password = request.POST.get('password')
        print(balance)
        print(password)
        rest = {'params':'','data':''}
        if not balance:
            rest['data'] = '请输入兑换金额'
            rest['params'] = 'balance'
        elif not balance.isdigit():
            rest['data'] = '请输入数字'
            rest['params'] = 'balance'
        elif int(balance) > int(user.balance):
            rest['data'] = '金额不足,请充值'
            rest['params'] = 'balance'
        elif not password:
            rest['data'] = '请输入密码'
            rest['params'] = 'password'
        elif not authenticate(username=user.username,password=password):
            rest['data'] = '密码不正确'
            rest['params'] = 'password'
        else:
            user.sum_balance(int(balance),0)
            user.sum_integral(int(balance)*10,1)
            source = '用户充值'
            user.integral_save(int(balance)*10,source,1)
        return JsonResponse(rest)


    return render(request,'user_manage/user_point_convert.html',{
        'be_integral':be_integral,
    })

def user_point_list(request):
    return render(request, 'user_manage/user_point_list.html')
