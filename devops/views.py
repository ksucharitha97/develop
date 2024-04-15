from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, mixins, status
from rest_framework.authentication import (BasicAuthentication, TokenAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from .models import Article
from .serializers import ArticleSerializer

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

# @csrf_exempt decorator used to protect our views that means
# APIs/Endpoints which are performing HTTP Methods like POST/PUT/DELETE.
# """


@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def article_detail(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return HttpResponse(f"<h1>Article Object for id {id} is not found</h1>", status=404)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        print(serializer.data)
        return JsonResponse(serializer.data)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=data)
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
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def article_list_view(request):
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


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def article_detail_view(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return Response({"message": "Object Not Found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response({"message", f"{article.title} object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# --------Django REST Framework Function Based Views--------


# --------DRF Class Based Views | APIView --------
# class based view helps much better than function based views. It is much easy to write the code and clean.
class ArticleAPIView(APIView):
    authentication_classes = [SessionAuthentication,
                              TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

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


class ArticleDetailsAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return Response({"message": f"Article object for id {id} is Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        article = Article.objects.get(id=id)
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response({"message", f"{article.title} object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
# --------DRF Class Based Views | APIView --------

# --------DRF Class Based Views | GenericAPIView --------


class ArticleGenericAPIView(generics.GenericAPIView,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request):
        return self.update(request)

    def delete(self, request, id):
        return self.destroy(request)

# --------DRF Class Based Views | GenericAPIView --------


# --------DRF Class  Viewssets--------------------------------
class ArticleViewSet(viewsets.ViewSet):

    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        qureyset = Article.objects.all()
        article = get_object_or_404(qureyset, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destory(self, request, pk=None):
        # default router doesn't support DELETE Method on the endpoint
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response({"message": f"Article object <{article}> deleted successfully"}, status=status.HTTP_404_NOT_FOUND)


class ArticleGenericViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def destroy(self, request, *args, **kwargs):
        """ Overrided the destory() to customize the Response message """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Article object <{instance}> deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)


class ArticleModelViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

# --------DRF Class  Viewssets--------------------------------


class GoldLoanAPIView(APIView):
    def post(self, request):
        data = request.data
        # write your business logic below
        
        if "actual_principal" in data:
            principal_amount = int(data["actual_principal"])
        else:
            principal_amount = data["gold_weight"] * data["gold_loan_price_per_gram"]

        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")
        no_of_days = (end_date - start_date).days

        interest_rate = data['interest_rate'] # float
        interest_amount_per_year = (principal_amount * 1 * interest_rate)/100
        interest_amount_per_day = interest_amount_per_year/365
        total_interest = interest_amount_per_day * no_of_days

        total_amount = principal_amount + total_interest
        result = {"Principal Amount":principal_amount,
                "Total Amount":total_amount}
        
        return Response(data=result, status=status.HTTP_200_OK)
