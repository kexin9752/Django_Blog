from rest_framework.renderers import JSONRenderer

from article.models import Article
from comment.models import CommentModel
from mall.models import Goods
from system.models import PhotoDetailModel, UserWrite


class baserenderer(JSONRenderer):
    def render(self,data,accepted_media_type=None,renderer_context=None):
        if renderer_context:
            if isinstance(data,dict):
                msg = data.pop('msg','请求成功')
                code = data.pop('code',0)
            else:
                msg = '请求成功'
                code = 0
            # art_count = Article.objects.all().count()
            # photo_count = PhotoDetailModel.objects.all().count()
            # write_count = UserWrite.objects.all().count()
            # note_count = CommentModel.objects.filter(note_id=1).count()
            # comment_count = CommentModel.objects.exclude(note_id=1).count()
            # goods_count = Goods.objects.all().count()
            result = {
                'msg':msg,
                'code':code,
                # 'art_count':art_count,
                # 'photo_count': photo_count,
                # 'write_count': write_count,
                # 'note_count': note_count,
                # 'comment_count': comment_count,
                # 'goods_count': goods_count,
                'data':data
            }
            return super().render(result,accepted_media_type,renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
