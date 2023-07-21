from django.urls import include, path
from rest_framework import routers

from .views import (TitleViewSet, CategoryViewSet,
                    GenreViewSet, UserViewSet,
                    signup, token,
                    ReviewViewSet, CommentViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register('users', UserViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')

auth_urls = [
    path('token/', token,
         name='token'),
    path('signup/', signup,
         name='signup'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls)),
]
