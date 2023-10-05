from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
# Create your views here.

# --------Normal Django Function Based Views--------
""" Syntax for Normal Django Function Based Views
def function_based_view_name(request):
    # it helps to return HTML tags as a HTTP response for normal django request
    return HttpResponse("<h1>Hi Suchi</h1>")
    # it helps to return HTML page as a response for normal django request
    return Render('template.html', context={"some":"values"})
    # it helps to return JSON object as a response for normal django request
    return JsonResponse(serializer.data, safe=False) 

@csrf_exempt decorator used to protect our views that means
APIs/Endpoints which are performing HTTP Methods like POST/PUT/DELETE.
"""


# @csrf_exempt
# def article_list(request):
#     if request.method == 'GET':
#         print("iam in here inside get request")
#         articles = Article.objects.get(id=1)
#         print(articles.id, articles.title, articles.author, articles.email)
#         serializer = ArticleSerializer(articles)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         print("iam in here inside post request")
#         data = JSONParser().parse(request)
#         serializer = ArticleSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#     return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)
# --------Normal Django Function Based Views--------


# --------Django REST Framework Function Based Views--------
""" Syntax for Django Rest Framework Function Based Views
@api_view(['GET', 'POST'])
def function_based_view_name(request):
    # it helps to return RestFramework Response as a JSON object for API request.
    return Response(serializer.data, status=HTTP_status_code)

# this decorator helps django to understand that the view is a drf api.
@api_view(list of HTTP methods)
"""

@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response({"message":"Object Not Found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    if request.method == 'PUT':
        print(f"request from PUT: {request}")
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response({"message", f"{article.title} object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
# --------Django REST Framework Function Based Views--------
# *************************************************************
# --------Django REST Framework class Based Views--------
# class based view helps much better than function based view its much easy to write the code and clean.
class ArticleAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Article_detailsAPIview(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return Response({"message":"Object Not Found"}, status=status.HTTP_404_NOT_FOUND)
    def get(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)