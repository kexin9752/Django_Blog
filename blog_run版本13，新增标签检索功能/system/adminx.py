import xadmin

from system.models import PhotoModel, PhotoDetailModel, Slider, VideoModel, VideoType, UserWrite


class PhotoAdmin(object):

    list_display = ("photo_name", "img", "view_count", "created_at")
    search_fields = ('photo_name', 'view_count')


xadmin.site.register(PhotoModel, PhotoAdmin)


class PhotoDetailAdmin(object):

    list_display = ("photo_obj", "photo_name", "img", "created_at")
    search_fields = ('photo_name', 'photo_obj')


xadmin.site.register(PhotoDetailModel, PhotoDetailAdmin)


class SliderAdmin(object):

    list_display = ("name", "desc", "img", "created_at","target_url")
    search_fields = ('name', 'desc')


xadmin.site.register(Slider, SliderAdmin)


class VideoModelAdmin(object):

    list_display = ("uid", "desc", "title", "video","created_at")
    search_fields = ('title', 'created_at')


xadmin.site.register(VideoModel, VideoModelAdmin)


class VideoTypeAdmin(object):

    list_display = ("name", "code")
    search_fields = ('name', 'code')


xadmin.site.register(VideoType, VideoTypeAdmin)


class UserWriteAdmin(object):

    list_display = ("name", "content","img","created_at")
    search_fields = ('name', 'content')


xadmin.site.register(UserWrite, UserWriteAdmin)