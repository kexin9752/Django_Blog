import xadmin

from mall.models import GoodsType, Goods, GoodsImage


class GoodsTypeAdmin(object):

    list_display = ("name", "code", "description", "picture","reorder","is_valid","created_at")
    search_fields = ('name', 'code')


xadmin.site.register(GoodsType, GoodsTypeAdmin)


class GoodsAdmin(object):

    list_display = ("uid", "goods_name", "goods_price", "goods_image","goods_number","goods_description","goods_status","is_valid","created_at","goods_type")
    search_fields = ('goods_name', 'goods_price')


xadmin.site.register(Goods, GoodsAdmin)


class GoodsImageAdmin(object):

    list_display = ("goods", "img", "created_at")
    search_fields = ('goods', 'created_at')


xadmin.site.register(GoodsImage, GoodsImageAdmin)