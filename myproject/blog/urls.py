from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='base'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug_post>/', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>', views.post_list, name='post_list_by_tag'),
    #
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDelateView.as_view(), name='post_delete'),
]






