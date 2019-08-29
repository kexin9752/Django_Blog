from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework import viewsets

import constants
from article.models import Article
from system.serializers import ArticleBestSerializer
from comment.models import CommentModel
from system.forms import LinkForm
from system.models import UserWrite, LinkModel, PhotoModel, PhotoDetailModel
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
