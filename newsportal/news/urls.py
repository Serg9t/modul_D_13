from django.urls import path
from django.views.decorators.cache import cache_page

from . import views


urlpatterns = [
    # path('', cache_page(60)(views.HomeNewsView.as_view()), name='home'),
    path('', views.HomeNewsView.as_view(), name='home'),
    path('category/<int:category_id>/', views.NewsByCategory.as_view(), name='category'),
    path('news/<int:news_id>/', views.PostDetailView.as_view(), name='view_news'),
    path('news/add-news/', views.CreateNews.as_view(), name='add_news'),
    path('news/articles/', views.ArticleView.as_view(), name='articles'),
    path('news/news/', views.NewsView.as_view(), name='news'),
    path('news/update/<int:pk>/', views.UpdateNews.as_view(), name='update_news'),
    path('news/delete/<int:pk>/', views.DeleteNews.as_view(), name='delete_news'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
]
