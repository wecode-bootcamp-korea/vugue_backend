from django.urls import path
from .views      import ArticleView
from .views      import SearchView

urlpatterns = [
    path('/articles/<int:category_id>', ArticleView.as_view()),
    path('/search', SearchView.as_view()),
]
