import os
from decimal import Decimal
from itsdangerous import SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as TJSS

from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum, Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework import viewsets

import constants
from accounts.forms import RegisterForm, LoginForm, UserProfileForm, UserAddressForm, UserArticleEditForm
from accounts.models import User, UserProfile, UserIntegral, UserBalance, Collect, UserMessage, UserMessageAccept, \
    UserAddress, Cart, OrderDetail, Order
from article.models import Classify, Article, Tag, Author
from utils import balance_sn, order_sn
from utils.balance_sn import sn_balance
from utils.verify import VerifyCode
from CeleryTask.tasks import send_activate_email


def user_register(request):

    if request.method == 'POST':
        form = RegisterForm(request=request,data=request.POST)
        params = request.POST.get('params')
        if form.is_valid():
            user = form.register()
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            # password = form.cleaned_data['password']
            # 正式处理发送邮件
            # 加密用户的身份信息，生成激活token
            serializer = TJSS(settings.SECRET_KEY, 900)
            info = {'confirm': user.id}
            token = serializer.dumps(info)
            # 默认解码为utf8
            token = token.decode()
            # 使用celery发邮件
            send_activate_email.delay(email, username, token)
            rest = {'data':'注册成功！邮件正在发送，请前往邮箱激活账号'}
            return JsonResponse(rest)
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


class UserActivate(View):
    """用户通过邮件激活功能"""

    def get(self, request, token):
        """点击邮件链接激活业务处理"""

        serializer = TJSS(settings.SECRET_KEY, 900)
        try:
            info = serializer.loads(token)

            # 获取要激活用户的id
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            # 跳转到登录页面
            return HttpResponseRedirect('/accounts/user/login/')

        except SignatureExpired as e:
            # 激活链接已过期，应重发激活邮件
            return HttpResponse('激活链接已过期！')


def user_login(request):
    if request.user.id:
        return HttpResponse('你已登录')
    form = LoginForm(request)
    if request.method == 'POST':
        form = LoginForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user:
                print(121)
                login(request,user)
                response = redirect('index')
                if request.META.get('HTTP_X_FORWARDED_FOR'):
                    ip = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    ip = request.META['REMOTE_ADDR']
                u = User.objects.get(username=username)
                u.ip_save(ip)
                # if request.POST.get('remember') == 'on':
                #     response.set_cookie('un', username,max_age=1296000)
                #     response.set_cookie('pw', password,max_age=1296000)
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




def verify_code(request):
    client = VerifyCode(request)
    return client.gen_code()


# @login_required(login_url='/accounts/user/login/')
def user_center_index(request):
    user = request.user
    #给一个第一次登陆的变量
    first_login = 0
    if user.is_fresh:
        user.sum_integral(5,1)
        user.integral_save(5,'每日登录',1)
        user.is_fresh = 0
        #如果进到了这里面，则设置为1，用于前端判断是否弹框
        first_login = 1
        user.save()
    order = Order.objects.filter(user=user).first()
    return render(request,'user_manage/user_center_index.html',{
        'order':order,
        'first_login':first_login
    })


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
            up = UserProfile.objects.get_or_create(user=user)
            up = up[0]

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
    user_profile = UserProfile.objects.filter(user=user).first()
    if request.method == 'POST':
        img = request.FILES.get('avatar',None)
        #可以在这里删除名字有覆盖的头像，但是有个问题，不同用户上传同名不同图片的头像就歇逼了
        #看看可不可以在储存头像的时候对头像名称进行处理，加上用户的id
        #可以是可以，用f.open存储头像自定义图片名字，然后向avatar中存入f
        #不过貌似比较麻烦，以后有需要再说吧
        if user_profile:
            user_profile.avatar = img
            user_profile.save()
        else:
            user_profile = UserProfile()
            user_profile.user = user
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


#
# def test_shop(request):
#     return render(request,'shopping.html')


class UserAddressView(View):

    def get(self,request):
        return render(request,'user_manage/user_address_add.html')

    def post(self,request):
        form = UserAddressForm(request=request,data=request.POST)
        if form.is_valid():
            user = request.user
            addr = UserAddress()
            is_default = form.cleaned_data.get('chkAgree')
            print(is_default)
            if is_default:
                UserAddress.objects.filter(user=user,is_valid=True,is_default=True).update(is_default=False)
            else:
                is_default = 0
            addr.user = user
            addr.is_default = int(is_default)
            addr.province = form.cleaned_data['txtProvince']
            addr.city = form.cleaned_data['txtCity']
            addr.area = form.cleaned_data['txtArea']
            addr.address = form.cleaned_data['txtAddress']
            addr.username = form.cleaned_data['txtAcceptName']
            addr.phone = form.cleaned_data['txtMobile']
            addr.email = form.cleaned_data['txtEmail']
            addr.post_code = form.cleaned_data['txtPostCode']
            addr.save()
            data = {'status': 1, 'msg': '添加成功'}
        else:
            data = {'status': 0, 'msg': '添加失败，请检查输入内容'}
            for e in form.errors:
                err = form.errors[e][0]
                data = {'status': 0, 'msg': '添加失败'+err}
        return JsonResponse(data)


class UserAddressList(ListView):
    model = UserAddress
    template_name = 'user_manage/user_address.html'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        addr = UserAddress.objects.filter(user=user,is_valid=True)
        if addr.count() != 0:
            addr_default = UserAddress.objects.filter(user=user, is_default=True)
            if not addr_default:
                addr_obj = addr.first()
                addr_obj.is_default = True
                addr_obj.save()
        return addr


class UserAddressDel(View):
    def post(self,request):
        print(request.POST)
        data = {'status': 0, 'msg': '删除失败,请稍后重试'}
        a_id = request.POST.getlist('checkId')
        try:
            a_list = a_id[0].split(',')
        except Exception as e:
            a_list = a_id
        if a_list:
            for a in a_list:
                message = get_object_or_404(UserAddress, pk=a)
                message.delete()
            data['status'] = 1
            data['msg'] = '已为您成功删除所选记录'
        return JsonResponse(data)


class UserAddressSetDefault(View):
    def post(self,request):
        data = {'status': 1, 'msg': '收货地址更改成功'}
        try:
            user = request.user
            addr_id = request.POST.get('id')
            addr = UserAddress.objects.get(pk=addr_id)
            addr.is_default = True
            UserAddress.objects.filter(is_default=True,user=user).update(is_default=False)
            addr.save()
            Order.objects.filter(user=user,order_status=constants.ORDER_STATUS_SUBMIT).update(order_address=addr)
        except Exception as e:
            data['status'] = 0
            data['msg'] = '设置失败，请重试'
        return JsonResponse(data)


class UserShoppingList(ListView):
    model = Cart
    template_name = 'user_manage/user_shopping.html'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)


class UserShoppingDel(View):
    def post(self, request):
        print(request.POST)
        data = {'status': 0, 'msg': '删除失败,请稍后重试'}
        a_id = request.POST.getlist('checkId')
        try:
            a_list = a_id[0].split(',')
        except Exception as e:
            a_list = a_id
        if a_list:
            for a in a_list:
                message = get_object_or_404(Cart, pk=a)
                message.delete()
            data['status'] = 1
            data['msg'] = '已为您成功删除所选记录'
        return JsonResponse(data)


class UserOrderCreate(View):

    def post(self, request):
        print(request.POST)
        user = request.user
        addr = UserAddress.objects.filter(user=user, is_default=True, is_valid=True).first()
        print(addr)
        if not addr:
            data = {'status': 0, 'msg': '订单生成失败,请先设置收货地址'}
            return JsonResponse(data)
        data = {'status': 0, 'msg': '订单生成失败,请稍后重试'}
        a_id = request.POST.getlist('checkId')
        try:
            a_list = a_id[0].split(',')
        except Exception as e:
            a_list = a_id
        if a_list:
            cart_list = Cart.objects.filter(id__in=a_list)
            order = Order()
            order.user = user
            order.order_address = addr
            order.order_sn = order_sn.sn_order()
            order.goods_count = cart_list.aggregate(Sum('count'))['count__sum']
            order.order_price = cart_list.aggregate(Sum('total_price'))['total_price__sum']
            order.save()
            with transaction.atomic():
                for cart in cart_list:
                    order_detail = OrderDetail()
                    order_detail.order = order
                    order_detail.goods_id = cart.goods.id
                    order_detail.goods_name = cart.name
                    order_detail.goods_price = cart.price
                    order_detail.goods_number = cart.count
                    order_detail.goods_total = cart.total_price
                    order_detail.goods_image = cart.img
                    order_detail.save()
                    cart.delete()
            data['status'] = 1
            data['msg'] = '已为您成功生成订单'
        return JsonResponse(data)


class UserOrderList(ListView):
    model = Order
    template_name = 'user_manage/user_order-list.html'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        order = Order.objects.filter(user=user, order_status=constants.ORDER_STATUS_SUBMIT)
        status = self.request.GET.get('status')
        if status == 'submit':
            pass
        elif status == 'paied':
            order = Order.objects.filter(user=user, order_status=constants.ORDER_STATUS_PAIED)
        elif status == 'send':
            order = Order.objects.filter(user=user, order_status=constants.ORDER_STATUS_SEND)
        elif status == 'done':
            order = Order.objects.filter(user=user, order_status=constants.ORDER_STATUS_DONE)
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get('status')
        context['status'] = status
        return context


class UserOrderDel(View):

    def post(self, request):
        print(request.POST)
        data = {'status': 0, 'msg': '删除失败,请稍后重试'}
        a_id = request.POST.getlist('checkId')
        try:
            a_list = a_id[0].split(',')
        except Exception as e:
            a_list = a_id
        if a_list:
            with transaction.atomic():
                for a in a_list:
                    message = get_object_or_404(Order, pk=a)
                    message.delete()
            data['status'] = 1
            data['msg'] = '已为您成功删除所选记录'
        return JsonResponse(data)


class UserOrderDetail(View):

    def get(self,request):
        user = request.user
        sn = request.GET.get('sn')
        order = Order.objects.filter(user=user,order_sn=sn).first()
        return render(request,'user_manage/user_order_detail.html',{
            'order':order
        })


class PayOrder(View):
    def post(self,request):
        user = request.user
        sn = request.POST.get('checkSn')
        data = {'status': 1, 'msg': '恭喜您，支付成功'}
        if sn:
            order = Order.objects.filter(user=user,order_sn=sn).first()
            pay_price = int(order.order_price)
            try:
                user.sum_integral(pay_price,0)
                user.integral_save(pay_price,'购买商品',0)
                order.order_status = constants.ORDER_STATUS_PAIED
                order.save()
            except Exception as e:
                data = {'status': 0, 'msg': '积分不足，请充值后购买'}
        else:
            data = {'status': 0, 'msg': '当前网络波动，请刷新重试'}
        return JsonResponse(data)


class UserArticleEdit(View):

    def get(self,request):
        art_uid = request.GET.get('checkUid')
        if art_uid:
            art = Article.objects.get(uid=art_uid)
        classify = Classify.objects.all()
        return render(request,'user_manage/user_article_edit.html',locals())

    def post(self,request):
        print(request.POST)
        print(request.FILES)
        user = request.user
        title = request.POST.get('title')
        classify = request.POST.get('classify')
        content = request.POST.get('content')
        tags = request.POST.getlist('tags')
        fabu = request.POST.get('fabu')
        caogao = request.POST.get('caogao')
        art_id = request.POST.get('article_id')
        if art_id:
            art = Article.objects.get(pk=art_id)
        else:
            art = Article()
        art.title = title
        art.classify = Classify.objects.filter(code=classify).first()
        art.content = content
        print(fabu,111)
        print(caogao,222)
        if fabu:
            art.status = constants.ARTICLE_STATUS_WAIT
        elif caogao:
            art.status = constants.ARTICLE_STATUS_DRAFT
        img = request.FILES.get('img')
        if img:
            art.img = img
        author = Author.objects.get_or_create(name=user.username)
        art.author = author[0]
        art.save()
        if tags:
            for t in tags:
                tag_obj = Tag.objects.get_or_create(name=t)
                art.tag.add(tag_obj[0])
                art.save()
        return HttpResponseRedirect('/accounts/user/article/list/?status=wait')


class UserArticleList(ListView):
    model = Article
    template_name = 'user_manage/user_article_pass_list.html'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        author = Author.objects.get_or_create(name=user.username)
        art_list = Article.objects.filter(author=author[0],status=constants.ARTICLE_STATUS_PASS)
        status = self.request.GET.get('status')
        if status == 'pass':
            pass
        elif status == 'wait':
            art_list = Article.objects.filter(author=author[0], status=constants.ARTICLE_STATUS_WAIT)
        elif status == 'ban':
            art_list = Article.objects.filter(author=author[0], status=constants.ARTICLE_STATUS_FAIL)
        elif status == 'draft':
            art_list = Article.objects.filter(author=author[0], status=constants.ARTICLE_STATUS_DRAFT)
        return art_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get('status')
        context['status'] = status
        return context


class UserArticleDel(View):

    def post(self, request):
        print(request.POST)
        data = {'status': 0, 'msg': '删除失败,请稍后重试'}
        a_id = request.POST.getlist('checkId')
        try:
            a_list = a_id[0].split(',')
        except Exception as e:
            a_list = a_id
        if a_list:
            with transaction.atomic():
                for a in a_list:
                    message = get_object_or_404(Article, pk=a)
                    message.delete()
            data['status'] = 1
            data['msg'] = '已为您成功删除所选记录'
        return JsonResponse(data)