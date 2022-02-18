from django.urls import path
from .views import PostListView, PostDetailView, PostEditView, PostDeleteView, CommentDeleteView, ProfileView, ProfileEditView, AddFollower, RemoveFollower, Like, Dislike, UserSearch, CreateThread, ListThreads, ThreadView, CreateMessage, ThreadEditView

urlpatterns = [
    path('', PostListView.as_view(), name = 'post-list'),
    path('post/<int:pk>', PostDetailView.as_view(), name = 'post-detail'),
    path('post/edit/<int:pk>', PostEditView.as_view(), name = 'post-edit'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name = 'post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>', CommentDeleteView.as_view(), name = 'comment-delete'),
    path('post/<int:pk>/like', Like.as_view(), name = 'like'),
    path('post/<int:pk>/dislike', Dislike.as_view(), name = 'dislike'),
    path('profile/<int:pk>', ProfileView.as_view(), name = 'profile'),
    path('profile/edit/<int:pk>', ProfileEditView.as_view(), name = 'profile-edit'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name = 'add-follower'),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name = 'remove-follower'),
    path('search/', UserSearch.as_view(), name = 'profile-search'),
    path('inbox/', ListThreads.as_view(), name = 'inbox'),
    path('inbox/create-thread', CreateThread.as_view(), name = 'create-thread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name = 'thread'),
    path('inbox/edit/<int:pk>/', ThreadEditView.as_view(), name = 'thread-edit'),
    path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name = 'create-message'),
]