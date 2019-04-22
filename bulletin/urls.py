from django.urls import path

from . import views

# アプリケーションの名前空間
# https://docs.djangoproject.com/ja/2.0/intro/tutorial03/
app_name = 'bulletin'

urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # # ex: /post/create/
    # path('post/create/', views.create, name='create'),
    #
    # # ex: /post/1/
    # path('post/<int:pk>/', views.detail, name='detail'),
    #
    # # ex: /post/1/update/
    # path('post/<int:pk>/update/', views.update, name='update'),
    #
    # # ex: /post/1/delete
    # path('post/<int:pk>/delete/', views.delete, name='delete'),
]
