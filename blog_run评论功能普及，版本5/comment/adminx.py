import xadmin

from comment.models import CommentModel, ReCommentModel


class CommentAdmin(object):

    list_display = ("user_id", "u_name", "u_code","txtContent","art_uid","note_id","level_msg_id","photo_id","mall_id","created_at")
    search_fields = ('user_id', 'u_name')


xadmin.site.register(CommentModel, CommentAdmin)


class ReCommentAdmin(object):

    list_display = ("comment", "self_reply", "u_name","u_code","art_uid","to_code","to_recode","txtContent","img","created_at")
    search_fields = ('comment', 'self_reply')


xadmin.site.register(ReCommentModel, CommentAdmin)

