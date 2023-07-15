from django.urls import include, path
from rest_framework import routers

from .views import (TitleViewSet, CategoryViewSet,
                    GenreViewSet, UserViewSet,
                    SignUpViewSet, TokenViewSet,
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

urlpatterns = [
    path('v1/auth/token/', TokenViewSet.as_view({'post': 'create'}),
         name='token'),
    path('v1/auth/signup/', SignUpViewSet.as_view({'post': 'create'}),
         name='signup'),
    path('v1/', include(router_v1.urls)),
]
