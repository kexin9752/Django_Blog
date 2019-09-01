from article.models import Article


def article_new(request):
    new_art = Article.objects.order_by('-created_at').first()
    art_count = Article.objects.all().count()
    return {'new_art':new_art,'art_count':art_count}
