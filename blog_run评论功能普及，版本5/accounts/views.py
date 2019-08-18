import os
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework import viewsets

import constants
from accounts.forms import RegisterForm, LoginForm, UserProfileForm
from accounts.models import User, UserProfile, UserIntegral, UserBalance, Collect, UserMessage, UserMessageAccept
from utils import balance_sn
from utils.balance_sn import sn_balance
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

class UserIntegralList(ListView):
    model = UserIntegral
    template_name = 'user_manage/user_point_list.html'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return UserIntegral.objects.filter(user=user)


def user_integral_del(request):
    data = {'status':0,'msg':'请先勾选再进行删除'}
    if request.method == 'POST':
        integral_id = request.POST.getlist('checkId[]')
        if integral_id:
            for i in integral_id:
                ui = get_object_or_404(UserIntegral, pk=i)
                ui.delete()
            data['status'] = 1
            data['msg'] = '删除成功'
    return JsonResponse(data)

class UserRecharge(View):
    def get(self,request):
        return render(request,'user_manage/user_amount_recharge.html')

    def post(self,request):
        user = request.user
        order_amount = request.POST.get('order_amount')
        payment_id = request.POST.get('payment_id')
        if payment_id == '3':
            method = constants.BALANCE_METHOD_ALIBABA
        elif payment_id == '4':
            method = constants.BALANCE_METHOD_WECAHT
        else:
            method = constants.BALANCE_METHOD_BANK
        UserBalance.objects.create(
            user=user,
            sn=sn_balance(),
            method=method,
            cash=Decimal(order_amount),
            status=constants.USER_UNPAY
        )
        data = {'status':1,'msg':'第三方支付接口正在努力搭建中,本次充值不扣取任何费用'}
        return JsonResponse(data)


class UserBalanceView(ListView):
    model = UserBalance
    template_name = 'user_manage/user_amount_log.html'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return UserBalance.objects.filter(user=user)


class UserBalanceDel(View):

    def post(self,request):
        print(request.POST)
        data = {'status':0,'msg':'删除失败,请稍后重试'}
        b_id = request.POST.getlist('checkId')
        try:
            b_list = b_id[0].split(',')
        except Exception as e:
            b_list = b_id
        if b_list:
            for b in b_list:
                balance = get_object_or_404(UserBalance,pk=b)
                balance.delete()
            data['status'] = 1
            data['msg'] = '已为您成功删除所选记录'
        return JsonResponse(data)


#因为支付接口还未接入，所以此功能待完善
def user_balance_list(request):
    return render(request,'user_manage/user_amount_list.html')

# class UserIntegralViewSet(viewsets.ModelViewSet):
#     queryset = UserIntegral.objects.all()


class UserCollectView(ListView):
    model = Collect
    template_name = 'user_manage/user_favorite.html'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return Collect.objects.filter(user=user)


class UserCollectDel(View):

    def post(self,request):
        print(request.POST)
        data = {'status':0,'msg':'删除失败,请稍后重试'}
        c_id = request.POST.getlist('checkId')
        try:
            c_list = c_id[0].split(',')
        except Exception as e:
            c_list = c_id
        if c_list:
            for c in c_list:
                collect = get_object_or_404(Collect,pk=c)
                collect.delete()
            data['status'] = 1
            data['msg'] = '已为您成功删除所选记录'
        return JsonResponse(data)


def user_center_avatar(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        img = request.FILES.get('avatar',None)
        #可以在这里删除名字有覆盖的头像，但是有个问题，不同用户上传同名不同图片的头像就歇逼了
        #看看可不可以在储存头像的时候对头像名称进行处理，加上用户的id
        #可以是可以，用f.open存储头像自定义图片名字，然后向avatar中存入f
        #不过貌似比较麻烦，以后有需要再说吧
        user_profile.avatar = img
        user_profile.save()
    return render(request,'user_manage/user_center_avatar.html',{
        'user_profile':user_profile
    })


class UserMessageAdd(View):
    def get(self,request):
        return render(request,'user_manage/user_message_add.html')

    def post(self,request):
        user = request.user
        data = {'status':0,'msg':'发送失败,请重试'}
        code = request.POST.get('txtCode')
        v_code = VerifyCode(request)
        if v_code.validate_code(code):
            to_username = request.POST.get('txtUserName')
            to_user = User.objects.filter(username=to_username).first()
            if not to_user or to_user.username == 'system_admin':
                data = {'status': 0, 'msg': '沙雕,没有这个用户'}
                return JsonResponse(data)
            title = request.POST.get('txtTitle')
            content = request.POST.get('txtContent')
            UserMessage.objects.create(
                user=user,
                title=title,
                content=content,
                to_user=to_user.id
            )
            UserMessageAccept.objects.create(
                user=user,
                title=title,
                content=content,
                to_user=to_user.id
            )
            data = {'status': 1, 'msg': '已发送'}
        else:
            data = {'status': 0, 'msg': '验证码输错辣'}

        return JsonResponse(data)


class UserMessageList(ListView):
    model = UserMessage
    template_name = 'user_manage/user_message_accept.html'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        if self.request.GET.get('params') == 'accept':
            system_admin = get_object_or_404(User, username='system_admin')
            return UserMessageAccept.objects.filter(to_user=user.id).exclude(user=system_admin)
        elif self.request.GET.get('params') == 'send':
            return UserMessage.objects.filter(user=user)
        elif self.request.GET.get('params') == 'system':
            system_admin = get_object_or_404(User,username='system_admin')
            return UserMessage.objects.filter(user=system_admin)


class UserMessageDel(View):
    def post(self,request):
        print(request.POST)
        data = {'status': 0, 'msg': '删除失败,请稍后重试'}
        m_id = request.POST.getlist('checkId')
        try:
            m_list = m_id[0].split(',')
        except Exception as e:
            m_list = m_id
        if m_list:
            for m in m_list:
                message = get_object_or_404(UserMessage, pk=m)
                message.delete()
            data['status'] = 1
            data['msg'] = '已为您成功删除所选记录'
        return JsonResponse(data)


class UserMessageAcceptDel(View):
    def post(self,request):
        print(request.POST)
        data = {'status': 0, 'msg': '删除失败,请稍后重试'}
        m_id = request.POST.getlist('checkId')
        try:
            m_list = m_id[0].split(',')
        except Exception as e:
            m_list = m_id
        if m_list:
            for m in m_list:
                message = get_object_or_404(UserMessageAccept, pk=m)
                message.delete()
            data['status'] = 1
            data['msg'] = '已为您成功删除所选记录'
        return JsonResponse(data)


class UserMessageDetail(DetailView):
    model = UserMessage
    slug_url_kwarg = 'pk'
    template_name = 'user_manage/user_message_detail.html'

class UserMessageAcceptDetail(DetailView):
    model = UserMessageAccept
    slug_url_kwarg = 'pk'
    template_name = 'user_manage/user_message_detail.html'