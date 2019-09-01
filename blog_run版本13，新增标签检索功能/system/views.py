import random

from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from itsdangerous import SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as TJSS

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework import viewsets

import constants
from CeleryTask.tasks import send_forget_password_email, send_password_reset_email
from accounts.models import User
from article.models import Article, Tag
from system.serializers import ArticleBestSerializer
from comment.models import CommentModel
from system.forms import LinkForm, ForgetPasswordForm
from system.models import UserWrite, LinkModel, PhotoModel, PhotoDetailModel, VideoModel, VideoType
from utils.verify import VerifyCode


def about_me(request):
    return render(request,'about.html')


class WriteSome(ListView):
    model = UserWrite
    template_name = 'write_some.html'
    paginate_by = 12


class WriteContent(DetailView):
    model = UserWrite
    template_name = 'write_content.html'
    slug_url_kwarg = 'pk'
    slug_field = 'pk'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_view_count()
        # self.object.view_count += 1
        # self.object.save(update_fields=['view_count'])
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = CommentModel.objects.filter(level_msg_id=self.object.id)
        p = Paginator(comment, 5)
        page_obj = p.page(1)
        context['page_obj'] = page_obj
        return context


class FeedBack(ListView):
    model = CommentModel
    template_name = 'feedback.html'
    paginate_by = 10

    def get_queryset(self):
        return CommentModel.objects.filter(note_id=1)


class LinkView(View):
    def get(self,request):
        comment_top_ten = CommentModel.objects.filter(note_id=1)[:10]
        wait_link = LinkModel.objects.filter(status=constants.WEB_LINK_WAIT)
        pass_link = LinkModel.objects.filter(status=constants.WEB_LINK_PASS)
        inner_link = LinkModel.objects.filter(is_inner=True)
        return render(request,'link.html',{
            'comment_top_ten':comment_top_ten,
            'wait_link':wait_link,
            'pass_link':pass_link,
            'inner_link':inner_link
        })

    def post(self,request):
        print(request.POST)
        code = request.POST.get('txtCode')
        v_code = VerifyCode(request)
        if not v_code.validate_code(code):
            data = {
                'msg': '验证码错啦',
                'status': 0,
            }
            return JsonResponse(data)
        form = LinkForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            txtTitle = form.cleaned_data.get('txtTitle')
            txtUserName = form.cleaned_data.get('txtUserName')
            txtUserTel = form.cleaned_data.get('txtUserTel')
            txtEmail = form.cleaned_data.get('txtEmail')
            txtSiteUrl = form.cleaned_data.get('txtSiteUrl')
            txaArticle = form.cleaned_data.get('txaArticle')
            obj = LinkModel()
            obj.web_name = txtTitle
            obj.contact_man = txtUserName
            obj.phone = txtUserTel
            obj.email = txtEmail
            obj.web_link = txtSiteUrl
            obj.web_description = txaArticle
            obj.save()
            data = {
                'msg': '申请成功',
                'status': 1,
            }
            return JsonResponse(data)
        else:
            print(form.errors)
            error_list = []
            for i in ['txtTitle','txtUserName','txtUserTel','txtEmail','txtSiteUrl','txaArticle']:
                error = form.errors.get(i)
                if error:
                    error_list.append(error[0])
            if len(error_list) <= 0:
                data = {
                    'msg': '申请失败，请重试',
                    'status': 0,
                }
                return JsonResponse(data)
            data = {
                'msg': error_list[0],
                'status': 0,
            }
            return JsonResponse(data)
        # web_name = request.POST.get('txtTitle')
        # contact_man = request.POST.get('txtUserName')
        # phone = request.POST.get('txtUserTel')
        # email = request.POST.get('txtEmail')
        # web_link = request.POST.get('txtSiteUrl')
        # web_description = request.POST.get('txaArticle')


class PhotoList(ListView):
    model = PhotoModel
    template_name = 'photo.html'
    paginate_by = 4


class PhotoDetail(ListView):
    model = PhotoDetailModel
    template_name = 'show-Photo.html'
    paginate_by = 4

    def get_queryset(self):
        photo_id = self.request.GET.get('photo')
        if photo_id == 'all':
            return PhotoDetailModel.objects.all()
        else:
            photo_obj = get_object_or_404(PhotoModel,pk=photo_id)
            return PhotoDetailModel.objects.filter(photo_obj=photo_obj)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo_id = self.request.GET.get('photo')
        context['photo_id'] = photo_id
        print(photo_id)

        comment = CommentModel.objects.filter(photo_id=photo_id)
        p = Paginator(comment, 5)
        page_obj = p.page(1)
        context['page_obj'] = page_obj
        return context


def forget_password(request):
    form = ForgetPasswordForm()
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            to_email = user.email
            serializer = TJSS(settings.SECRET_KEY, 900)
            info = {'username':username}
            secret_username = serializer.dumps(info)
            secret_username = secret_username.decode()
            send_forget_password_email(to_email,username,secret_username)
            return redirect('accounts:user_login')
    return render(request,'forget.html',{
        'form':form
    })


def password_reset(request,secret_username):
    serializer = TJSS(settings.SECRET_KEY, 900)
    info = serializer.loads(secret_username)
    username = info['username']
    print(username)
    user = User.objects.get(username=username)
    random_list = [chr(i) for i in list(range(65, 91)) + list(range(97, 123))] + [str(j) for j in range(10)]
    new_password = ''.join(random.sample(random_list, 9))
    print(new_password)
    user.set_password(new_password)
    send_password_reset_email(user.email,username,new_password)
    user.save()
    return render(request,'forget_back.html')


class MusicView(View):
    def get(self,request):
        return render(request,'music.html')


class VideoShow(DetailView):
    model = VideoModel
    template_name = 'VideoShow.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get(self,request,*args,**kwargs):
        response = super().get(request,*args,**kwargs)
        self.object.view_count += 1
        self.object.save(update_fields=['view_count'])
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        num = random.choice([1,2,3,4])
        video_list = VideoModel.objects.filter(is_valid=True)[:num]
        context['video_list'] = video_list
        return context

def cktest(request):
    return render(request,'cktest.html')


class VideoList(ListView):
    model = VideoModel
    template_name = 'video.html'
    paginate_by = 5

    def get_queryset(self):
        cls = self.request.GET.get('type')
        response = VideoModel.objects.filter(is_valid=True)
        if cls:
            classify = get_object_or_404(VideoType,code=cls)
            response = VideoModel.objects.filter(is_valid=True,classify=classify)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        cls = self.request.GET.get('type')
        if cls:
            context['code'] = cls
        return context


class TagList(ListView):
    model = Article
    template_name = 'tag_search.html'
    paginate_by = 10

    def get_queryset(self):
        tag_uid = self.request.GET.get('tag')
        return Article.objects.filter(tag__uid=tag_uid)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tag_uid = self.request.GET.get('tag')
        tag = Tag.objects.filter(uid=tag_uid).first()
        context['tag_name'] = ''
        if tag:
            context['tag_name'] = tag.name
        context['tag_uid'] = tag_uid
        return context


# from django.shortcuts import render,HttpResponse

# # Create your views here.
# def web_test(request):
#     return render(request,'websocket.html')
#
# from dwebsocket.decorators import accept_websocket
# @accept_websocket
# def path(request):
#     if request.is_websocket():
#         print(1)
#         request.websocket.send('下载完成'.encode('utf-8'))







