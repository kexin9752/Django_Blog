import json

from django.views import View
from rest_framework import viewsets
from rest_framework.request import Request
from django.http import QueryDict, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

import constants
from mall.models import Goods
from system.models import PhotoDetailModel

from system.serializers import *


# def get_parameter_dic(request, *args, **kwargs):
#
#     if isinstance(request, Request) == False:
#         return {}
#
#     query_params = request.query_params
#     if isinstance(query_params, QueryDict):
#         query_params = query_params.dict()
#     result_data = request.data
#     if isinstance(result_data, QueryDict):
#         result_data = result_data.dict()
#
#     if query_params != {}:
#         return query_params
#     else:
#         return result_data

class UserWriteViewSet(viewsets.ModelViewSet):

    queryset = UserWrite.objects.order_by('-created_at')[:3]
    serializer_class = UserWriteSerializer


class ArticleBestApi(APIView):
    def get(self,request):
        params = request.query_params
        status = params.get('status') if params else ''
        print(status)
        if status == 'art_best':
            art_best_list = Article.objects.filter(is_best=True,is_valid=True, status=constants.ARTICLE_STATUS_PASS)[:3]
            serializer = ArticleBestSerializer(art_best_list,many=True)
            return Response(serializer.data)
        elif status == 'art_list':
            art_rank_list = Article.objects.order_by('-view_count')[:6]
            serializer = ArticleBestSerializer(art_rank_list,many=True)
            return Response(serializer.data)

        elif status == 'art_new':
            art_new_list = Article.objects.order_by('-created_at')[:1]
            serializer = ArticleBestSerializer(art_new_list,many=True)
            return Response(serializer.data)
        elif status == 'article':
            art_list = Article.objects.all()[:12]
            serializer = ArticleBestSerializer(art_list,many=True)
            return Response(serializer.data)

class NoteMsgViewSet(viewsets.ModelViewSet):

    queryset = CommentModel.objects.filter(note_id=1).order_by('-created_at')[:3]
    serializer_class = NoteMsgSerializer


class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()[:30]
    serializer_class = TagSerializer

class LinkViewSet(viewsets.ModelViewSet):

    queryset = LinkModel.objects.filter(status=constants.WEB_LINK_PASS)
    serializer_class = LinkSerializer


class GoodsViewSet(viewsets.ModelViewSet):

    queryset = Goods.objects.order_by('-view_count')[:5]
    serializer_class = GoodsSerializer


class CountDataApi(View):
    def get(self,request):
        art_count = Article.objects.all().count()
        photo_count = PhotoDetailModel.objects.all().count()
        write_count = UserWrite.objects.all().count()
        note_count = CommentModel.objects.filter(note_id=1).count()
        comment_count = CommentModel.objects.exclude(note_id=1).count()
        goods_count = Goods.objects.all().count()
        data = {
            'msg':'请求成功',
            'code':200,
            'data':{
                'art_count':art_count,
                'photo_count': photo_count,
                'write_count': write_count,
                'note_count': note_count,
                'comment_count': comment_count,
                'goods_count': goods_count,
            }
        }
        return JsonResponse(data)

