from django . urls import path
from .views import article_list, article_detail,ArticleAPIView,Article_detailsAPIview


urlpatterns = [
    # path('article/', article_list, name='article_list'),
    path('article',ArticleAPIView.as_view()),
    path('article',article_detail,name= 'article_detail'),
    path('detail/<int:id>/',Article_detailsAPIview.as_view()),
]
