from django.urls import path
from .views      import ArticleView
from .views      import SearchView
from .views      import DetailView

urlpatterns = [
    path('/articles/<int:category_id>', ArticleView.as_view()),
    path('/search', SearchView.as_view()),
    path('/details/<int:detail_id>', DetailView.as_view()),
]
