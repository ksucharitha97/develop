from django.urls import path, include

from .views import (ArticleAPIView, ArticleDetailsAPIView,
                    ArticleGenericAPIView, article_detail, ArticleViewSet, article_detail_view,
                    article_list, article_list_view, ArticleModelViewSet, ArticleGenericViewSet,
                    GoldLoanAPIView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='articles_viewset')
router.register('genericviewset/article', ArticleGenericViewSet,
                basename='articles_generic_viewset'),
router.register('modelviewset/article', ArticleModelViewSet,
                basename='articles_model_viewset')

urlpatterns = [
    # URLs for Django Function Based Views
    path('article/', article_list, name='article_list'),
    path('detail/<int:id>/', article_detail, name='article_detail'),

    # URLs for DRF Function Based Views
    path('api/article/', article_list_view, name='article_list_view'),
    path('api/detail/<int:id>/', article_detail_view, name='article_detail_view'),

    # URLs for DRF Class Based Views | APIView
    path('api/cbv/article/', ArticleAPIView.as_view(),
         name='article_list_api_view'),
    path('api/cbv/detail/<int:id>/',
         ArticleDetailsAPIView.as_view(), name='article_detail_api_view'),

    # URLs for DRF Class Based Views | GenericAPIView
    path('generic/article/', ArticleGenericAPIView.as_view(),
         name='article_list_generic_view'),
    path('generic/detail/<int:id>/',
         ArticleGenericAPIView.as_view(), name='article_detail_generic_view'),

    # URLs for DRF Class Based Views | Viewsets
    path('viewset/', include(router.urls), name='article_viewset'),
    path('viewset/<int:pk>/', include(router.urls), name='article_viewset_id'),

    path('calculate/gold-loan/', GoldLoanAPIView.as_view(), name='gold-loan-view')
]
