"""ParkingLot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views as account_views
from lot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    path('lots/', views.LotListView.as_view(), name='list_lots'),
    path('lots/new/', views.NewLotView.as_view(), name='create_lot'),
    path('lots/<slug:lot_id>/', views.QuestionListView.as_view(),
         name='list_questions'),
    path('lots/<slug:lot_id>/edit/', views.UpdateLotView.as_view(),
         name='lot_update'),
    path('lots/<slug:lot_id>/new/', views.new_question, name='new_question'),
    path('lots/<slug:lot_id>/questions/<int:question_pk>/',
         views.PostListView.as_view(), name='question_comments'),
    path('lots/<slug:lot_id>/questions/<int:question_pk>/post_comment/',
         views.post_comment, name='post_comment'),
    path('lots/<slug:lot_id>/questions/<int:question_pk>/post_comment/cbv/',
         views.PostCreateView.as_view(), name='post_comment_cbv'),
    path('lots/<slug:lot_id>/questions/<int:question_pk>/comments/<int:post_pk>/edit/',  # noqa
         views.PostUpdateView.as_view(), name='edit_comment'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
