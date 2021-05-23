from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters
# from rest_framework.generics import get_object_or_404
# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework import viewsets  # , status
import datetime as dt
from django.utils import timezone
from api.models import Profile, Post, Media, HashTag, PeopleTag
from api.serializers import UserSerializer, ProfileSerializer, PostSerializer, MediaSerializer, HashTagSerializer, \
    PeopleTagSerializer
from api.permission import IsUserOrReadonly

# User ViewSet

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Profile Filter & ViewSet

class ProfileFilter(FilterSet):
    nickname__icontains = filters.CharFilter(field_name='content', lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = ['user', 'name', 'nickname', 'website', 'email', 'phone', 'birthday']


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = ProfileFilter
    permission_classes = [IsUserOrReadonly]


# Post Filter & ViewSet

class PostFilter(FilterSet):
    pub_date__gt = filters.DateFilter(field_name='pub_date', lookup_expr='gt')  # 입력된 날짜 이후에 게시된 Post 필터링
    pub_date__lt = filters.DateFilter(field_name='pub_date', lookup_expr='lt')  # 입력된 날짜 이전에 게시된 Post 필터링
    pub_date__range = filters.DateFromToRangeFilter(field_name='pub_date', lookup_expr='range')  # 입력된 기간 내 게시된 Post 필터링
    content__icontains = filters.CharFilter(field_name='content',
                                            lookup_expr='icontains')  # 입력된 값을 content field value에 갖고 있는 Post 필터링
    pub_date__recent_12h = filters.BooleanFilter(field_name='pub_date', method='filter_recent_12h')

    class Meta:
        model = Post
        fields = ['profile', 'pub_date', 'content', 'location']  # 해당 Field에 대해 lookup_expr = 'exact' 필터링

    def filter_recent_12h(self, queryset, pub_date, value):
        current_time = timezone.now()
        ref_time = current_time - dt.timedelta(hours=12)
        if value:
            filtered_queryset = queryset.filter(pub_date__gt=ref_time)
        else:
            filtered_queryset = queryset.filter(pub_date__lt=ref_time)
        return filtered_queryset


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = PostFilter
    permission_classes = [IsUserOrReadonly]


# Media Filter & ViewSet

class MediaFilter(FilterSet):
    class Meta:
        model = Media
        fields = ['post']


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = MediaFilter
    permission_classes = [IsUserOrReadonly]


# HashTag Filter & ViewSet

class HashTagFilter(FilterSet):
    name__icontains = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = HashTag
        fields = ['post', 'name']


class HashTagViewSet(viewsets.ModelViewSet):
    queryset = HashTag.objects.all()
    serializer_class = HashTagSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = HashTagFilter
    permission_classes = [IsUserOrReadonly]


# PeopleTag Filter & ViewSet

class PeopleTagFilter(FilterSet):
    name__icontains = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = PeopleTag
        fields = ['media', 'name']


class PeopleTagViewSet(viewsets.ModelViewSet):
    queryset = PeopleTag.objects.all()
    serializer_class = PeopleTagSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = PeopleTagFilter
    permission_classes = [IsUserOrReadonly]

# class UserList(APIView):
#     def get(self, request, format=None):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PostList(APIView):
#
#     # GET REQUEST 를 받는다.
#     # Post model 의 모든 instance 를 불러오는 method
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     # POST REQUEST 를 받는다.
#     # Post model 에 새로운 instance 를 불러오는 method
#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PostDetail(APIView):
#
#     # arg 에 들어가는 pk 와 같은 pk의 instance가 Post model에 존재하는 지 확인한다.
#     # 존재할 경우 해당 instance를 불러오고 그렇지 않을 경우 404 error를 발생시킨다.
#     def get_object(self, pk):
#         return get_object_or_404(Post, pk=pk)
#
#     # GET REQUEST 를 받는다.
#     # Post model 의 pk 번 instance 를 불러오는 method
#     def get(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     # PUT REQUEST 를 받는다.
#     # Post model 의 pk 번 instance 를 수정하는 method
#     def put(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # DELETE REQUEST 를 받는다.
#     # Post model 의 pk 번 instance 를 삭제하는 method
#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
