import datetime
import re

from django import forms
from django.contrib.auth import authenticate, login

import constants
from accounts.models import User, UserProfile, UserIntegral
from django.db import models

from article.models import Article
from utils.verify import VerifyCode


class RegisterForm(forms.ModelForm):
    repassword = forms.CharField(label='确认密码',max_length=128)
    verify_code = forms.CharField(label='验证码',max_length=4,min_length=4)

    def __init__(self,request,*args,**kwargs):
        super(RegisterForm, self).__init__(*args,**kwargs)
        self.request = request

    class Meta:
        model = User
        fields = ["password","nickname","username","email"]


    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if not nickname:
            raise forms.ValidationError('用户昵称不能为空')
        elif len(nickname) > 20 or len(nickname) < 3:
            raise forms.ValidationError('昵称长度在3-20个字符之间')
        return nickname

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if 6 < len(username) < 15:
                user = User.objects.filter(username=username).first()
                if user:
                    raise forms.ValidationError('用户名已存在')
            else:
                raise forms.ValidationError('用户名长度应为7-15个字符之间')
        else:
            raise forms.ValidationError('用户名不能为空')
        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')
        pattern = r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
        if email:
            if not re.search(pattern,email):
                raise forms.ValidationError('请输入正确的邮箱格式')
        return email

    def clean_verify_code(self):
        verify_code = self.cleaned_data.get('verify_code')
        if not VerifyCode(self.request).validate_code(verify_code):
            raise forms.ValidationError('验证码错误')
        return verify_code

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repassword = cleaned_data.get('repassword')
        if not password:
            raise forms.ValidationError('密码不能为空')
        elif len(password) < 7:
            raise forms.ValidationError('密码不能小于7位数')
        elif not repassword:
            raise forms.ValidationError('确认密码不能为空')
        elif not password == repassword:
            raise forms.ValidationError('两次密码前后不一致')
        return cleaned_data

    def register(self):
        username = self.cleaned_data.get('username')
        nickname = self.cleaned_data.get('nickname')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        u = User.objects.create_user(
            username=username,
            password=password,
            nickname=nickname,
            email=email
        )
        UserIntegral.objects.create(
            user=u,
            integral=20,
            source='新用户注册赠送积分',
            detail='+20',
        )
        user = authenticate(username=username,password=password)
        login(self.request,user)
        return user


class LoginForm(forms.Form):
    verify_code = forms.CharField(label='验证码', max_length=4, min_length=4)
    username = forms.CharField(label='用户名',max_length=32)
    password = forms.CharField(label='密码',max_length=64)

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request

    def clean_verify_code(self):
        verify_code = self.cleaned_data.get('verify_code')
        if verify_code:
            verify = VerifyCode(self.request)
            if not verify.validate_code(verify_code):
                raise forms.ValidationError('验证码不正确')
        else:
            raise forms.ValidationError('验证码不能为空')
        return verify_code

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username:
            if User.objects.filter(username=username).exists():
                if password:
                    if not authenticate(username=username,password=password):
                        raise forms.ValidationError('密码不正确')
                else:
                    raise forms.ValidationError('密码不能为空')
            else:
                raise forms.ValidationError('用户名不存在')
        else:
            raise forms.ValidationError('用户名不能为空')
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    # real_name = forms.CharField(label='真实姓名',max_length=12,min_length=2)
    # gender = forms.ChoiceField(widget=forms.RadioSelect,choices=constants.USER_GENDER_CHOICES)
    # age = forms.IntegerField(label='年龄')
    # qq = forms.IntegerField(label='QQ账号')
    # region = forms.CharField(label='所在地区', max_length=64, required=True)
    # address = forms.CharField(label='详细地址',max_length=128)
    email = forms.EmailField(label='邮箱')
    nickname = forms.CharField(label='昵称',max_length=28,min_length=2)
    # phone_no = forms.CharField(label='手机号码',max_length=11,min_length=11)
    class Meta:
        model = UserProfile
        fields = ['real_name','age','qq','address','phone_no','gender','province','city','area']

    def clean(self):
        cleaned_data = super().clean()
        phone_no = cleaned_data.get('phone_no')
        print(phone_no)
        pattern = r'1[3-8][0-9]{9}'
        if phone_no:
            print(phone_no)
            if not re.search(pattern,phone_no):
                print(1)
                raise forms.ValidationError('请输入正确的手机号码')
        return cleaned_data


class UserAddressForm(forms.Form):

    txtAcceptName = forms.CharField(label='收件人姓名',max_length=12,error_messages={
        'required':'收件人不能为空',
        'invalid':'必须为中文或英文字母',
        'max_length':'长度不得超过12个字符'
    })
    txtProvince = forms.CharField(label='省份',max_length=12)
    txtCity = forms.CharField(label='城市',max_length=12)
    txtArea = forms.CharField(label='区域',max_length=12)
    txtAddress = forms.CharField(label='详细地址',max_length=128,error_messages={
        'max_length':'详细地址内容最大长度为128个字符'
    })
    txtMobile = forms.CharField(label='联系方式',max_length=11,min_length=11,error_messages={
        'required':'联系电话不能为空',
        'max_length':'请输入正确的手机号码'
    })
    txtEmail = forms.EmailField(label='邮件',required=False,error_messages={
        'invalid':'请输入正确的邮箱格式'
    })
    txtPostCode = forms.CharField(label='邮件编码',max_length=10,required=False)
    txtCode = forms.CharField(label='验证码',max_length=4,min_length=4,error_messages={
        'required':'验证码不能为空',
        'max_length':'请输入正确的验证码'
    })
    chkAgree = forms.CharField(label='是否设置会默认地址',required=False)

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request

    def clean_txtMobile(self):
        txtMobile = self.cleaned_data.get('txtMobile')
        pattern = r'1[3-8][0-9]{9}'
        if txtMobile:
            if not re.search(pattern, txtMobile):
                raise forms.ValidationError('请输入正确的手机号码')
        return txtMobile

    def clean_txtCode(self):
        txtCode = self.cleaned_data.get('txtCode')
        if txtCode:
            verify = VerifyCode(self.request)
            if not verify.validate_code(txtCode):
                raise forms.ValidationError('验证码不正确')
        else:
            raise forms.ValidationError('验证码不能为空')
        return txtCode


class UserArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['content']