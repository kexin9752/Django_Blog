import xadmin

from system.models import PhotoModel, PhotoDetailModel


class PhotoAdmin(object):

    list_display = ("photo_name", "img", "view_count", "created_at")
    search_fields = ('photo_name', 'view_count')


xadmin.site.register(PhotoModel, PhotoAdmin)


class PhotoDetailAdmin(object):

    list_display = ("photo_obj", "photo_name", "img", "created_at")
    search_fields = ('photo_name', 'photo_obj')


xadmin.site.register(PhotoDetailModel, PhotoDetailAdmin)
