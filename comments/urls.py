from django.urls import path
from . import views
from .views import LikeCommentView, DislikeCommentView

urlpatterns = [
    path('create/<int:post_id>/', views.CreateCommentView.as_view(), name='create_comment'),
    path('like/<int:comment_id>/', LikeCommentView.as_view(), name='like_comment'),
    path('dislike/<int:comment_id>/', DislikeCommentView.as_view(), name='dislike_comment'),
    
]

