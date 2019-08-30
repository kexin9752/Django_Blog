import xadmin

from article.models import Article, Tag, Classify, Author


class ArticleAdmin(object):

    list_display = ("title", "author", "classify", "tag","is_valid","is_best","reorder")
    search_fields = ('title', 'is_valid')
    actions = ['disable_user', 'enable_user']

    def disable_article(self, request, queryset):
        queryset.update(is_valid=False)

    disable_article.short_description = "批量禁用用户"

    def enable_article(self, request, queryset):
        queryset.update(is_valid=True)

    enable_article.short_description = '批量启用用户'


xadmin.site.register(Article, ArticleAdmin)


class TagAdmin(object):
    list_display = ("name",)


xadmin.site.register(Tag, TagAdmin)


class ClassifyAdmin(object):
    list_display = ("name",)

xadmin.site.register(Classify, ClassifyAdmin)


class AuthorAdmin(object):
    list_display = ("name","gender","age")


xadmin.site.register(Author, AuthorAdmin)

