from django.urls import path
from .views      import ArticleView

urlpatterns = [
    path('/articles/<int:category_id>', ArticleView.as_view()),
]
