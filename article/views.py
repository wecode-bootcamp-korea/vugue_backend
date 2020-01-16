from django.views import View
from django.http  import JsonResponse

from .models      import (
    Articles,
    ArticleDetails,
    Categories,
    Tags,
    CategoryTagArticles,
    Video
)

from django.db.models import Q

class CategoryView(View):
    def get(self, request):
        categories = list(Categories.objects.values())
        return JsonResponse({'Category':categories}, status = 200)

class TagView(View):
    def get(self,request):
        tags = list(Tags.objects.values())
        return JsonResponse({'Tag': tags}, status = 200)

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

            articles = CategoryTagArticles.objects.select_related('article','category').filter(category_id = category_id).order_by('id')[offset*limit:(offset+1)*limit]
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

class DetailView(View):

    def get(self, request, detail_id):
        try:
            limit = request.GET.get('limit', 120)
            category_id = request.GET.get('category_id', 1)

            detail = ArticleDetails.objects.get(id=detail_id)
            detail_info = [{
                'title' : detail.title,
                'caption_date' : detail.caption_date,
                'description' : detail.description
            }]
            
            articles = CategoryTagArticles.objects.select_related('article').filter(category_id = category_id).order_by('id')[0:limit]
            article_list = [{
                'title' : props.article.title,
                'caption_date' : props.article.caption_date,
                'image_url' : props.article.image_url,
                'caption' : props.article.caption,
                'detail_id' : props.article.article_detail_id
            } for props in articles]
            return JsonResponse({'detail':detail_info, 'article_list':article_list}, status=200)
        except ArticleDetails.DoesNotExist:
            return JsonResponse({'message':'INVALID_ID'}, status = 404)

class MainView(View):
    MAIN_TAG = 12
    def get(self, request):
        try:
            limit = int(request.GET.get('limit', 15))
            main_articles = CategoryTagArticles.objects.select_related('article','tag').filter(tag_id = self.MAIN_TAG).order_by('id')[0:limit]
            article_list = [{
                'title' : props.article.title,
                'image_url' : props.article.image_url,
                'detail_id' : props.article.article_detail_id
            } for props in main_articles]
            return JsonResponse({'data':article_list}, status=200)
        except ValueError:
            return JsonResponse({'message':'INVALID_VALUE'}, status = 400)

class VideoView(View):
    def get(self, request):
        offset = int(request.GET.get('offset',0))
        limit  = int(request.GET.get('limit',12))
        videos = Video.objects.select_related('category').order_by('id')[offset * limit: (offset+1) * limit]
        data   = [{
            'id'               : props.id,
            'title'            : props.title,
            'background_image' : props.background_image,
            } for props in videos]
        return JsonResponse(list(data), safe=False, status = 200)

class VideoDetailView(View):
    def get(self, request, video_id):
        try:
            video      = Video.objects.select_related('category').get(id=video_id)
            data       = {
                'id'               : video.id,
                'title'            : video.title,
                'background_image' : video.background_image,
                'category'         : video.category.name,
                'video_url'        : video.video_url,
                'content'          : video.content,
                } 
            return JsonResponse(data, safe = False, status = 200)
        except Video.DoesNotExist:
            return JsonResponse({'message':'ARTICLE_NOT_FOUND'}, status =404)
