import random

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView

import constants
from accounts.models import Cart
from comment.models import CommentModel
from mall.models import Goods


class DownView(ListView):
    model = Goods
    template_name = 'down.html'
    paginate_by = 8


class DownContent(DetailView):
    model = Goods
    template_name = 'downShow.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get(self,request,*args,**kwargs):
        response = super().get(request,*args,**kwargs)
        self.object.view_count += 1
        self.object.save(update_fields=['view_count'])
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        num = int(self.request.GET.get('num'))
        context['num'] = num
        goods = Goods.objects.filter(is_valid=True,goods_status=constants.GOODS_STATUS_SELL)
        print(goods)
        if num != 0:
            up_goods = goods[num-1]
            context['up_goods'] = up_goods
            context['up_num'] = num-1
        if num != goods.count()-1:
            down_goods = goods[num+1]
            context['down_goods'] = down_goods
            context['down_num'] = num + 1

        # 随机推荐文章，
        love_goods_list = []
        goods_list = Goods.objects.all()
        love_num = goods_list.count()
        run_count = random.choice([1,2,3,4])
        for i in range(run_count):
            random_num = random.choice(range(love_num))
            goods_obj = goods_list[random_num]
            love_goods_list.append(goods_obj)
        context['love_goods_list'] = love_goods_list

        mall_uid = self.object.uid
        comment = CommentModel.objects.filter(mall_uid=mall_uid)
        p = Paginator(comment,5)
        page_obj = p.page(1)
        context['page_obj'] = page_obj

        is_add = Cart.objects.filter(goods=self.object).exists()
        context['is_add'] = is_add
        return context


def goods_shopping(request):
    user = request.user
    goods_id = request.GET.get('id')
    goods = get_object_or_404(Goods,pk=goods_id)

    Cart.objects.create(
        user=user,
        goods=goods,
        name=goods.goods_name,
        img=goods.goods_image,
        price=goods.goods_price,
        count=1,
        total_price=int(goods.goods_price)
    )
    data = {'status':1,'msg':'恭喜您,添加购物车成功'}
    return JsonResponse(data)