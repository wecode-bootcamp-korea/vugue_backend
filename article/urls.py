from django.urls import path
from .views      import (
    ArticleView, 
    SearchView, 
    DetailView, 
    VideoView, 
    VideoDetailView,
    CategoryView,
    TagView,
    MainView
)

urlpatterns = [
    path('/category', CategoryView.as_view()),
    path('/tag', TagView.as_view()),
    path('/<int:category_id>', ArticleView.as_view()),
    path('/search', SearchView.as_view()),
    path('/details/<int:detail_id>', DetailView.as_view()),
    path('/main', MainView.as_view()),
    path('/video', VideoView.as_view()),
    path('/video/<int:video_id>', VideoDetailView.as_view())
]
