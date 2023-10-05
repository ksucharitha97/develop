from django.urls import path

from .views import (ArticleAPIView, ArticleDetailsAPIview, article_detail,
                    article_detail_view, article_list, article_list_view)

urlpatterns = [
    # URLs for Django Function Based Views 
    # path('article/', article_list, name='article_list'),
    # path('detail/<int:id>/', article_detail, name='article_detail'),

    # URLs for DRF Function Based Views 
    # path('article/', article_list_view, name='article_list_view'),
    # path('detail/<int:id>/', article_detail_view, name='article_detail_view'),

    # URLs for DRF Class Based Views
    path('article', ArticleAPIView.as_view(), name='article_list'),
    path('detail/<int:id>/', ArticleDetailsAPIview.as_view(), name='article_detail'),
]
