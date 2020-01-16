from django.views import View
from django.http  import JsonResponse

from .models      import CategoryTagArticles
from .models      import Articles

from django.db.models import Q

class ArticleView(View):

    def _article_data(self, articles):
        data = [{
                'title'        : props.article.title,
                'image_url'    : props.article.image_url,
                'detail_id'    : props.article.article_detail.id
        } for props in articles]
        return data

    def get(self, request, category_id):
        try:
            offset = int(request.GET.get('offset', 0))
            limit = int(request.GET.get('limit', 12))

            if 'tag_id' in request.GET:
                tag_id = int(request.GET.get('tag_id'))    
                articles = CategoryTagArticles.objects.select_related('article','category','tag').filter(category_id = category_id, tag_id = tag_id).order_by('id')[offset:limit]
                data = self._article_data(articles)
                return JsonResponse({'data':data}, status=200)

            articles = CategoryTagArticles.objects.select_related('article','category').filter(category_id = category_id).order_by('id')[offset:limit]
            data = self._article_data(articles)

            return JsonResponse({'data':data}, status=200)
        except ValueError:
            return JsonResponse({'message':'INVALID_VALUE'}, status = 400)

class SearchView(View):
    def get(self, request):
        if 'keyword' in request.GET:
            keyword = request.GET.get('keyword')
            articles = Articles.objects.filter(Q(title__icontains=keyword)|Q(caption__icontains=keyword))
            article_list = [{
                'title' : article.title,
                'image_url' : article.image_url,
                'detail_id' : article.article_detail_id
            } for article in list(articles.all())]

            return JsonResponse({'data':article_list}, status=200)
        
        return JsonResponse({'message':'NO_KEYWORD'}, status = 400)
